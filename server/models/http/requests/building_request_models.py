from pydantic import BaseModel


class BuildingRegister(BaseModel):
    name: str


class BuildingUpdate(BaseModel):
    name: str
