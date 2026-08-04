"""Database connection layer. The ONLY way the app opens SQLite.

Every connection: foreign_keys ON + actor functions registered. The audit
triggers call casework_actor_type()/casework_actor_id(); a connection
opened any other way cannot mutate audited tables (fails loudly) -- that
is the audit invariant's enforcement, do not work around it.
"""

import sqlite3
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent / "schema" / "schema.sql"


class Actor:
    """Per-connection mutable actor; set at request start."""

    def __init__(self):
        self.actor_type = "system"
        self.actor_id = None

    def set(self, actor_type, actor_id):
        self.actor_type = actor_type
        self.actor_id = actor_id


class Connection(sqlite3.Connection):
    """sqlite3.Connection is slotted in 3.14; subclass to carry .actor."""

    actor: Actor


def connect(path):
    # check_same_thread=False: the client HTTP server (U2.5) handles
    # requests on worker threads against the app's single connection,
    # serialized by the server's lock. The app itself is
    # single-threaded; this is not a concurrency invitation.
    conn = sqlite3.connect(path, factory=Connection,
                           check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    actor = Actor()
    conn.create_function("casework_actor_type", 0, lambda: actor.actor_type)
    conn.create_function("casework_actor_id", 0, lambda: actor.actor_id)
    conn.actor = actor
    return conn


def create_db(path):
    """Apply schema.sql to a fresh database at path (or ':memory:')."""
    conn = connect(path)
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    return conn
