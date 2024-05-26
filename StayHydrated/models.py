from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from typing import List
from datetime import datetime
from werkzeug.security import generate_password_hash


# Base Class To Create Orm Related Classes MetaData Can be Added
class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String, unique=True)
    name: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)
    registration_date: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )

    personal_data: Mapped["PersonalData"] = relationship(back_populates="user")
    bottles: Mapped[List["Bottle"]] = relationship(back_populates="user")
    goal: Mapped["Goal"] = relationship(back_populates="user")
    records: Mapped[List["Record"]] = relationship(back_populates="user")

    def __init__(
        self,
        username: str,
        password: str,
        name: str,
        surname: str,
        email: str,
    ) -> None:

        self.username = username
        self.password = generate_password_hash(password)
        self.email = email
        self.name = name
        self.surname = surname

    def __repr__(self) -> str:
        return f"User: id={self.id}, username={self.username}, email={self.email}, name={self.name}, surname={self.surname}, registration_date={self.registration_date}, avatar_id={self.avatar_id}"

    def serialize(self) -> tuple:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        data.pop("password")
        data["registration_date"] = data["registration_date"].strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return data


class PersonalData(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sex: Mapped[bool] = mapped_column(Boolean)
    born_date: Mapped[datetime] = mapped_column(DateTime)
    wake_up_time: Mapped[datetime] = mapped_column(DateTime)
    sleep_time: Mapped[datetime] = mapped_column(DateTime)
    weight: Mapped[int] = mapped_column(Integer)
    height: Mapped[int] = mapped_column(Integer)
    activity_level: Mapped[int] = mapped_column(Integer)
    climate: Mapped[int] = mapped_column(Integer)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), unique=True)
    avatar_id: Mapped[int] = mapped_column(Integer, ForeignKey("avatar.id"))

    user: Mapped["User"] = relationship(back_populates="personal_data")
    avatar: Mapped["Avatar"] = relationship(back_populates="personal_data")

    def __init__(
        self,
        user_id: int,
        avatar_id: int,
        sex: bool,
        born_date: datetime,
        wake_up_time: datetime,
        sleep_time: datetime,
        weight: int,
        height: int,
        activity_level: int,
        climate: int,
    ) -> None:
        self.user_id = user_id
        self.avatar_id = avatar_id
        self.sex = sex
        self.born_date = born_date
        self.wake_up_time = wake_up_time
        self.sleep_time = sleep_time
        self.weight = weight
        self.height = height
        self.activity_level = activity_level
        self.climate = climate

    def __repr__(self) -> str:
        return f"Goal: id={self.id}, name={self.name}, user_id={self.user_id}"

    def serialize(self) -> tuple:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return data


class Goal(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    daily_amount: Mapped[int] = mapped_column(Integer)
    completed_days: Mapped[int] = mapped_column(Integer, default=0)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="goal")

    def __init__(
        self,
        user_id: int,
        daily_amount: int,
    ) -> None:

        self.user_id = user_id
        self.daily_amount = daily_amount

    def __repr__(self) -> str:
        return f"Goal: id={self.id}, name={self.name}, user_id={self.user_id}"

    def serialize(self) -> tuple:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return data


class Bottle(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    serial_number: Mapped[int] = mapped_column(Integer, unique=True)
    capacity: Mapped[int] = mapped_column(Integer)
    current_amount: Mapped[int] = mapped_column(Integer, default=0)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="bottles")

    def __init__(
        self,
        user_id: int,
        serial_number: int,
        capacity: int,
    ) -> None:

        self.user_id = user_id
        self.serial_number = serial_number
        self.capacity = capacity

    def __repr__(self) -> str:
        return f"Bottle: id={self.id}, serial_numer={self.serial_number}, capacity={self.capacity} user_id={self.user_id}"

    def serialize(self) -> tuple:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return data


class Record(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    amount: Mapped[int] = mapped_column(Integer)
    record_type: Mapped[bool] = mapped_column(Boolean)

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    user: Mapped["User"] = relationship(back_populates="records")

    def __init__(
        self,
        user_id:int,
        amount: int,
        record_type: bool,
    ) -> None:

        self.user_id = user_id
        self.amount = amount
        self.record_type = record_type

    def __repr__(self) -> str:
        return f"Record: id={self.id}, record_time={self.record_time}, amount={self.amount}, record_type={self.record_type}, user_id={self.user_id}"

    def serialize(self) -> tuple:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return data


class Avatar(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    folder_path: Mapped[str] = mapped_column(String)

    personal_data: Mapped["PersonalData"] = relationship(back_populates="avatar")
    reminders: Mapped[List["Reminder"]] = relationship(back_populates="avatar")

    def __init__(
        self,
        name: str,
        folder_path: str,
    ) -> None:
        self.name = name
        self.folder_path = folder_path

    def __repr__(self) -> str:
        return f"Avatar: id={self.id}, name={self.name}"

    def serialize(self) -> tuple:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return data


class Reminder(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String)
    message_type: Mapped[int] = mapped_column(Integer)
    message: Mapped[str] = mapped_column(String)

    avatar_id: Mapped[int] = mapped_column(Integer, ForeignKey("avatar.id"))

    avatar: Mapped["Avatar"] = relationship(back_populates="reminders")

    def __repr__(self) -> str:
        return f"RemindMessage: id={self.id}, name={self.name}, message_type={self.message_type}"

    def serialize(self) -> tuple:
        data = {c.name: getattr(self, c.name) for c in self.__table__.columns}
        return data
