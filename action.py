'''
defines an action of an automation.  to start this action will simply be to set
an output pin to 0 or 1

this should be an abstract class and then concrete classes for each type of action
to start, will just create a "PinAction" type which will set an output pin to 0 or 1

actions can be abstracted out for plugins, like a ScreenAction (to display values on a screen),
or to send a message, etc.
'''
class Action:
    def __init__(self):
        pass

    def run(self):
        pass


'''
config is a json string
the init method takes the json string configuration 

'''
class PinAction(Action):
    def __init__(self, pin_number: int, value: bool):
        self._pin_number = pin_number
        self._value = value

    def run(self):
        print("I ran the PinAction")
        print(self)

