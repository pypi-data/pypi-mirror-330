import hashlib
import random

import base58
from ecdsa import SigningKey, SECP256k1

# 生成BTC地址
def maker_address():
    private_key_hex= ''.join(random.choice('0123456789abcdef') for _ in range(64))
    address=make_address_by_hex(private_key_hex)
    return (private_key_hex,address)
# 生成BTC地址
def make_address_by_hex(private_key_hex):
    private_key_hex = private_key_hex.rjust(64, "0")
    private_key = bytes.fromhex(private_key_hex)
    sk = SigningKey.from_string(private_key, curve=SECP256k1)
    # 压缩地址
    uncompressed_public_key = sk.get_verifying_key().to_string('compressed')
    public_key_hash = hashlib.new('ripemd160', hashlib.sha256(uncompressed_public_key).digest()).digest()
    p2pkh_uncompressed_address = base58.b58encode_check(bytes.fromhex('00') + public_key_hash).decode()
    return p2pkh_uncompressed_address


# 生成BTC地址160地址
def make_h160_by_hex(private_key_hex):
    private_key_hex = private_key_hex.rjust(64, "0")
    private_key = bytes.fromhex(private_key_hex)
    sk = SigningKey.from_string(private_key, curve=SECP256k1)
    # 压缩地址
    uncompressed_public_key = sk.get_verifying_key().to_string('compressed')
    public_key_hash = hashlib.new('ripemd160', hashlib.sha256(uncompressed_public_key).digest()).digest()
    return public_key_hash.hex()

# 生成BTC地址160地址
def piv_to_puk(private_key_hex):
    private_key_hex = private_key_hex.rjust(64, "0")
    private_key = bytes.fromhex(private_key_hex)
    sk = SigningKey.from_string(private_key, curve=SECP256k1)
    # 压缩地址
    uncompressed_public_key = sk.get_verifying_key().to_string('compressed')
    return uncompressed_public_key.hex()
def piv_to_puk_xy(private_key_hex):
    private_key_hex = private_key_hex.rjust(64, "0")
    private_key = bytes.fromhex(private_key_hex)
    sk = SigningKey.from_string(private_key, curve=SECP256k1)
    # 压缩地址
    uncompressed_public_key = sk.get_verifying_key().to_string('uncompressed').hex()
    x=uncompressed_public_key[2:66]
    y=uncompressed_public_key[66:]
    return x,y
def address_to_h160(address):
    # Base58 解码
    decoded_bytes = base58.b58decode_check(address)
    # 去掉版本字节（00），得到 h160
    h160 = decoded_bytes[1:]
    # 将 h160 转换为十六进制字符串
    h160_hex = h160.hex()
    return h160_hex
def h160_to_address(h160):
    h160 = bytes.fromhex(h160)
    address = base58.b58encode_check(bytes.fromhex('00') + h160).decode()
    return address
if __name__ == '__main__':
    print(piv_to_puk_xy("000000000000000000000000000000033e7665705359f04f28b88cf897c603c9"))

