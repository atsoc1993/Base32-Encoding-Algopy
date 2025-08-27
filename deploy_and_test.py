from contract_files.client import SenderToUtf8Factory
from algosdk.account import address_from_private_key
from algokit_utils import AlgorandClient, SigningAccount, CommonAppCallParams, AlgoAmount
from dotenv import load_dotenv, set_key
import os

algorand = AlgorandClient.testnet()
load_dotenv('.env')
sk = os.getenv('test_account_1')
pk = address_from_private_key(sk)
print(pk)
signing_account = SigningAccount(
    private_key=sk,
    address=pk,
)


factory = SenderToUtf8Factory(
    algorand=algorand,
    default_sender=signing_account.address,
    default_signer=signing_account.signer,
)

client, txn_response = factory.send.create.bare()

txn_response = client.send.base32_sender_address(
    params=CommonAppCallParams(
        max_fee=AlgoAmount(algo=0.01)
    ),
    send_params={
        'cover_app_call_inner_transaction_fees': True
    }
        
    
)
print(txn_response.tx_id)