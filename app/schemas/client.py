from infra.database.models import Client
from schemas._base import BaseModel, IgnoreCaseEnum, NonEmptyStr, RequestModel, NonNegativeInt, Age


class ClientGenderEnum(IgnoreCaseEnum):
    male = 'MALE'
    female = 'FEMALE'


class ClientResponse(BaseModel):
    client_id: NonEmptyStr
    login: NonEmptyStr
    age: Age
    location: NonEmptyStr
    gender: ClientGenderEnum

    @classmethod
    def from_object(cls, client: Client):
        return cls(client_id=client.id, **client.to_dict())


class ClientRequest(ClientResponse, RequestModel):
    ...
