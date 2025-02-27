from datetime import datetime
from typing import List, Optional

from thirdwave_sdk.utils.eth_utils import evm_from_bytes
from enum import Enum
from dataclasses import dataclass


class Currency(Enum):
    CURRENCY_UNSPECIFIED = 0
    CURRENCY_USD = 1

    def __str__(self):
        return self.name


class BlockchainName(Enum):
    UNSPECIFIED = 0
    ETHEREUM = 1
    BINANCE = 2
    POLYGON = 3
    ARBITRUM = 4
    BASE = 5


def blockchain_id_to_symbol(blockchain_id: int) -> str:
    blockchain_enum = BlockchainName(blockchain_id)
    mapping = {
        BlockchainName.ARBITRUM: "ARB",
        BlockchainName.BASE: "BASE",
        BlockchainName.BINANCE: "BNB",
        BlockchainName.ETHEREUM: "ETH",
        BlockchainName.POLYGON: "POL",
    }
    return mapping.get(blockchain_enum, "UNSPECIFIED")

class TransactionPatternName(Enum):
    UNSPECIFIED = 0
    CONTINUOUS = 1
    HIGH_VELOCITY = 2
    SUSPICIOUS_WALLET_NETWORK = 3
    TIMED = 4
    
    def __str__(self):
        return self.name


@dataclass
class EvmTransaction:
    _hash: bytes
    _blockchain: BlockchainName
    timestamp: datetime

    @property
    def hash(self) -> str:
        return str(self._hash.hex())

    @property
    def blockchain(self) -> BlockchainName:
        return self._blockchain

    def __repr__(self):
        return f"EvmTransaction(hash={self.hash}, blockchain={self.blockchain}, timestamp={self.timestamp})"

    def __str__(self):
        return self.__repr__()


@dataclass
class BotBehaviors:
    continuous_engagement: bool
    funding_network: bool
    temporal_activity: bool
    transaction_velocity: bool

    def __repr__(self):
        return (
            f"BotBehaviors(continuous_engagement={self.continuous_engagement}, "
            f"funding_network={self.funding_network}, temporal_activity={self.temporal_activity}, "
            f"transaction_velocity={self.transaction_velocity})"
        )

    def __str__(self):
        return self.__repr__()


@dataclass
class Erc20TokenHolding:
    _blockchain: BlockchainName
    _balance: float
    _address: bytes

    @property
    def address(self):
        return evm_from_bytes(self._address)

    @property
    def balance(self):
        return self._balance

    @property
    def blockchain(self) -> str:
        return blockchain_id_to_symbol(self._blockchain)

    def __repr__(self):
        return (
            f"Erc20TokenHolding(blockchain={self.blockchain}, balance={self.balance}, "
            f"address={self.address})"
        )

    def __str__(self):
        return self.__repr__()


@dataclass
class NativeTokenHolding:
    _blockchain: BlockchainName
    _balance: float

    @property
    def blockchain(self) -> str:
        return blockchain_id_to_symbol(self._blockchain)

    @property
    def balance(self):
        return self._balance

    def __repr__(self):
        return (
            f"NativeTokenHolding(blockchain={self.blockchain}, balance={self.balance})"
        )

    def __str__(self):
        return self.__repr__()


@dataclass
class Spend:
    total: float
    games: float

    def __repr__(self):
        return f"Spend(total={self.total}, games={self.games})"

    def __str__(self):
        return self.__repr__()

@dataclass
class TransactionPattern:
    key: TransactionPatternName
    value: bool
    
    def __str__(self):
        return self.__repr__()


@dataclass
class WalletAssociationFamily:
    family_id: str
    addresses: list[str]

    def __repr__(self):
        return f"WalletAssociationFamily(family_id={self.family_id}, addresses={self.addresses})"

    def __str__(self):
        return self.__repr__()

    
class EvmWallet:
    def __init__(
        self,
        address: bytes,
        active_chains: list[BlockchainName],
        associated_wallets_family: WalletAssociationFamily,
        balance: float,
        bot_warning: bool,
        bot_behaviors: BotBehaviors,
        erc20_token_holdings: List[Erc20TokenHolding],
        engagement_score: int,
        first_expense_transaction: Optional[EvmTransaction],
        first_funding_transaction: Optional[EvmTransaction],
        first_seen_at: datetime,
        hodler_score: int,
        native_token_holdings: List[NativeTokenHolding],
        outbound_transaction_value: float,
        outbound_transaction_count: float,
        spend: Spend,
        transaction_patterns: List[TransactionPattern],
        updated_at: datetime,
        waverank: int,
    ):
        self._address = address
        self._active_chains = active_chains
        self._associated_wallets_family = associated_wallets_family
        self._balance = balance
        self._bot_behaviors = bot_behaviors
        self._bot_warning = bot_warning
        self._engagement_score = engagement_score
        self._erc20_token_holdings = erc20_token_holdings
        self._first_expense_transaction = first_expense_transaction
        self._first_funding_transaction = first_funding_transaction
        self._first_seen_at = first_seen_at
        self._hodler_score = hodler_score
        self._native_token_holdings = native_token_holdings
        self._outbound_transaction_count = outbound_transaction_count
        self._outbound_transaction_value = outbound_transaction_value
        self._spend = spend
        self._transaction_patterns = transaction_patterns
        self._updated_at = updated_at
        self._waverank = waverank
    @property
    def active_chains(self) -> list[BlockchainName]:
        return self._active_chains

    @property
    def address(self):
        return evm_from_bytes(self._address)

    @property
    def associated_wallets_family(self):
        return self._associated_wallets_family

    @property
    def balance(self):
        return self._balance

    @property
    def bot_behaviors(self):
        return self._bot_behaviors

    @property
    def bot_warning(self):
        return self._bot_warning

    @property
    def engagement_score(self):
        return self._engagement_score

    @property
    def erc20_token_holdings(self):
        return self._erc20_token_holdings

    @erc20_token_holdings.setter
    def erc20_token_holdings(self, erc20_token_holdings: List[Erc20TokenHolding]):
        self._erc20_token_holdings = erc20_token_holdings

    @property
    def first_expense_transaction(self):
        return self._first_expense_transaction

    @property
    def first_funding_transaction(self):
        return self._first_funding_transaction

    @property
    def first_seen_at(self):
        return self._first_seen_at

    @property
    def hodler_score(self):
        return self._hodler_score

    @property
    def native_token_holdings(self):
        return self._native_token_holdings

    @property
    def outbound_transaction_count(self):
        return self._outbound_transaction_count

    @property
    def outbound_transaction_value(self):
        return self._outbound_transaction_value

    @property
    def spend(self):
        return self._spend

    @property
    def transaction_patterns(self):
        return self._transaction_patterns

    @property
    def updated_at(self):
        return self._updated_at

    @property
    def waverank(self):
        return self._waverank

    def __repr__(self):
        return (
            f"EvmWallet(address={self.address}, bot_behaviors={self.bot_behaviors}, "
            f"active_chains={self.active_chains}, "
            f"erc20_token_holdings={self.erc20_token_holdings}, first_expense_transaction={self.first_expense_transaction}, "
            f"first_funding_transaction={self.first_funding_transaction}, hodler_score={self.hodler_score}, bot_warning={self.bot_warning}, "
            f"native_token_holdings={self.native_token_holdings}, spend={self.spend}, balance={self.balance}, "
            f"waverank={self.waverank})")

    def __str__(self):
        return self.__repr__()


class EvmWalletResponse:
    def __init__(self, wallet: EvmWallet):
        self.wallet = wallet

    @staticmethod
    def from_grpc(response) -> "EvmWalletResponse":
        wallet = EvmWallet(
            address=response.wallet.address,
            active_chains=list(set(
            [
                holding.blockchain
                for holding in response.wallet.erc20_token_holdings
                if holding.blockchain != BlockchainName.UNSPECIFIED
            ] +
            [
                holding.blockchain
                for holding in response.wallet.native_token_holdings
                if holding.blockchain != BlockchainName.UNSPECIFIED
            ]
            )),
            associated_wallets_family=WalletAssociationFamily(
            family_id=response.wallet.associated_wallets_family.family_id,
            addresses=[evm_from_bytes(addr) for addr in response.wallet.associated_wallets_family.addresses],
            ),
            balance=response.wallet.balance,
            bot_behaviors=BotBehaviors(
            response.wallet.bot_behaviors.continuous,
            response.wallet.bot_behaviors.suspicious_wallet_network,
            response.wallet.bot_behaviors.timed,
            response.wallet.bot_behaviors.high_velocity,
            ),
            bot_warning=response.wallet.bot_warning,
            engagement_score=response.wallet.engagement_score,
            erc20_token_holdings=[
            Erc20TokenHolding(
                holding.blockchain,
                holding.balance,
                holding.address,
            )
            for holding in response.wallet.erc20_token_holdings
            ],
            first_expense_transaction=(
            EvmTransaction(
                response.wallet.first_expense_transaction.hash,
                response.wallet.first_expense_transaction.blockchain,
                response.wallet.first_expense_transaction.timestamp.ToDatetime(),
            )
            if response.wallet.HasField("first_expense_transaction")
            else None
            ),
            first_funding_transaction=(
            EvmTransaction(
                response.wallet.first_funding_transaction.hash,
                response.wallet.first_funding_transaction.blockchain,
                response.wallet.first_funding_transaction.timestamp.ToDatetime(),
            )
            if response.wallet.HasField("first_funding_transaction")
            else None
            ),
            first_seen_at=response.wallet.first_seen_at.ToDatetime(),
            hodler_score=response.wallet.hodler_score,
            native_token_holdings=[
            NativeTokenHolding(
                holding.blockchain,
                holding.balance,
            )
            for holding in response.wallet.native_token_holdings
            ],
            outbound_transaction_count=response.wallet.outbound_transaction_count,
            outbound_transaction_value=response.wallet.outbound_transaction_value,
            spend=Spend(
            response.wallet.spend.total,
            response.wallet.spend.games,
            ),
            transaction_patterns=[
            TransactionPattern(pattern.key, pattern.value)
            for pattern in response.wallet.transaction_patterns
            if pattern.key != TransactionPatternName.UNSPECIFIED
            ],
            updated_at=response.wallet.updated_at.ToDatetime(),
            waverank=response.wallet.waverank,
        )
        return EvmWalletResponse(wallet)

    def __repr__(self):
        return f"EvmWalletResponse(wallet={self.wallet})"

    def __str__(self):
        return self.__repr__()
