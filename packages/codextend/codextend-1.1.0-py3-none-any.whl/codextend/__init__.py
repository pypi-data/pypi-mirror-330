# module titlefile
# codextend.py

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import chardet
import base64
import os

def binary_file(codepath, numbits=8, numbytes=None, start_line=None, end_line=None):
    """
    Convert file content to binary representation.

    Parameters:
    codepath (str): The path to the file.
    numbits (int): The number of bits to use for each byte (default is 8).
    numbytes (int, optional): The number of bytes to read from the file.
    start_line (int, optional): The starting line number to convert.
    end_line (int, optional): The ending line number to convert.

    Returns:
    str: The binary representation of the file content.
    """
    try:
        with open(codepath, 'rb') as file:
            byte_data = file.read()
        binarydata = ' '.join(format(byte, f'0{numbits}b') for byte in byte_data)
        return binarydata
    except FileNotFoundError:
        return f"The file {codepath} was not found."
    except Exception as e:
        return f"{e}"

def bin_text(oriext, start_line=1, end_line=None, numbytes=None, numbits=8):
    """
    Convert text to binary representation.

    Parameters:
    oriext (str): The original text to convert.
    start_line (int): The starting line number to convert.
    end_line (int, optional): The ending line number to convert.
    numbytes (int, optional): The number of bytes to convert from each line.
    numbits (int): The number of bits to use for each byte.

    Returns:
    str: The binary representation of the text.
    """
    try:
        lines = oriext.splitlines()
        if end_line is not None and (start_line > end_line or start_line < 1):
            return "Invalid line range."
        selected_lines = lines[start_line - 1:end_line]
        bin_lines = []
        for line in selected_lines:
            byte_data = line.encode('utf-8')[:numbytes]
            bin_line = ' '.join(format(byte, f'0{numbits}b') for byte in byte_data)
            bin_lines.append(bin_line)
        return '\n'.join(bin_lines)
    except Exception as e:
        return f"{e}"

def cvet(encet, fenc, tenc):
    """
    Convert text encoding.

    Parameters:
    encet (str): The text to convert.
    fenc (str): The original encoding of the text.
    tenc (str): The target encoding to convert the text to.

    Returns:
    str: The converted text.
    """
    try:
        if fenc.upper() != 'UTF-8':
            encet = encet.encode(fenc).decode('utf-8')
        cenc = encet.encode('utf-8').decode(tenc)
        return cenc
    except UnicodeDecodeError as e:
        return f"{e}"
    except UnicodeEncodeError as e:
        return f"{e}"
    except Exception as e:
        return f"{e}"

def cfen(codepath, tarcode):
    """
    Convert file encoding.

    Parameters:
    codepath (str): The path to the file.
    tarcode (str): The target encoding to convert the file to.

    Returns:
    str: A message indicating success or the error encountered.
    """
    try:
        with open(codepath, 'rb') as file:
            raw_data = file.read()
        detected_encoding = chardet.detect(raw_data)['encoding']
        print(f"Detected file encoding: {detected_encoding}")

        if detected_encoding != 'utf-8':
            content = raw_data.decode(detected_encoding, errors='ignore')
            converted_content = content.encode('utf-8').decode('utf-8')
        else:
            converted_content = raw_data.decode('utf-8', errors='ignore')
        final_content = converted_content.encode(tarcode, errors='ignore').decode(tarcode, errors='ignore')
        with open(codepath, 'w', encoding=tarcode, errors='ignore') as file:
            file.write(final_content)
        return "File encoding converted successfully."
    except FileNotFoundError:
        return f"The file {codepath} was not found."
    except Exception as e:
        return f"{e}"

def hex_file(codepath, numbytes=None, start_line=None, end_line=None):
    """
    Convert file content to hexadecimal representation.

    Parameters:
    codepath (str): The path to the file.
    numbytes (int, optional): The number of bytes to read from the file.
    start_line (int, optional): The starting line number to convert.
    end_line (int, optional): The ending line number to convert.

    Returns:
    str: The hexadecimal representation of the file content.
    """
    try:
        with open(codepath, 'rb') as file:
            if numbytes is not None:
                byte_data = file.read(numbytes)
            else:
                byte_data = file.read()
        hexdata = ' '.join(format(byte, '02x') for byte in byte_data)
        return hexdata
    except FileNotFoundError:
        return f"The file {codepath} was not found."
    except Exception as e:
        return f"An error occurred: {e}"

def hex_text(oriext, start_line=1, end_line=None, numbytes=None):
    """
    Convert text to hexadecimal representation.

    Parameters:
    oriext (str): The original text to convert.
    start_line (int): The starting line number to convert.
    end_line (int, optional): The ending line number to convert.
    numbytes (int, optional): The number of bytes to convert from each line.

    Returns:
    str: The hexadecimal representation of the text.
    """
    try:
        lines = oriext.splitlines()
        if end_line is not None and (start_line > end_line or start_line < 1):
            return "Invalid line range."
        selected_lines = lines[start_line - 1:end_line]
        hex_lines = []
        for line in selected_lines:
            byte_data = line.encode('utf-8')[:numbytes]
            hex_line = ' '.join(format(byte, '02x') for byte in byte_data)
            hex_lines.append(hex_line)
        return '\n'.join(hex_lines)
    except Exception as e:
        return f"{e}"
def base64_text(text, mode='encode'):
    """
    Encode or decode text using Base64.

    Parameters:
    text (str): The text to encode or decode.
    mode (str): The operation mode. 'encode' to encode text to Base64, 
                'decode' to decode Base64 text to original text. 
                Default is 'encode'.

    Returns:
    str: The Base64 encoded string if mode is 'encode', 
         or the decoded text if mode is 'decode'.
    """
    try:
        if mode.lower() == 'encode':
            encoded_bytes = base64.b64encode(text.encode('utf-8'))
            return encoded_bytes.decode('utf-8')
        elif mode.lower() == 'decode':
            decoded_bytes = base64.b64decode(text.encode('utf-8'))
            return decoded_bytes.decode('utf-8')
        else:
            return "Invalid mode. Use 'encode' or 'decode'."
    except Exception as e:
        return f"{e}"
def aes_encry(text, key, iv=None, mode="CBC", encoding="utf-8"):
    """
    Encrypt text using AES encryption.

    Parameters:
    text (str): The text to encrypt.
    key (str): The encryption key (must be 16, 24, or 32 bytes long).
    iv (bytes, optional): The initialization vector for modes like CBC.
                           If not provided, a random IV will be generated.
    mode (str): The AES mode of operation. Default is 'CBC'.
    encoding (str): The encoding of the input text. Default is 'utf-8'.

    Returns:
    str: The Base64-encoded encrypted text.
    """
    try:
        if len(key) not in [16, 24, 32]:
            return "Invalid key length. Key must be 16, 24, or 32 bytes long."
        key = key.encode(encoding)
        if iv is None:
            iv = os.urandom(16)  
        text_bytes = text.encode(encoding)
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        encryptor = cipher.encryptor()
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(text_bytes) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        encrypted_with_iv = iv + encrypted_data
        encrypted_base64 = base64.b64encode(encrypted_with_iv).decode(encoding)

        return encrypted_base64
    except Exception as e:
        return f"{e}"
def aes_decry(encrypted_text, key, encoding='utf-8'):
    """
    Decrypt AES-encrypted text.

    Parameters:
    encrypted_text (str): The Base64-encoded encrypted text.
    key (str): The decryption key (must be 16, 24, or 32 bytes long).
    encoding (str): The encoding of the decrypted text. Default is 'utf-8'.

    Returns:
    str: The decrypted text.
    """
    try:
        if len(key) not in [16, 24, 32]:
            return "Invalid key length. Key must be 16, 24, or 32 bytes long."
        key = key.encode(encoding)
        encrypted_with_iv = base64.b64decode(encrypted_text.encode(encoding))
        iv = encrypted_with_iv[:16]
        encrypted_data = encrypted_with_iv[16:]
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()
        decrypted_text = decrypted_data.decode(encoding)
        return decrypted_text
    except Exception as e:
        return f"{e}"
#end        