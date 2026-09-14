import orjson
import pytest


@pytest.mark.asyncio
async def test_message_broker(unit_message_broker):
    await unit_message_broker.start()

    # Отправляем сообщение
    await unit_message_broker.send_message(
        topic="users_exchange",
        key="events.user.created",
        value=orjson.dumps({"user_id": 123, "email": "test@example.com"}),
    )

    # Потребляем
    messages = []
    async for msg in unit_message_broker.start_consuming("users_queue"):
        messages.append(msg)
        if len(messages) >= 1:
            break

    assert len(messages) == 1
    assert messages[0]["routing_key"] == "events.user.created"
    assert messages[0]["body"]["user_id"] == 123

    await unit_message_broker.close()
