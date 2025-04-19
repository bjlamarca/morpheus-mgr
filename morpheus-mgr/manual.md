# Signals
*** Area
area = system
    type = message
        status = [clear, info, success, warning]
        message = Hello World
    type = update
    *not complete*

area = device
    type = update, command
    interface = hue
    device_id = 1
    command = on, off, dim
    value = 50