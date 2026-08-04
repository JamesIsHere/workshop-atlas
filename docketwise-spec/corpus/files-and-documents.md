# module: files-and-documents

Docketwise's own vocabulary (help-center category "Files and
Documents", 5 articles, fx-0003). Phase 3 fan-out module: full
extraction from the collection page (fx-0193) and articles fx-0194..
fx-0198, plus two tier-lifting captures: the marketing e-signature
page (fx-0199, the unmined /features/e-signature/ item) and the
official "Introducing e-Signatures from Docketwise" video (fx-0200,
embed-grep from fx-0194 -- the same embed also sits on fx-0199).
Carve: file storage mechanics (upload/folders/subfolders/assignment/
renaming/download/preview/print) + the e-Signature subsystem
(anchor/preparation/requests/signing/completion/status/notifications/
auto-filing). Two of the five articles are cross-module ground:
Document Upload Requests (fx-0197) joins smart-forms.document-requests
and MotaWord (fx-0198) joins integrations.motaword, in place of
duplicate entries.

## entry: files-and-documents.module-exists
- name: Files and Documents
- named-by-us: no
- description: Docketwise stores and displays the firm's documents
  -- completed immigration forms (PDFs), photo evidence, cover
  letters -- in a central Files area (the Files Dashboard / Files
  index) where firm uploads and client uploads live together
  (fx-0193, fx-0195, fx-0196). The pricing matrix attests the
  storage capability on the marketing family: Unlimited Cloud
  Storage on every plan (fx-0108).
- criterion: User navigates to the Files Dashboard -> the firm's
  uploaded files and folders are listed for viewing and management
- sources: fx-0193, fx-0195, fx-0196, fx-0108
- tier: confirmed
- detail: No limit on the total amount of file data stored on the
  account (fx-0196), matching the pricing matrix's Unlimited Cloud
  Storage row; the Advanced plan adds an Enhanced File Size Limit
  of 5GB per file (fx-0108). Per-file actions surface as icons on mouseover
  in the Files index (fx-0195).

## entry: files-and-documents.file-upload
- name: Uploading Files to Docketwise
- named-by-us: no
- description: Firm members upload files via the + New button on the
  Files Dashboard, a contact's or matter's Files tab, or a specific
  folder, or via the global Create New button: select or drag and
  drop the file, optionally assign a contact/matter, and click
  Upload (fx-0195, fx-0196).
- criterion: User clicks + New or Create New, selects File, picks a
  file, and clicks Upload -> the file is stored and listed under the
  chosen contact, matter, or folder
- sources: fx-0195, fx-0196
- tier: provisional
- detail: Any number of files can be uploaded at once (fx-0196).
  Upload size limits carry an intra-family discrepancy, both
  readings kept: 100 MB per file on Basic/Pro plans and 5 GB on
  Advanced (fx-0195, June 2024) vs 100 MB total per upload session
  (fx-0196, June 2026). Files can be renamed during upload
  (fx-0196). Create New while viewing a contact or matter
  auto-assigns the file to it (fx-0196). Uploading from inside a
  folder files it there; the Create New route cannot save into
  subfolders (fx-0195).

## entry: files-and-documents.folders
- name: Folders
- named-by-us: no
- description: Users create folders to organize uploaded files, from
  the Files Dashboard or from the Files tab of a specific contact or
  matter; a folder is unassigned, assigned to a contact, or assigned
  to a matter, with name and optional contact/matter set at creation
  (fx-0195).
- criterion: User clicks + New, chooses Folder, fills in the name
  and optional contact/matter, and clicks Create Folder -> the
  folder exists with the chosen assignment
- sources: fx-0193, fx-0195
- tier: provisional
- detail: Creating a folder from a contact's or matter's Files tab
  auto-assigns it (fx-0195). Assigning a matter requires the
  matter's primary contact to be the assigned contact (fx-0195).

## entry: files-and-documents.subfolders
- name: Subfolders
- named-by-us: no
- description: Any folder in Docketwise can hold subfolders: open
  the parent folder, click + New, and title the subfolder (fx-0195).
- criterion: User opens a folder, clicks + New, and creates a
  subfolder -> the subfolder exists inside the parent folder
- sources: fx-0195
- tier: provisional

## entry: files-and-documents.file-assignment
- name: Assigning an Existing File or Folder
- named-by-us: no
- description: An existing file or folder is re-assigned to a
  contact, matter, and/or folder by checking its box, clicking More
  Actions, indicating the destinations, and clicking Update
  (fx-0195).
- criterion: User selects a file or folder, indicates a contact,
  matter, and/or folder under More Actions, and clicks Update -> the
  item is saved to the indicated assignments
- sources: fx-0195
- tier: provisional
- detail: Assigning to a folder requires that folder's associated
  contact or matter to be specified; targeting a subfolder is done
  by selecting the parent folder, then the subfolder, in the same
  field (fx-0195).

## entry: files-and-documents.file-renaming
- name: Renaming Files and Folders
- named-by-us: no
- description: Files and folders are renamed in place via the pencil
  icon (on mouseover for files): enter the new name and hit
  Enter/Return (fx-0195).
- criterion: User clicks the pencil icon on a file or folder and
  enters a new name -> the item is renamed
- sources: fx-0195
- tier: provisional

## entry: files-and-documents.file-download
- name: Downloading an Individual File
- named-by-us: no
- description: An individual file is downloaded by mousing over it
  in the file list and clicking the download icon (fx-0195).
- criterion: User mouses over a file and clicks the download icon ->
  the file downloads
- sources: fx-0195
- tier: provisional

## entry: files-and-documents.bulk-file-download
- name: Bulk-Downloading Files
- named-by-us: no
- description: Multiple files and/or folders are downloaded together
  by checking their boxes and selecting More Actions > Download
  File(s) (fx-0195).
- criterion: User checks multiple files or folders and selects More
  Actions > Download File(s) -> the selected items download
- sources: fx-0195
- tier: provisional

## entry: files-and-documents.file-preview
- name: Previewing Files
- named-by-us: no
- description: Supported file types are previewed without
  downloading by mousing over the file and clicking the preview icon
  (fx-0195).
- criterion: User mouses over a supported file and clicks the
  preview icon -> the file content displays without a download
- sources: fx-0195
- tier: provisional
- detail: Supported types: .csv, .pdf, .doc, .docx, .txt, .png,
  .jpeg, .jpg, .xls, .xlsx (fx-0195).

## entry: files-and-documents.file-printing
- name: Printing Files
- named-by-us: no
- description: Files are printed directly, without downloading
  first, by mousing over the file and clicking the printer icon,
  then printing from the newly opened tab (fx-0195).
- criterion: User mouses over a file and clicks the printer icon ->
  the file opens in a new tab for printing
- sources: fx-0195
- tier: provisional

## entry: files-and-documents.esignature
- name: DocketWise e-Signature
- named-by-us: no
- description: A native e-signature capability gathers electronic
  signatures on files/documents entirely inside DocketWise: prepare
  a stored PDF, request signatures, and collect signed copies with
  no third-party e-signature tool (fx-0193, fx-0194, fx-0199). An
  official video introduces the feature (fx-0200).
- criterion: User prepares a stored PDF for e-signing and requests
  signatures -> signers sign electronically and the completed file
  is collected inside Docketwise
- sources: fx-0193, fx-0194, fx-0199, fx-0200
- tier: confirmed
- detail: Available for Pro or Advanced subscriptions (fx-0194).
  Marketing positions it as the only native e-signature solution in
  immigration software, replacing tools like HelloSign, with
  security framed around never loading documents onto another
  platform (fx-0199).

## entry: files-and-documents.esignature-preparation
- name: Preparing a File for e-Signing
- named-by-us: no
- description: From the Files index, the feather icon opens the
  e-Signature Setup modal where all signing parties are added; the
  Prepare/Edit Signature Document button then opens the Prepare
  e-Signature File page where fields are placed by selecting a field
  type and clicking a document location, assigned to a signer under
  Field Details, or deleted via the trashcan icon; Save & Continue
  saves the draft (fx-0194).
- criterion: User adds signers in the e-Signature Setup modal,
  places and assigns fields, and clicks Save & Continue -> the
  e-signature file draft is saved with its signers and fields
- sources: fx-0194
- tier: provisional
- detail: Signers and fields are editable up until signatures are
  requested (fx-0194). Only PDF documents can be prepared for
  e-signing; a PDF with editing restrictions cannot be downloaded
  after e-signing due to compatibility issues (fx-0194).

## entry: files-and-documents.esignature-requests
- name: Requesting Signatures on an e-Signature File
- named-by-us: no
- description: The Send e-Signature Request modal (after Save &
  Continue, or via the bell icon on the file) sends and re-sends
  signature requests: select the Email and/or SMS checkboxes per
  unsigned signer and click Send to Unsigned; each selected signer
  receives the request over the indicated channels (fx-0194).
  Marketing attests requesting e-signatures via email or text
  message (fx-0199).
- criterion: User selects Email and/or SMS for unsigned signers and
  clicks Send to Unsigned -> each selected signer receives an
  e-signature request over the indicated channels
- sources: fx-0194, fx-0199
- tier: confirmed
- detail: After a request is sent, the e-signature file can no
  longer be edited (fx-0194).

## entry: files-and-documents.esignature-signing
- name: Signing an e-Signature File
- named-by-us: no
- description: A requested signer receives a secure link, opens the
  document, and completes their required fields by clicking each
  field and entering a signature, initials, or text (fx-0194).
  Marketing attests a simple client signing flow, including signing
  from a mobile phone (fx-0199).
- criterion: Signer opens the secure link and completes the required
  fields -> the signature, initial, text, and date fields are
  captured on the document
- sources: fx-0194, fx-0199
- tier: confirmed
- detail: Firm members on the same Docketwise account sign via the
  Sign button on the e-signature file instead of a link (fx-0194).
  Signature and initial fields are drawn or typed; date fields
  auto-populate from the device's date (fx-0194).

## entry: files-and-documents.esignature-completion
- name: Completed e-Signature Files
- named-by-us: no
- description: After signing their portion, each signer receives a
  copy of the e-signature file with their completed portion; once
  all signers have finished, all signers receive a copy of the
  completed file (fx-0194).
- criterion: All signers complete their portions -> every signer
  receives a copy of the completed e-signature file
- sources: fx-0194
- tier: provisional

## entry: files-and-documents.esignature-status
- name: e-Signature Status
- named-by-us: no
- description: The Files index shows an e-Signature Status column
  with each file's current status; mousing over a pending status
  shows who still needs to sign, and the index filters by
  e-Signature Status (fx-0194). Marketing attests pending/signed
  visibility for managing multiple requests (fx-0199).
- criterion: User views the Files index -> each e-signature file
  shows its current status, pending signers appear on mouseover, and
  the list filters by e-Signature Status
- sources: fx-0194, fx-0199
- tier: confirmed
- detail: Marketing situates the pending/signed view "right inside
  your client portal" while help shows the status column on the
  Files index -- compatible placements, both readings kept
  (fx-0199, fx-0194).

## entry: files-and-documents.esignature-signed-notifications
- name: e-Signature Signed Notifications
- named-by-us: yes
- description: The firm is notified when a document is signed, via
  email or mobile notification (fx-0199, marketing "Stay on Track
  with Notifications" bullet; no help-center corroboration).
- criterion: Signer signs a requested document -> the firm user
  receives an email or mobile notification of the signature
- sources: fx-0199
- tier: provisional

## entry: files-and-documents.esignature-auto-filing
- name: Automated Filing
- named-by-us: no
- description: Once the client signs the required document, the
  signed document is filed automatically with case management and
  the firm receives a notification (fx-0199, marketing-only claim).
- criterion: Signer completes signing -> the signed document is
  automatically filed under the associated case without manual
  upload
- sources: fx-0199
- tier: provisional
