import hashlib

def verify_document_hash(uploaded_file, stored_hash):
    """
    Computes the SHA-256 hash of an uploaded file and compares it with the stored hash.
    
    Args:
        uploaded_file: The file object uploaded by the user.
        stored_hash: The original SHA-256 hash stored in the database.
        
    Returns:
        bool: True if hashes match (document verified), False otherwise (tampered).
    """
    sha256_hash = hashlib.sha256()
    
    # Read in chunks to avoid memory issues with large files
    for chunk in iter(lambda: uploaded_file.read(4096), b""):
        sha256_hash.update(chunk)
        
    # Reset file pointer to beginning after reading for hash
    uploaded_file.seek(0)
    
    computed_hash = sha256_hash.hexdigest()
    return computed_hash == stored_hash
