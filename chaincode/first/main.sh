export PATH=${PWD}/../../bin:$PATH
export FABRIC_CFG_PATH=$PWD/../../config/

peer lifecycle chaincode package first.tar.gz --path ./ --lang node --label first_2.0