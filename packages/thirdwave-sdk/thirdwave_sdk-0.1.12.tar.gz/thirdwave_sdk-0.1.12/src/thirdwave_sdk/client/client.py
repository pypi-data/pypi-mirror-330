import grpc
from thirdwave_sdk.client.base import ThirdwaveClientBase, Options
from thirdwave_sdk.services.evm_wallet_service import WalletService
from thirdwave_sdk.transport import AuthenticationInterceptor


class ThirdwaveClient(ThirdwaveClientBase):
    def __init__(self, api_key: str, options: Options):
        super().__init__(api_key, options)
        self.channel = None
        self.wallet = None

    async def initialize(self):
        if self.transport_type == "secure":
            interceptor = AuthenticationInterceptor(self.api_key,self.http_user_agent)
            self.channel = grpc.aio.secure_channel(self.endpoint, credentials=grpc.ssl_channel_credentials(), interceptors=[interceptor])
        elif self.transport_type == "insecure":
            self.channel = grpc.aio.insecure_channel(self.endpoint)
        else:
            raise ValueError("Unsupported transport type. Use 'secure' or 'insecure'.")

        # Initialize services after the channel is set up
        self.wallet = WalletService(self.channel, self.api_key, self.http_user_agent, self.content_type)

    async def close(self):
        if self.channel:
            await self.channel.close()
