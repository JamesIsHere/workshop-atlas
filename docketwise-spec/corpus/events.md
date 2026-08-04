# module: events

Docketwise's own vocabulary (help-center category "Events", 1
article, fx-0003; marketing calls the surface "Calendaring",
fx-0108/fx-0157). Phase 3 sparse-tail module: full extraction from
the collection page (fx-0239) and article fx-0240. No embeds.
Tripwire sweep: no events ITEM in the other four inventories;
fixture-content grep found the pricing plan-matrix row (fx-0108:
Calendaring on Basic, Pro, and Advanced -- fourth pricing-matrix
lift) and the case-management page's Calendaring section ("Schedule
appointments, deadlines, and other important events", fx-0157) --
anchor confirmed with no new fetch. Calendar sync ground is owned by
integrations (google-calendar, outlook-calendar). Carve: module
anchor + attendees + reminders + firm default reminder settings.

## entry: events.module-exists
- name: Events
- named-by-us: no
- description: Docketwise schedules events -- appointments,
  deadlines, and other important dates -- created and edited with
  attendees and reminder notifications; marketing brands the
  surface Calendaring (fx-0239, fx-0240, fx-0108, fx-0157).
- criterion: User creates an event -> it appears on the firm's
  Docketwise calendar and can be reopened and edited
- sources: fx-0239, fx-0240, fx-0108, fx-0157
- tier: confirmed
- detail: The pricing matrix lists Calendaring on all three plans
  (fx-0108). Events also attach to leads
  (docketwise-leads-crm.module-exists, fx-0235). External calendar
  sync is owned by integrations.google-calendar and
  integrations.outlook-calendar.

## entry: events.event-attendees
- name: Adding Attendees to an Event
- named-by-us: no
- description: Events carry attendees -- firm members and contacts
  -- added while creating the event or by editing an existing one,
  searched by name or email address (fx-0240).
- criterion: User searches a firm member or contact in the
  Attendees box and selects them -> that person is an attendee of
  the event
- sources: fx-0240
- tier: provisional

## entry: events.event-reminders
- name: Event Reminders
- named-by-us: no
- description: Events send reminder notifications to their
  attendees by email and/or SMS at a chosen offset before the event
  start -- a numerical value plus a unit of time (minutes, hours,
  days, weeks, months) -- with multiple reminders addable per event
  (fx-0239, fx-0240).
- criterion: User adds a notification to an event with a type,
  value, and unit -> attendees receive the reminder that far before
  the event's start time
- sources: fx-0239, fx-0240, fx-0277
- tier: confirmed
- detail: SMS Event Reminder Notifications named as a release in
  the Q3 2022 features-roundup video (fx-0277, chapter at 11:08).
  SMS reminders are Pro/Advanced-only (fx-0240). A firm
  member receiving SMS reminders needs a valid US mobile number
  under Settings > Preparer Information (fx-0240). Reminders reach
  yourself, colleagues, and clients (fx-0240).

## entry: events.default-reminder-settings
- name: Adding Default Reminder Settings
- named-by-us: no
- description: Firm-level default event notifications are
  configured under Settings > Event Settings: with Default
  Notifications for Events checked, a notification type, unit, and
  value (repeatable via + Add notification) apply to events by
  default (fx-0240).
- criterion: Admin enables Default Notifications for Events with a
  type, value, and unit -> new events carry those reminders by
  default
- sources: fx-0240
- tier: provisional
