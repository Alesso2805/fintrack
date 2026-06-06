from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


import app.models.user  # noqa: E402,F401
import app.models.financial  # noqa: E402,F401
