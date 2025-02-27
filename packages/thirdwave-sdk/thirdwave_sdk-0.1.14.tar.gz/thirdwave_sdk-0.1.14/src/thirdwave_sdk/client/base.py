from typing import TypedDict, Literal
import grpc

from thirdwave_sdk.utils.get_http_user_agent import get_http_user_agent


class Options(TypedDict, total=False):
    transport_type: Literal["secure", "insecure"]

class ApiKeyAuthMetadataPlugin(grpc.AuthMetadataPlugin):
    def __init__(self, api_key, user_agent, content_type):
        self.api_key = api_key
        self.user_agent = user_agent
        self.content_type = content_type
        
    def __call__(self, context, callback):
        metadata = (
            ("x-api-key", self.api_key),
            ("user-agent", self.user_agent),
            ("content-type", self.content_type),
        )

        callback(metadata, None)


class CustomHeaderMetadataPlugin(grpc.AuthMetadataPlugin):
    def __init__(self, headers):
        self.headers = headers

    def __call__(self, context, callback):
        metadata = [(key, value) for key, values in self.headers.items() for value in values]
        callback(metadata, None)



class ThirdwaveClientBase:
    def __init__(self, api_key: str, options: Options):
        self.endpoint = "api.thirdwavelabs.com"
        self.api_key = api_key
        self.transport_type = options.get("transport_type", "secure")
        self.channel: grpc.Channel
        self.http_user_agent = get_http_user_agent()
        self.content_type = "application/grpc"
        self.wallet = None