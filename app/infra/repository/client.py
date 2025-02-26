from exceptions import SQLException
from infra.database.models import Client
from infra.database.session import async_session
from infra.repository._base import BaseRepository
from sqlalchemy import insert, select, update
from sqlalchemy.exc import IntegrityError


class ClientRepository(BaseRepository[Client]):
    model = Client
    session = async_session

    async def bulk_clients(self, clients: list[dict]):
        ids = []

        async with self.session() as session:
            try:
                async with session.begin():
                    for client_data in clients:
                        client_id = client_data.pop('client_id')
                        ids.append(client_id)

                        client = await session.scalar(select(self.model).where(self.model.id == client_id))
                        if client is None:
                            await session.execute(insert(self.model).values(id=client_id, **client_data))
                        else:
                            await session.execute(update(self.model).where(self.model.id == client_id).values(**client_data))
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                raise SQLException

        async with self.session() as session:
            items = await session.scalars(select(self.model).where(self.model.id.in_(ids)))
            sorted_items = sorted(
                items.all(), key=lambda item: ids.index(item.id))

            return sorted_items
