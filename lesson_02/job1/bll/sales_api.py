from common.common import get_path_to_sales_data
from job1.dal import local_disk, sales_api
import os
import json
import shutil


def save_sales_to_local_disk(date: str, raw_dir: str) -> None:
   sales_data_path = get_path_to_sales_data(raw_dir)
    sales = sales_api.get_sales(date)
    filename = f"sales_{date}.json"
    with open(os.path.join(sales_data_path, filename), 'w') as f:
        json.dump(sales, f)

