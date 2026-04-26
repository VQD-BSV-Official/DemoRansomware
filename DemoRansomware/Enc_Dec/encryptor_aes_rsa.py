from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
import os

def pad(data):
    # Đệm dữ liệu để có độ dài là bội số của 16
    padding_length = AES.block_size - len(data) % AES.block_size
    padding = bytes([padding_length]) * padding_length
    return data + padding

def encrypt_file(input_file, key_file, bytes_to_encrypt=153605):
    # Tạo cặp khóa RSA
    rsa_key = RSA.generate(2048)
    private_key = rsa_key.export_key()
    public_key = rsa_key.publickey()
    
    # Tạo khóa AES ngẫu nhiên
    aes_key = get_random_bytes(32)  # Khóa AES-256 (32 byte)
    
    # Mã hóa khóa AES bằng khóa công khai RSA
    cipher_rsa = PKCS1_OAEP.new(public_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    
    # Lưu khóa AES mã hóa và khóa bí mật RSA
    with open(key_file, 'wb') as f:
        f.write(encrypted_aes_key)
        
    with open('private_key.pem', 'wb') as f:
        f.write(private_key)
    
    # Khởi tạo cipher AES với chế độ CBC
    iv = get_random_bytes(AES.block_size)
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    
    # Đọc file đầu vào
    with open(input_file, 'rb') as f:
        plaintext = f.read(bytes_to_encrypt)
        remaining_data = f.read()
    
    # Thêm đệm và mã hóa phần đầu
    padded_data = pad(plaintext)
    ciphertext = cipher_aes.encrypt(padded_data)
    
    # Ghi đè lên file gốc
    with open(input_file, 'wb') as f:
        f.write(iv + ciphertext + remaining_data)
    
    print(f"Đã mã hóa {bytes_to_encrypt} byte đầu tiên và ghi đè lên: {input_file}")
    print(f"Khóa AES mã hóa được lưu vào: {key_file}")
    print(f"Khóa bí mật RSA được lưu vào: private_key.pem")

if __name__ == "__main__":
    input_file = 'input.mov'
    key_file = 'key.bin'
    BYTES_TO_ENCRYPT = 153605  # Số byte cần mã hóa, có thể thay đổi
    encrypt_file(input_file, key_file, BYTES_TO_ENCRYPT)