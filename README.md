# Chore Manager 

A simple web app for managing shared household chores for families and roommates.

Create chores through the website and view them in Incomplete and Completed
sections. Editing, completing, and deleting chores through the website are not
implemented yet.

## Local setup (PowerShell)

Requires Python 3.10 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Open http://127.0.0.1:8000/ to see the chore list.
Select **Create a chore**, enter a title or description, responsible person's
name, and deadline, then submit to add an incomplete chore.

The Django project is in `config/`. The `chores/` app is registered in
`config/settings.py` and contains the chore model, list page, and create form.

Check the configuration with:

```powershell
.\.venv\Scripts\python.exe manage.py check
```
