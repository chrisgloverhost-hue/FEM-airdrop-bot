from decimal import Decimal

from hexbytes import HexBytes
from web3 import Web3
from web3.exceptions import TransactionNotFound
from web3.middleware import geth_poa_middleware

from utils.env import (
    FEM_CHAIN_ID,
    FEM_DECIMALS,
    FEM_ANNOUNCEMENT_CHAT_ID,
    FEM_PAYOUT_ENABLED,
    FEM_PAYOUT_PRIVATE_KEY,
    FEM_REWARD_AMOUNT,
    FEM_RPC_URL,
)


def create_web3():
    if FEM_PAYOUT_ENABLED != "YES":
        raise RuntimeError("FEM payouts are disabled; set FEM_PAYOUT_ENABLED=YES")
    if not FEM_RPC_URL or not FEM_CHAIN_ID or not FEM_PAYOUT_PRIVATE_KEY:
        raise RuntimeError("FEM payout RPC, chain ID, and signing key must be configured")
    if not FEM_ANNOUNCEMENT_CHAT_ID:
        raise RuntimeError("FEM_ANNOUNCEMENT_CHAT_ID must be configured before payouts")

    client = Web3(Web3.HTTPProvider(FEM_RPC_URL, request_kwargs={"timeout": 30}))
    if not client.is_connected():
        raise RuntimeError("Could not connect to the FEM RPC endpoint")
    if client.eth.chain_id != FEM_CHAIN_ID:
        raise RuntimeError("FEM RPC chain ID does not match FEM_CHAIN_ID")
    client.middleware_onion.inject(geth_poa_middleware, layer=0)
    return client


def get_payout_wallet_info():
    client = create_web3()
    account = client.eth.account.from_key(FEM_PAYOUT_PRIVATE_KEY)
    amount_wei = int(Decimal(FEM_REWARD_AMOUNT) * (10 ** FEM_DECIMALS))
    gas_price = client.eth.gas_price
    required_balance = amount_wei + 21000 * gas_price
    balance = client.eth.get_balance(account.address)
    divisor = Decimal(10) ** FEM_DECIMALS
    return {
        "address": account.address,
        "balance": Decimal(balance) / divisor,
        "required_balance": Decimal(required_balance) / divisor,
        "can_pay_next": balance >= required_balance,
    }


def prepare_payout(recipient):
    client = create_web3()
    if not Web3.is_address(recipient):
        raise ValueError("Recipient wallet is not a valid EVM address")

    recipient = Web3.to_checksum_address(recipient)
    account = client.eth.account.from_key(FEM_PAYOUT_PRIVATE_KEY)
    amount_wei = int(Decimal(FEM_REWARD_AMOUNT) * (10 ** FEM_DECIMALS))
    transaction = {
        "chainId": FEM_CHAIN_ID,
        "nonce": client.eth.get_transaction_count(account.address, "pending"),
        "to": recipient,
        "value": amount_wei,
        "gas": 21000,
        "gasPrice": client.eth.gas_price,
    }
    required_balance = amount_wei + transaction["gas"] * transaction["gasPrice"]
    if client.eth.get_balance(account.address) < required_balance:
        raise RuntimeError("FEM payout wallet has insufficient FEM for the reward and gas")
    signed = account.sign_transaction(transaction)
    return Web3.to_hex(signed.rawTransaction), Web3.to_hex(signed.hash)


def broadcast_payout(raw_transaction, transaction_hash):
    client = create_web3()
    try:
        receipt = client.eth.get_transaction_receipt(transaction_hash)
    except TransactionNotFound:
        receipt = None

    if receipt is None:
        try:
            client.eth.send_raw_transaction(HexBytes(raw_transaction))
        except Exception:
            # A previously broadcast transaction may be reported as already known.
            pass
        receipt = client.eth.wait_for_transaction_receipt(transaction_hash, timeout=180)

    if receipt["status"] != 1:
        raise RuntimeError("FEM payout transaction reverted on chain")
    return transaction_hash