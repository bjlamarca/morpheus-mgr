from system.server import ServerManger, ServerWebsocket

from ui.mainwin import start_app
from hue.models import update_tables


if __name__ == "__main__":
    print('Starting Morpheus Manager...')
    connection = ServerWebsocket()
       
    start_app()
    #update_tables()
    