from system.hub import HubManger, HubSocket

from ui.mainwin import start_app
from hue.models import update_tables


if __name__ == "__main__":
    print('Starting Morpheus Manager...')
    connection = HubSocket()
    connection.start_hub_connection()
       
    start_app()
    #update_tables()
    