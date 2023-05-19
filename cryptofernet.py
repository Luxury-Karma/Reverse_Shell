import cryptography.exceptions
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet


def create_key():
    # Generates a key
    __key = Fernet.generate_key()
    return __key


def encrypt_str(__n_key: bytes, __s_msg: str):
    __n_encoded_msg = __s_msg.encode()
    # initialize the Fernet class
    __fernet = Fernet(__n_key)
    # encrypt the message
    return __fernet.encrypt(__n_encoded_msg)


def decrypt_str(__n_key: bytes, __n_encoded_msg: bytes):
    try:
        # initialize the Fernet class
        __fernet = Fernet(__n_key)
        return __fernet.decrypt(__n_encoded_msg)
    except cryptography.fernet.InvalidToken:
        return set_error(-10, 'Invalid key', 'String can not be decrypt : Invalid key')

