import json
import os
import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
import time
from typing import Any, Optional

import requests
from eth_account import Account
from eth_account.messages import encode_defunct, encode_typed_data
from eth_typing import Hash32, HexAddress, HexStr
from hexbytes import HexBytes
from web3 import Web3
from web3.contract import Contract
from web3.exceptions import ContractCustomError

from tread_contracts.deployments import DEPLOYMENTS, SUPPORTED_CHAINS
from tread_contracts.util import (
    SolidityError,
    decode_custom_error,
    keccak_abi_unpacked,
    keccak_string,
    strip_hex,
)

DEFAULT_TIMEOUT = 3000

ABI_RELATIVE_PATH = "abi"
ABI_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    ABI_RELATIVE_PATH,
)

# Ref: https://docs.gelato.network/web3-services/relay/tracking-your-relay-request#task-states
GELATO_BASE_URL = "https://api.gelato.digital"
GELATO_EXEC_SUCCESS = "ExecSuccess"
GELATO_TERMINAL_STATUSES = [
    GELATO_EXEC_SUCCESS,
    "ExecReverted",
    "Cancelled",
]
GELATO_POLL_INTERVAL_SECONDS = 0.5

EIP712_DOMAIN_TYPE = (
    "EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"
)
EIP712_PREFIX_BYTES2 = bytes.fromhex("1901")

# Used by EIP-712 signing “method 2” which supports easier debugging.
# Only supports (most of) the builtin types.
EIP712_SUPPORTED_TYPES = [
    r"u?int\d+",
    r"bytes\d+",
    r"address",
    r"string",
    r"bytes",
]


@dataclass
class Eip712DomainInfo:
    name: str
    version: str


class TransactionRevertError(RuntimeError):

    def __init__(self, receipt):
        self.receipt = receipt


class BaseContractClient(ABC):

    def __init__(
        self,
        *,
        web3: Optional[Web3] = None,
        web3_provider: Optional[Web3.HTTPProvider] = None,
        rpc_url: Optional[str] = None,
        timeout: Optional[int] = DEFAULT_TIMEOUT,
        chain_id: Optional[int] = None,
        private_key: Optional[str] = None,
        gelato_api_key: Optional[str] = None,
    ):
        # Configured parameters initial values.
        self._account = None
        self._chain_id = chain_id
        self._timeout = timeout
        self._web3 = None
        self._gelato_api_key = gelato_api_key

        # Other initial state.
        self._cached_contracts: dict[HexAddress, Contract] = {}
        self._cached_eip712_nonces: dict[Eip712NonceKey, int] = {}

        # Initialize provider.
        if web3 is not None or web3_provider is not None or rpc_url is not None:
            if web3_provider is None and rpc_url is not None:
                web3_provider = Web3.HTTPProvider(
                    rpc_url, request_kwargs={"timeout": self._timeout}
                )
            self._web3 = web3 or Web3(web3_provider)
            self._chain_id = self.chain_id or self._web3.eth.chain_id

        # TODO: Validate and maybe sanitize format of the key.
        if private_key is not None:
            self._account = self.web3.eth.account.from_key(private_key)

        # Validate parameters.
        if self._chain_id not in SUPPORTED_CHAINS:
            raise RuntimeError(f"Unsupported chain ID: {self._chain_id}")

    # ---------- #
    # Properties #
    # ---------- #

    @property
    @abstractmethod
    def contract(self) -> Contract:
        pass

    @property
    def chain_id(self):
        return self._chain_id

    @property
    def timeout(self):
        return self._timeout

    @property
    def account(self) -> HexAddress:
        if self._account is None:
            raise RuntimeError("Client was not initialized with a private key")
        return self._account

    @property
    def account_address(self) -> HexAddress:
        if self._account is None:
            raise RuntimeError("Client was not initialized with a private key")
        return self._account.address

    @property
    def web3(self) -> Web3:
        web3 = self._web3
        if web3 is None:
            raise RuntimeError("Client was not initialized with a web3 provider")
        return web3

    # ---------------- #
    # Internal Methods #
    # ---------------- #

    def _create_contract(
        self,
        abi_name: str,
        address: HexAddress,
    ) -> Contract:
        if self._web3 is None:
            raise RuntimeError("Client was not initialized with a web3 provider")

        abi_path = os.path.join(ABI_DIR, f"{abi_name}.json")
        try:
            with open(abi_path, "r") as f:
                abi = json.load(f)
        except FileNotFoundError:
            raise RuntimeError(f"Could not find ABI: {abi_name}")
        return self._web3.eth.contract(
            address=Web3.to_checksum_address(address),
            abi=abi,
        )

    def _call_contract_read(self, funcName: str, *args: list[Any]) -> Any:
        try:
            return getattr(self.contract.functions, funcName)(*args).call()
        except ContractCustomError as e:
            error_message = decode_custom_error([self.contract.abi], e.args[0])
            if error_message is None:
                raise e
            raise SolidityError(error_message) from e

    def _call_contract_write_metatx(self, unsent_tx: dict[str, Any]) -> HexStr:
        response = requests.post(
            f"{GELATO_BASE_URL}/relays/v2/sponsored-call",
            headers={"Content-Type": "application/json"},
            json={
                "chainId": self.chain_id,
                "target": unsent_tx["to"],
                "data": unsent_tx["data"],
                "sponsorApiKey": self._gelato_api_key,
            },
        )
        data = response.json()
        if "taskId" not in data:
            raise RuntimeError(
                "Gelato task failed with message: " + data.get("message", "")
            )
        task_id = data["taskId"]
        status = ""
        taskData = {}
        while status not in GELATO_TERMINAL_STATUSES:
            if taskData:
                time.sleep(GELATO_POLL_INTERVAL_SECONDS)
            response = requests.get(
                f"{GELATO_BASE_URL}/tasks/status/{task_id}",
            )
            data = response.json()
            taskData = data["task"]
            status = taskData["taskState"]
        if status == GELATO_EXEC_SUCCESS:
            return HexStr(taskData["transactionHash"])
        raise RuntimeError(
            f"Gelato task failed with status and message: "
            f"{status}: {taskData['lastCheckMessage']}"
        )

    def _call_contract_write(
        self, funcName: str, *args: list[Any], use_meta_tx: bool
    ) -> HexStr:
        nonce = self.web3.eth.get_transaction_count(self.account.address)
        try:
            unsent_tx = getattr(self.contract.functions, funcName)(
                *args
            ).build_transaction(
                {
                    "from": self.account.address,
                    "nonce": nonce,
                }
            )
        except ContractCustomError as e:
            error_message = decode_custom_error([self.contract.abi], e.args[0])
            if error_message is None:
                raise e
            raise SolidityError(error_message) from e

        if use_meta_tx:
            if self._gelato_api_key is None:
                raise RuntimeError("Gelato API key is required for meta transactions")
            return self._call_contract_write_metatx(unsent_tx)

        signed_tx = self.account.sign_transaction(unsent_tx)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return HexStr(f"0x{tx_hash.hex()}")

    def _eip712_sign_helper_1(
        self,
        domain_info: Eip712DomainInfo,
        primary_type: str,  # e.g. 'MyAction'
        fields: list[str],  # e.g. 'uint256 value'
        values: list[Any],
    ) -> HexBytes:
        """Sign an EIP-712 message using eth_account.messages.encode_typed_data."""
        types = {
            primary_type: [
                {"name": field.split()[1], "type": field.split()[0]} for field in fields
            ]
        }
        message = {
            "types": types,
            "primaryType": primary_type,
            "domain": {
                "name": domain_info.name,
                "version": domain_info.version,
                "chainId": self.chain_id,
                "verifyingContract": self.contract.address,
            },
            "message": {fields[i].split()[1]: v for i, v in enumerate(values)},
        }
        signable_message = encode_typed_data(full_message=message)
        return Account.sign_message(signable_message, self.account.key).signature

    def _eip712_sign_helper_2(
        self,
        domain_info: Eip712DomainInfo,
        type_str: str,
        fields: list[str],
        orig_values: list[Any],
    ) -> HexBytes:
        """Sign an EIP-712 message by constructing the digest manually.

        This method currently only supports basic types, but offers easier debugging
        compared with using the eth_account library method.
        """
        orig_types = [field.split()[0] for field in fields]
        for field_type in orig_types:
            if not any(
                re.match(pattern, field_type) for pattern in EIP712_SUPPORTED_TYPES
            ):
                raise ValueError(
                    f"Unsupported type in EIP712 type string: {field_type}"
                )
        values = [
            (
                keccak_string(v)
                if orig_types[i] == "string"
                else (
                    Web3.solidity_keccak(["bytes"], [v])
                    if orig_types[i] == "bytes"
                    else v
                )
            )
            for i, v in enumerate(orig_values)
        ]
        types = ["bytes32" if t in ["string", "bytes"] else t for t in orig_types]

        domain_hash = keccak_abi_unpacked(
            ["bytes32", "bytes32", "bytes32", "uint256", "address"],
            [
                keccak_string(EIP712_DOMAIN_TYPE),
                keccak_string(domain_info.name),
                keccak_string(domain_info.version),
                self.chain_id,
                self.contract.address,
            ],
        )
        struct_hash = keccak_abi_unpacked(
            ["bytes32", *types],
            [
                keccak_string(type_str),
                *values,
            ],
        )
        eip712_hash = Web3.solidity_keccak(
            [
                "bytes2",
                "bytes32",
                "bytes32",
            ],
            [
                EIP712_PREFIX_BYTES2,
                domain_hash,
                struct_hash,
            ],
        )
        return Account._sign_hash(eip712_hash, self.account.key).signature

    def _eip712_sign(
        self,
        domain_info: Eip712DomainInfo,
        type_str: str,
        values: list[Any],
    ) -> HexBytes:
        # Parse the type string.
        primary_type = type_str.partition("(")[0]
        fields_match = re.match(r".*\((.*)\)", type_str)
        if not fields_match:
            raise ValueError(f"Invalid type string: {type_str}")
        fields = fields_match.group(1).split(",")

        return self._eip712_sign_helper_1(
            domain_info,
            primary_type,
            fields,
            values,
        )

    # -------------- #
    # Public Methods #
    # -------------- #

    def get_contract(
        self,
        abi_name: str,
        address: Optional[HexAddress] = None,
    ) -> Contract:
        if address is None:
            if self._chain_id is None:
                raise RuntimeError("Client was not initialized with a chain ID")
            address = DEPLOYMENTS[abi_name][self._chain_id]
        if address not in self._cached_contracts:
            self._cached_contracts[address] = self._create_contract(
                abi_name,
                address,
            )
        return self._cached_contracts[address]

    def wait_for_tx_or_throw(
        self,
        tx_hash: str,
    ) -> dict[str, Any]:
        # TODO: Validate and maybe sanitize format of the hash.
        tx_hash_bytes = bytes.fromhex(strip_hex(tx_hash))
        tx_hash_32 = Hash32(tx_hash_bytes)

        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash_32)
        if tx_receipt["status"] == 0:
            raise TransactionRevertError(tx_receipt)
        return tx_receipt
