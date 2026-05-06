import os
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

KEYS_DIR = 'instance/keys'

def generate_keys():
    """Generate RSA public/private key pair and save to disk if they don't exist."""
    os.makedirs(KEYS_DIR, exist_ok=True)
    private_key_path = os.path.join(KEYS_DIR, 'private.pem')
    public_key_path = os.path.join(KEYS_DIR, 'public.pem')
    
    if not os.path.exists(private_key_path) or not os.path.exists(public_key_path):
        key = RSA.generate(2048)
        private_key = key.export_key()
        with open(private_key_path, 'wb') as f:
            f.write(private_key)
            
        public_key = key.publickey().export_key()
        with open(public_key_path, 'wb') as f:
            f.write(public_key)
            
def get_public_key():
    """Load the public key from disk."""
    generate_keys() # Ensure keys exist
    public_key_path = os.path.join(KEYS_DIR, 'public.pem')
    with open(public_key_path, 'rb') as f:
        return RSA.import_key(f.read())
        
def get_private_key():
    """Load the private key from disk."""
    generate_keys() # Ensure keys exist
    private_key_path = os.path.join(KEYS_DIR, 'private.pem')
    with open(private_key_path, 'rb') as f:
        return RSA.import_key(f.read())

def encrypt_hash(hash_text):
    """Encrypts a hash string (or any string) using the public key."""
    public_key = get_public_key()
    cipher_rsa = PKCS1_OAEP.new(public_key)
    # The string must be converted to bytes before encryption
    encrypted_bytes = cipher_rsa.encrypt(hash_text.encode('utf-8'))
    return encrypted_bytes

def decrypt_hash(encrypted_bytes):
    """Decrypts bytes back to original hash string using the private key."""
    private_key = get_private_key()
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_bytes = cipher_rsa.decrypt(encrypted_bytes)
    return decrypted_bytes.decode('utf-8')
