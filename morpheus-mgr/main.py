from system.hub import HubManger, HubSoteria
from ui.mainwin import start_app

if __name__ == "__main__":
    print('Starting Morpheus Manager...')
    #db_connect = HubManger()
    #db_connect.connect_db_hub()
    connection = HubSoteria()
    connection.start_hub_connection()
    start_app()
    #on close
    print('Closing Morpheus Manager...')
    socket = HubSoteria()
    socket.disconnect_socket()  