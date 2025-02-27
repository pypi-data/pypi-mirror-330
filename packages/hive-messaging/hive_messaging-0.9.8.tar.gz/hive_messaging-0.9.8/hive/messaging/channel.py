import inspect
import json
import logging
import os
import sys
import warnings

from functools import cache, cached_property
from traceback import format_exc
from typing import Callable, Optional
from uuid import uuid4

from pika import BasicProperties, DeliveryMode

from . import semantics
from .message import Message
from .wrapper import WrappedPikaThing

logger = logging.getLogger(__name__)


class Channel(WrappedPikaThing):
    """The primary entry point for interacting with Hive's message bus.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._pre_publish_hooks = []

    # QUEUES are declared by their consuming service

    # CONSUME_* methods process to completion or dead-letter the message

    # REQUESTS are things we're asking to be done:
    # - Each request queue has exactly one consuming service
    # - Publish delivers the message or raises an exception
    # - Consume processes to completion or dead-letters the message

    def publish_request(self, **kwargs):
        return self._publish_direct(
            self.requests_exchange,
            **kwargs
        )

    def consume_requests(self, **kwargs):
        return self._consume_direct(
            self.requests_exchange,
            **kwargs
        )

    # RPC REQUESTS wrap standard requests, and mostly share the same
    # semantics.

    def publish_rpc_request(
            self,
            request: bytes | dict,
            *,
            routing_key: str,
            correlation_id: Optional[str] = None,
            reply_to: Optional[str] = None,
            **kwargs
    ) -> str:
        if not reply_to:
            reply_to = self.rpc_responses_queue_for(routing_key)
        if not correlation_id:
            correlation_id = str(uuid4())
        self.publish_request(
            message=request,
            routing_key=routing_key,
            correlation_id=correlation_id,
            reply_to=reply_to,
            **kwargs
        )
        return correlation_id

    def consume_rpc_requests(
            self,
            *,
            on_message_callback: Callable,
            **kwargs
    ):
        def _wrapped_callback(channel: Channel, request: Message):
            response_routing_key = request.reply_to
            correlation_id = request.correlation_id

            try:
                response = on_message_callback(channel, request)
            except Exception:
                response = {"error": format_exc()}

            return self._publish_direct(
                message=response,
                routing_key=response_routing_key,
                exchange="",
                correlation_id=correlation_id,
            )

        return self.consume_requests(
            on_message_callback=_wrapped_callback,
            **kwargs
        )

    def consume_rpc_responses_for(self, requests_queue: str, **kwargs):
        return self.consume_rpc_responses(
            queue=self.rpc_responses_queue_for(requests_queue),
            **kwargs
        )

    def consume_rpc_responses(self, **kwargs):
        return self._basic_consume(**kwargs)

    # EVENTS are things that have happened:
    # - DIRECT EVENTS have the same semantics as requests
    #
    # - FANOUT EVENTS are different:
    #   - Transient events fan-out to zero-many consuming services
    #   - Publish drops messages with no consumers

    def publish_event(self, *, mandatory: bool = False, **kwargs):
        if mandatory:
            return self._publish_direct(
                self.direct_events_exchange,
                **kwargs
            )
        return self._publish_fanout(**kwargs)

    def maybe_publish_event(self, **kwargs):
        semantics.publish_may_drop(kwargs)
        try:
            self.publish_event(**kwargs)
        except Exception:
            logger.warning("EXCEPTION", exc_info=True)

    def consume_events(
            self,
            queue: str,
            mandatory: bool = False,
            **kwargs
    ):
        if mandatory:
            return self._consume_direct(
                self.direct_events_exchange,
                queue=queue,
                **kwargs
            )
        return self._consume_fanout(queue, **kwargs)

    # Lower level handlers for REQUESTS and EVENTS

    def _publish_direct(self, exchange: str, **kwargs):
        semantics.publish_must_succeed(kwargs)
        return self._publish(exchange=exchange, **kwargs)

    def _publish_fanout(self, routing_key: str, **kwargs):
        semantics.publish_may_drop(kwargs)
        exchange = self._fanout_exchange_for(routing_key)
        return self._publish(exchange=exchange, **kwargs)

    def _consume_direct(
            self,
            exchange: str,
            *,
            queue: str,
            on_message_callback: Callable,
    ):
        self.queue_declare(
            queue,
            dead_letter_routing_key=queue,
            durable=True,
        )

        self.queue_bind(
            queue=queue,
            exchange=exchange,
            routing_key=queue,
        )

        return self._basic_consume(queue, on_message_callback)

    def _consume_fanout(
            self,
            routing_key: str,
            *,
            on_message_callback: Callable,
    ):
        exchange = self._fanout_exchange_for(routing_key)
        if (queue := self.consumer_name):
            queue = f"{queue}.{routing_key}"

        queue = self.queue_declare(
            queue,
            exclusive=True,
        ).method.queue

        self.queue_bind(
            queue=queue,
            exchange=exchange,
        )

        return self._basic_consume(queue, on_message_callback)

    @cached_property
    def consumer_name(self) -> str:
        """Name for per-consumer fanout queues to this channel.
        May be overwritten or overridden (you'll actually have
        to if more than one channel per process consumes the
        same fanout "queue").
        """
        return ".".join(
            part for part in os.path.basename(sys.argv[0]).split("-")
            if part != "hive"
        )

    @cached_property
    def exclusive_queue_prefix(self) -> str:
        """Prefix for named exclusive queues on this channel.
        Should be the empty string for production environments.
        """
        envvar = "HIVE_EXCLUSIVE_QUEUE_PREFIX"
        result = os.environ.get(envvar, "").rstrip(".")
        if not result:
            return ""
        return f"{result}."

    # Exchanges

    @cache
    def _fanout_exchange_for(self, routing_key: str) -> str:
        return self._hive_exchange(
            exchange=routing_key,
            exchange_type="fanout",
            durable=True,
        )

    @cached_property
    def direct_events_exchange(self) -> str:
        return self._hive_exchange(
            exchange="events",
            exchange_type="direct",
            durable=True,
        )

    @cached_property
    def requests_exchange(self) -> str:
        return self._hive_exchange(
            exchange="requests",
            exchange_type="direct",
            durable=True,
        )

    @cached_property
    def dead_letter_exchange(self) -> str:
        return self._hive_exchange(
            exchange="dead.letter",
            exchange_type="direct",
            durable=True,
        )

    def _hive_exchange(self, exchange: str, **kwargs) -> str:
        name = f"hive.{exchange}"
        self.exchange_declare(exchange=name, **kwargs)
        return name

    # Queues

    def rpc_responses_queue_for(self, request_queue: str) -> str:
        stem = request_queue.removesuffix(".requests")
        return self.queue_declare(
            f"{self.consumer_name}.{stem}.responses",
            exclusive=True,
        ).method.queue

    def queue_declare(
            self,
            queue: str,
            *,
            dead_letter_routing_key: Optional[str] = None,
            arguments: Optional[dict[str, str]] = None,
            **kwargs
    ):
        if kwargs.get("exclusive", False) and queue:
            queue = f"{self.exclusive_queue_prefix}{queue}"

        if dead_letter_routing_key:
            DLX_ARG = "x-dead-letter-exchange"
            if arguments:
                if DLX_ARG in arguments:
                    raise ValueError(arguments)
                arguments = arguments.copy()
            else:
                arguments = {}

            dead_letter_queue = f"x.{dead_letter_routing_key}"
            self._pika.queue_declare(
                dead_letter_queue,
                durable=True,
            )

            dead_letter_exchange = self.dead_letter_exchange
            self.queue_bind(
                queue=dead_letter_queue,
                exchange=dead_letter_exchange,
                routing_key=dead_letter_routing_key,
            )

            arguments[DLX_ARG] = dead_letter_exchange

        if arguments:
            kwargs["arguments"] = arguments
        return self._pika.queue_declare(
            queue,
            **kwargs
        )

    def add_pre_publish_hook(self, hook: Callable):
        self._pre_publish_hooks.append(hook)

    def _publish(self, **kwargs):
        for hook in self._pre_publish_hooks:
            try:
                hook(self, **kwargs)
            except Exception:
                logger.exception("EXCEPTION")
        return self._basic_publish(**kwargs)

    def _basic_publish(
            self,
            *,
            message: bytes | dict,
            exchange: str = "",
            routing_key: str = "",
            content_type: Optional[str] = None,
            correlation_id: Optional[str] = None,
            delivery_mode: DeliveryMode = DeliveryMode.Persistent,
            mandatory: bool = True,
            reply_to: Optional[str] = None,
    ):
        payload, content_type = self._encapsulate(message, content_type)
        return self.basic_publish(
            exchange=exchange,
            routing_key=routing_key,
            body=payload,
            properties=BasicProperties(
                content_type=content_type,
                correlation_id=correlation_id,
                delivery_mode=delivery_mode,  # Persist across broker restarts.
                reply_to=reply_to,
            ),
            mandatory=mandatory,  # Don't fail silently.
        )

    @staticmethod
    def _encapsulate(
            msg: bytes | dict,
            content_type: Optional[str],
    ) -> tuple[bytes, str]:
        """Prepare messages for transmission.
        """
        if not isinstance(msg, bytes):
            return json.dumps(msg).encode("utf-8"), "application/json"
        if not content_type:
            raise ValueError(f"content_type={content_type}")
        return msg, content_type

    @property
    def prefetch_count(self):
        return getattr(self, "_prefetch_count", None)

    @prefetch_count.setter
    def prefetch_count(self, value):
        if self.prefetch_count == value:
            return
        if self.prefetch_count is not None:
            raise ValueError(value)
        self.basic_qos(prefetch_count=value)
        self._prefetch_count = value

    def _prepare_omcb(self, cb: Callable) -> Callable:
        """Prepare on_message_callback.
        """
        sig = inspect.signature(cb)
        num_params = len(sig.parameters)
        if num_params == 2:
            return cb
        if num_params != 4:
            raise TypeError(cb)

        warnings.warn(DeprecationWarning(
            "Pika-style on-message callbacks are deprecated"
        ))

        def _wrapped_callback(channel: Channel, msg: Message):
            return cb(channel, msg.method, msg.properties, msg.body)

        return _wrapped_callback

    def _basic_consume(
            self,
            queue: str,
            on_message_callback: Callable,
    ):
        on_message_callback = self._prepare_omcb(on_message_callback)

        self.prefetch_count = 1  # Receive one message at a time.

        def _wrapped_callback(channel: Channel, message: Message):
            delivery_tag = message.method.delivery_tag
            try:
                result = on_message_callback(channel, message)
                channel.basic_ack(delivery_tag=delivery_tag)
                return result
            except Exception as e:
                channel.basic_reject(delivery_tag=delivery_tag, requeue=False)
                logged = False
                try:
                    if isinstance(e, NotImplementedError) and e.args:
                        traceback = e.__traceback__
                        while (next_tb := traceback.tb_next):
                            traceback = next_tb
                        code = traceback.tb_frame.f_code
                        try:
                            func = code.co_qualname
                        except AttributeError:
                            func = code.co_name  # Python <=3.10
                        logger.warning("%s:%s:UNHANDLED", func, e)
                        logged = True

                except Exception:
                    logger.exception("NESTED EXCEPTION")
                if not logged:
                    logger.exception("EXCEPTION")

        return self.basic_consume(
            queue=queue,
            on_message_callback=_wrapped_callback,
        )

    def basic_consume(
            self,
            queue: str,
            on_message_callback,
            *args,
            **kwargs
    ):
        def _wrapped_callback(channel, *args, **kwargs):
            assert channel is self._pika
            return on_message_callback(self, Message(*args, **kwargs))

        return self._pika.basic_consume(
            queue=queue,
            on_message_callback=_wrapped_callback,
            *args,
            **kwargs
        )


class PublisherChannel:
    def __init__(self, invoker, channel):
        self._invoker = invoker
        self._channel = channel

    def __getattr__(self, attr):
        result = getattr(self._channel, attr)
        if not callable(result):
            return result
        return PublisherInvoker(self._invoker, result)


class PublisherInvoker:
    def __init__(self, invoker, func):
        self._invoke = invoker
        self._func = func

    def __call__(self, *args, **kwargs):
        return self._invoke(self._func, *args, **kwargs)
