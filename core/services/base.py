from core.abstract import App


class BaseService:

    def __init__(self, app: App):
        self.app = app
        self.db = app.db_async
        self.session_class = self.db.session_class
