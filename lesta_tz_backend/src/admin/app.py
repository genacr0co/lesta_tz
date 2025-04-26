from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin.contrib.sqla import Admin
from starlette_admin import I18nConfig

from src.schemas_validation import *
from src.config import SECRET_KEY
from src.db import engine

from .models import Word
from .provider import MyAuthProvider
from starlette_admin.contrib.sqla.ext.pydantic import ModelView

from starlette_admin.contrib.sqla import  ModelView as SqlaModelView

admin = Admin(
    engine,
    title="Lesta TF_IDF admin",
    base_url="/admin",
    auth_provider=MyAuthProvider(),
    middlewares=[Middleware(SessionMiddleware, secret_key=SECRET_KEY)],
    i18n_config = I18nConfig(default_locale="ru"),
)

admin.add_view(SqlaModelView(Word))


