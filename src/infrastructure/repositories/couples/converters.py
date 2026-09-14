from src.domain.entities.couples import Couple


def convert_couple_entity_to_document(couple: Couple) -> dict:
    return {
        'oid': couple.oid,
        'title': couple.title,
        'first_user_oid': couple.first_user_oid,
        'second_user_oid': couple.second_user_oid,
        'created_at': couple.created_at,
    }


def convert_couple_document_to_entity(couple_document: dict) -> Couple:
    return Couple(
        oid=couple_document['oid'],
        title=couple_document['title'],
        first_user_oid=couple_document['first_user_oid'],
        second_user_oid=couple_document['second_user_oid'],
        created_at=couple_document['created_at'],
    )
