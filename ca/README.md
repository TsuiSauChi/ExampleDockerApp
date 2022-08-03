# Certificiate Authority Workflow 

The folder are to be run in sequence 1) requstor.py 2) ca.py 3) validator.py 

## Workflow 

### Requestor 
Requestor would send a certificiate signing request (CSR) to the CA for a certificiate 

1) Create a RSA key pair 
2) Create a CSR
3) Create a digital signature using CSR

### CA
Certificiate Authority would validate the CSR and create a certificiate for the requestor 

1) Create a RSA key pair 
2) Get CSR from requestor 
3) Validate digital signature of CSR
4) Create a digital certificiate for the requestor
5) Create a digital signature using certificiate 

### Validator 
Validator would validator the requestor certificiate via the CA 

1) Get digitial certificiate from the requestor 
2) Validate digital signature of certificiate 
3) Check the expiration date of certificiate 


