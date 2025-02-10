from db.repositories.example import ExampleRepository
from .base import BaseService


class ExampleService(BaseService):

    async def do_something(self):
        async with self.session_class() as session:
            return await ExampleRepository(session).get_all_async()
