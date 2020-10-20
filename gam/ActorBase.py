from .ElementBase import *


class ActorBase(ElementBase):
    """
    Store user information about an actor and the corresponding g4 object
    """

    def __init__(self, actor_type, name):
        ElementBase.__init__(self, actor_type, name)
        # define the actions that will trigger the actor
        # (this attribute is a vector<string> on the cpp side)
        self.actions = []
        # default required user info
        self.user_info.attachedTo = 'World'

    def __del__(self):
        print('ActorBase destructor')

    def __str__(self):
        s = f'str ActorBase {self.user_info.name} of type {self.user_info.type}'
        return s

    def initialize(self):
        # check the user parameters
        self.check_user_info()
