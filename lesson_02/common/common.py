import os
import shutil
import json


def get_path_to_sales_data(path_from_request : str) -> str:
    '''
    If path start with backslash we need to remove backslash
    Because it will get absolute path 
    And save our data to root of disc
    '''
    if path_from_request[0]=='/':
        path_from_request = path_from_request[1:]
    path_from_request = path_from_request.replace('/', '\\')
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(current_dir)
    sales_data_path = os.path.join(root,  path_from_request)
    if not os.path.exists(sales_data_path):
        os.makedirs(sales_data_path)
        print(f"Directory '{sales_data_path}' created.")
    else:
        shutil.rmtree(sales_data_path)
        print(f"Cleaned existing directory: {sales_data_path}")
    return sales_data_path

    