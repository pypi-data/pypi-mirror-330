from decimal import Decimal

from mm_crypto_utils import Nodes, Proxies, random_node, random_proxy
from mm_std import Err, Ok, Result, hr


def get_balance(nodes: str, account_address: str, coin_type: str, timeout: float = 5.0, proxy: str | None = None) -> Result[int]:
    url = f"{random_node(nodes)}/accounts/{account_address}/resource/0x1::coin::CoinStore%3C{coin_type}%3E"
    res = hr(url, proxy=proxy, timeout=timeout)
    try:
        if res.json.get("error_code") == "resource_not_found":
            return Ok(0, data=res.to_dict())
        return Ok(int(res.json["data"]["coin"]["value"]), data=res.to_dict())
    except Exception as err:
        return Err(err, data=res.to_dict())


def get_balance_with_retries(
    retries: int, nodes: Nodes, account_address: str, coin_type: str, timeout: float = 5.0, proxies: Proxies = None
) -> Result[int]:
    res: Result[int] = Err("not started yet")
    for _ in range(retries):
        res = get_balance(random_node(nodes), account_address, coin_type, timeout=timeout, proxy=random_proxy(proxies))
        if res.is_ok():
            return res
    return res


def get_decimal_balance_with_retries(
    retries: int,
    nodes: Nodes,
    account_address: str,
    coin_type: str,
    decimals: int,
    round_ndigits: int = 5,
    timeout: float = 5.0,
    proxies: Proxies = None,
) -> Result[Decimal]:
    return get_balance_with_retries(retries, nodes, account_address, coin_type, timeout=timeout, proxies=proxies).and_then(
        lambda o: Ok(round(Decimal(o / 10**decimals), ndigits=round_ndigits))
    )
