import uuid
from typing import Dict, Any, Optional, Callable, Awaitable

from .hooks import eggai_register_stop
from .transport.base import Transport
from .transport import get_default_transport


class Channel:
    """
    A channel that publishes messages to a given 'name' on its own Transport.
    Default name is "eggai.channel".
    Lazy connection on first publish or subscription.
    """

    def __init__(self, name: str = "eggai.channel", transport: Optional[Transport] = None):
        """
        :param name: Channel (topic) name.
        :param transport: A concrete transport instance.
        """
        self._name = name
        self._default_group_id = name + "_group_" + uuid.uuid4().hex
        self._transport = transport
        self._connected = False
        self._stop_registered = False

    async def _ensure_connected(self):
        if not self._connected:
            if self._transport is None:
                self._transport = get_default_transport()

            # Connect with group_id=None for publish-only by default,
            # but the transport may support both publishing and subscribing on the same connection.
            await self._transport.connect()
            self._connected = True
            # Auto-register stop
            if not self._stop_registered:
                await eggai_register_stop(self.stop)
                self._stop_registered = True

    async def publish(self, message: Dict[str, Any]):
        """
        Lazy-connect on first publish.
        """
        await self._ensure_connected()
        await self._transport.publish(self._name, message)

    async def subscribe(self, callback: Callable[[Dict[str, Any]], Awaitable[None]], group_id: Optional[str] = None):
        """
        Subscribe to this channel by registering a callback to be invoked on message receipt.

        :param callback: An asynchronous function that takes a message dict as its parameter.
        :param group_id: The consumer group ID to use. If None, a default group ID is generated.
        """
        await self._ensure_connected()
        await self._transport.subscribe(self._name, callback, group_id or self._default_group_id)

    async def stop(self):
        if self._connected:
            await self._transport.disconnect()
            self._connected = False
