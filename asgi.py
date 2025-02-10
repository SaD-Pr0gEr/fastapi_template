from core import make_app
from core.config import Misc


misc = Misc()
application = make_app(
    misc.TOML_CONFIG, misc.PSQL_ENV, misc.REDIS_ENV, misc.MAIN_ENV, misc
)
