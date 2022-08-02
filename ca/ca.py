from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
import datetime

# Step 1: Generate the private key; What about the public key?
key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

public_key = key.public_key()

# Write private key to localhost
with open("./ca/private.pem", "wb") as f:
    f.write(key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format = serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase")
    ))

# Write public key to localhost
with open("./ca/public.pem", "wb") as f:
    f.write(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.PKCS1
    ))

f = open("./requestor/csr.pem", "rb").read()
csr = x509.load_pem_x509_csr(f)

# Get subject from CSR
requestor = {}
for i in csr.subject:
    requestor[str(i.oid._name)] = i.value
print(requestor)

builder = x509.CertificateBuilder()
builder = builder.subject_name(x509.Name([
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, requestor["organizationName"]),
    x509.NameAttribute(NameOID.ORGANIZATION_NAME, requestor["commonName"]),
]))

# Set Issuers Name
builder = builder.issuer_name(x509.Name([
    x509.NameAttribute(NameOID.COMMON_NAME, u'exampleCA'),
]))
# Set Serial Number
builder = builder.serial_number(x509.random_serial_number())
# Set expiry date to tmr
builder = builder.not_valid_before(datetime.datetime.today() - datetime.timedelta(1, 0, 0))
builder = builder.not_valid_after(datetime.datetime.today() + datetime.timedelta(1, 0, 0))
# Insert public key
builder = builder.public_key(public_key)

# Sign CSR with private key and hash
certificate = builder.sign(
    private_key=key, algorithm=hashes.SHA256(),
)

with open("./ca/ca.pem", "wb") as f:
    f.write(certificate.public_bytes(serialization.Encoding.PEM))
