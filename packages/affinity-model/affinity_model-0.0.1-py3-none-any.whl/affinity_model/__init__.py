from pydantic import BaseModel, model_serializer


class MyBaseModel(BaseModel):
    pass


__all__ = ["MyBaseModel", "v1", "v2"]
