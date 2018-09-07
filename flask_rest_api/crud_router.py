from .crud_operations import create, readall, readone, update, delete
from .abstract_resource import AbstractResource


class CrudRouter(AbstractResource):
    def __init__(self):
        self.__create = lambda *args, **kwargs: ('', 400)
        self.__readall = lambda *args, **kwargs: ('', 400)
        self.__readone = lambda *args, **kwargs: ('', 400)
        self.__update = lambda *args, **kwargs: ('', 400)
        self.__delete = lambda *args, **kwargs: ('', 400)
        return

    def create(self, decorated_function):
        def create_wrapper():
            return create(decorated_function)

        self.__create = create_wrapper
        return create_wrapper

    def readall(self, decorated_function):
        def readall_wrapper():
            return readall(decorated_function)

        self.__readall = readall_wrapper
        return readall_wrapper

    def readone(self, decorated_function):
        def readone_wrapper(entity_id):
            return readone(decorated_function, entity_id)

        self.__readone = readone_wrapper
        return readone_wrapper

    def update(self, decorated_function):
        def update_wrapper(entity_id):
            return update(decorated_function, entity_id)

        self.__update = update_wrapper
        return update_wrapper

    def delete(self, decorated_function):
        def delete_wrapper(entity_id):
            return delete(decorated_function, entity_id)

        self.__delete = delete_wrapper
        return delete_wrapper

    def get_create_view_func(self):
        return self.__create

    def get_readall_view_func(self):
        return self.__readall

    def get_readone_view_func(self):
        return self.__readone

    def get_update_view_func(self):
        return self.__update

    def get_delete_view_func(self):
        return self.__delete
