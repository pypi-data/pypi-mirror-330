import grpc
import collections
from typing import Callable, Union

from grpc.aio import StreamStreamCall
from grpc.aio._typing import ResponseIterableType

HTTP_AUTHENTICATION_HEADER = "x-api-key"
HTTP_USER_AGENT_HEADER = "user-agent"

class AuthenticationInterceptor(grpc.aio.UnaryUnaryClientInterceptor,
                                grpc.aio.UnaryStreamClientInterceptor,
                                grpc.aio.StreamStreamClientInterceptor,):
    def __init__(self, api_key: str, user_agent: str):
        self.access_token = api_key
        self.user_agent = user_agent

    async def intercept_unary_unary(self, continuation: Callable, client_call_details: grpc.ClientCallDetails, request):
        metadata = list(client_call_details.metadata or [])
        metadata.append((HTTP_AUTHENTICATION_HEADER, self.access_token))
        metadata.append((HTTP_USER_AGENT_HEADER, self.user_agent))

        new_details = self._update_client_call_details(client_call_details, metadata)
        return await continuation(new_details, request)

    async def intercept_unary_stream(self, continuation: Callable, client_call_details: grpc.ClientCallDetails, request):
        metadata = list(client_call_details.metadata or [])
        metadata.append((HTTP_AUTHENTICATION_HEADER, self.access_token))
        metadata.append((HTTP_USER_AGENT_HEADER, self.user_agent))

        new_details = self._update_client_call_details(client_call_details, metadata)
        return await continuation(new_details, request)

    async def intercept_stream_stream(self, continuation: Callable,
                                      client_call_details: grpc.ClientCallDetails,
                                      request_iterator) -> Union[ResponseIterableType, StreamStreamCall]:
        metadata = list(client_call_details.metadata or [])
        metadata.append((HTTP_AUTHENTICATION_HEADER, self.access_token))
        metadata.append((HTTP_USER_AGENT_HEADER, self.user_agent))

        new_details = self._update_client_call_details(client_call_details, metadata)
        return await continuation(new_details, request_iterator)

    def _update_client_call_details(self, original: grpc.ClientCallDetails, metadata):
        ClientCallDetails = collections.namedtuple(
            "ClientCallDetails",
            ("method", "timeout", "metadata", "credentials", "wait_for_ready"),
        )

        return ClientCallDetails(
            method=original.method,
            timeout=original.timeout,
            metadata=metadata,
            credentials=original.credentials,
            wait_for_ready=getattr(original, "wait_for_ready", False),
        )
