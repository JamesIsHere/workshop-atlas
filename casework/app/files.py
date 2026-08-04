"""File store core (U4.1): the Files Dashboard custody surface.

Firm uploads, client uploads, and produced artifacts live together
in one files table (fx-0193/0195/0196); this module is the
management surface over it: upload, folders/subfolders, assignment,
rename, download (single + bulk zip), preview, print. Content is
stored content-addressed (sha256) under a storage dir -- the same
scheme U2.4 client uploads already use. Preview types per the
adapted wording: pdf, png, jpeg/jpg, txt, csv (Office formats are
post-v1, conversion dependency).
"""

import hashlib
import io
import zipfile
from pathlib import Path

PREVIEW_TYPES = {
    ".pdf": "application/pdf",
    ".png": "image/png",
    ".jpeg": "image/jpeg",
    ".jpg": "image/jpeg",
    ".txt": "text/plain",
    ".csv": "text/csv",
}


def store_content(storage_dir, content):
    """Content-addressed storage: bytes -> (sha256, stored path)."""
    sha = hashlib.sha256(content).hexdigest()
    path = Path(storage_dir) / sha[:2]
    path.mkdir(parents=True, exist_ok=True)
    target = path / sha
    if not target.exists():
        target.write_bytes(content)
    return sha, str(target)


# --- folders ---

def create_folder(conn, name, now, contact_id=None, matter_id=None,
                  parent_id=None, user_id=None):
    """+ New > Folder. Assigning a matter requires the matter's
    primary contact to be the assigned contact (fx-0195); giving the
    matter alone assigns its primary contact."""
    if matter_id is not None:
        primary = _primary_contact(conn, matter_id)
        if contact_id is None:
            contact_id = primary
        elif contact_id != primary:
            raise ValueError(
                f"matter {matter_id} requires its primary contact"
                f" {primary} as the assigned contact")
    if parent_id is not None:
        _live_folder(conn, parent_id)
    return conn.execute(
        "INSERT INTO folders (name, parent_id, contact_id, matter_id,"
        " created_at, created_by) VALUES (?,?,?,?,?,?)",
        (name, parent_id, contact_id, matter_id, now, user_id)).lastrowid


def _live_folder(conn, folder_id):
    row = conn.execute(
        "SELECT * FROM folders WHERE id=? AND deleted_at IS NULL",
        (folder_id,)).fetchone()
    if row is None:
        raise ValueError(f"no folder {folder_id}")
    return row


def _primary_contact(conn, matter_id):
    row = conn.execute("SELECT primary_contact_id FROM matters WHERE id=?",
                       (matter_id,)).fetchone()
    if row is None:
        raise ValueError(f"no matter {matter_id}")
    return row["primary_contact_id"]


def subfolders(conn, folder_id):
    return conn.execute(
        "SELECT * FROM folders WHERE parent_id=? AND deleted_at IS NULL"
        " ORDER BY name, id", (folder_id,)).fetchall()


# --- upload / custody ---

def _content_type(name):
    ext = "." + name.rsplit(".", 1)[-1].lower() if "." in name else ""
    return PREVIEW_TYPES.get(ext, "application/octet-stream")


def upload_file(conn, name, content, now, storage_dir, contact_id=None,
                matter_id=None, folder_id=None, user_id=None):
    """+ New / Create New upload: store the bytes, list the file
    under the chosen contact, matter, or folder (fx-0195/0196).
    Uploading from inside a folder files it there. Renaming during
    upload = passing the wanted name."""
    if folder_id is not None:
        folder = _live_folder(conn, folder_id)
        if contact_id is None:
            contact_id = folder["contact_id"]
        if matter_id is None:
            matter_id = folder["matter_id"]
    sha, stored = store_content(storage_dir, content)
    return conn.execute(
        "INSERT INTO files (name, folder_id, contact_id, matter_id,"
        " sha256, size_bytes, stored_path, content_type, source,"
        " uploaded_at, uploaded_by_user_id)"
        " VALUES (?,?,?,?,?,?,?,?,'firm',?,?)",
        (name, folder_id, contact_id, matter_id, sha, len(content),
         stored, _content_type(name), now, user_id)).lastrowid


def save_produced(conn, name, content, now, storage_dir, contact_id=None,
                  matter_id=None, folder_id=None, smart_form_id=None):
    """Custody for app-produced artifacts (shared documents, packet
    output, notes exports, signed e-signature files): a files row
    with source='produced'."""
    sha, stored = store_content(storage_dir, content)
    return conn.execute(
        "INSERT INTO files (name, folder_id, contact_id, matter_id,"
        " sha256, size_bytes, stored_path, content_type, source,"
        " produced_from_smart_form_id, uploaded_at)"
        " VALUES (?,?,?,?,?,?,?,?,'produced',?,?)",
        (name, folder_id, contact_id, matter_id, sha, len(content),
         stored, _content_type(name), smart_form_id, now)).lastrowid


def get_file(conn, file_id):
    row = conn.execute(
        "SELECT * FROM files WHERE id=? AND deleted_at IS NULL",
        (file_id,)).fetchone()
    if row is None:
        raise ValueError(f"no file {file_id}")
    return row


def list_files(conn, contact_id=None, matter_id=None, folder_id=None,
               esign_status=None):
    """The Files index: firm, client, and produced files together;
    filterable by scope and by e-Signature Status (fx-0194). Each row
    carries esign_status (NULL = never prepared)."""
    q = ("SELECT f.*, ("
         "SELECT e.status FROM esign_files e WHERE e.file_id=f.id"
         " AND e.deleted_at IS NULL ORDER BY e.id DESC LIMIT 1"
         ") AS esign_status FROM files f WHERE f.deleted_at IS NULL")
    params = []
    if contact_id is not None:
        q += " AND f.contact_id=?"
        params.append(contact_id)
    if matter_id is not None:
        q += " AND f.matter_id=?"
        params.append(matter_id)
    if folder_id is not None:
        q += " AND f.folder_id=?"
        params.append(folder_id)
    rows = conn.execute(q + " ORDER BY f.id", params).fetchall()
    if esign_status is not None:
        rows = [r for r in rows if r["esign_status"] == esign_status]
    return rows


# --- assignment / rename ---

def assign(conn, item_type, item_id, contact_id=None, matter_id=None,
           folder_id=None):
    """More Actions > Update: re-assign an existing file or folder to
    a contact, matter, and/or folder (fx-0195). Subfolder targeting
    is passing the subfolder's id."""
    if item_type not in ("file", "folder"):
        raise ValueError(f"unknown item type {item_type}")
    if matter_id is not None:
        primary = _primary_contact(conn, matter_id)
        if contact_id is None:
            contact_id = primary
        elif contact_id != primary:
            raise ValueError(
                f"matter {matter_id} requires its primary contact"
                f" {primary} as the assigned contact")
    if item_type == "file":
        if folder_id is not None:
            _live_folder(conn, folder_id)
        conn.execute(
            "UPDATE files SET contact_id=?, matter_id=?, folder_id=?"
            " WHERE id=?", (contact_id, matter_id, folder_id, item_id))
    else:
        conn.execute(
            "UPDATE folders SET contact_id=?, matter_id=?"
            " WHERE id=?", (contact_id, matter_id, item_id))


def rename(conn, item_type, item_id, new_name):
    """The pencil icon: rename in place (fx-0195)."""
    table = {"file": "files", "folder": "folders"}.get(item_type)
    if table is None:
        raise ValueError(f"unknown item type {item_type}")
    conn.execute(f"UPDATE {table} SET name=? WHERE id=?",
                 (new_name, item_id))


# --- download / preview / print ---

def download(conn, file_id):
    """The download icon: (name, bytes)."""
    f = get_file(conn, file_id)
    return f["name"], Path(f["stored_path"]).read_bytes()


def bulk_download(conn, file_ids=(), folder_ids=()):
    """More Actions > Download File(s): selected files and folders
    (with their contents) leave as one zip (fx-0195)."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for fid in file_ids:
            name, content = download(conn, fid)
            z.writestr(name, content)
        for folder_id in folder_ids:
            folder = _live_folder(conn, folder_id)
            for f in list_files(conn, folder_id=folder_id):
                z.writestr(f"{folder['name']}/{f['name']}",
                           Path(f["stored_path"]).read_bytes())
    return buf.getvalue()


def preview(conn, file_id):
    """The preview icon: (content_type, bytes) without a download.
    Only the v1 preview types render (adapted wording)."""
    f = get_file(conn, file_id)
    ext = "." + f["name"].rsplit(".", 1)[-1].lower() if "." in f["name"] else ""
    if ext not in PREVIEW_TYPES:
        raise ValueError(f"preview not supported for {f['name']}")
    return PREVIEW_TYPES[ext], Path(f["stored_path"]).read_bytes()


def print_view(conn, file_id):
    """The printer icon: the file opens in a new tab for printing --
    mechanically, displayable content without a download (fx-0195)."""
    f = get_file(conn, file_id)
    return f["content_type"], Path(f["stored_path"]).read_bytes()
