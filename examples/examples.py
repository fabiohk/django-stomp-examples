import logging
import uuid

from django_stomp.builder import build_publisher
from django_stomp.services.consumer import Payload
from django_stomp.services.producer import auto_open_close_connection
from django_stomp.services.producer import do_inside_transaction

logger = logging.getLogger(__name__)


def publish(destination: str):
    """
    Publish an empty dictionary to the given destination.
    """
    publisher = build_publisher(f"publisher-{uuid.uuid4()}")
    with publisher.auto_open_close_connection() as publisher:
        publisher.send({}, destination)


def publish_under_transaction(destination: str, message_count: int):
    """
    Publish `message_count` empty dictionaries to the given destination under a transaction.

    If any error occur while sending a message, the transaction is aborted and no
    message is effectively sent to the destination.
    """
    publisher = build_publisher(f"publisher-{uuid.uuid4()}")
    with auto_open_close_connection(publisher), do_inside_transaction(publisher):
        for _ in range(message_count):
            publisher.send({}, destination)


def ack_callback(payload: Payload):
    """
    Acknoweledge that the message was received, informing the broker that it can
    remove the message from queue.
    """
    logger.info(payload)
    payload.ack()


def nack_callback(payload: Payload):
    """
    Acknoweledge that the message was received, but inform the broker that it cannot
    successfully process the message, requesting it to send the message to a DLQ
    (dead-lettered queue) that will be processed later.
    """
    logger.info(payload)
    payload.nack()


def exception_callback(payload: Payload):
    """
    Raise an exception, leaving it to django-stomp to deal with it. Django-stomp will, then,
    nack the message, requesting the broker to send the message to a DLQ.
    """
    logger.info(payload)
    raise Exception("Won't process!")
