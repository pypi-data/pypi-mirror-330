from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv('API_KEY')
rpc_url = os.getenv('RPC_URL')
private_key = os.getenv('PRIVATE_KEY')
multi_sig_address = os.getenv('MULTI_SIG_ADDRESS')