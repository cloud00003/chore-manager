# Chore Manager

## Product Summary

Chore Manager is a simple web application for families and roommates who want to organize shared household chores.

The goal is to make it easy to see what needs to be done, who is responsible for each task, and when it is due.

## Target Users

- Families
- Roommates sharing household responsibilities

## Core Features

1. **Create a chore**
   - Task title or description
   - Responsible person
   - Deadline

2. **View incomplete chores**
   - Show all unfinished tasks in an **Incomplete** section
   - Display the responsible person and deadline for each task
   - Mark unfinished tasks whose deadline has passed as **Overdue**

3. **Complete a chore**
   - Allow a user to mark a task as completed
   - Move completed tasks from **Incomplete** to **Completed**

4. **Manage existing chores**
   - Edit a task
   - Delete a task
   - View completed tasks in a separate **Completed** section

## Responsible Person

The responsible person's name is entered as plain text. No user accounts or individual profiles are required.

## Main User Flow

1. A user creates a chore.
2. They enter what needs to be done, who is responsible, and the deadline.
3. The chore appears in the **Incomplete** section.
4. If the deadline passes before the chore is completed, it is marked as **Overdue**.
5. When the chore is finished, the user marks it as completed.
6. The chore moves to the **Completed** section.
7. Existing chores can also be edited or deleted.

## Out of Scope for the First Version

- User registration and authentication
- Notifications
- Recurring chores
- Chat
- Statistics or rankings
