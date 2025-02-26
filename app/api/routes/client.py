from typing import List

from api.dependencies import get_exists_client
from fastapi import APIRouter, Depends
from infra.database.models import Client
from schemas.client import ClientRequest, ClientResponse
from services.client import ClientService

router = APIRouter(prefix='/clients', tags=['Clients'])


@router.get('/{client_id}', response_model=ClientResponse)
async def get_client(client: Client = Depends(get_exists_client)):
    return ClientResponse.from_object(client)


@router.post('/bulk', response_model=List[ClientResponse], status_code=201)
async def bulk_clients(clients: List[ClientRequest], service: ClientService = Depends(ClientService)):
    items = await service.bulk([client.model_dump() for client in clients])

    return [
        ClientResponse.from_object(client) for client in items
    ]
