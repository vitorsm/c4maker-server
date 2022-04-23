import uuid
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from c4maker_server import configs
from c4maker_server.adapters.models import DiagramDB, UserDB, DiagramItemDB, DiagramItemRelationshipDB, UserAccessDB

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = configs.DB_CONNECTION_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = configs.ENCRYPT_SECRET_KEY
app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=configs.HOURS_TO_EXPIRATION_TOKEN)


if __name__ == '__main__':
    db = SQLAlchemy(app, session_options={"autoflush": True})

    user = db.session.query(UserDB).get("43affbd5-01cb-4f96-aa1c-d0d145587b8b")
    diagram = db.session.query(DiagramDB).get("81fe3c90-4247-4dd5-8ae2-786e8dcbc855")
    diagram_item1 = db.session.query(DiagramItemDB).get("915d0d5b-bf78-4515-a2df-bd464aa7f6f4")
    diagram_item2 = db.session.query(DiagramItemDB).get("0d79ee51-ac68-4e40-bbe5-7565fd63232f")

    user_access = UserAccessDB()
    user_access.user_id = user.id
    user_access.diagram_id = diagram.id
    user_access.user_permission = "EDIT"

    user.user_access.append(user_access)
    db.session.commit()

    # item_id = str(uuid.uuid4())
    #
    # relationship1 = DiagramItemRelationshipDB()
    # relationship1.from_diagram_item_id = item_id
    # relationship1.to_diagram_item_id = diagram_item1.id
    # relationship1.description = "desc 6"
    # relationship1.details = None
    #
    # diagram_item = DiagramItemDB()
    # diagram_item.id = item_id
    # diagram_item.name = "Item 6"
    # diagram_item.item_description = "Desc 6"
    # diagram_item.details = "details 6"
    # diagram_item.item_type = "PERSON"
    # diagram_item.diagram_id = diagram.id
    # diagram_item.parent_id = None
    # diagram_item.created_by = user.id
    # diagram_item.modified_by = user.id
    # diagram_item.relationships.append(relationship1)
    # db.session.add(diagram_item)
    # db.session.commit()

    # diagram_item = DiagramItemDB()
    # diagram_item.id = str(uuid.uuid4())
    # diagram_item.name = "Item 2"
    # diagram_item.item_description = "Desc 2"
    # diagram_item.details = "details 2"
    # diagram_item.item_type = "PERSON"
    # diagram_item.diagram_id = diagram.id
    # diagram_item.parent_id = diagram_item1.id
    # diagram_item.created_by = user.id
    # diagram_item.modified_by = user.id
    # db.session.add(diagram_item)
    # db.session.commit()

    # diagram_item = DiagramItemDB()
    # diagram_item.id = str(uuid.uuid4())
    # diagram_item.name = "Item 1"
    # diagram_item.item_description = "Desc 1"
    # diagram_item.details = "details"
    # diagram_item.item_type = "PERSON"
    # diagram_item.diagram_id = diagram.id
    # diagram_item.parent_id = None
    # diagram_item.created_by = user.id
    # diagram_item.modified_by = user.id
    # db.session.add(diagram_item)
    # db.session.commit()

    # diagram = DiagramDB()
    # diagram.id = str(uuid.uuid4())
    # diagram.name = "Diagram"
    # diagram.description = "description"
    # diagram.created_by = user.id
    # diagram.modified_by = user.id
    # diagram.created_at = None
    # diagram.modified_at = None
    # db.session.add(diagram)
    # db.session.commit()

    print(user.name)
    # user = UserDB()
    # user.id = str(uuid.uuid4())
    # user.name = "Vitor"
    # user.login = "vitor"
    # user.password = "senha"
    # db.session.add(user)
    # db.session.commit()

    app.run(host='0.0.0.0', port=configs.HOST_PORT)
