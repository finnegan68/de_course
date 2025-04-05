from job1.dal import local_disk, sales_api
import os
import json
import shutil


def save_sales_to_local_disk(date: str, raw_dir: str) -> None:

    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    file_storage_dir = os.path.join(parent_dir,  'file_storage')
    if not os.path.exists(file_storage_dir):
        os.makedirs(file_storage_dir)
        print(f"Directory '{file_storage_dir}' created.")
    else:
        shutil.rmtree(file_storage_dir)
        print(f"Directory '{file_storage_dir}' has been cleaned.")
    
    sales = sales_api.get_sales(date)

    sales_data_path = file_storage_dir
    for folder in raw_dir.split('/'):
        sales_data_path += folder + '\\'
   
    os.makedirs(sales_data_path)
    filename = f"sales_{date}.json"
    with open(os.path.join(sales_data_path, filename), 'w') as f:
        json.dump(sales, f)
