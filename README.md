# Helpdesk Ticket API

## Project overview

A small REST API for support tickets: create, list, update, and delete tickets stored in PostgreSQL. The service is built with FastAPI and SQLAlchemy, and the whole stack (API + database) runs with Docker Compose.

## Features

- `POST /tickets` — create a ticket
- `GET /tickets` — list tickets, filter by `status` and `priority`, search in title and description
- `GET /tickets/{id}` — get one ticket
- `PATCH /tickets/{id}` — update a ticket
- `DELETE /tickets/{id}` — delete a ticket
- Interactive OpenAPI docs at `/docs`
- Tables created automatically on startup

Ticket fields: title, description, status (`open`, `in_progress`, `done`), priority (`low`, `medium`, `high`), category, timestamps.

## Tech stack

Python 3.12, FastAPI, Pydantic v2, SQLAlchemy 2.0, PostgreSQL (psycopg), Docker Compose, pytest (SQLite in tests), GitHub Actions.

## How to run

```bash
docker compose up --build
```

API: [http://localhost:8000](http://localhost:8000)  
Docs: [http://localhost:8000/docs](http://localhost:8000/docs)

Tests use in-memory SQLite (no Postgres required):

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest
```

## What I built

I designed the ticket data model and the REST API, then implemented the service end to end: models, schemas, endpoints, Docker setup, and tests. I used Cursor as an AI assistant and reviewed, tested, and adjusted every change myself.

## Key decisions

- **FastAPI** for request validation and generated OpenAPI docs, so the API is easy to try without extra tooling.
- **PostgreSQL** as a production-style relational store for tickets.
- **SQLite in tests** so pytest is fast and does not need a running database.
- **Docker Compose** so the API and Postgres start with one command.
- **AI-first workflow** with Cursor: I specified the design, then reviewed and tested the generated code instead of treating the model as the source of truth.

## What I would improve

- Authentication (who can create or close tickets)
- Pagination on the ticket list
- Alembic migrations instead of `create_all` on startup
- User roles (agent vs. requester)
- A Flutter frontend for a full client–server demo
