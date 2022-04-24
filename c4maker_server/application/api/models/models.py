from flask_restx import fields, Api, Model


def get_reduced_user_model() -> dict:
    return {
        "id": fields.String(required=False),
        "name": fields.String(required=True),
        "login": fields.String(required=True)
    }


def __get_generic_entity_model(reduced_user_model: Model) -> dict:
    return {
        "created_by": fields.Raw(model=reduced_user_model, required=False),
        "modified_by": fields.Raw(model=reduced_user_model, required=False),
        "created_at": fields.DateTime(required=False),
        "modified_at": fields.DateTime(required=False)
    }


def get_diagram_model(reduced_user_model: Model) -> dict:
    generic = __get_generic_entity_model(reduced_user_model)
    generic.update({
        "id": fields.String(required=False),
        "name": fields.String(required=True),
        "description": fields.String(required=True)
    })

    return generic


def get_user_access_model(diagram_model: Model) -> dict:
    return {
        "diagram": fields.Raw(model=diagram_model, required=True),
        "permission": fields.String(required=True)
    }


def get_user_model(user_access_model: Model) -> dict:
    user = get_reduced_user_model()
    user.update({
        "password": fields.String(required=True),
        "user_access": fields.Raw(model=user_access_model)
    })

    return user


def get_diagram_item(reduced_user_model: Model, diagram_model: Model) -> dict:
    generic = __get_generic_entity_model(reduced_user_model)
    generic.update({
        "id": fields.String(required=False),
        "name": fields.String(required=True),
        "item_description": fields.String(required=False),
        "details": fields.String(required=False),
        "item_type": fields.String(required=True),
        "diagram": fields.Raw(model=diagram_model, required=True),
        "relationships": fields.String(required=True),
        "parent": fields.Raw()
    })

    return generic
