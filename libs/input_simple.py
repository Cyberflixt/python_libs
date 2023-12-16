
from pynput import keyboard
from pynput.mouse import Button, Controller

"""Keyboard"""

class Keyboard:
    def __init__(self):
        self.keys_down = []
        self.get = self.key_down
        self.start()
    
    def key_down(self, key):
        return key.lower() in self.keys_down

    def key_name(self, k):
        try:
            # Alpha numeric key
            k = str(k.char)
        except AttributeError:
            # Special key
            k = str(k)
        k = k.replace('Key.','')
        return k.lower()

    def on_press(self, k):
        k = self.key_name(k)
        if not(k in self.keys_down):
            self.keys_down.append(k)

    def on_release(self, k):
        k = self.key_name(k)
        if k in self.keys_down:
            self.keys_down.remove(k)

    def start(self):
        self.listener = keyboard.Listener(
            on_press = self.on_press,
            on_release = self.on_release
        )
        self.listener.start()

class Mouse:
    def __init__(self):
        self.mouse = Controller()

    def get(self):
        """Return the mouse position"""
        return self.mouse.position

    def args_vector(self, *args):
        v = args
        if len(args)==2:
            v = (args[0], args[1])
        return v
    
    def set(self, *args):
        """Sets the mouse position, return position"""
        v = self.args_vector(*args)
        self.mouse.position = v
        return v

    def move(self, *args):
        """Move the mouse relatively, return position"""
        v = self.args_vector(*args)
        self.mouse.move(v)
        return self.mouse.position

    def down(self):
        # Press and release
        self.mouse.press(Button.left)
        
    def up(self):
        self.mouse.release(Button.left)


