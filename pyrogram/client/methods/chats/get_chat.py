# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

import pyrogram
from pyrogram.api import functions, types
from ...ext import BaseClient


class GetChat(BaseClient):
    async def get_chat(self,
                       chat_id: Union[int, str]) -> "pyrogram.Chat":
        """Use this method to get up to date information about the chat (current name of the user for
        one-on-one conversations, current username of a user, group or channel, etc.)

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            On success, a :obj:`Chat <pyrogram.Chat>` object is returned.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChannel):
            r = await self.send(functions.channels.GetFullChannel(peer))
        elif isinstance(peer, (types.InputPeerUser, types.InputPeerSelf)):
            r = await self.send(functions.users.GetFullUser(peer))
        else:
            r = await self.send(functions.messages.GetFullChat(peer.chat_id))

        return pyrogram.Chat._parse_full(self, r)
