import os
import requests
import datetime as dt
import json

from dotenv import load_dotenv

load_dotenv()

trade_hist_start_iso = dt.datetime.isoformat(dt.datetime.now() - dt.timedelta(days=7))
now_iso = dt.datetime.isoformat(dt.datetime.now())

trade_account_id = os.environ['meta_api_account_id']
trade_auth_token = os.environ['meta_api_auth_token']
base_url = "https://mt-client-api-v1.london.agiliumtrade.ai"
account_info_end_point = f"/users/current/accounts/{trade_account_id}/account-information"
read_positions_end_point = f"/users/current/accounts/{trade_account_id}/positions"
read_deals_end_point = f"/users/current/accounts/{trade_account_id}/history-deals/time/{trade_hist_start_iso}/{now_iso}"


headers = {
    "auth-token": trade_auth_token,
    "Content-Type": "application/json"
}
#
# response = requests.get(headers=headers, url=base_url+read_deals_end_point)





