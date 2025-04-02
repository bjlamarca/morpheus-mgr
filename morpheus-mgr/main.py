from system.server import ServerManger, ServerSocket

from ui.mainwin import start_app
from hue.models import update_tables


if __name__ == "__main__":
    print('Starting Morpheus Manager...')
    #connection = ServerSocket()
       
    start_app()
    #update_tables()
    