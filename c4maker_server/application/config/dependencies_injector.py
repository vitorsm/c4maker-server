from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from injector import Module, Binder, singleton

from c4maker_server.adapters.bcrypt_encryption_service import BCryptEncryptionService
from c4maker_server.adapters.mysql.mysql_client import MySQLClient
from c4maker_server.adapters.mysql.mysql_diagram_item_repository import MySQLDiagramItemRepository
from c4maker_server.adapters.mysql.mysql_diagram_repository import MySQLDiagramRepository
from c4maker_server.adapters.mysql.mysql_user_repository import MySQLUserRepository
from c4maker_server.adapters.mysql.mysql_workspace_item_repository import MySQLWorkspaceItemRepository
from c4maker_server.adapters.mysql.mysql_workspace_repository import MySQLWorkspaceRepository
from c4maker_server.application.api.security.flask_authentication_repository import FlaskAuthenticationRepository
from c4maker_server.services.diagram_item_service import DiagramItemService
from c4maker_server.services.diagram_service import DiagramService
from c4maker_server.services.ports.diagram_item_repository import DiagramItemRepository
from c4maker_server.services.ports.diagram_repository import DiagramRepository
from c4maker_server.services.ports.user_repository import UserRepository
from c4maker_server.services.ports.workspace_item_repository import WorkspaceItemRepository
from c4maker_server.services.ports.workspace_repository import WorkspaceRepository
from c4maker_server.services.user_service import UserService
from c4maker_server.services.workspace_item_service import WorkspaceItemService
from c4maker_server.services.workspace_service import WorkspaceService


class DependenciesInjector(Module):

    def __init__(self, app: Flask):
        self.app = app

    def configure(self, binder: Binder):
        mysql_client = MySQLClient(SQLAlchemy(self.app, session_options={"autoflush": False}))

        workspace_repository = MySQLWorkspaceRepository(mysql_client)
        workspace_item_repository = MySQLWorkspaceItemRepository(mysql_client)
        diagram_repository = MySQLDiagramRepository(mysql_client)
        diagram_item_repository = MySQLDiagramItemRepository(mysql_client)
        user_repository = MySQLUserRepository(mysql_client)
        authentication_repository = FlaskAuthenticationRepository()

        workspace_service = WorkspaceService(workspace_repository, authentication_repository)
        workspace_item_service = WorkspaceItemService(workspace_item_repository, authentication_repository,
                                                      workspace_service)
        diagram_service = DiagramService(diagram_repository, authentication_repository, workspace_service)
        diagram_item_service = DiagramItemService(diagram_item_repository, authentication_repository, diagram_service,
                                                  workspace_item_service)
        user_service = UserService(user_repository, BCryptEncryptionService(), authentication_repository)

        binder.bind(MySQLClient, to=mysql_client, scope=singleton)
        binder.bind(WorkspaceRepository, to=workspace_repository, scope=singleton)
        binder.bind(WorkspaceItemRepository, to=workspace_item_repository, scope=singleton)
        binder.bind(DiagramRepository, to=diagram_repository, scope=singleton)
        binder.bind(DiagramItemRepository, to=diagram_item_repository, scope=singleton)
        binder.bind(UserRepository, to=user_repository, scope=singleton)
        binder.bind(WorkspaceService, to=workspace_service, scope=singleton)
        binder.bind(WorkspaceItemService, to=workspace_item_service, scope=singleton)
        binder.bind(DiagramService, to=diagram_service, scope=singleton)
        binder.bind(DiagramItemService, to=diagram_item_service, scope=singleton)
        binder.bind(UserService, to=user_service, scope=singleton)
