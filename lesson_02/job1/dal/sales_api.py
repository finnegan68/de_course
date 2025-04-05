from typing import List, Dict, Any
from dotenv import load_dotenv
import os
import requests


API_URL = 'https://fake-api-vycpfa6oca-uc.a.run.app/'

load_dotenv()
AUTH_TOKEN = os.environ.get("API_AUTH_TOKEN")

def get_sales(date: str) -> List[Dict[str, Any]]:
    """
    Get data from sales API for specified date.

    :param date: data retrieve the data from
    :return: list of records
    """
    all_sales = []
    page = 1
    headers = {'Authorization': AUTH_TOKEN,
            "Content-Type": "application/json"}

    while True:
        try:
            response = requests.get(
                API_URL + '/sales',
                params={'date': date, 'page': page},
                headers = headers
            )
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                print(f"Page {page} does not exist or you already got all data. Exiting.")
            else:
                print(f"HTTP error occurred: {e}")
            break
            
        try:
            data = response.json()
        except ValueError as e:
            print(f"Error parsing JSON: {e}")
            break  
            
        all_sales.extend(data)
        page += 1

    print(all_sales)
    return all_sales
