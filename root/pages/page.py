import abc
from flask import Blueprint

class Page(Blueprint):
    __metaclass__ = abc.ABCMeta

    def __init__(self, *args, **kwargs):
        Blueprint.__init__(self, *args, **kwargs)

        self.__config = {}

    @abc.abstractmethod
    def GetName(self):
        return

    @abc.abstractmethod
    def GetRootUrl(self):
        return

    def SetConfig(self, app):
        self.__config = dict([(key,value) for (key,value) in 
                      app.config.items()])

    def GetConfig(self):
        return self.__config

