from typing import Any, Optional
from uuid import uuid4

from eth_utils.abi import function_abi_to_4byte_selector, collapse_if_tuple
from eth_abi.abi import decode, encode
from web3 import Web3


class SolidityError(Exception):
    pass


def decode_custom_error(abis, error_data) -> Optional[str]:
    """Adapted from https://github.com/ethereum/web3.py/pull/2795#issue-1558580172"""
    error_abi_items = [item for abi in abis for item in abi if item["type"] == "error"]
    for error in error_abi_items:
        name = error["name"]
        data_types = [
            collapse_if_tuple(abi_input) for abi_input in error.get("inputs", [])
        ]
        error_signature_hex = function_abi_to_4byte_selector(error).hex()
        if error_signature_hex.casefold() == str(error_data)[2:10].casefold():
            params = ",".join(
                [
                    str(x)
                    for x in decode(data_types, bytes.fromhex(str(error_data)[10:]))
                ]
            )
            return f"{name}({params})"
    return None


def bytes32_to_hex(bytes32: bytes) -> str:
    return "0x" + bytes32.hex()


def keccak_string(input: str) -> bytes:
    return Web3.solidity_keccak(["string"], [input])


def keccak_abi_unpacked(types: list[str], values: list[Any]) -> bytes:
    return Web3.keccak(primitive=encode(types, values))


def random_uint128() -> int:
    return int(str(uuid4()).replace("-", ""), 16)


def strip_hex(s: str) -> str:
    if s.startswith("0x"):
        return s[2:]
    return s
