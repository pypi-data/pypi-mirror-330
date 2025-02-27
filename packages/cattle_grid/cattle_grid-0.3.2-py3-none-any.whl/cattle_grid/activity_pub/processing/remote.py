import logging

from cattle_grid.activity_pub.models import InboxLocation
from cattle_grid.model import FetchMessage

from cattle_grid.dependencies import LookupAnnotation
from cattle_grid.model.lookup import Lookup

from cattle_grid.model.processing import ToSendMessage
from .common import MessageBovineActor


logger = logging.getLogger(__name__)


async def fetch_object(
    msg: FetchMessage,
    actor: MessageBovineActor,
    lookup: LookupAnnotation,
):
    """Handles retrieving a remote object"""

    try:
        lookup_result = await lookup(Lookup(uri=msg.uri, actor=msg.actor))
        if lookup_result.result:
            return lookup_result.result
    except Exception as e:
        logger.error("Something went up with lookup")
        logger.exception(e)

        lookup_result = Lookup(uri=msg.uri, actor=msg.actor)

    result = await actor.get(lookup_result.uri, fail_silently=True)

    return result


async def resolve_inbox(actor, target):
    """Resolves the inbox of target for actor using
    a cache"""
    cached = await InboxLocation.get_or_none(actor=target)
    if cached:
        return cached.inbox

    target_actor = await actor.get(target)
    if not target_actor:
        return None

    inbox = target_actor.get("inbox")
    if inbox is None:
        return

    await InboxLocation.update_or_create(actor=target, defaults={"inbox": inbox})

    return inbox


async def sending_message(
    msg: ToSendMessage,
    actor: MessageBovineActor,
):
    """Handles sending a message"""
    inbox = await resolve_inbox(actor, msg.target)
    if inbox:
        result = await actor.post(inbox, msg.data)
        logger.info("Got %s for sending to %s", str(result), inbox)
