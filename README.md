# TeaTaiMi (development)

Simple Flask app for TeaTaiMi order tracking and management.

Getting started (local development)

1. Create and activate a virtual environment (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Example environment variables (PowerShell):

```powershell
$env:DB_HOST = 'localhost'
$env:DB_USER = 'root'
$env:DB_PASS = ''
$env:DB_NAME = 'teataimi'
```

4. Run the app:

```powershell
python testViewDatabase.py
```

Deploying

This repo includes a `Procfile` to run the app with Gunicorn. Recommended platforms: Render, Railway, DigitalOcean App Platform.

On the platform set the environment variables `DB_HOST`, `DB_USER`, `DB_PASS`, `DB_NAME`. For Render, set the start command to:

```
gunicorn --bind 0.0.0.0:$PORT testViewDatabase:app
```

Security note

Do not commit secrets. Use environment variables on your host platform to store credentials.
