from flask_restx import fields, Api, Model


class NullableRaw(fields.Raw):
    __schema_type__ = ['object', 'null']

    def format(self, value):
        if value and not isinstance(value, dict):
            raise ValueError("Invalid value for nullable object %s".format(value))

        return value

def get_reduced_user_model() -> dict:
    return {
        "id": fields.String(required=False),
        "name": fields.String(required=True),
        "login": fields.String(required=True)
    }


def get_reduced_entity_model() -> dict:
    return {
        "id": fields.String(required=True)
    }


def __get_generic_entity_model(reduced_user_model: Model) -> dict:
    return {
        "created_by": fields.Raw(model=reduced_user_model, required=False),
        "modified_by": fields.Raw(model=reduced_user_model, required=False),
        "created_at": fields.DateTime(required=False),
        "modified_at": fields.DateTime(required=False)
    }


def get_diagram_model(reduced_user_model: Model, reduced_workspace_model: Model) -> dict:
    generic = __get_generic_entity_model(reduced_user_model)
    generic.update({
        "id": fields.String(required=False),
        "workspace": fields.Raw(model=reduced_workspace_model, required=True),
        "name": fields.String(required=True),
        "description": fields.String(required=True),
        "diagram_type": fields.String(required=True)
    })

    return generic


def get_workspace_model(reduced_user_model: Model, reduced_workspace_model: Model) -> dict:
    generic = __get_generic_entity_model(reduced_user_model)
    generic.update({
        "id": fields.String(required=False),
        "name": fields.String(required=True),
        "description": fields.String(required=False),
        "diagrams": fields.List(fields.Raw(model=get_diagram_model(reduced_user_model, reduced_workspace_model)),
                                required=False)
    })

    return generic


def get_reduced_workspace_model(reduced_user_model: Model) -> dict:
    generic = __get_generic_entity_model(reduced_user_model)
    generic.update({
        "id": fields.String(required=True),
        "name": fields.String(required=False)
    })

    return generic


def get_workspace_item(reduced_user_model: Model, reduced_workspace_model: Model) -> dict:
    generic = __get_generic_entity_model(reduced_user_model)
    generic.update({
        "id": fields.String(required=False),
        "workspace": fields.Raw(model=reduced_workspace_model, required=False),
        "workspace_item_type": fields.String(required=True),
        "key": fields.String(required=True),
        "name": fields.String(required=True),
        "description": fields.String(required=False),
        "details": fields.String(required=False)
    })

    return generic


def get_user_access_model(workspace_model: Model) -> dict:
    return {
        "workspace": fields.Raw(model=workspace_model, required=True),
        "permission": fields.String(required=True)
    }


def get_user_model(user_access_model: Model) -> dict:
    user = get_reduced_user_model()
    user.update({
        "password": fields.String(required=True),
        "user_access": fields.Raw(model=user_access_model)
    })

    return user


def get_relationship_model(reduced_entity_model: Model) -> dict:
    return {
        "diagram_item": fields.Raw(model=reduced_entity_model, required=True),
        "description": fields.String(required=False),
        "details": fields.String(required=False)
    }

def get_diagram_item(workspace_item_model: Model, diagram_model: Model, relationship_model: Model,
                     reduced_entity_model: Model) -> dict:
    return {
        "id": fields.String(required=False),
        "workspace_item": fields.Raw(model=workspace_item_model, required=True),
        "diagram": fields.Raw(model=diagram_model, required=True),
        "relationships": fields.List(fields.Raw(required=False, model=relationship_model), required=False),
        "diagram_item_type": fields.String(required=True),
        "parent": NullableRaw(required=False, model=reduced_entity_model),
        "data": fields.Raw(required=True)
    }
