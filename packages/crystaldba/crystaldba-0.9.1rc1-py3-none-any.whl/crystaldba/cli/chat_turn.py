import logging
from typing import Iterator

from crystaldba.cli.chat_response_followup import ChatResponseFollowupProtocol
from crystaldba.shared.api import ChatMessage
from crystaldba.shared.api import DbaChatSyncProtocol
from crystaldba.shared.api import StartupMessage


class ChatTurn:
    def __init__(
        self,
        dba_chat_client: DbaChatSyncProtocol,
        chat_response_followup: ChatResponseFollowupProtocol,
    ):
        self.dba_chat_client = dba_chat_client
        self.chat_response_followup = chat_response_followup
        self.logger = logging.getLogger(__name__)

    def run_to_completion(self, message: ChatMessage | StartupMessage) -> Iterator[str]:
        if isinstance(message, ChatMessage) and not message.message.strip():
            yield from ()
            return

        next_chatrequest_to_send = self.chat_response_followup.create_chatrequest(message)
        while next_chatrequest_to_send is not None:
            try:
                for chat_response in self.dba_chat_client.handle(next_chatrequest_to_send):
                    str_or_next_chatrequest_to_send = self.chat_response_followup.from_chatresponse_to_possible_new_chatrequest(chat_response)
                    if str_or_next_chatrequest_to_send is None:
                        self.logger.debug("CLIENT_LOOP: All done with this turn")
                        return
                    if isinstance(str_or_next_chatrequest_to_send, str):
                        self.logger.debug("CLIENT_LOOP: Returning string")
                        yield str_or_next_chatrequest_to_send
                        # Reset for next iteration
                        next_chatrequest_to_send = None
                    else:
                        self.logger.debug("CLIENT_LOOP: Returning new chatrequest")
                        next_chatrequest_to_send = str_or_next_chatrequest_to_send
                        break

            except (KeyboardInterrupt, EOFError) as e:
                self.logger.debug("CLIENT_LOOP: Handling keyboard interrupt")
                raise e
