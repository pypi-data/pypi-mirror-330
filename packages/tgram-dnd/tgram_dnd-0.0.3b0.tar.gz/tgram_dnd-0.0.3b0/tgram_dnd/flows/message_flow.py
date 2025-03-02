from tgram_dnd.blocks import MessageBlock

from tgram import TgBot, filters
from tgram.types import Message

from typing import List, Optional, Union

class MessageFlow:
    def __init__(
        self,
        blocks: Union[List[MessageBlock], MessageBlock],
        filter: Optional[filters.Filter] = None,
    ):
        self.blocks = [blocks] if not isinstance(blocks, list) else blocks
        self.filter = filter or filters.all

    def add_bot(self, bot: TgBot):
        self.bot = bot

    def load_plugin(self) -> None:
        '''loads plugin into the bot'''
        @self.bot.on_message(self.filter)
        async def handle(
            bot: TgBot,
            m: Message
        ):
            for block in self.blocks:

                for action in block.actions:
                    action.add_bot(self.bot)

                await block.exec(bot, m)