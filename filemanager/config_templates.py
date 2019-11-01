default_config = {
    'web': {
        'port': 5000,
        'debug': True
    },
    'engine': {
        'save_folder': '',
    },
    'admin': {
        'username': 'admin',
        'password': 'google228'
    }
}

config_types = {
    'default_config': {'data': default_config, 'setting': False},
}

config_names = list(config_types.keys())
