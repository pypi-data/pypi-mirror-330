from mm_aptos import ans


def test_address_to_primary_name():
    address = "0x68e6982c788b50e3caccc834a4764763381d7201be996914e1310139a35854ed"
    assert ans.address_to_primary_name(address).ok == "vitalik"


def test_address_to_name():
    address = "0x68e6982c788b50e3caccc834a4764763381d7201be996914e1310139a35854ed"
    assert ans.address_to_name(address).ok == "vitalik"
