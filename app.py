import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn, wait_for_confirmation

addr1 = "G7Q33VB3446YK7GDFJI4ZME3VEIMHGZEUEMEBKKDZWZBQ4D5PFPTUTZDEI"
passphrase1 = "blade fiber rookie indicate brick spin ethics orange field omit wasp expose square dinosaur candy vehicle muffin this mosquito sort echo edge test above wall"
private_key1 = mnemonic.to_private_key(passphrase1)

addr2 = "ZXCKOQR4IB7VSSHYUYXL2FUEHZTCSOO23VWKISNLQF6N6CRRWHZIUEVCJE"
passphrase2 = "beyond whip neck jewel process walnut garage icon today cat pass dizzy plunge soft police surround negative audit rhythm cat inquiry van noble about horn"
private_key2 = mnemonic.to_private_key(passphrase2)

addr3 = "K6ESGQLWQM3DAKMEJB76PSILRS5Z33UFZJ66RDEJCCCH2JL4HKNC3KBDYE"
passphrase3 = "draft once theory arrest price syrup spy flight high moon say maid leave drink then observe trick afford extra symptom matrix moral memory abandon code"
private_key3 = mnemonic.to_private_key(passphrase3)

asset_id=148928435

algod_client = algod.AlgodClient('','https://testnet-api.algonode.cloud')


# account_info = algod_client.account_info(addr)
# print("Account balance: {} microAlgos".format(account_info.get('amount')) + "\n")

def assetCreation():
    # CREATE ASSET
    params = algod_client.suggested_params()

    txn = AssetConfigTxn(
        sender=addr1,
        sp=params,
        total=10000,
        default_frozen=False,
        unit_name="MMT",
        asset_name="Machine Money Token",
        manager=addr1,
        reserve=addr1,
        freeze=addr1,
        clawback=addr1,
        url="https://path/to/my/asset/details", 
        decimals=0
    )
    # Sign with secret key of creator
    stxn = txn.sign(private_key1)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))   
    except Exception as err:
        print(err)
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
    # print("Decoded note: {}".format(base64.b64decode(
    #     confirmed_txn["txn"]["txn"]["note"]).decode()))
    try:
        ptx = algod_client.pending_transaction_info(txid)
        asset_id = ptx["asset-index"]
        print("Asset ID: ",asset_id)
    except Exception as e:
        print(e)


def modifyAsset():

    params = algod_client.suggested_params()
    txn = AssetConfigTxn(
        sender=addr1,
        sp=params,
        index=asset_id, 
        manager=addr2,
        reserve=addr1,
        freeze=addr1,
        clawback=addr1
    )
    # sign by the current manager - Account 2
    stxn = txn.sign(private_key1)

    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))   
    except Exception as err:
        print(err)


def receiveAsset():
    params = algod_client.suggested_params()
    txn = AssetTransferTxn(
        sender=addr3,
        sp=params,
        receiver=addr3,
        amt=0,
        index=asset_id
    )
    stxn = txn.sign(private_key3)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))    
    except Exception as err:
        print(err)


def transferAsset():
    # TRANSFER ASSET
    # transfer asset of 10 from account 1 to account 3
    params = algod_client.suggested_params()
    # comment these two lines if you want to use suggested params
    # params.fee = 1000
    # params.flat_fee = True
    txn = AssetTransferTxn(
        sender=addr2,
        sp=params,
        receiver=addr1,
        amt=5,
        index=asset_id
    )
    stxn = txn.sign(private_key2)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))
    except Exception as err:
        print(err)


def assetFreeze():
    # FREEZE ASSET
    params = algod_client.suggested_params()
    txn = AssetFreezeTxn(
        sender=addr1,
        sp=params,
        index=asset_id,
        target=addr3,
        new_freeze_state=True   
    )
    stxn = txn.sign(private_key1)

    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))    
    except Exception as err:
        print(err)

def assetRevoke():
    # REVOKE ASSET
    params = algod_client.suggested_params()
    txn = AssetTransferTxn(
        sender=addr1,
        sp=params,
        receiver=addr1,
        amt=5,
        index=asset_id,
        revocation_target=addr2
    )
    stxn = txn.sign(private_key1)
    # Send the transaction to the network and retrieve the txid.
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))      
    except Exception as err:
        print(err)


def assetDestroy():
    params = algod_client.suggested_params()
    txn = AssetConfigTxn(
        sender=addr2,
        sp=params,
        index=asset_id,
        strict_empty_address_check=False
    )
    # Sign with secret key of creator
    stxn = txn.sign(private_key2)
    try:
        txid = algod_client.send_transaction(stxn)
        print("Signed transaction with txID: {}".format(txid))
        # Wait for the transaction to be confirmed
        confirmed_txn = wait_for_confirmation(algod_client, txid, 4) 
        print("TXID: ", txid)
        print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))     
    except Exception as err:
        print(err)

