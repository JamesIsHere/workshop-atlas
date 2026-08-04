# module: internal-chat

Docketwise's own vocabulary (help-center category "Internal Chat", 1
article, fx-0003; feature name "Docketwise Chat"). Phase 3
sparse-tail module: full extraction from the collection page
(fx-0230) and article fx-0231. No embeds. Tripwire sweep: no
internal-chat ITEM in the other four inventories; fixture-content
grep found the pricing plan-matrix row (fx-0108: Internal Chat on
Basic, Pro, and Advanced) -- anchor lifted to confirmed with no new
fetch, third pricing-matrix hit of the sparse tail. Carve: module
anchor + individual chats + group chats + desktop notifications.

## entry: internal-chat.module-exists
- name: Docketwise Chat
- named-by-us: no
- description: Docketwise Chat is internal instant messaging inside
  Docketwise: staff send chat messages to teammates individually or
  in group chats from a Chat surface (fx-0230, fx-0231, fx-0108).
- criterion: User navigates to Chat -> they can send an instant
  message to a teammate inside Docketwise
- sources: fx-0230, fx-0231, fx-0108
- tier: confirmed
- detail: The pricing matrix lists Internal Chat as available on
  all three plans -- Basic, Pro, and Advanced (fx-0108).

## entry: internal-chat.individual-chats
- name: Individual Chats
- named-by-us: no
- description: One-to-one chats are started from the Chat surface by
  finding a colleague under open chats, via the search bar, or in
  the contacts list, typing a message, and sending with
  Enter/Return (fx-0231).
- criterion: User selects a colleague in Chat, types a message, and
  hits Enter -> the message is sent to that colleague
- sources: fx-0231
- tier: provisional

## entry: internal-chat.group-chats
- name: Group Chats
- named-by-us: no
- description: Group chats are created via the Create Group button
  with a title/subject and members chosen by (+)/(-) selection; the
  group exists once the creator sends the first message (fx-0231).
- criterion: User creates a group with a title and members and sends
  the first message -> the group chat is created and the message is
  delivered to its members
- sources: fx-0231
- tier: provisional
- detail: A group's name and members cannot be edited once it has
  been created (fx-0231).

## entry: internal-chat.desktop-notifications
- name: Desktop Notifications
- named-by-us: no
- description: Chat desktop notifications are enabled by toggling
  the Desktop Notification slider on the Chat surface, provided the
  browser has allowed desktop notifications for Docketwise
  (fx-0231).
- criterion: User activates the Desktop Notification toggle in Chat
  (with browser permission granted) -> incoming chat messages raise
  desktop notifications
- sources: fx-0231
- tier: provisional
