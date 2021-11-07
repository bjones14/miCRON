'''
Defines the automation class which is used to run configurable automations
at specified rates and carry out specific actions based on conditionals

JSON-configurable automations that run in this loop
need to define configuration for an automation

automation class:
  frequency_in_ms: how often to run the automation check
  trigger:
    when x > y for z seconds: allow variables or constants for x/y an then constant for z, store timer in class
  action:
    turn on pin #
    turn off pin #

automation has a trigger (time, value_change, etc)
the trigger dictates when the automation will be run
initially, the only trigger to be supported will be TimeTrigger
make a parent abstract class of trigger with different concrete subclasses like
TimeTrigger, ValueTrigger, etc.
eventually the automation can have multiple triggers.
the triggers will need a way to tell the automation to run.  

once an automation is triggered a condition is then evaluated.
a condition, to start at least, will be treated like an if/else statement
the user can map any number of actions to a conditional output - to start
there will just be a true condition and a false condition, and based on which
one of the conditions are true will dictate which action to take

'''
class automation:

    def __init__(self, rate_ms, conditions, actions):
        pass

    def run(self):
        pass