from system.server import ServerManger
server_manager = ServerManger()
server_manager.connect_db_server()

from ui.mainwin import start_app
from hue.models import update_tables
from system.server import ServerManger



if __name__ == "__main__":
    print('Starting Morpheus Manager...')
    start_app()
    #update_tables()
    