from algosdk.v2client.algod import AlgodClient
from algosdk.abi import ABIType
from base64 import b64decode

node_token = ''
node_server = 'https://mainnet-api.4160.nodely.dev'

algod_client = AlgodClient(node_token, node_server)

rug_ninja_app_id = 2020762574

token_holding_box_schema = ABIType.from_string('(address,uint64)')

# Token to check holdings for
target_token_id = 2639168320

application_boxes = algod_client.application_boxes(rug_ninja_app_id)['boxes']

total_holders = 0

for box in application_boxes:
    
    decoded_box_name = b64decode(box['name'])

    if len(decoded_box_name) == 40:
        decoded_box_content = token_holding_box_schema.decode(decoded_box_name)
        
        address = decoded_box_content[0]
        token_id = decoded_box_content[1]

        if decoded_box_content[1] == target_token_id:

            tokens_held = int.from_bytes(
                b64decode(algod_client.application_box_by_name(rug_ninja_app_id, decoded_box_name)['value']),
                'big'
            )

            #If a box exists they are at least holding 1 token, otherwise the box autodeletes 
            total_holders += 1
            
            print(f'Tokens Held by {address[:6]}... : {tokens_held:,.0f}')
