from .ElementBase import *


class ActorBase(ElementBase):
    """
    Store user information about an actor and the corresponding g4 object
    """

    def __init__(self, name):
        ElementBase.__init__(self, name)
        # define the actions that will trigger the actor
        # (this attribute is a vector<string> on the cpp side)
        # default required user info
        self.user_info.attached_to = 'World'

    def __del__(self):
        pass

    def __str__(self):
        s = f'str ActorBase {self.user_info.name} of type {self.user_info.type}'
        return s