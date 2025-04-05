from typing import List, Dict, Any
import os
import requests
from dotenv import load_dotenv


API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app/'

env_path = os.path.join(os.path.dirname(__file__), '..', '..', '.env')
load_dotenv(env_path)
token = os.getenv("AUTH_TOKEN")


def get_sales(date: str) -> List[Dict[str, Any]]:
    """
    Get data from sales API for specified date.

    :param date: data retrieve the data from
    :return: list of records
    """
    all_sales = []
    page = 1
    headers = {'Authorization': token}
    while True:
        response = requests.get(
            API_URL + '/sales',
            params={'date': date, 'page': page},
            headers = headers
        )
        if not response:
            break  
            
        data = response.json()
        all_sales.extend(data)
        page += 1

    return all_sales
