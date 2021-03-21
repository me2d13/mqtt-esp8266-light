import ujson

class State:
    def __init__(self):
        self.red = 255
        self.green = 255
        self.blue = 255
        self.brightness = 255
        self.is_on = False
        self.log_mqtt = True


    def load_state(self):
        with open("state.json", "r") as f:
            config = ujson.loads(f.read())
            print("Loaded state", config)
            for key in config:
                setattr(self, key, config[key])

    def save_state(self):
        state_str = ujson.dumps(self.__dict__)
        print('Saving state', state_str)
        with open("state.json", "w") as f:
            f.write(state_str)
