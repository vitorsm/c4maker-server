from datetime import timedelta

from flask import Flask

from c4maker_server import configs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = configs.DB_CONNECTION_STR
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = configs.ENCRYPT_SECRET_KEY
app.config['JWT_AUTH_URL_RULE'] = "/api/auth/authenticate"
app.config['JWT_EXPIRATION_DELTA'] = timedelta(hours=configs.HOURS_TO_EXPIRATION_TOKEN)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=configs.HOST_PORT)
