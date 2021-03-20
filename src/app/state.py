import ujson

class State:
    def __init__(self):
        self.red = 0
        self.green = 0
        self.blue = 0
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
