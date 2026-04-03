from pydantic import BaseModel, Field


class CreateProduct(BaseModel):
    name: str
    sale: int = Field(ge=0)
