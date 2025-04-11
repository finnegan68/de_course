import os
import shutil


def get_path_to_sales_data(path_from_request : str) -> str:
    path_from_request = path_from_request.replace('/'. '\\')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(os.path.dirname(current_dir))
    sales_data_path = os.path.join(parent_dir,  path_from_request)
    if not os.path.exists(sales_data_path):
        os.makedirs(sales_data_path)
        print(f"Directory '{sales_data_path}' created.")
    else:
        shutil.rmtree(sales_data_path)
        print(f"Cleaned existing directory: {sales_data_path}")
    return sales_data_path