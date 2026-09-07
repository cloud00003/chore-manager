# Chore Manager 

A simple web app for managing shared household chores for families and roommates.

Create chores through the website and view them in Incomplete and Completed
sections. Incomplete chores with past deadlines are marked Overdue, and chores
can be marked as completed. Chores in either section can be edited or deleted.

## Local setup (PowerShell)

Requires Python 3.10 or newer.
The project uses Django 5.2 and SQLite. The commands below use the virtual
environment directly; activation and `uv` are not required.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
```

Start the development server from the project directory:

```powershell
.\.venv\Scripts\python.exe manage.py runserver
```

Stop the server with **Ctrl+C** before starting another instance. If a newly
added route produces `NoReverseMatch`, restart the server to load the current
URL configuration.

Open http://127.0.0.1:8000/ to see the chore list.
Select **Create a chore**, enter a title or description, responsible person's
name, and deadline, then submit to add an incomplete chore.
Select **Mark as completed** to move a chore to Completed and remove its overdue
label. Deadlines before today are overdue; deadlines today are not. Today follows
the Django time zone setting (currently UTC).
Select **Edit** to update a chore's details without changing its completion
status. Select **Delete** to open a confirmation page, then confirm deletion or
choose **Cancel** to return to the list.

The Django project is in `config/`. The `chores/` app is registered in
`config/settings.py` and contains the chore model, list page, and create form.

## Checks and tests

Run Django system checks and the full test suite:

```powershell
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test
```

The tests use a separate temporary database. They cover model validation,
populated and empty list sections, create/edit errors, overdue date boundaries,
completion, deletion, missing records, and CSRF protection.

## Workflow verification

1. Create a chore with a deadline before today. Confirm its details and
   **Overdue** label appear under **Incomplete**.
2. Open **Edit**, check the prefilled fields, change the details, and save.
   Missing required fields or an invalid date should show validation errors.
3. Select **Mark as completed**. Confirm the chore moves to **Completed** and
   loses its overdue label and completion button.
4. Open **Delete**, then **Cancel**, and confirm the chore remains. Open
   **Delete** again and confirm deletion; the chore should disappear.
5. On an empty database, confirm both sections show their empty messages.

Task 8 verification: all 23 tests and Django system checks passed. The live
HTTP form flow above was exercised with a temporary chore, including validation,
cancel, and final deletion. Empty states were verified by the test suite.
This was an HTTP walkthrough, not a visual browser review.
