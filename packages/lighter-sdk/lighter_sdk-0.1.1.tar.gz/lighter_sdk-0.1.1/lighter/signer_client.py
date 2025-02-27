import ctypes
import platform
import logging
import os
import time

from eth_account import Account
import lighter
from lighter.configuration import Configuration
from lighter.models import TxHash
from lighter.transactions import CreateOrder, CancelOrder, Withdraw

logging.basicConfig(level=logging.DEBUG)


class SignerClient:
    USDC_TICKER_SCALE = 1e6

    TX_TYPE_CREATE_SUB_ACCOUNT = 9
    TX_TYPE_CREATE_PUBLIC_POOL = 10
    TX_TYPE_UPDATE_PUBLIC_POOL = 11
    TX_TYPE_TRANSFER = 12
    TX_TYPE_WITHDRAW = 13
    TX_TYPE_CREATE_ORDER = 14
    TX_TYPE_CANCEL_ORDER = 15
    TX_TYPE_CANCEL_ALL_ORDERS = 16
    TX_TYPE_MODIFY_ORDER = 17
    TX_TYPE_MINT_SHARES = 18
    TX_TYPE_BURN_SHARES = 19

    ORDER_TYPE_LIMIT = 0
    ORDER_TYPE_MARKET = 1
    ORDER_TYPE_STOP_LOSS = 2
    ORDER_TYPE_STOP_LOSS_LIMIT = 3
    ORDER_TYPE_TAKE_PROFIT = 4
    ORDER_TYPE_TAKE_PROFIT_LIMIT = 5
    ORDER_TYPE_TWAP = 6

    ORDER_TIME_IN_FORCE_IMMEDIATE_OR_CANCEL = 0
    ORDER_TIME_IN_FORCE_GOOD_TILL_TIME = 1
    ORDER_TIME_IN_FORCE_POST_ONLY = 2

    NIL_TRIGGER_PRICE = 0
    DEFAULT_28_DAY_ORDER_EXPIRY = -1
    DEFAULT_10_MIN_AUTH_EXPIRY = -1
    MINUTE = 60

    def __init__(
        self, url, private_key, chain_id=300, api_key_index=0, account_index=-1
    ):
        if private_key.startswith("0x"):
            private_key = private_key[2:]
        self.url = url
        self.private_key = private_key
        self.chain_id = chain_id
        self.api_key_index = api_key_index
        self.account_index = account_index
        self.signer = self._initialize_signer()
        self.api_client = lighter.ApiClient(configuration=Configuration(host=url))
        self.tx_api = lighter.TransactionApi(self.api_client)
        self.create_client()
        self.l1_address = Account.from_key(private_key).address

    def _initialize_signer(self):
        is_linux = platform.system() == "Linux"
        is_mac = platform.system() == "Darwin"
        is_x64 = platform.machine().lower() in ("amd64", "x86_64")
        is_arm = platform.machine().lower() == "arm64"

        current_file_directory = os.path.dirname(os.path.abspath(__file__))
        path_to_signer_folders = os.path.join(current_file_directory, "signers")

        if is_arm and is_mac:
            logging.debug("Detected ARM architecture on macOS.")
            return ctypes.CDLL(
                os.path.join(path_to_signer_folders, "signer-arm64.dylib")
            )
        elif is_linux and is_x64:
            logging.debug("Detected x64/amd architecture on Linux.")
            return ctypes.CDLL(os.path.join(path_to_signer_folders, "signer-amd64.so"))
        else:
            raise Exception(
                f"Unsupported platform/architecture: {platform.system()}/{platform.machine()} only supports Linux(x86) and Darwin(arm64)"
            )

    async def set_account_index(self) -> int:
        if self.account_index != -1:
            return self.account_index

        accounts = await lighter.AccountApi(self.api_client).accounts_by_l1_address(
            l1_address=self.l1_address
        )
        if len(accounts.sub_accounts) > 0:
            self.account_index = min(acc.index for acc in accounts.sub_accounts)
            return self.account_index

        return -1

    def create_client(self):
        self.signer.CreateClient.argtypes = [
            ctypes.c_char_p,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_longlong,
        ]
        self.signer.CreateClient.restype = ctypes.c_void_p
        self.signer.CreateClient(
            self.url.encode("utf-8"),
            self.private_key.encode("utf-8"),
            self.chain_id,
            self.api_key_index,
            self.account_index,
        )

    def sign_create_order(
        self,
        market_index,
        client_order_index,
        base_amount,
        price,
        is_ask,
        order_type,
        time_in_force,
        reduce_only,
        trigger_price,
        order_expiry=DEFAULT_28_DAY_ORDER_EXPIRY,
        nonce=-1,
    ):
        self.signer.SignCreateOrder.argtypes = [
            ctypes.c_int,
            ctypes.c_longlong,
            ctypes.c_longlong,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_longlong,
            ctypes.c_longlong,
        ]
        self.signer.SignCreateOrder.restype = ctypes.c_char_p
        return self.signer.SignCreateOrder(
            market_index,
            client_order_index,
            base_amount,
            price,
            int(is_ask),
            order_type,
            time_in_force,
            reduce_only,
            trigger_price,
            order_expiry,
            nonce,
        ).decode("utf-8")

    def sign_cancel_order(self, market_index, order_index, nonce=-1):
        self.signer.SignCancelOrder.argtypes = [
            ctypes.c_int,
            ctypes.c_longlong,
            ctypes.c_longlong,
        ]
        self.signer.SignCancelOrder.restype = ctypes.c_char_p
        return self.signer.SignCancelOrder(market_index, order_index, nonce).decode(
            "utf-8"
        )

    def sign_withdraw(self, usdc_amount, nonce=-1):
        self.signer.SignWithdraw.argtypes = [ctypes.c_longlong, ctypes.c_longlong]
        self.signer.SignWithdraw.restype = ctypes.c_char_p
        return self.signer.SignWithdraw(usdc_amount, nonce).decode("utf-8")

    def sign_create_sub_account(self, nonce=-1):
        self.signer.SignCreateSubAccount.argtypes = [ctypes.c_longlong]
        self.signer.SignCreateSubAccount.restype = ctypes.c_char_p
        return self.signer.SignCreateSubAccount(nonce).decode("utf-8")

    def sign_cancel_all_orders(self, time_in_force, time, nonce=-1):
        self.signer.SignCancelAllOrders.argtypes = [
            ctypes.c_int,
            ctypes.c_longlong,
            ctypes.c_longlong,
        ]
        self.signer.SignCancelAllOrders.restype = ctypes.c_char_p
        return self.signer.SignCancelAllOrders(time_in_force, time, nonce).decode(
            "utf-8"
        )

    def sign_modify_order(
        self, market_index, order_index, base_amount, price, trigger_price, nonce=-1
    ):
        self.signer.SignModifyOrder.argtypes = [
            ctypes.c_int,
            ctypes.c_longlong,
            ctypes.c_longlong,
            ctypes.c_longlong,
            ctypes.c_longlong,
            ctypes.c_longlong,
        ]
        self.signer.SignModifyOrder.restype = ctypes.c_char_p
        return self.signer.SignModifyOrder(
            market_index, order_index, base_amount, price, trigger_price, nonce
        ).decode("utf-8")

    def sign_transfer(self, to_account_index, usdc_amount, nonce=-1):
        self.signer.SignTransfer.argtypes = [
            ctypes.c_longlong,
            ctypes.c_longlong,
            ctypes.c_longlong,
        ]
        self.signer.SignTransfer.restype = ctypes.c_char_p
        return self.signer.SignTransfer(to_account_index, usdc_amount, nonce).decode(
            "utf-8"
        )

    def sign_create_public_pool(
        self, operator_fee, initial_total_shares, min_operator_share_rate, nonce=-1
    ):
        self.signer.SignCreatePublicPool.argtypes = [
            ctypes.c_longlong,
            ctypes.c_longlong,
            ctypes.c_longlong,
            ctypes.c_longlong,
        ]
        self.signer.SignCreatePublicPool.restype = ctypes.c_char_p
        return self.signer.SignCreatePublicPool(
            operator_fee, initial_total_shares, min_operator_share_rate, nonce
        ).decode("utf-8")

    def sign_update_public_pool(
        self, public_pool_index, status, operator_fee, min_operator_share_rate, nonce=-1
    ):
        self.signer.SignUpdatePublicPool.argtypes = [
            ctypes.c_longlong,
            ctypes.c_int,
            ctypes.c_longlong,
            ctypes.c_longlong,
            ctypes.c_longlong,
        ]
        self.signer.SignUpdatePublicPool.restype = ctypes.c_char_p
        return self.signer.SignUpdatePublicPool(
            public_pool_index, status, operator_fee, min_operator_share_rate, nonce
        ).decode("utf-8")

    def sign_mint_shares(self, public_pool_index, share_amount, nonce=-1):
        self.signer.SignMintShares.argtypes = [
            ctypes.c_longlong,
            ctypes.c_longlong,
            ctypes.c_longlong,
        ]
        self.signer.SignMintShares.restype = ctypes.c_char_p
        return self.signer.SignMintShares(
            public_pool_index, share_amount, nonce
        ).decode("utf-8")

    def sign_burn_shares(self, public_pool_index, share_amount, nonce=-1):
        self.signer.SignBurnShares.argtypes = [
            ctypes.c_longlong,
            ctypes.c_longlong,
            ctypes.c_longlong,
        ]
        self.signer.SignBurnShares.restype = ctypes.c_char_p
        return self.signer.SignBurnShares(
            public_pool_index, share_amount, nonce
        ).decode("utf-8")

    def sign_update_leverage(self, market_index, leverage, nonce=-1):
        self.signer.SignUpdateLeverage.argtypes = [
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_longlong,
        ]
        self.signer.SignUpdateLeverage.restype = ctypes.c_char_p
        return self.signer.SignUpdateLeverage(market_index, leverage, nonce).decode(
            "utf-8"
        )

    def create_auth_token_with_expiry(self, deadline: int=DEFAULT_10_MIN_AUTH_EXPIRY):
        if deadline == SignerClient.DEFAULT_10_MIN_AUTH_EXPIRY:
            deadline = int(time.time() + 10 * SignerClient.MINUTE)
        self.signer.CreateAuthToken.argtypes = [ctypes.c_longlong]
        self.signer.CreateAuthToken.restype = ctypes.c_char_p
        return self.signer.CreateAuthToken(deadline).decode("utf-8")

    async def create_order(
        self,
        market_index,
        client_order_index,
        base_amount,
        price,
        is_ask,
        order_type,
        time_in_force,
        reduce_only=False,
        trigger_price=NIL_TRIGGER_PRICE,
        order_expiry=-1,
        nonce=-1,
    ) -> (CreateOrder, TxHash):
        tx_info = self.sign_create_order(
            market_index,
            client_order_index,
            base_amount,
            price,
            int(is_ask),
            order_type,
            time_in_force,
            int(reduce_only),
            trigger_price,
            order_expiry,
            nonce,
        )
        logging.debug(f"Create Order Tx Info: {tx_info}")

        api_response = await self.tx_api.send_tx(
            tx_type=self.TX_TYPE_CREATE_ORDER, tx_info=tx_info
        )
        logging.debug(f"Create Order Send Tx Response: {api_response}")
        return CreateOrder.from_json(tx_info), api_response

    async def cancel_order(
        self, market_index, order_index, nonce=-1
    ) -> (CancelOrder, TxHash):
        tx_info = self.sign_cancel_order(market_index, order_index, nonce)
        logging.debug(f"Cancel Order Tx Info: {tx_info}")

        api_response = await self.tx_api.send_tx(
            tx_type=self.TX_TYPE_CANCEL_ORDER, tx_info=tx_info
        )
        logging.debug(f"Cancel Order Send Tx Response: {api_response}")
        return CancelOrder.from_json(tx_info), api_response

    async def withdraw(self, usdc_amount, nonce=-1) -> (Withdraw, TxHash):
        usdc_amount = int(usdc_amount * self.USDC_TICKER_SCALE)

        tx_info = self.sign_withdraw(usdc_amount, nonce)
        logging.debug(f"Withdraw Tx Info: {tx_info}")

        api_response = await self.tx_api.send_tx(
            tx_type=self.TX_TYPE_WITHDRAW, tx_info=tx_info
        )
        logging.debug(f"Withdraw Send Tx Response: {api_response}")
        return Withdraw.from_json(tx_info), api_response

    async def create_sub_account(self, nonce=-1):
        tx_info = self.sign_create_sub_account(nonce)
        logging.debug(f"Create Sub Account Tx Info: {tx_info}")

        api_response = await self.tx_api.send_tx(
            tx_type=self.TX_TYPE_CREATE_SUB_ACCOUNT, tx_info=tx_info
        )
        logging.debug(f"Create Sub Account Send Tx Response: {api_response}")
        return api_response

    async def cancel_all_orders(self, time_in_force, time, nonce=-1):
        tx_info = self.sign_cancel_all_orders(time_in_force, time, nonce)
        logging.debug(f"Cancel All Orders Tx Info: {tx_info}")

        api_response = await self.tx_api.send_tx(
            tx_type=self.TX_TYPE_CANCEL_ALL_ORDERS, tx_info=tx_info
        )
        logging.debug(f"Cancel All Orders Send Tx Response: {api_response}")
        return api_response

    async def modify_order(
        self, market_index, order_index, base_amount, price, trigger_price, nonce=-1
    ):
        tx_info = self.sign_modify_order(
            market_index, order_index, base_amount, price, trigger_price, nonce
        )
        logging.debug(f"Modify Order Tx Info: {tx_info}")

        api_response = await self.tx_api.send_tx(
            tx_type=self.TX_TYPE_MODIFY_ORDER, tx_info=tx_info
        )
        logging.debug(f"Modify Order Send Tx Response: {api_response}")
        return api_response

    async def transfer(self, to_account_index, usdc_amount, nonce=-1):
        usdc_amount = int(usdc_amount * self.USDC_TICKER_SCALE)

        tx_info = self.sign_transfer(to_account_index, usdc_amount, nonce)
        logging.debug(f"Transfer Tx Info: {tx_info}")

        api_response = await self.tx_api.send_tx(
            tx_type=self.TX_TYPE_TRANSFER, tx_info=tx_info
        )
        logging.debug(f"Transfer Send Tx Response: {api_response}")
        return api_response

    async def create_public_pool(
        self, operator_fee, initial_total_shares, min_operator_share_rate, nonce=-1
    ):
        tx_info = self.sign_create_public_pool(
            operator_fee, initial_total_shares, min_operator_share_rate, nonce
        )
        logging.debug(f"Create Public Pool Tx Info: {tx_info}")

        api_response = await self.tx_api.send_tx(
            tx_type=self.TX_TYPE_CREATE_PUBLIC_POOL, tx_info=tx_info
        )
        logging.debug(f"Create Public Pool Send Tx Response: {api_response}")
        return api_response

    async def update_public_pool(
        self, public_pool_index, status, operator_fee, min_operator_share_rate, nonce=-1
    ):
        tx_info = self.sign_update_public_pool(
            public_pool_index, status, operator_fee, min_operator_share_rate, nonce
        )
        logging.debug(f"Update Public Pool Tx Info: {tx_info}")

        api_response = await self.tx_api.send_tx(
            tx_type=self.TX_TYPE_UPDATE_PUBLIC_POOL, tx_info=tx_info
        )
        logging.debug(f"Update Public Pool Send Tx Response: {api_response}")
        return api_response

    async def mint_shares(self, public_pool_index, share_amount, nonce=-1):
        tx_info = self.sign_mint_shares(public_pool_index, share_amount, nonce)
        logging.debug(f"Mint Shares Tx Info: {tx_info}")

        api_response = await self.tx_api.send_tx(
            tx_type=self.TX_TYPE_MINT_SHARES, tx_info=tx_info
        )
        logging.debug(f"Mint Shares Send Tx Response: {api_response}")
        return api_response

    async def burn_shares(self, public_pool_index, share_amount, nonce=-1):
        tx_info = self.sign_burn_shares(public_pool_index, share_amount, nonce)
        logging.debug(f"Burn Shares Tx Info: {tx_info}")

        api_response = await self.tx_api.send_tx(
            tx_type=self.TX_TYPE_BURN_SHARES, tx_info=tx_info
        )
        logging.debug(f"Burn Shares Send Tx Response: {api_response}")
        return api_response

    async def close(self):
        await self.api_client.close()
