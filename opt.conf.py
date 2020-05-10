from configparser import ConfigParser

config = ConfigParser()

config['Heartbeat'] = {
    'KeepALive': 'true',
    'HeartbeatTimer': 3
}

config['MaximumPackages'] = {
    'MaximumPackages': 25,
    'Start': 'false'
}

with open("configuration.ini", "w") as configFile:
    config.write(configFile)

