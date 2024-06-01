from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models import User
from app.tests.utils.conversation import (
    create_random_conversation,
    create_random_conversation_with_random_messages,
)


def test_read_conversation(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
    current_user: User,
) -> None:
    conversation = create_random_conversation_with_random_messages(db, current_user)
    response = client.get(
        f"{settings.API_V1_STR}/conversations/{conversation.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert "id" in content
    assert "created_at" in content
    assert "modified_at" in content
    assert "owner_id" not in content
    assert len(content["messages"]) == 2
    message = content["messages"][0]
    assert "id" in message
    assert "created_at" in message
    assert "role" in message
    assert "content" in message
    assert "conversation_id" not in message
    assert "owner_id" not in message


def test_read_conversation_not_found(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    response = client.get(
        f"{settings.API_V1_STR}/conversations/999",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Conversation not found"


def test_read_conversation_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    conversation = create_random_conversation(db)
    response = client.get(
        f"{settings.API_V1_STR}/conversations/{conversation.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"


def test_read_conversations(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
    current_user: User,
) -> None:
    create_random_conversation(db, current_user)
    create_random_conversation(db, current_user)
    response = client.get(
        f"{settings.API_V1_STR}/conversations/",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert len(content["data"]) >= 2


def test_delete_conversation(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
    current_user: User,
) -> None:
    conversation = create_random_conversation(db, current_user)
    response = client.delete(
        f"{settings.API_V1_STR}/conversations/{conversation.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["message"] == "Conversation deleted successfully"


def test_delete_conversation_not_found(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    response = client.delete(
        f"{settings.API_V1_STR}/conversations/999",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Conversation not found"


def test_delete_conversation_not_enough_permissions(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    conversation = create_random_conversation(db)
    response = client.delete(
        f"{settings.API_V1_STR}/conversations/{conversation.id}",
        headers=normal_user_token_headers,
    )
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "Not enough permissions"
