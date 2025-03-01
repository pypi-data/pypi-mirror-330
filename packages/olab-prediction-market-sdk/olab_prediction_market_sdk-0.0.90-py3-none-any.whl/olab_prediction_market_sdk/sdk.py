import logging
import math
from time import time

from eth_typing import ChecksumAddress, HexStr
from olab_open_api.api_client import ApiClient
from olab_open_api.api.open_api import OlabOpenApi
from olab_open_api.configuration import Configuration
from olab_prediction_market_sdk.chain.safe.utils import fast_to_checksum_address
from .chain.contract_caller import ContractCaller
from .chain.py_order_utils.builders.order_builder import OrderBuilder
from .chain.py_order_utils.model.order import OrderDataInput, OrderData, PlaceOrderDataInput
from .chain.py_order_utils.constants import ZERO_ADDRESS, ZX
from .chain.py_order_utils.model.signatures import POLY_GNOSIS_SAFE
from .chain.py_order_utils.model.sides import BUY, SELL, OrderSide
from .chain.py_order_utils.model.order_type import LIMIT_ORDER, MARKET_ORDER
from .model import TopicStatus, TopicType
from .chain.py_order_utils.utils import calculate_order_amounts

API_INTERNAL_ERROR_MSG = "Unable to process your request. Please contact technical support."
MISSING_MARKET_ID_MSG = "market_id is required."
MISSING_TOKEN_ID_MSG = "token_id is required."

class InvalidParamError(Exception):
    pass

class OpenApiError(Exception):
    pass

class Client:
    def __init__(self, host='', apikey='', rpc_url='', private_key: HexStr = '', multi_sig_addr = '',
                 conditional_tokens_addr: ChecksumAddress = '', multisend_addr: ChecksumAddress = ''):
        self.conf = Configuration(host=host, api_key=apikey)
        multi_sig_addr = fast_to_checksum_address(multi_sig_addr)
        self.contract_caller = ContractCaller(rpc_url=rpc_url, private_key=private_key, multi_sig_addr=multi_sig_addr,
                                              conditional_tokens_addr=conditional_tokens_addr,
                                              multisend_addr=multisend_addr)
        self.api_client = ApiClient(self.conf)
        self.api = OlabOpenApi(self.api_client)

    def enable_trading(self):
        currency_list_response = self.get_currencies()
        currency_list = currency_list_response['result']['list']
        # print("currency_list: {}".format(currency_list['result']))
        supported_quote_tokens: dict = {}
        for currency in currency_list:
            currency_address = fast_to_checksum_address(currency['currency_address'])
            ctf_exchange_address = fast_to_checksum_address(currency['ctfexchange_address'])
            supported_quote_tokens[currency_address] = ctf_exchange_address

        print('supported_quote_tokens: {}'.format(supported_quote_tokens))
        return self.contract_caller.enable_trading(supported_quote_tokens)

    def split(self, market_id: int = 1, amount: int = 0, check_approval=True):
        # Enable trading first for all trade operations.
        if check_approval:
            self.enable_trading()
        topic_detail = self.get_market(market_id)
        # print("topic_detail: {}".format(topic_detail))
        errno = topic_detail['errno']
        if errno != 0:
            raise OpenApiError("Failed to get the market: {}".format(topic_detail))

        status = topic_detail['result']['data']['status']
        if not (status == TopicStatus.ACTIVATED.value or status == TopicStatus.RESOLVED.value or status == TopicStatus.RESOLVING.value):
            raise OpenApiError('Cannot split on non-activated/resolving/resolved market')
        collateral = fast_to_checksum_address(topic_detail['result']['data']['currencyAddress'])
        condition_id = topic_detail['result']['data']['conditionId']
        # print('split: collateral {} condition {}'.format(collateral, condition_id))

        return self.contract_caller.split(collateral_token=collateral, condition_id=bytes.fromhex(condition_id), amount=amount)

    def merge(self, market_id: int = 1, amount: int = 0, check_approval=True):
        # Enable trading first for all trade operations.
        if check_approval:
            self.enable_trading()
        topic_detail = self.get_market(market_id)
        # print("topic_detail: {}".format(topic_detail))
        errno = topic_detail['errno']
        if errno != 0:
            raise OpenApiError("Failed to get the market: {}".format(topic_detail))

        status = topic_detail['result']['data']['status']
        if not (status == TopicStatus.ACTIVATED.value or status == TopicStatus.RESOLVED.value or status == TopicStatus.RESOLVING.value):
            raise OpenApiError('Cannot merge on non-activated/resolving/resolved market')
        collateral = fast_to_checksum_address(topic_detail['result']['data']['currencyAddress'])
        condition_id = topic_detail['result']['data']['conditionId']
        # print('split: collateral {} condition {}'.format(collateral, condition_id))

        return self.contract_caller.merge(collateral_token=collateral, condition_id=bytes.fromhex(condition_id),
                                          amount=amount)

    def redeem(self, market_id: int = 1, check_approval=True):
        # Enable trading first for all trade operations.
        if check_approval:
            self.enable_trading()
        topic_detail = self.get_market(market_id)
        errno = topic_detail['errno']
        if errno != 0:
            raise OpenApiError("Failed to get the market: {}".format(topic_detail))

        status = topic_detail['result']['data']['status']
        if not status == TopicStatus.RESOLVED.value:
            raise OpenApiError('Cannot redeem on non-resolved market')
        collateral = topic_detail['result']['data']['currencyAddress']
        condition_id = topic_detail['result']['data']['conditionId']
        print('redeem: collateral {} condition {}'.format(collateral, condition_id))
        return self.contract_caller.redeem(collateral_token=collateral, condition_id=bytes.fromhex(condition_id))

    def get_currencies(self):
        thread = self.api.openapi_currency_get(self.conf.api_key, async_req=True)
        result = thread.get()
        return result
    
    def get_markets(self, topic_type: TopicType = None, page: int = 1, limit: int = 20):
        """Get markets with pagination support.
        
        Args:
            topic_type: Optional filter by topic type
            page: Page number (>= 1)
            limit: Number of items per page (1-20)
        """
        if page < 1:
            raise InvalidParamError("page must be >= 1")
        if not 1 <= limit <= 20:
            raise InvalidParamError("limit must be between 1 and 20")
            
        thread = self.api.openapi_topic_get(
            self.conf.api_key,
            topic_type=topic_type.value if topic_type else None,
            page=page,
            limit=limit,
            async_req=True
        )
        result = thread.get()
        return result
    
    def get_market(self, market_id):
        try:
            if not market_id:
                raise InvalidParamError(MISSING_MARKET_ID_MSG)
            
            thread = self.api.openapi_topic_topic_id_get(market_id, self.conf.api_key, async_req=True)
            result = thread.get()
            return result
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get market: {e}")

    def get_categorical_market(self, market_id):
        try:
            if not market_id:
                raise InvalidParamError(MISSING_MARKET_ID_MSG)
            
            thread = self.api.openapi_topic_multi_topic_id_get(market_id, self.conf.api_key, async_req=True)
            result = thread.get()
            return result
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get categorical market: {e}")
    
    def get_candles(self, token_id, interval="1hour", start_time=int(time()), bars=60):
        try:
            if not token_id:
                raise InvalidParamError(MISSING_TOKEN_ID_MSG)
            
            if not interval:
                raise InvalidParamError('interval is required')
                
            thread = self.api.openapi_order_kline_get(token_id, interval, start_time, bars, self.conf.api_key, async_req=True)
            result = thread.get()
            return result
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get candles: {e}")
    
    def get_orderbook(self, token_id):
        try:
            if not token_id:
                raise InvalidParamError(MISSING_TOKEN_ID_MSG)
            
            thread = self.api.openapi_order_orderbook_get(token_id, self.conf.api_key, async_req=True)
            result = thread.get()
            return result
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get orderbook: {e}")
    
    def get_depth(self, token_id):
        try:
            if not token_id:
                raise InvalidParamError(MISSING_TOKEN_ID_MSG)
            
            thread = self.api.openapi_order_market_depth_get(token_id, self.conf.api_key, async_req=True)
            result = thread.get()
            return result
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get depth: {e}")
    
    def _place_order(self, data: OrderDataInput, exchange_addr='', chain_id=8453, currency_addr='', currency_decimal=0, check_approval=False):
        if check_approval:
            self.enable_trading()
        try:
            if not exchange_addr:
                raise InvalidParamError('exchange_addr is required')
            if not chain_id:
                raise InvalidParamError('chain_id is required')        
            
            builder = OrderBuilder(exchange_addr, chain_id, self.contract_caller.signer)
            takerAmount = 0
            
            if data.orderType == MARKET_ORDER:
                takerAmount = 0
                data.price = "0"
                recalculated_maker_amount = data.makerAmount * math.pow(10, currency_decimal)
            if data.orderType == LIMIT_ORDER:
                recalculated_maker_amount, takerAmount = calculate_order_amounts(
                    price=float(data.price),
                    maker_amount=data.makerAmount * math.pow(10, currency_decimal),
                    side=data.side,
                    decimals=currency_decimal
                )
            
            order_data = OrderData(
                maker=self.contract_caller.multi_sig_addr,
                taker=ZERO_ADDRESS,
                tokenId=data.tokenId,
                makerAmount=recalculated_maker_amount,
                takerAmount=takerAmount,
                feeRateBps='0',
                side=data.side,  # Using OrderSide enum directly
                signatureType=POLY_GNOSIS_SAFE,
                signer=self.contract_caller.signer.address()
            )
            signerOrder = builder.build_signed_order(order_data)
            
            order_dict = signerOrder.order.dict()
          
            v2_add_order_req_body = dict(
                salt=str(order_dict['salt']),
                topicId=data.marketId,
                maker=order_dict['maker'],
                signer=order_dict['signer'],
                taker=order_dict['taker'],
                tokenId=str(order_dict['tokenId']),
                makerAmount=str(order_dict['makerAmount']),
                takerAmount=str(order_dict['takerAmount']),
                expiration=str(order_dict['expiration']),
                nonce=str(order_dict['nonce']),
                feeRateBps=str(order_dict['feeRateBps']),
                # convert OrderSide to int
                side=str(order_dict['side']),
                signatureType=str(order_dict['signatureType']),
                signature=signerOrder.signature,
                sign=signerOrder.signature,
                contractAddress="",
                currencyAddress=currency_addr,
                price=data.price,
                tradingMethod=int(data.orderType),
                timestamp=int(time()),
                safeRate='0',
                orderExpTime='0'
            )

            thread = self.api.openapi_order_post(self.conf.api_key, v2_add_order_req=v2_add_order_req_body, async_req=True)
            return thread.get()
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to place order: {e}")
    
    def place_order(self, data: PlaceOrderDataInput, check_approval=False):        
        currency_list_response = self.get_currencies()
        currency_list = currency_list_response['result']['list']
        
        market_response = self.get_market(data.marketId)
        market = market_response['result']['data']
        currencyAddr = market['currencyAddress']
        
        # find currency from currency_list by currency_addr
        currency = next((item for item in currency_list if str.lower(item['currency_address']) == str.lower(currencyAddr)), None)
        exchange_addr = currency['ctfexchange_address']
        chain_id = currency['chain_id']
        
        makerAmount = 0
        minimal_maker_amount = 0.01
        
        # reject if market buy and makerAmountInBaseToken is provided
        if(data.side == OrderSide.BUY and data.orderType == MARKET_ORDER and data.makerAmountInBaseToken):
            raise InvalidParamError('makerAmountInBaseToken is not allowed for market buy')
        
        # reject if market sell and makerAmountInQuoteToken is provided
        if(data.side == OrderSide.SELL and data.orderType == MARKET_ORDER and data.makerAmountInQuoteToken):
            raise InvalidParamError('makerAmountInQuoteToken is not allowed for market sell')
        
        # need amount to be in quote token
        if(data.side == OrderSide.BUY):
            # e.g. yes/no
            if(data.makerAmountInBaseToken):
                makerAmount = float(data.makerAmountInBaseToken) * float(data.price)
                # makerAmountInBaseToken should be at least 1 otherwise throw error
                if(float(data.makerAmountInBaseToken) < minimal_maker_amount):
                    raise ValueError("makerAmountInBaseToken must be at least 0.01")
            # e.g. usdc
            if(data.makerAmountInQuoteToken):
                makerAmount = float(data.makerAmountInQuoteToken)
                # makerAmountInQuoteToken should be at least 1 otherwise throw error
                if(float(data.makerAmountInQuoteToken) < minimal_maker_amount):
                    raise ValueError("makerAmountInQuoteToken must be at least 0.01")
        if(data.side == OrderSide.SELL):
            # e.g. yes/no
            if(data.makerAmountInBaseToken):
                makerAmount = float(data.makerAmountInBaseToken)
                # makerAmountInBaseToken should be at least 1 otherwise throw error
                if(float(data.makerAmountInBaseToken) < minimal_maker_amount):
                    raise ValueError("makerAmountInBaseToken must be at least 0.01")
            # e.g. usdc
            if(data.makerAmountInQuoteToken):
                makerAmount = float(data.makerAmountInQuoteToken) / float(data.price)
                # makerAmountInQuoteToken should be at least 1 otherwise throw error
                if(float(data.makerAmountInQuoteToken) < minimal_maker_amount):
                    raise ValueError("makerAmountInQuoteToken must be at least 0.01")
        
        
        input = OrderDataInput(
            marketId=data.marketId,
            tokenId=data.tokenId,
            makerAmount=makerAmount,
            price=data.price,
            orderType=data.orderType,
            side=data.side
        )
        
        return self._place_order(input, exchange_addr, chain_id, currencyAddr, int(currency['decimal']), check_approval)
    
    def cancel_order(self, trans_no):
        if not trans_no or not isinstance(trans_no, str):
            raise InvalidParamError('trans_no must be a non-empty string')
        
        request_body = dict(trans_no=trans_no)
        thread = self.api.openapi_order_cancel_order_post(self.conf.api_key, view_cancel_order_request=request_body, async_req=True)
        return thread.get()
    
    def get_my_orders(self, market_id=0, status="", limit=10):
        try:
            if not isinstance(market_id, int):
                raise InvalidParamError('market_id must be an integer')
            
            thread = self.api.openapi_order_get(self.conf.api_key, topic_id=market_id, status=status, limit=limit, async_req=True)
            return thread.get()
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get open orders: {e}")
    
    def get_my_positions(self, market_id=0, page=1, pageSize=10):
        try: 
            if not isinstance(market_id, int):
                raise InvalidParamError('market_id must be an integer')
            
            if not isinstance(page, int):
                raise InvalidParamError('page must be an integer')
            
            if not isinstance(pageSize, int):
                raise InvalidParamError('pageSize must be an integer')
            
            
            thread = self.api.openapi_portfolio_get(self.conf.api_key, topic_id=market_id, page=page, limit=pageSize, async_req=True)
            return thread.get()
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get my positions: {e}")
    
    def get_my_balances(self):
        try:
            wallet_address = self.contract_caller.signer.address()
            thread = self.api.openapi_user_wallet_address_balance_get(wallet_address, self.conf.api_key, async_req=True)
            return thread.get()
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get my balances: {e}")
        
        return response
    
    def get_my_trades(self, market_id=0, limit=10):
        try:
            if not isinstance(market_id, int):
                raise InvalidParamError('market_id must be an integer')
            
            thread = self.api.openapi_trade_get(self.conf.api_key, topic_id=market_id, limit=limit, async_req=True)
            return thread.get()
        except InvalidParamError as e:
            logging.error(f"Validation error: {e}")
            raise
        except Exception as e:
            logging.error(f"API error: {e}")
            raise OpenApiError(f"Failed to get my trades: {e}")