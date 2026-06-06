from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


import app.models.user
import app.models.financial
import app.models.imports
import app.models.audit
