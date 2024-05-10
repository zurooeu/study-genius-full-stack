from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.models import User
from app.tests.utils.conversation import create_random_conversation


def test_post_initial_message(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    data = {"content": "Hello world!"}
    response = client.post(
        f"{settings.API_V1_STR}/chat",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert "conversation_id" in content
    assert "content" in content


def test_post_unable_to_pass_different_role(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    data = {"content": "Hello world!", "role": "system"}
    response = client.post(
        f"{settings.API_V1_STR}/chat",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 400
    content = response.json()
    assert content["detail"] == "Misconfigured chat role"


def test_post_second_message(
    client: TestClient,
    normal_user_token_headers: dict[str, str],
    db: Session,
    current_user: User,
) -> None:
    conversation = create_random_conversation(db, current_user)
    data = {"content": "Hello world!"}
    response = client.post(
        f"{settings.API_V1_STR}/chat/{conversation.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 200
    content = response.json()
    assert content["conversation_id"] == conversation.id
    assert "content" in content


def test_post_second_message_conversation_not_found(
    client: TestClient, normal_user_token_headers: dict[str, str]
) -> None:
    data = {"content": "Hello world!"}
    response = client.post(
        f"{settings.API_V1_STR}/chat/999999",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 404
    content = response.json()
    assert content["detail"] == "Conversation not found"


def test_post_second_message_not_allowed(
    client: TestClient, normal_user_token_headers: dict[str, str], db: Session
) -> None:
    conversation = create_random_conversation(db)
    data = {"content": "Hello world!"}
    response = client.post(
        f"{settings.API_V1_STR}/chat/{conversation.id}",
        headers=normal_user_token_headers,
        json=data,
    )
    assert response.status_code == 403
    content = response.json()
    assert content["detail"] == "You are not allowed to perform this action"
