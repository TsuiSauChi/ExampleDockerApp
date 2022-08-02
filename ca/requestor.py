from distutils.command.build import build
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa 
from cryptography import x509 
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
import datetime

# Step 1: Generate the private key; What about the public key?
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

print("Private Key", key)
public_key = key.public_key()
print("Public Key", public_key)

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

# Step 2: Create Signing Request
builder = x509.CertificateSigningRequestBuilder()
builder = builder.subject_name(x509.Name([
    # Provide various details about who we are for CA to validate
    # What other information is included here?
    # CA info; CA digital signature
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"Example"),
    x509.NameAttribute(NameOID.COMMON_NAME, u"example.com"),
]))

request = builder.sign(
    key, hashes.SHA256()
)

with open("./requestor/csr.pem", "wb") as f:
    f.write(request.public_bytes(serialization.Encoding.PEM))
