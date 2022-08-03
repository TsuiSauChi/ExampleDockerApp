from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import padding

### STEP 1: Get Certificiate
# Load Certificiate
f = open("./ca/cert.pem", "rb").read()
cert = x509.load_pem_x509_certificate(f)

### STEP 2: Vet Signature
# Load Requestor public key
with open("./ca/public.pem", "rb") as key_file:
    ca_public_key = serialization.load_pem_public_key(
        key_file.read()
    )

# Load Signature 
cert_signature = open("./ca/signature.txt", "rb").read()

# Vet Signature; with public key, csr, and signature
try:
    ca_public_key.verify(
        cert_signature,
        cert.public_bytes(encoding=serialization.Encoding.PEM),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

### STEP 3: Check Expiration Date
    print(cert.not_valid_after)
    print(cert.not_valid_before)
except:
    print("Invalid Signature")