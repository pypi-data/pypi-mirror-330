import random
import ecdsa
from eth_utils import keccak


# 生成BTC地址
def maker_address():
    private_key_hex= ''.join(random.choice('0123456789abcdef') for _ in range(64))
    address=make_address_by_hex(private_key_hex)
    return (private_key_hex,address)
# 生成BTC地址
def make_address_by_hex(private_key_hex):
    private_key_hex = private_key_hex.rjust(64, "0")
    private_key = bytes.fromhex(private_key_hex)
    sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)
    vk = sk.get_verifying_key()

    public_key = vk.to_string("uncompressed")
    public_key = public_key[1:]
    keccak_hash = keccak(public_key)

    # 取后20字节作为地址
    address_bytes = keccak_hash[-20:]
    address = "0x" + address_bytes.hex()

    return  address

if __name__ == '__main__':
    print(maker_address())

