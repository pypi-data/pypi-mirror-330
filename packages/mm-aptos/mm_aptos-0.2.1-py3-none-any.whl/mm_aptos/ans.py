from mm_crypto_utils import Proxies, random_proxy
from mm_std import Err, Ok, Result, hr


# noinspection DuplicatedCode
def address_to_primary_name(address: str, timeout: int = 5, proxies: Proxies = None, attempts: int = 3) -> Result[str]:
    result: Result[str] = Err("not_started")
    url = f"https://www.aptosnames.com/api/mainnet/v1/primary-name/{address}"
    for _ in range(attempts):
        res = hr(url, proxy=random_proxy(proxies), timeout=timeout)
        data = res.to_dict()
        try:
            if res.code == 200 and res.json == {}:
                return Ok("", data=data)
            return Ok(res.json["name"], data=data)
        except Exception as e:
            result = Err(e, data=data)
    return result


# noinspection DuplicatedCode
def address_to_name(address: str, timeout: int = 5, proxies: Proxies = None, attempts: int = 3) -> Result[str]:
    result: Result[str] = Err("not_started")
    url = f"https://www.aptosnames.com/api/mainnet/v1/name/{address}"
    for _ in range(attempts):
        res = hr(url, proxy=random_proxy(proxies), timeout=timeout)
        data = res.to_dict()
        try:
            if res.code == 200 and res.json == {}:
                return Ok("", data=data)
            return Ok(res.json["name"], data=data)
        except Exception as e:
            result = Err(e, data=data)
    return result
