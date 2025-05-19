
area = system
type = message
        status = [clear, info, success, warning, error]
        message = Hello World
    type = update
    'type': 'soteria_handshake' {
        'id': '',
        'identifier': ''
        'status'
        'message'
    }

    type = command
        value    

    *not complete*

area = device
    type = update, command
    interface = hue
    device_id = 1
    command = on, off, dim
    value = 50

area = 'interface'
    type = ''