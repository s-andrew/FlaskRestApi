from abc import ABCMeta, abstractmethod
from functools import partial

from .crud_operations import create, readall, readone, update, delete
from .abstract_resource import AbstractResource


class CrudResource(AbstractResource):
    __metaclass__ = ABCMeta

    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def readall(self):
        pass

    @abstractmethod
    def readone(self, entity_id):
        pass

    @abstractmethod
    def update(self, entity_id, entity):
        pass

    @abstractmethod
    def delete(self, entity_id):
        pass

    @classmethod
    def get_create_view_func(cls):
        partial(cls.create, None)
        return partial(create, partial(cls.create, None))

    @classmethod
    def get_readall_view_func(cls):
        return partial(readall, partial(cls.readall, None))

    @classmethod
    def get_readone_view_func(cls):
        return partial(readone, partial(cls.readone, None))

    @classmethod
    def get_update_view_func(cls):
        return partial(update, partial(cls.update, None))

    @classmethod
    def get_delete_view_func(cls):
        return partial(delete, partial(cls.delete, None))
