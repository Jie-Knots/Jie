import types
from functools import wraps
from inspect import isawaitable

from sanic.views import HTTPMethodView
from sanic.request import Request


class ViewRoute:
    """Decorat a HTTPMethodView instance to be registered as a route.
    """

    def __init__(self, app, url, *args, **kwargs):
        """

        :param app: sanic app or blueprint
        :param url: path of the URL
        """
        self.app = app
        self.url = url

    def __call__(self, instance):
        """Add instance's view to app.

        :param instance: a instance of HTTPMethodView
        :return instance
        """
        def decorate(instance):

            if not getattr(self, '__name__', None):
                wraps(instance)(self)
            self.app.add_route(instance.as_view(), self.url)
        
        decorate(instance)
        return instance

    def __get__(self, instance, cls):
        if instance is None:
            return self
        else:
            return types.MethodType(self, instance)


def db_transaction(func):
    """A decorator to add db connection and start transaction
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request = args[0] if isinstance(args[0], Request) else args[1]
        pool = request.app.env.db_pool
        db_connection = await pool.acquire()
        tr = db_connection.transaction()
        await tr.start()
        try:
            result = func(*args, **dict(kwargs, db_connection=db_connection))
            if isawaitable(result):
                result = await result
        except:
            await tr.rollback()
            raise
        else:
            await tr.commit()
        finally:
            await db_connection.close()
            await pool.release(db_connection)
        return result
    return wrapper


class DBTransactionView(HTTPMethodView):
    """Add database transaction to decorators
    """
    decorators = [db_transaction]
