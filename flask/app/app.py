import os
import json

from flask import Flask, render_template, request
from web3 import Web3
from solc import compile_standard, install_solc
from decimal import Decimal
from pprint import pprint

install_solc('v0.4.25')
os.environ['SOLC_BINARY'] = "/root/.py-solc/solc-v0.4.25/bin/solc"

app = Flask(__name__)

provider = Web3(Web3.WebsocketProvider('ws://geth:8546'))
provider.eth.defaultAccount = provider.eth.accounts[0]

v1_contracts = v2_contracts = []
v1_flag = "flag{defcoin_only_goes_up}"
v2_flag = "flag{r/WallStreetBets}"

v1_contracts = ["0x93BEEae74c1cee23d048AfF83BFADeBD49Da1762"]

def get_solc(filename):
    with open(f'static/solc/{filename}', 'r') as FILE:
        return FILE.read()

@app.route('/')
def home():
    return render_template('pages/index.html', v1_solc=get_solc("v1.sol"), v2_solc=get_solc("v2.sol"))

@app.route('/v1_deploy')
def v1_deploy():
    #return "0x93BEEae74c1cee23d048AfF83BFADeBD49Da1762"

    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "v1.sol": {
                "content": get_solc("v1.sol")
            }
        },
        "settings":
            {
                "outputSelection": {
                    "*": {
                        "*": [
                            "metadata", "evm.bytecode"
                            , "evm.bytecode.sourceMap"
                        ]
                    }
                }
            }
        })


    bytecode = compiled_sol['contracts']['v1.sol']['DynamicStretching']['evm']['bytecode']['object']
    abi = json.loads(compiled_sol['contracts']['v1.sol']['DynamicStretching']['metadata'])['output']['abi']

    v1 = provider.eth.contract(abi=abi, bytecode=bytecode)

    valueInWei = provider.toWei(Decimal('.001'), 'ether')

    tx_hash = v1.constructor().transact({'from': provider.eth.defaultAccount, 'value': valueInWei})
    print("Waiting for tx.....")
    tx_receipt = provider.eth.waitForTransactionReceipt(tx_hash)
    print(f"Done Deploying! - {tx_receipt['contractAddress']}")
    v2_contracts.append(tx_receipt['contractAddress'])

    return tx_receipt['contractAddress']

@app.route('/v2_deploy')
def v2_deploy():
    compiled_sol = compile_standard({
        "language": "Solidity",
        "sources": {
            "v2.sol": {
                "content": get_solc("v2.sol")
            }
        },
        "settings":
            {
                "outputSelection": {
                    "*": {
                        "*": [
                            "metadata", "evm.bytecode"
                            , "evm.bytecode.sourceMap"
                        ]
                    }
                }
            }
        })


    bytecode = compiled_sol['contracts']['v2.sol']['OneShotOneKill']['evm']['bytecode']['object']
    abi = json.loads(compiled_sol['contracts']['v2.sol']['OneShotOneKill']['metadata'])['output']['abi']

    v2 = provider.eth.contract(abi=abi, bytecode=bytecode)

    valueInWei = provider.toWei(Decimal('.001'), 'ether')

    tx_hash = v2.constructor().transact({'from': provider.eth.defaultAccount, 'value': valueInWei})
    print("Waiting for tx.....")
    tx_receipt = provider.eth.waitForTransactionReceipt(tx_hash)
    print(f"Done Deploying! - {tx_receipt['contractAddress']}")
    v2_contracts.append(tx_receipt['contractAddress'])

    return tx_receipt['contractAddress']

@app.route('/validate/<contract_address>')
def validate(contract_address):
    if not provider.isAddress(contract_address):
        return "Not a valid address!"

    elif contract_address in v1_contracts:
        balance = float(provider.fromWei(provider.eth.getBalance(contract_address), 'ether'))
        if balance == 0:
            return v1_flag
        else:
            return f"The contract at {contract_address} still has a balance of {balance}ETH"
        
    elif contract_address in v2_contracts:
        balance = float(provider.fromWei(provider.eth.getBalance(contract_address), 'ether'))
        if balance == 0:
            return v2_flag
        else:
            return f"The contract at {contract_address} still has a balance of {balance}ETH"

    return "Address not generated by this application!"

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', debug=False, port=port, use_reloader=True, threaded=True)
