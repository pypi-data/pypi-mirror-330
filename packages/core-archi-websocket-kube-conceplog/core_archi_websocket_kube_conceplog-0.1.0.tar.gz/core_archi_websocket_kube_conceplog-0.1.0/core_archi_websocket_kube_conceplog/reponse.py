from pydantic import BaseModel


class Reponse(BaseModel):
    user:str
    reponse:str