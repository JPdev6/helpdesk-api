# helpdesk-api

FastAPI service for creating and managing support tickets. Tickets are stored in PostgreSQL with SQLAlchemy 2.0.

## Requirements

- Python 3.12
- Docker (optional, for PostgreSQL + API)

## Run with Docker Compose

```bash
docker compose up --build
```

The API is available at `http://localhost:8000`. Interactive docs: `http://localhost:8000/docs`.

Tables are created automatically when the API starts.

## Run locally

Create a virtual environment and install dependencies:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Start PostgreSQL (for example with Docker):

```bash
docker compose up postgres
```

Then start the API:

```bash
export DATABASE_URL=postgresql+psycopg://helpdesk:helpdesk@localhost:5432/helpdesk
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

If `DATABASE_URL` is not set, the app defaults to `postgresql+psycopg://helpdesk:helpdesk@localhost:5432/helpdesk`.

## Tests

Tests use an in-memory SQLite database and do not require PostgreSQL:

```bash
pytest
```

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `POST` | `/tickets` | Create a ticket |
| `GET` | `/tickets` | List tickets (`status`, `priority`, `search`) |
| `GET` | `/tickets/{id}` | Get one ticket |
| `PATCH` | `/tickets/{id}` | Update a ticket |
| `DELETE` | `/tickets/{id}` | Delete a ticket |
