from typing import List, Any

from eth_typing import HexStr, ChecksumAddress, Hash32
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import Contract
from web3.providers import HTTPProvider

from .exception import BalanceNotEnough, NoPositionsToRedeem
from .safe.constants import NULL_HASH
from .safe.multisend import MultiSendTx, MultiSendOperation
from .safe.safe import Safe
from .py_order_utils.signer import Signer
from .safe.utils import get_empty_tx_params


class ContractCaller:
    def __init__(self, rpc_url='', private_key: HexStr = '', multi_sig_addr: ChecksumAddress = '',
                 conditional_tokens_addr: ChecksumAddress = '', multisend_addr: ChecksumAddress = ''):
        self.private_key = private_key
        self.signer = Signer(self.private_key)

        self.multi_sig_addr = multi_sig_addr
        self.conditional_tokens_addr = conditional_tokens_addr
        self.multisend_addr = multisend_addr
        w3 = Web3(HTTPProvider(rpc_url))
        self.w3 = w3
        self.safe = Safe(w3, private_key, multi_sig_addr, multisend_addr)

    @property
    def conditional_tokens(self) -> Contract:
        from .contracts.conditional_tokens import abi
        return self.w3.eth.contract(self.conditional_tokens_addr, abi=abi)

    def get_erc20_contract(self, address: ChecksumAddress):
        from .contracts.erc20 import abi
        return self.w3.eth.contract(address, abi=abi)

    def split(self, collateral_token: ChecksumAddress, condition_id: Hash32,
              amount: int, partition: list = [1, 2], parent_collection_id: Hash32 = NULL_HASH) -> tuple[HexBytes, HexBytes, Any]:

        # Check balance of collateral
        balance = self.get_erc20_contract(collateral_token).functions \
            .balanceOf(self.multi_sig_addr).call()
        print('balance: {}'.format(balance))
        if balance < amount:
            raise BalanceNotEnough()

        multi_send_txs: List[MultiSendTx] = []

        data = HexBytes(
            self.conditional_tokens.functions.splitPosition(
                collateral_token, parent_collection_id, condition_id, partition, amount
            ).build_transaction(get_empty_tx_params())["data"]
        )

        multi_send_txs.append(MultiSendTx(
            operation=MultiSendOperation.CALL.value,
            to=self.conditional_tokens_addr,
            value=0,
            data=data,
        ))

        return self.safe.execute_multisend(multi_send_txs)

    def merge(self, collateral_token: ChecksumAddress, condition_id: Hash32,
              amount: int, partition: list = [1, 2], parent_collection_id: Hash32 = NULL_HASH) -> tuple[HexBytes, HexBytes, Any]:

        # Check balance of positions
        for index_set in partition:
            position_id = self.get_position_id(condition_id, index_set=index_set, collateral_token=collateral_token)
            balance = self.conditional_tokens.functions \
                .balanceOf(self.multi_sig_addr, position_id).call()
            # print('balance: {}'.format(balance))
            if balance < amount:
                raise BalanceNotEnough()

        multi_send_txs: List[MultiSendTx] = []

        data = HexBytes(
            self.conditional_tokens.functions.mergePositions(
                collateral_token, parent_collection_id, condition_id, partition, amount
            ).build_transaction(get_empty_tx_params())["data"]
        )

        multi_send_txs.append(MultiSendTx(
            operation=MultiSendOperation.CALL.value,
            to=self.conditional_tokens_addr,
            value=0,
            data=data,
        ))

        return self.safe.execute_multisend(multi_send_txs)

    def redeem(self, collateral_token: ChecksumAddress, condition_id: Hash32,
              partition: list = [1, 2], parent_collection_id: Hash32 = NULL_HASH) -> tuple[HexBytes, HexBytes, Any]:

        # Check balance of positions
        has_positions = False
        for index_set in partition:
            position_id = self.get_position_id(condition_id, index_set=index_set, collateral_token=collateral_token)
            balance = self.conditional_tokens.functions \
                .balanceOf(self.multi_sig_addr, position_id).call()
            # print('balance: {}'.format(balance))
            if balance > 0:
                has_positions = True
                break

        if not has_positions:
            raise NoPositionsToRedeem

        multi_send_txs: List[MultiSendTx] = []

        data = HexBytes(
            self.conditional_tokens.functions.redeemPositions(
                collateral_token, parent_collection_id, condition_id, partition
            ).build_transaction(get_empty_tx_params())["data"]
        )

        multi_send_txs.append(MultiSendTx(
            operation=MultiSendOperation.CALL.value,
            to=self.conditional_tokens_addr,
            value=0,
            data=data,
        ))

        return self.safe.execute_multisend(multi_send_txs)

    def enable_trading(self, supported_quote_tokens: dict) -> tuple[HexBytes, HexBytes, Any]:
        multi_send_txs: List[MultiSendTx] = []

        from .contracts.erc20 import abi
        for erc20_address, ctf_exchange_address in supported_quote_tokens.items():
            erc20_contract = self.w3.eth.contract(erc20_address, abi=abi)
            allowance = erc20_contract.functions.allowance(self.multi_sig_addr, ctf_exchange_address).call()
            # decimals = erc20_contract.functions.decimals().call()
            decimals = 18

            # Used for trading on ctf_exchange
            min_threshold = 1000000000 * 10**decimals
            allowance_to_update = 2*1000000000 * 10**decimals
            if allowance < min_threshold:
                data = HexBytes(
                    erc20_contract.functions.approve(
                        ctf_exchange_address, allowance_to_update
                    ).build_transaction(get_empty_tx_params())["data"]
                )

                multi_send_txs.append(MultiSendTx(
                    operation=MultiSendOperation.CALL.value,
                    to=erc20_address,
                    value=0,
                    data=data,
                ))

            # Used for splitting
            allowance = erc20_contract.functions.allowance(self.multi_sig_addr, self.conditional_tokens_addr).call()
            if allowance < min_threshold:
                data = HexBytes(
                    erc20_contract.functions.approve(
                        self.conditional_tokens_addr, allowance_to_update
                    ).build_transaction(get_empty_tx_params())["data"]
                )

                multi_send_txs.append(MultiSendTx(
                    operation=MultiSendOperation.CALL.value,
                    to=erc20_address,
                    value=0,
                    data=data,
                ))

            # Approve ctf_exchange for using conditional tokens
            is_approved_for_all = self.conditional_tokens.functions.isApprovedForAll(
                self.multi_sig_addr, ctf_exchange_address).call()
            if is_approved_for_all is False:
                data = HexBytes(
                    self.conditional_tokens.functions.setApprovalForAll(
                        ctf_exchange_address, True
                    ).build_transaction(get_empty_tx_params())["data"]
                )

                multi_send_txs.append(MultiSendTx(
                    operation=MultiSendOperation.CALL.value,
                    to=self.conditional_tokens_addr,
                    value=0,
                    data=data,
                ))

        if len(multi_send_txs) > 0:
            return self.safe.execute_multisend(multi_send_txs)
        else:
            return HexBytes(b'0x'), HexBytes(b'0x'), None

    def get_position_id(self, condition_id: Hash32, index_set: int, collateral_token: ChecksumAddress,
                        parent_condition_id=NULL_HASH):
        collection_id = self.conditional_tokens.functions.getCollectionId(
            parent_condition_id, condition_id, index_set).call()

        return self.conditional_tokens.functions.getPositionId(collateral_token, collection_id).call()
