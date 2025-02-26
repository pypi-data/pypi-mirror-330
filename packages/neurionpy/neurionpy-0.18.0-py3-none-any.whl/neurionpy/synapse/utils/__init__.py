import json
import math
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple, Union, Callable

import grpc
from dateutil.parser import isoparse

from neurionpy.auth.interface import Auth
from neurionpy.bank.interface import Bank
from neurionpy.distribution.interface import Distribution
from neurionpy.params.interface import Params
from neurionpy.protos.cosmos.base.query.v1beta1.pagination_pb2 import PageRequest
from neurionpy.staking.interface import Staking
from neurionpy.synapse.client.bank import create_bank_send_msg
from neurionpy.synapse.client.distribution import create_withdraw_delegator_reward
from neurionpy.synapse.client.staking import (
    ValidatorStatus,
    create_delegate_msg,
    create_redelegate_msg,
    create_undelegate_msg,
)
from neurionpy.synapse.client.utils import (
    ensure_timedelta,
    get_paginated,
    prepare_and_broadcast_basic_transaction,
)
from neurionpy.synapse.config import NetworkConfig
from neurionpy.synapse.exceptions import NotFoundError, QueryTimeoutError
from neurionpy.synapse.gas import GasStrategy
from neurionpy.synapse.tx import Transaction, TxState, SigningCfg
from neurionpy.synapse.tx_helpers import MessageLog, SubmittedTx, TxResponse
from neurionpy.synapse.utils.constants import DEFAULT_QUERY_INTERVAL_SECS, DEFAULT_QUERY_TIMEOUT_SECS
from neurionpy.synapse.utils.types import Account, Coin, Validator, StakingPosition, COSMOS_SDK_DEC_COIN_PRECISION, \
    StakingSummary, UnbondingPositions, Block
from neurionpy.synapse.wallet import Wallet
from neurionpy.crypto.address import Address
from neurionpy.protos.cosmos.auth.v1beta1.auth_pb2 import BaseAccount
from neurionpy.protos.cosmos.auth.v1beta1.query_pb2 import QueryAccountRequest
from neurionpy.protos.cosmos.bank.v1beta1.query_pb2 import (
    QueryAllBalancesRequest,
    QueryBalanceRequest,
)
from neurionpy.protos.cosmos.base.tendermint.v1beta1.query_pb2 import (
    GetBlockByHeightRequest,
    GetLatestBlockRequest,
)
from neurionpy.protos.cosmos.crypto.ed25519.keys_pb2 import (  # noqa # pylint: disable=unused-import
    PubKey,
)
from neurionpy.protos.cosmos.distribution.v1beta1.query_pb2 import (
    QueryDelegationRewardsRequest,
)
from neurionpy.protos.cosmos.params.v1beta1.query_pb2 import QueryParamsRequest
from neurionpy.protos.cosmos.staking.v1beta1.query_pb2 import (
    QueryDelegatorDelegationsRequest,
    QueryDelegatorUnbondingDelegationsRequest,
    QueryValidatorsRequest,
)


from neurionpy.protos.cosmos.tx.v1beta1.service_pb2 import (
    BroadcastMode,
    BroadcastTxRequest,
    GetTxRequest,
    SimulateRequest,
)
from neurionpy.tendermint.interface import CosmosBaseTendermint
from neurionpy.tx.interface import TxInterface


class NeurionUtils:
    """Neurion Utils."""

    def __init__(
            self,
            cfg: NetworkConfig,
            auth: Auth,
            param: Params,
            bank: Bank,
            staking: Staking,
            distribution: Distribution,
            txs: TxInterface,
            tendermint: CosmosBaseTendermint,
            gas_strategy: Optional[GasStrategy] = None,
            query_interval_secs: int = DEFAULT_QUERY_INTERVAL_SECS,
            query_timeout_secs: int = DEFAULT_QUERY_TIMEOUT_SECS,
    ):
        """Init ledger client.

        :param cfg: Network configurations
        :param query_interval_secs: int. optional interval int seconds
        :param query_timeout_secs: int. optional interval int seconds
        :param wallet: Wallet, defaults to None
        """
        self._query_interval_secs = query_interval_secs
        self._query_timeout_secs = query_timeout_secs
        self._network_config = cfg
        self._gas_strategy: GasStrategy = gas_strategy
        self._auth = auth
        self._params = param
        self._bank = bank
        self._staking = staking
        self._distribution = distribution
        self._txs = txs
        self._tendermint = tendermint



    @property
    def network_config(self) -> NetworkConfig:
        """Get the network config.

        :return: network config
        """
        return self._network_config

    @property
    def gas_strategy(self) -> GasStrategy:
        """Get gas strategy.

        :return: gas strategy
        """
        return self._gas_strategy

    @gas_strategy.setter
    def gas_strategy(self, strategy: GasStrategy):
        """Set gas strategy.

        :param strategy: strategy
        :raises RuntimeError: Invalid strategy must implement GasStrategy interface
        """
        if not isinstance(strategy, GasStrategy):
            raise RuntimeError("Invalid strategy must implement GasStrategy interface")
        self._gas_strategy = strategy

    def query_account(self, address: Address) -> Account:
        """Query account.

        :param address: address
        :raises RuntimeError: Unexpected account type returned from query
        :return: account details
        """
        request = QueryAccountRequest(address=str(address))
        response = self._auth.Account(request)

        account = BaseAccount()
        if not response.account.Is(BaseAccount.DESCRIPTOR):
            raise RuntimeError("Unexpected account type returned from query")
        response.account.Unpack(account)

        return Account(
            address=address,
            number=account.account_number,
            sequence=account.sequence,
        )

    def query_params(self, subspace: str, key: str) -> Any:
        """Query Prams.

        :param subspace: subspace
        :param key: key
        :return: Query params
        """
        req = QueryParamsRequest(subspace=subspace, key=key)
        resp = self._params.Params(req)
        return json.loads(resp.param.value)

    def query_bank_balance(self, address: Address, denom: Optional[str] = None) -> int:
        """Query bank balance.

        :param address: address
        :param denom: denom, defaults to None
        :return: bank balance
        """
        denom = denom or self.network_config.fee_denomination

        req = QueryBalanceRequest(
            address=str(address),
            denom=denom,
        )

        resp = self._bank.Balance(req)
        assert resp.balance.denom == denom  # sanity check

        return resp.balance.amount

    def query_bank_all_balances(self, address: Address) -> List[Coin]:
        """Query bank all balances.

        :param address: address
        :return: bank all balances
        """
        req = QueryAllBalancesRequest(address=str(address))
        resp = self._bank.AllBalances(req)

        return [Coin(amount=coin.amount, denom=coin.denom) for coin in resp.balances]

    def prepare_and_broadcast_basic_transaction(
            self,
            tx: "Transaction",  # type: ignore # noqa: F821
            sender: "Wallet",  # type: ignore # noqa: F821
            account: Optional["Account"] = None,  # type: ignore # noqa: F821
            gas_limit: Optional[int] = None,
            memo: Optional[str] = None,
    ) -> SubmittedTx:
        """Prepare and broadcast basic transaction.

        :param client: Ledger client
        :param tx: The transaction
        :param sender: The transaction sender
        :param account: The account
        :param gas_limit: The gas limit
        :param memo: Transaction memo, defaults to None

        :return: broadcast transaction
        """
        # the sender must be a valid wallet
        if not isinstance(sender, Wallet):
            raise RuntimeError("Invalid sender, must be a Wallet instance")
        # query the account information for the sender
        if account is None:
            account = self.query_account(sender.address())

        if gas_limit is not None:
            # simply build the fee from the provided gas limit
            fee = self.estimate_fee_from_gas(gas_limit)
        else:
            # we need to build up a representative transaction so that we can accurately simulate it
            tx.seal(
                SigningCfg.direct(sender.public_key(), account.sequence),
                fee="",
                gas_limit=0,
                memo=memo,
            )
            tx.sign(sender.signer(), self.network_config.chain_id, account.number)
            tx.complete()

            # simulate the gas and fee for the transaction
            gas_limit, fee = self.estimate_gas_and_fee_for_tx(tx)

        # finally, build the final transaction that will be executed with the correct gas and fee values
        tx.seal(
            SigningCfg.direct(sender.public_key(), account.sequence),
            fee=fee,
            gas_limit=gas_limit,
            memo=memo,
        )
        tx.sign(sender.signer(), self.network_config.chain_id, account.number)
        tx.complete()

        return self.broadcast_tx(tx)

    def ensure_timedelta(interval: Union[int, float, timedelta]) -> timedelta:
        """
        Return timedelta for interval.

        :param interval: timedelta or seconds in int or float

        :return: timedelta
        """
        return interval if isinstance(interval, timedelta) else timedelta(seconds=interval)

    DEFAULT_PER_PAGE_LIMIT = None

    def get_paginated(
            initial_request: Any,
            request_method: Callable,
            pages_limit: int = 0,
            per_page_limit: Optional[int] = DEFAULT_PER_PAGE_LIMIT,
    ) -> List[Any]:
        """
        Get pages for specific request.

        :param initial_request: request supports pagination
        :param request_method: function to perform request
        :param pages_limit: max number of pages to return. default - 0 unlimited
        :param per_page_limit: Optional int: amount of records per one page. default is None, determined by server

        :return: List of responses
        """
        pages: List[Any] = []
        pagination = PageRequest(limit=per_page_limit)

        while pagination and (len(pages) < pages_limit or pages_limit == 0):
            request = initial_request.__class__()
            request.CopyFrom(initial_request)
            request.pagination.CopyFrom(pagination)

            resp = request_method(request)

            pages.append(resp)

            pagination = None

            if resp.pagination.next_key:
                pagination = PageRequest(limit=per_page_limit, key=resp.pagination.next_key)
        return pages

    def send_tokens(
            self,
            destination: Address,
            amount: int,
            denom: str,
            sender: Wallet,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Send tokens.

        :param destination: destination address
        :param amount: amount
        :param denom: denom
        :param sender: sender
        :param memo: memo, defaults to None
        :param gas_limit: gas limit, defaults to None
        :return: prepare and broadcast the transaction and transaction details
        """
        # build up the store transaction
        tx = Transaction()
        tx.add_message(
            create_bank_send_msg(sender.address(), destination, amount, denom)
        )

        return prepare_and_broadcast_basic_transaction(
            self, tx, sender, gas_limit=gas_limit, memo=memo
        )

    def query_validators(
            self, status: Optional[ValidatorStatus] = None
    ) -> List[Validator]:
        """Query validators.

        :param status: validator status, defaults to None
        :return: List of validators
        """
        filtered_status = status or ValidatorStatus.BONDED

        req = QueryValidatorsRequest()
        if filtered_status != ValidatorStatus.UNSPECIFIED:
            req.status = filtered_status.value

        resp = self._staking.Validators(req)

        validators: List[Validator] = []
        for validator in resp.validators:
            validators.append(
                Validator(
                    address=Address(validator.operator_address),
                    tokens=int(float(validator.tokens)),
                    moniker=str(validator.description.moniker),
                    status=ValidatorStatus.from_proto(validator.status),
                )
            )
        return validators

    def query_staking_summary(self, address: Address) -> StakingSummary:
        """Query staking summary.

        :param address: address
        :return: staking summary
        """
        current_positions: List[StakingPosition] = []

        req = QueryDelegatorDelegationsRequest(delegator_addr=str(address))

        for resp in get_paginated(
                req, self._staking.DelegatorDelegations, per_page_limit=1
        ):
            for item in resp.delegation_responses:
                req = QueryDelegationRewardsRequest(
                    delegator_address=str(address),
                    validator_address=str(item.delegation.validator_address),
                )
                rewards_resp = self._distribution.DelegationRewards(req)

                stake_reward = 0
                for reward in rewards_resp.rewards:
                    if reward.denom == self.network_config.staking_denomination:
                        stake_reward = (
                                int(float(reward.amount)) // COSMOS_SDK_DEC_COIN_PRECISION
                        )
                        break

                current_positions.append(
                    StakingPosition(
                        validator=Address(item.delegation.validator_address),
                        amount=int(float(item.balance.amount)),
                        reward=stake_reward,
                    )
                )

        unbonding_summary: Dict[str, int] = {}
        req = QueryDelegatorUnbondingDelegationsRequest(delegator_addr=str(address))

        for resp in get_paginated(req, self._staking.DelegatorUnbondingDelegations):
            for item in resp.unbonding_responses:
                validator = str(item.validator_address)
                total_unbonding = unbonding_summary.get(validator, 0)

                for entry in item.entries:
                    total_unbonding += int(float(entry.balance))

                unbonding_summary[validator] = total_unbonding

        # build the final list of unbonding positions
        unbonding_positions: List[UnbondingPositions] = []
        for validator, total_unbonding in unbonding_summary.items():
            unbonding_positions.append(
                UnbondingPositions(
                    validator=Address(validator),
                    amount=total_unbonding,
                )
            )

        return StakingSummary(
            current_positions=current_positions, unbonding_positions=unbonding_positions
        )

    def delegate_tokens(
            self,
            validator: Address,
            amount: int,
            sender: Wallet,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Delegate tokens.

        :param validator: validator address
        :param amount: amount
        :param sender: sender
        :param memo: memo, defaults to None
        :param gas_limit: gas limit, defaults to None
        :return: prepare and broadcast the transaction and transaction details
        """
        tx = Transaction()
        tx.add_message(
            create_delegate_msg(
                sender.address(),
                validator,
                amount,
                self.network_config.staking_denomination,
            )
        )

        return prepare_and_broadcast_basic_transaction(
            self, tx, sender, gas_limit=gas_limit, memo=memo
        )

    def redelegate_tokens(
            self,
            current_validator: Address,
            next_validator: Address,
            amount: int,
            sender: Wallet,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Redelegate tokens.

        :param current_validator: current validator address
        :param next_validator: next validator address
        :param amount: amount
        :param sender: sender
        :param memo: memo, defaults to None
        :param gas_limit: gas limit, defaults to None
        :return: prepare and broadcast the transaction and transaction details
        """
        tx = Transaction()
        tx.add_message(
            create_redelegate_msg(
                sender.address(),
                current_validator,
                next_validator,
                amount,
                self.network_config.staking_denomination,
            )
        )

        return prepare_and_broadcast_basic_transaction(
            self, tx, sender, gas_limit=gas_limit, memo=memo
        )

    def undelegate_tokens(
            self,
            validator: Address,
            amount: int,
            sender: Wallet,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """Undelegate tokens.

        :param validator: validator
        :param amount: amount
        :param sender: sender
        :param memo: memo, defaults to None
        :param gas_limit: gas limit, defaults to None
        :return: prepare and broadcast the transaction and transaction details
        """
        tx = Transaction()
        tx.add_message(
            create_undelegate_msg(
                sender.address(),
                validator,
                amount,
                self.network_config.staking_denomination,
            )
        )

        return prepare_and_broadcast_basic_transaction(
            self, tx, sender, gas_limit=gas_limit, memo=memo
        )

    def claim_rewards(
            self,
            validator: Address,
            sender: Wallet,
            memo: Optional[str] = None,
            gas_limit: Optional[int] = None,
    ) -> SubmittedTx:
        """claim rewards.

        :param validator: validator
        :param sender: sender
        :param memo: memo, defaults to None
        :param gas_limit: gas limit, defaults to None
        :return: prepare and broadcast the transaction and transaction details
        """
        tx = Transaction()
        tx.add_message(create_withdraw_delegator_reward(sender.address(), validator))

        return prepare_and_broadcast_basic_transaction(
            self, tx, sender, gas_limit=gas_limit, memo=memo
        )

    def estimate_gas_for_tx(self, tx: Transaction) -> int:
        """Estimate gas for transaction.

        :param tx: transaction
        :return: Estimated gas for transaction
        """
        return self._gas_strategy.estimate_gas(tx)

    def estimate_fee_from_gas(self, gas_limit: int) -> str:
        """Estimate fee from gas.

        :param gas_limit: gas limit
        :return: Estimated fee for transaction
        """
        fee = math.ceil(gas_limit * self.network_config.fee_minimum_gas_price)
        return f"{fee}{self.network_config.fee_denomination}"

    def estimate_gas_and_fee_for_tx(self, tx: Transaction) -> Tuple[int, str]:
        """Estimate gas and fee for transaction.

        :param tx: transaction
        :return: estimate gas, fee for transaction
        """
        gas_estimate = self.estimate_gas_for_tx(tx)
        fee = self.estimate_fee_from_gas(gas_estimate)
        return gas_estimate, fee

    def wait_for_query_tx(
            self,
            tx_hash: str,
            timeout: Optional[timedelta] = None,
            poll_period: Optional[timedelta] = None,
    ) -> TxResponse:
        """Wait for query transaction.

        :param tx_hash: transaction hash
        :param timeout: timeout, defaults to None
        :param poll_period: poll_period, defaults to None

        :raises QueryTimeoutError: timeout

        :return: transaction response
        """
        timeout = (
            ensure_timedelta(timeout)
            if timeout
            else timedelta(seconds=self._query_timeout_secs)
        )
        poll_period = (
            ensure_timedelta(poll_period)
            if poll_period
            else timedelta(seconds=self._query_interval_secs)
        )

        start = datetime.now()
        while True:
            try:
                return self.query_tx(tx_hash)
            except NotFoundError:
                pass

            delta = datetime.now() - start
            if delta >= timeout:
                raise QueryTimeoutError()

            time.sleep(poll_period.total_seconds())

    def query_tx(self, tx_hash: str) -> TxResponse:
        """query transaction.

        :param tx_hash: transaction hash
        :raises NotFoundError: Tx details not found
        :raises grpc.RpcError: RPC connection issue
        :return: query response
        """
        req = GetTxRequest(hash=tx_hash)
        try:
            resp = self._txs.GetTx(req)
        except grpc.RpcError as e:
            details = e.details()
            if "not found" in details:
                raise NotFoundError() from e
            raise
        except RuntimeError as e:
            details = str(e)
            if "tx" in details and "not found" in details:
                raise NotFoundError() from e
            raise

        return self._parse_tx_response(resp.tx_response)

    @staticmethod
    def _parse_tx_response(tx_response: Any) -> TxResponse:
        # parse the transaction logs
        logs = []
        for log_data in tx_response.logs:
            events = {}
            for event in log_data.events:
                events[event.type] = {a.key: a.value for a in event.attributes}
            logs.append(
                MessageLog(
                    index=int(log_data.msg_index), log=log_data.msg_index, events=events
                )
            )

        # parse the transaction events
        events = {}
        for event in tx_response.events:
            event_data = events.get(event.type, {})
            for attribute in event.attributes:
                event_data[attribute.key.decode()] = attribute.value.decode()
            events[event.type] = event_data

        timestamp = None
        if tx_response.timestamp:
            timestamp = isoparse(tx_response.timestamp)

        return TxResponse(
            hash=str(tx_response.txhash),
            height=int(tx_response.height),
            code=int(tx_response.code),
            gas_wanted=int(tx_response.gas_wanted),
            gas_used=int(tx_response.gas_used),
            raw_log=str(tx_response.raw_log),
            logs=logs,
            events=events,
            timestamp=timestamp,
        )

    def simulate_tx(self, tx: Transaction) -> int:
        """simulate transaction.

        :param tx: transaction
        :raises RuntimeError: Unable to simulate non final transaction
        :return: gas used in transaction
        """
        if tx.state != TxState.Final:
            raise RuntimeError("Unable to simulate non final transaction")

        req = SimulateRequest(tx=tx.tx)
        resp = self._txs.Simulate(req)

        return int(resp.gas_info.gas_used)

    def broadcast_tx(self, tx: Transaction) -> SubmittedTx:
        """Broadcast transaction.

        :param tx: transaction
        :return: Submitted transaction
        """
        # create the broadcast request
        broadcast_req = BroadcastTxRequest(
            tx_bytes=tx.tx.SerializeToString(), mode=BroadcastMode.BROADCAST_MODE_SYNC
        )

        # broadcast the transaction
        resp = self._txs.BroadcastTx(broadcast_req)
        tx_digest = resp.tx_response.txhash

        # check that the response is successful
        initial_tx_response = self._parse_tx_response(resp.tx_response)
        initial_tx_response.ensure_successful()

        return SubmittedTx(self, tx_digest)

    def query_latest_block(self) -> Block:
        """Query the latest block.

        :return: latest block
        """
        req = GetLatestBlockRequest()
        resp = self._tendermint.GetLatestBlock(req)
        return Block.from_proto(resp.block)

    def query_block(self, height: int) -> Block:
        """Query the block.

        :param height: block height
        :return: block
        """
        req = GetBlockByHeightRequest(height=height)
        resp = self._tendermint.GetBlockByHeight(req)
        return Block.from_proto(resp.block)

    def query_height(self) -> int:
        """Query the latest block height.

        :return: latest block height
        """
        return self.query_latest_block().height

    def query_chain_id(self) -> str:
        """Query the chain id.

        :return: chain id
        """
        return self.query_latest_block().chain_id