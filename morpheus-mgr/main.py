from system.hub import HubManger, HubSocket
from ui.mainwin import start_app

if __name__ == "__main__":
    print('Starting Morpheus Manager...')
    #db_connect = HubManger()
    #db_connect.connect_db_hub()
    connection = HubSocket()
    connection.start_hub_connection()
    start_app()
    #on close
    print('Closing Morpheus Manager...')
    socket = HubSocket()
    socket.disconnect_socket()  