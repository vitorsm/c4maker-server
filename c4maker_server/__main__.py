
from c4maker_server import configs
from c4maker_server.application.api import app
from c4maker_server.application import controllers_imports

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=configs.HOST_PORT)
