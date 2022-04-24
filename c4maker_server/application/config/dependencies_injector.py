from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Module, Binder, singleton

from c4maker_server.adapters.mysql.mysql_client import MySQLClient
from c4maker_server.adapters.mysql.mysql_diagram_item_repository import MySQLDiagramItemRepository
from c4maker_server.adapters.mysql.mysql_diagram_repository import MySQLDiagramRepository
from c4maker_server.services.diagram_item_service import DiagramItemService
from c4maker_server.services.diagram_service import DiagramService
from c4maker_server.services.ports.diagram_item_repository import DiagramItemRepository
from c4maker_server.services.ports.diagram_repository import DiagramRepository


class DependenciesInjector(Module):

    def __init__(self, app: Flask):
        self.app = app

    def configure(self, binder: Binder):
        mysql_client = MySQLClient(SQLAlchemy(self.app, session_options={"autoflush": False}))

        diagram_repository = MySQLDiagramRepository(mysql_client)
        diagram_item_repository = MySQLDiagramItemRepository(mysql_client)

        diagram_service = DiagramService(diagram_repository)
        diagram_item_service = DiagramItemService(diagram_item_repository, diagram_service)

        binder.bind(DiagramRepository, to=diagram_repository, scope=singleton)
        binder.bind(DiagramItemRepository, to=diagram_item_repository, scope=singleton)
        binder.bind(DiagramService, to=diagram_service, scope=singleton)
        binder.bind(DiagramItemService, to=diagram_item_service, scope=singleton)
