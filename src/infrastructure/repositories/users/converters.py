from src.domain.entities.users import User


def convert_user_entity_to_document(user: User) -> dict:
    return {
        'oid': user.oid,
        'telegram_id': user.telegram_id,
        'name': user.name,
        'created_at': user.created_at,
    }


def convert_user_document_to_entity(user_document: dict) -> User:
    return User(
        oid=user_document['oid'],
        telegram_id=user_document['telegram_id'],
        name=user_document['name'],
        created_at=user_document['created_at'],
    )
