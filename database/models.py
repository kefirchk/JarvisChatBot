from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Mapped, mapped_column

Base = declarative_base()


class UserValuesOrm(Base):
    __tablename__ = "user_values"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[str]
    user_id: Mapped[int]

