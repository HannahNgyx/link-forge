# link-forge

A small local integration platform used to learn Integrations Engineer skills: APIs, webhooks, sync, and data quality.

**Current phase:** HTTP and API foundation. Employees are stored in memory. Restarting the server clears them.

## Setup

Python 3.12+.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run

From the project root:

```powershell
python -m uvicorn app.main:app --reload
```

- API docs: http://127.0.0.1:8000/docs
- Health: `GET /health`

On Windows, prefer `python -m uvicorn` and `python -m pytest` if `uvicorn.exe` / `pytest.exe` fail with Access is denied.

## API

| Method | Path | Success |
| --- | --- | --- |
| `GET` | `/health` | `200` |
| `POST` | `/employees` | `201` |
| `GET` | `/employees` | `200` (list) |
| `GET` | `/employees/{id}` | `200` or `404` |

Create body:

```json
{
  "first_name": "Ada",
  "last_name": "Lovelace",
  "work_email": "ada@example.com"
}
```

The server assigns `id`. Missing fields return `422`.

## Tests

```powershell
python -m pytest
```
