import pytest
from mm_std import get_dotenv


@pytest.fixture
def mainnet_rpc_url() -> str:
    return get_dotenv("MAINNET_RPC_URL")


@pytest.fixture
def okx_address() -> str:
    return "0x834d639b10d20dcb894728aa4b9b572b2ea2d97073b10eacb111f338b20ea5d7"
