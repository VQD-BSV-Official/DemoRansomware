# from Crypto.Cipher import AES, PKCS1_OAEP
# from Crypto.PublicKey import RSA

# def decrypt_file(input_file, key_file, private_key_file, bytes_to_encrypt=153605):
#     # Đọc khóa bí mật RSA
#     with open(private_key_file, 'rb') as f:
#         private_key = RSA.import_key(f.read())
    
#     # Đọc khóa AES mã hóa
#     with open(key_file, 'rb') as f:
#         encrypted_aes_key = f.read()
    
#     # Giải mã khóa AES bằng khóa bí mật RSA
#     cipher_rsa = PKCS1_OAEP.new(private_key)
#     aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    
#     # Đọc file mã hóa
#     with open(input_file, 'rb') as f:
#         encrypted_data = f.read()
    
#     # Tách IV, ciphertext và phần không mã hóa
#     iv = encrypted_data[:AES.block_size]
#     padded_length = ((bytes_to_encrypt // AES.block_size) + 1) * AES.block_size
#     ciphertext = encrypted_data[AES.block_size:AES.block_size + padded_length]
#     remaining_data = encrypted_data[AES.block_size + padded_length:]
    
#     # Khởi tạo cipher AES và giải mã
#     cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
#     padded_data = cipher_aes.decrypt(ciphertext)
    
#     # Loại bỏ đệm
#     padding_length = padded_data[-1]
#     plaintext = padded_data[:-padding_length]
    
#     # Ghi đè lên file gốc
#     with open(input_file, 'wb') as f:
#         f.write(plaintext + remaining_data)
    
#     print(f"Đã giải mã và ghi đè lên: {input_file}")

# if __name__ == "__main__":
#     input_file = 'YTB_VID11.mp4'
#     key_file = 'AES_KEY_DO_NOT_DELETE.key'
#     private_key_file = 'PRIVATE_KEY_DO_NOT_DELETE.key'
#     BYTES_TO_ENCRYPT = 153605  # Phải khớp với số byte đã mã hóa
#     decrypt_file(input_file, key_file, private_key_file, BYTES_TO_ENCRYPT)











import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA


def decrypt_file(input_file, aes_key, bytes_to_encrypt=153605):
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()

    iv = encrypted_data[:AES.block_size]
    padded_length = ((bytes_to_encrypt // AES.block_size) + 1) * AES.block_size

    ciphertext = encrypted_data[
        AES.block_size : AES.block_size + padded_length
    ]
    remaining_data = encrypted_data[
        AES.block_size + padded_length :
    ]

    cipher_aes = AES.new(aes_key, AES.MODE_CBC, iv)
    padded_data = cipher_aes.decrypt(ciphertext)

    padding_length = padded_data[-1]
    plaintext = padded_data[:-padding_length]

    with open(input_file, 'wb') as f:
        f.write(plaintext + remaining_data)

    print(f"✔ Đã giải mã: {input_file}")


def decrypt_path(input_path, key_file, private_key_file,
                 bytes_to_encrypt=153605,
                 exts=None):
    # đọc private key RSA
    with open(private_key_file, 'rb') as f:
        private_key = RSA.import_key(f.read())

    # đọc AES key (đã bị RSA mã hóa)
    with open(key_file, 'rb') as f:
        encrypted_aes_key = f.read()

    cipher_rsa = PKCS1_OAEP.new(private_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)

    # chuẩn hóa extension
    if exts:
        exts = tuple(e.lower() for e in exts)

    if os.path.isfile(input_path):
        decrypt_file(input_path, aes_key, bytes_to_encrypt)

    elif os.path.isdir(input_path):
        for root, _, files in os.walk(input_path):
            for name in files:
                if exts and not name.lower().endswith(exts):
                    continue
                full_path = os.path.join(root, name)
                try:
                    decrypt_file(full_path, aes_key, bytes_to_encrypt)
                except Exception as e:
                    print(f"✘ Lỗi {full_path}: {e}")
    else:
        print("❌ Đường dẫn không tồn tại")


decrypt_path(
    input_path="F:\\Disk_Lab",
    key_file="AES_KEY_DO_NOT_DELETE.key",
    private_key_file="PRIVATE_KEY_DO_NOT_DELETE.key"
)
