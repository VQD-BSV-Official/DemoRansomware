from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

def decrypt_file(input_file, key_file, private_key_file, bytes_to_encrypt=153632):
    # Đọc khóa bí mật RSA
    with open(private_key_file, 'rb') as f:
        private_key = RSA.import_key(f.read())
    
    # Đọc khóa AES mã hóa
    with open(key_file, 'rb') as f:
        encrypted_aes_key = f.read()
    
    # Giải mã khóa AES bằng khóa bí mật RSA
    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    
    # Đọc file mã hóa
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    
    # Tách IV, ciphertext và phần không mã hóa
    iv = encrypted_data[:AES.block_size]
    padded_length = ((bytes_to_encrypt // AES.block_size) + 1) * AES.block_size
    ciphertext = encrypted_data[AES.block_size:AES.block_size + padded_length]
    remaining_data = encrypted_data[AES.block_size + padded_length:]
    
    # Khởi tạo cipher AES và giải mã
    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    padded_data = cipher_aes.decrypt(ciphertext)
    
    # Loại bỏ đệm
    padding_length = padded_data[-1]
    plaintext = padded_data[:-padding_length]
    
    # Ghi đè lên file gốc
    with open(input_file, 'wb') as f:
        f.write(plaintext + remaining_data)
    
    print(f"Đã giải mã và ghi đè lên: {input_file}")

if __name__ == "__main__":
    input_file = 'input.mov'
    key_file = 'key.bin'
    private_key_file = 'private_key.pem'
    BYTES_TO_ENCRYPT = 153632  # Phải khớp với số byte đã mã hóa
    decrypt_file(input_file, key_file, private_key_file, BYTES_TO_ENCRYPT)