"""
RPC utilities
"""
from typing import Union

from starkware.starknet.services.api.feeder_gateway.response_objects import (
    StarknetBlock,
)

from starknet_devnet.blueprints.rpc.structures.types import (
    BlockId,
    Felt,
    PredefinedRpcErrorCode,
    RpcError,
)
from starknet_devnet.state import state
from starknet_devnet.util import StarknetDevnetException


def block_tag_to_block_number(block_id: BlockId) -> BlockId:
    """
    Changes block_id from "latest" / "pending" tag to dict with "block_number" field
    """
    if isinstance(block_id, str):
        if block_id in ["latest", "pending"]:
            return {"block_number": block_id}
        raise RpcError(
            code=PredefinedRpcErrorCode.INVALID_PARAMS.value, message="Invalid params"
        )

    return block_id


async def get_block_by_block_id(block_id: BlockId) -> StarknetBlock:
    """
    Get block using different method depending on block_id type
    """
    block_id = block_tag_to_block_number(block_id)

    try:
        if "block_hash" in block_id:
            return await state.starknet_wrapper.blocks.get_by_hash(
                block_hash=block_id["block_hash"]
            )
        return await state.starknet_wrapper.blocks.get_by_number(
            block_number=block_id["block_number"]
        )
    except StarknetDevnetException as ex:
        raise RpcError.from_spec_name("BLOCK_NOT_FOUND") from ex


async def assert_block_id_is_valid(block_id: BlockId) -> None:
    """
    Assert block_id is valid
    """
    if isinstance(block_id, dict):
        if "block_hash" in block_id and "block_number" in block_id:
            raise RpcError(
                code=-1,
                message="Parameters block_hash and block_number are mutually exclusive.",
            )

        if "block_hash" in block_id or "block_number" in block_id:
            return

    if isinstance(block_id, str):
        if block_id in ("latest", "pending"):
            return

    raise RpcError(
        code=PredefinedRpcErrorCode.INVALID_PARAMS.value,
        message="Invalid value for block id.",
    )


def rpc_felt(value: Union[int, str]) -> Felt:
    """
    Convert value to 0x prefixed felt
    The value can be base 10 integer, base 10 string or base 16 string
    """
    if isinstance(value, str):
        value = int(value) if value.isnumeric() else int(value, 16)

    if value == 0:
        return "0x0"
    return hex(value)


def rpc_storage_key(value: Union[int, str]) -> Felt:
    """
    Convert value to 0x0 prefixed storage key.
    The value can be base 10 integer, base 10 string or base 16 string
    """
    value = rpc_felt(value)

    return "0x0" + value.lstrip("0x")


def gateway_felt(value: Union[int, str]) -> str:
    """
    Convert value to 0x prefixed felt
    The value can be base 10 integer, base 10 string or base 16 string
    """
    if isinstance(value, str):
        value = int(value) if value.isnumeric() else int(value, 16)

    return hex(value)


def rpc_root(root: Union[int, str]) -> Felt:
    """
    Convert 0 prefixed root to 0x prefixed root
    """
    return rpc_felt(root)


def rpc_response(message_id: int, content: dict) -> dict:
    """
    Wrap response content in rpc format
    """
    return {"jsonrpc": "2.0", "id": message_id, "result": content}


def rpc_error(message_id: int, code: int, message: str) -> dict:
    """
    Wrap error in rpc format
    """
    return {
        "jsonrpc": "2.0",
        "id": message_id,
        "error": {"code": code, "message": message},
    }
