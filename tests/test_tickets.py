from fastapi.testclient import TestClient


def create_ticket(client: TestClient, **overrides) -> dict:
    payload = {
        "title": "Printer is jammed",
        "description": "The office printer on floor 2 will not print.",
        "status": "open",
        "priority": "medium",
        "category": "hardware",
    }
    payload.update(overrides)
    response = client.post("/tickets", json=payload)
    assert response.status_code == 201
    return response.json()


def test_create_ticket(client: TestClient):
    body = create_ticket(client)
    assert body["id"] == 1
    assert body["title"] == "Printer is jammed"
    assert body["status"] == "open"
    assert body["priority"] == "medium"
    assert body["category"] == "hardware"
    assert "created_at" in body
    assert "updated_at" in body


def test_list_tickets(client: TestClient):
    create_ticket(client, title="First")
    create_ticket(client, title="Second")
    response = client.get("/tickets")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_filter_tickets_by_status(client: TestClient):
    create_ticket(client, title="Open ticket", status="open")
    create_ticket(client, title="Done ticket", status="done")
    response = client.get("/tickets", params={"status": "done"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["title"] == "Done ticket"


def test_filter_tickets_by_priority(client: TestClient):
    create_ticket(client, title="Low", priority="low")
    create_ticket(client, title="High", priority="high")
    response = client.get("/tickets", params={"priority": "high"})
    assert response.status_code == 200
    results = response.json()
    assert len(results) == 1
    assert results[0]["title"] == "High"


def test_search_tickets_in_title_and_description(client: TestClient):
    create_ticket(client, title="VPN outage", description="Cannot connect to office network")
    create_ticket(client, title="Mouse broken", description="Cursor does not move")
    by_title = client.get("/tickets", params={"search": "vpn"})
    assert by_title.status_code == 200
    assert len(by_title.json()) == 1
    assert by_title.json()[0]["title"] == "VPN outage"

    by_description = client.get("/tickets", params={"search": "cursor"})
    assert by_description.status_code == 200
    assert len(by_description.json()) == 1
    assert by_description.json()[0]["title"] == "Mouse broken"


def test_get_ticket(client: TestClient):
    created = create_ticket(client)
    response = client.get(f"/tickets/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == created["title"]


def test_get_ticket_not_found(client: TestClient):
    response = client.get("/tickets/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Ticket not found"


def test_update_ticket(client: TestClient):
    created = create_ticket(client)
    response = client.patch(
        f"/tickets/{created['id']}",
        json={"status": "in_progress", "priority": "high"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "in_progress"
    assert body["priority"] == "high"
    assert body["title"] == created["title"]


def test_update_ticket_not_found(client: TestClient):
    response = client.patch("/tickets/999", json={"title": "Nope"})
    assert response.status_code == 404


def test_delete_ticket(client: TestClient):
    created = create_ticket(client)
    response = client.delete(f"/tickets/{created['id']}")
    assert response.status_code == 204
    assert client.get(f"/tickets/{created['id']}").status_code == 404


def test_delete_ticket_not_found(client: TestClient):
    response = client.delete("/tickets/999")
    assert response.status_code == 404
