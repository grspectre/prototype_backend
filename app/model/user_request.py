from pydantic import BaseModel, Field, field_serializer, EmailStr
from uuid import UUID, uuid4
from datetime import date, datetime
from typing import List
from enum import Enum


class RequestReason(str, Enum):
    network = "нет доступа к сети"
    phone = "не работает телефон"
    email = "не приходят письма"


class UserRequest(BaseModel):
    id: UUID = Field(default_factory=uuid4, description="Unique ID")
    last_name: str = Field(default="Фамилия", pattern=r"^[А-ЯЁ][А-яёЁ]+$", description="Client last name")
    first_name: str = Field(default="Имя", pattern=r"^[А-ЯЁ][А-яёЁ]+$", description="Client first name")
    birthday: date = Field(default = date(1970, 1, 1), description="User birthday")
    phone_number: str | None = Field(default=None, pattern=r"\d{10,15}", description="User phone number")
    email: EmailStr | None = Field(default=None, description="User email")
    detection_datetime: datetime = Field(default=datetime.now(), description="Detection datetime")
    reason: List[RequestReason] = Field(default=[])


if __name__ == '__main__':
    req1 = UserRequest(reason=[RequestReason.network, RequestReason.email])
    print(req1.model_dump_json())