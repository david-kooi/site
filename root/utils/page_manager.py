import bisect

class PageManager(object):

    __instance = None

    def __init__(self):
        self.__page_list = []

    def RegisterPage(self, page):
        bisect.insort(self.__page_list, page.GetName())

    def GetPageList(self):
        return self.__page_list

    def GetInstance():
        """
        Return instance of singleton.
        """
        if(PageManager.__instance is None):
            PageManager.__instance = PageManager()
        return PageManager.__instance

    #define static method
    GetInstance = staticmethod(GetInstance)
