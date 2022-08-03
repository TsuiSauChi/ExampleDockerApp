from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa 
from cryptography import x509 
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

### STEP 1: Generate the private key; What about the public key?
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = key.public_key()

# Write private key to localhost
with open("./requestor/private.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format = serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase")
    ))

# Write public key to localhost
with open("./requestor/public.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1
    ))

### STEP 2: Create Signing Request
builder = x509.CertificateSigningRequestBuilder()
builder = builder.subject_name(x509.Name([
    # Provide various details about who we are for CA to validate
    # What other information is included here?
    # CA info; CA digital signature
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Example"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"example.com"),
]))

csr = builder.sign(
    key, hashes.SHA256()
)

with open("./requestor/csr.pem", "wb") as f:
    f.write(csr.public_bytes(serialization.Encoding.PEM))

### STEP 3: Signing the CSR
signature = key.sign(
    csr.public_bytes(encoding=serialization.Encoding.PEM),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

with open("./requestor/signature.txt", "wb") as f:
    f.write(signature)


# Questions 
# Need to encyrpt CSR with CA private key