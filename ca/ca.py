from cryptography import x509
from cryptography.hazmat.primitives.asymmetric import rsa 
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import padding
import datetime

# STEP 1: Generate the private key; What about the public key?
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

### STEP 2: Get CSR
# Load CSR
f = open("./requestor/csr.pem", "rb").read()
csr = x509.load_pem_x509_csr(f)

### STEP 3: Vet Signature
# Load Requestor public key
with open("./requestor/public.pem", "rb") as key_file:
    requestor_public_key = serialization.load_pem_public_key(
        key_file.read()
    )

# Load Signature 
csr_signature = open("./requestor/signature.txt", "rb").read()

# Vet Signature; with public key, csr, and signature
try:
    requestor_public_key.verify(
        csr_signature,
        csr.public_bytes(encoding=serialization.Encoding.PEM),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

### STEP 4: Create Signature
    # Get subject from CSR
    requestor = {}
    for i in csr.subject:
        requestor[str(i.oid._name)] = i.value

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

    with open("./ca/cert.pem", "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))

### STEP 5: Signing the Certificiate
    signature = key.sign(
        certificate.public_bytes(encoding=serialization.Encoding.PEM),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH           
        ),
        hashes.SHA256()
    )
    with open("./ca/signature.txt", "wb") as f:
        f.write(signature)
except:
    print("Invalid Signature")

