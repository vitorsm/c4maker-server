
from c4maker_server import configs
from c4maker_server.application.api import app

# from c4maker_server.application.api.controllers.diagram_controller import DiagramController
# from c4maker_server.application.api.controllers.user_controller import UserController

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=configs.HOST_PORT)
