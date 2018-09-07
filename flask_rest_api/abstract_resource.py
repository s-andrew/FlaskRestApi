from abc import ABCMeta, abstractmethod


class AbstractResource:
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_create_view_func(self):
        pass

    @abstractmethod
    def get_readall_view_func(self):
        pass

    @abstractmethod
    def get_readone_view_func(self):
        pass

    @abstractmethod
    def get_update_view_func(self):
        pass

    @abstractmethod
    def get_delete_view_func(self):
        pass
