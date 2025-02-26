import time
import uuid
from os import getenv
from typing import Any, Dict

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (DeclarativeBase, Mapped, declared_attr,
                            mapped_column, relationship)

IMAGES_URL = getenv('IMAGES_URL', 'http://localhost:8080/images/')


def generate_uuid():
    return str(uuid.uuid4())


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[str] = mapped_column(
        String, default=generate_uuid, primary_key=True, unique=True)

    def to_dict(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return self.__class__.__name__ + f'({self.id})'


class CurrentDate(Base):
    __tablename__ = 'current_date'

    value = mapped_column(Integer, nullable=False)


class Client(Base):
    __tablename__ = 'clients'

    login = mapped_column(String, nullable=False)
    age = mapped_column(Integer, nullable=False)
    location = mapped_column(String, nullable=False)
    gender = mapped_column(String, nullable=False)


class Advertiser(Base):
    __tablename__ = 'advertisers'

    name = mapped_column(String, nullable=False)


class Campaign(Base):
    __tablename__ = 'campaigns'

    impressions_limit = mapped_column(Integer, nullable=False)
    clicks_limit = mapped_column(Integer, nullable=False)
    cost_per_impression = mapped_column(Float, nullable=False)
    cost_per_click = mapped_column(Float, nullable=False)

    ad_title = mapped_column(String, nullable=False)
    ad_text = mapped_column(String, nullable=False)

    start_date = mapped_column(Integer, nullable=False)
    end_date = mapped_column(Integer, nullable=False)

    gender = mapped_column(String, nullable=True)
    age_from = mapped_column(Integer, nullable=True)
    age_to = mapped_column(Integer, nullable=True)
    location = mapped_column(String, nullable=True)

    image_count = mapped_column(Integer, default=0)

    advertiser_id = mapped_column(ForeignKey('advertisers.id'), nullable=False)
    advertiser: Mapped[Advertiser] = relationship()

    @property
    def images(self):
        return [IMAGES_URL + f'{self.id}_{ind}.png?_={int(time.time())}' for ind in range(1, self.image_count + 1)]


class MLScore(Base):
    __tablename__ = 'ml_scores'

    client_id = mapped_column(ForeignKey('clients.id'), nullable=False)
    client: Mapped[Client] = relationship()

    advertiser_id = mapped_column(ForeignKey('advertisers.id'), nullable=False)
    advertiser: Mapped[Advertiser] = relationship()

    score = mapped_column(Integer, nullable=False)


class ClientCampaign(Base):
    __abstract__ = True

    date = mapped_column(Integer, default=0)
    cost = mapped_column(Float, default=0)

    @declared_attr
    def client_id(cls):
        return mapped_column(ForeignKey('clients.id'))

    @declared_attr
    def client(cls) -> Mapped['Client']:
        return relationship(lazy='subquery')

    @declared_attr
    def campaign_id(cls):
        return mapped_column(ForeignKey('campaigns.id', ondelete='SET NULL'))

    @declared_attr
    def campaign(cls) -> Mapped['Campaign']:
        return relationship(lazy='subquery')


class Impression(ClientCampaign):
    __tablename__ = 'impressions'


class Click(ClientCampaign):
    __tablename__ = 'clicks'
