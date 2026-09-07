# Chore Manager backlog

Based on `_docs/plan.md`. The Django project and registered `chores` app already
exist. Tasks are ordered by dependency; tasks 1–3 are complete and tasks 4–8 are pending.

Planning assumption: a deadline is a calendar date. An unfinished chore becomes
overdue when its deadline is earlier than the current local date; chores due
today are not overdue.

## 1. Store chores

- [x] Add a `Chore` model with required title/description, responsible person's
  name (plain text), deadline, and a completion flag defaulting to false.
- [x] Create the initial migration.
- Done when: a chore can be saved and retrieved with these fields and defaults.
- Depends on: existing scaffold.

## 2. Show the chore list

- [x] Add app URLs, connect them to the project, and serve the list at `/`.
- [x] Add a simple page with separate **Incomplete** and **Completed** sections.
  Display each chore's title, responsible person, and deadline, with an empty
  state for each section.
- Done when: saved chores appear in the correct section; verify both sections
  and the empty page with Django view tests.
- Depends on: 1.

## 3. Create a chore

- [x] Add a Django ModelForm and a create page linked from the list.
- [x] Validate required fields and the deadline, display errors, and redirect
  to the list after saving. Use POST with CSRF protection for submission.
- Done when: a valid submission creates an incomplete chore; tests cover valid
  input and invalid submissions that do not create records.
- Depends on: 1, 2.

## 4. Mark overdue chores

- [ ] Derive overdue status from the deadline and completion flag, and display
  **Overdue** beside qualifying incomplete chores.
- Done when: tests cover yesterday, today, and tomorrow, plus a completed chore
  with a past deadline. Only unfinished chores before today are overdue.
- Depends on: 1, 2.

## 5. Complete a chore

- [ ] Add a completion button to each incomplete chore and a POST-only,
  CSRF-protected action that saves completion and redirects to the list.
- Done when: completing a chore moves it to **Completed** and removes its overdue
  label; tests verify persistence and that GET cannot change completion.
- Depends on: 2, 4.

## 6. Edit a chore

- [ ] Link chores in both sections to an edit page that reuses the chore form.
- [ ] Save changes to title/description, responsible person, and deadline while
  preserving completion status; redirect to the list after a successful POST.
- Done when: tests cover editing incomplete and completed chores, validation
  errors, and a missing chore returning 404.
- Depends on: 3, 5.

## 7. Delete a chore

- [ ] Add a delete link for chores in both sections and a confirmation page with
  a cancel link. Delete only through a CSRF-protected POST.
- Done when: tests verify deletion, a missing chore returning 404, and that
  opening the confirmation page leaves the chore intact.
- Depends on: 2, 5.

## 8. Verify the complete flow

- [ ] Run Django system checks and the test suite; manually walk through create,
  list, overdue display, edit, complete, and delete.
- [ ] Check links, form errors, and empty states, and update the README with
  usage and test commands.
- Done when: the plan's main user flow works end to end and setup instructions
  match the implementation.
- Depends on: 3–7.

## Scope limits

No user registration, authentication, individual profiles, notifications,
recurring chores, chat, statistics, or rankings. Keep the first version to
standard Django views, forms, and templates using the existing SQLite setup.
