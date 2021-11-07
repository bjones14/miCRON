'''
This is a helper class that adapts the PCD8544 to work with miCRON.

It will define actions that the micropython_pcd8544 library provides.

It will provide action classes for all the actions the device can provide.

Probably create a wrapper class here called miCRON_PCD8544 that will create an instance
of the micropython_PCD8544 class and then also contain action subclasses for each type of
action supported and its implementation.


'''

from micropython_pcd8544 import PCD8544
from action import Action
import framebuf

'''
wrapper class

this wrapper class will initialize the PCD8544 and create action wrappers that miCRON can use

may eventually want to encapsulate more in the lowest level driver

also want to simplify the driver, I think there are unncessary steps with it

'''
class micron_PCD8544():
    def __init__(self, spi, cs, dc, rst):
        self._PCD8544 = PCD8544(spi, cs, dc, rst)

        # create action object(s)
        self._text_action = TextAction(self._PCD8544) 
    
    @property
    def text_action(self):
      return self._text_action
      

'''
This action will write text to the display.
'''
class TextAction(Action):
    def __init__(self, PCD8544):
        super().__init__()
        self._PCD8544 = PCD8544

    def run(self, buffer):
        self._PCD8544.data(buffer)

