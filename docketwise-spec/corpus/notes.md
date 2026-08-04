# module: notes

Docketwise's own vocabulary (help-center category "Notes", 2
articles, fx-0003). Phase 3 sparse-tail module: full extraction from
the collection page (fx-0221) and articles fx-0222..fx-0223. No
embeds on any page. Tripwire sweep: no notes ITEM in the other four
inventories; fixture-content grep found the homepage pitch "capture
notes" (fx-0001, marketing) -- anchor lifted to confirmed with no
new fetch. fx-0207's notes mentions (AI summarization of notes,
writing assistant available in notes) are writing-assistant surface
ground already folded into docketwise-iq.writing-assistant detail --
no action here. Carve: module anchor + creation + firm-member
assignment + contact/matter association + categories + pinning +
PDF export.

## entry: notes.module-exists
- name: Notes
- named-by-us: no
- description: Docketwise notes track the progress of a case: notes
  are listed on a Notes Dashboard and on Notes tabs of contact and
  matter overview pages (fx-0221, fx-0222, fx-0223, fx-0001).
- criterion: User opens the Notes Dashboard or a contact/matter
  Notes tab -> the notes for that scope are listed
- sources: fx-0221, fx-0222, fx-0223, fx-0001
- tier: confirmed
- detail: The homepage platform pitch attests "capture notes" among
  the core surface (fx-0001). Viewing all notes at once is billed as
  a full timeline of the life of the matter (fx-0223).

## entry: notes.note-creation
- name: Creating a Note
- named-by-us: no
- description: Notes are created from the Notes Dashboard or the
  Notes tab of a contact or matter overview page via the Add Note
  button, with an optional title, note content, related Contact,
  Matter, and Assignee(s), and an optional category (fx-0223).
- criterion: User clicks Add Note on the Notes Dashboard or a
  contact/matter Notes tab, enters content, and confirms -> the
  note is created in that scope
- sources: fx-0223
- tier: provisional
- detail: A checkbox at creation notifies all members of the firm
  of the note regardless of their notification settings (fx-0223).

## entry: notes.note-assignment
- name: Assigning a Note to a Firm Member
- named-by-us: no
- description: Notes are assigned by default to their creator and
  can be assigned to any other staff member at the firm by adding
  them in the note's assignee field; assignees can be removed
  (fx-0223).
- criterion: User clicks a note's assignee field, selects a firm
  member, and clicks Update -> the note carries that member as an
  assignee
- sources: fx-0223
- tier: provisional

## entry: notes.note-client-association
- name: Updating a Note's Contact/Matter
- named-by-us: no
- description: A note's assigned contact/matter follows its creation
  surface -- Dashboard notes start unassigned, contact-tab notes
  auto-assign to that contact, matter-tab notes auto-assign to that
  matter and its primary contact -- and can be updated after
  creation via Set a Client (fx-0223).
- criterion: User clicks Set a Client (or the note's assigned
  contact) on a note, selects a contact/matter, and clicks Update
  -> the note is associated with the selection
- sources: fx-0223
- tier: provisional

## entry: notes.note-categories
- name: Note Categories
- named-by-us: no
- description: Notes carry categories: four pre-made (Government
  Action, Memo, Meeting, Phone Call) plus custom categories created
  under Settings > Notes Settings and shared across the firm's
  account; a category is set at creation or after, and note views
  filter by category (fx-0223).
- criterion: User creates a custom category in Notes Settings and
  assigns it to a note -> notes can be filtered by that category
- sources: fx-0223, fx-0277
- tier: confirmed
- detail: Custom Note Categories named as a release in the Q3 2022
  features-roundup video (fx-0277, chapter at 8:22).

## entry: notes.pinned-notes
- name: Pinned Notes
- named-by-us: no
- description: A note can be pinned, making it appear at the top of
  the listed notes on the Notes Dashboard and the Notes tabs of the
  associated contact and matter overview pages (fx-0223).
- criterion: User pins a note -> the note appears at the top of the
  note list on the Notes Dashboard and associated Notes tabs
- sources: fx-0223
- tier: provisional

## entry: notes.notes-export
- name: Exporting Notes for a Contact or Matter
- named-by-us: no
- description: The notes pertaining to a specific contact or matter
  export to a PDF document via the Export button on the Notes tab
  of that contact's or matter's overview page (fx-0222).
- criterion: User clicks Export on a contact or matter Notes tab ->
  a PDF document of that contact's/matter's notes is produced
- sources: fx-0222
- tier: provisional
