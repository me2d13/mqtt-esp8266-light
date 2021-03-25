import app.secrets as secrets
from machine import Pin, PWM


class Light:
    def __init__(self, state):
        freq = 200
        self.pin_r = PWM(Pin(secrets.PIN_R, Pin.OUT), freq)
        self.pin_g = PWM(Pin(secrets.PIN_G, Pin.OUT), freq)
        self.pin_b = PWM(Pin(secrets.PIN_B, Pin.OUT), freq)
        self.state = state
        def empty_log(message):
            pass
        self.log_function = empty_log
        self.set_pin_value_by_state()

        #self.pin_values = self.calculate_state_from_message_payload(state)

    def set_pin_value_by_state(self):
        '''
        Set real PWM values at pins by self.state
        '''
        red = green = blue = 0
        if self.state.is_on:
            red = 1023 if self.state.red == 255 else self.state.red * 4
            green = 1023 if self.state.green == 255 else self.state.green * 4
            blue = 1023 if self.state.blue == 255 else self.state.blue * 4
            red = red * self.state.brightness / 255
            green = green * self.state.brightness / 255
            blue = blue * self.state.brightness / 255

        if secrets.OUTPUT_INVERTED:
            red = 1023 - red
            green = 1023 - green
            blue = 1023 - blue
        
        log_message = "Setting PWM RGB to {} {} {}".format(red, green, blue)
        print(log_message)
        self.log_function(log_message)
        self.pin_r.duty(red)
        self.pin_g.duty(green)
        self.pin_b.duty(blue)
        

    def calculate_state_from_message_payload(self, payload):
        '''
        Read parsed mqtt JSON message and update state accrdingly.
        Return True if something has changed so pin values should be updated
        Return False on parse error or no/empty request
        '''
        change_requested = False
        if 'state' in payload:
            if payload["state"] == "ON":
                self.state.is_on = True
                change_requested = True
            elif payload["state"] == "OFF":
                self.state.is_on = False
                change_requested = True
        if 'color' in payload:
            color = payload["color"]
            if 'r' in color:
                self.state.red = color['r']
                change_requested = True
            if 'g' in color:
                self.state.green = color['g']
                change_requested = True
            if 'b' in color:
                self.state.blue = color['b']
                change_requested = True
        if 'brightness' in payload:
            self.state.brightness = payload['brightness']
            change_requested = True
        
        return change_requested

    def on_message(self, message_as_dict):
        change_requested = self.calculate_state_from_message_payload(message_as_dict)
        if change_requested:
            self.set_pin_value_by_state()
            self.state.save_state()
