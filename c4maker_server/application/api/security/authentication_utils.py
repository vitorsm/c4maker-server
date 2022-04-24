from flask import Flask
from flask_jwt import JWT
from injector import Injector


def fill_jwt_auth_function(app: Flask, injector: Injector) -> JWT:

    def authenticate(login: str, password: str):
        
