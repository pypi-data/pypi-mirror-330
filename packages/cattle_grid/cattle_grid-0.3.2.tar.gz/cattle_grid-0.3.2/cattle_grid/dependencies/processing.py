import logging

from typing import Annotated
from faststream import Depends

from cattle_grid.activity_pub.models import Actor
from cattle_grid.model.common import WithActor


logger = logging.getLogger(__name__)


class ProcessingError(ValueError): ...


async def actor_id(msg: WithActor) -> str:
    return msg.actor


async def actor_for_message(actor_id: str = Depends(actor_id)):
    actor = await Actor.get_or_none(actor_id=actor_id)

    if actor is None:
        raise ProcessingError("Actor not found")

    return actor


MessageActor = Annotated[Actor, Depends(actor_for_message)]
"""Returns the actor for the message"""
