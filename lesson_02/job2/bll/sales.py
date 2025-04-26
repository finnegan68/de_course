import os
import shutil
import json
from fastavro import writer, parse_schema
from datetime import date as dt_date
from util.util import get_root


def format_path(some_path: str) -> str:
    if some_path[0]=='/':
        some_path = some_path[1:]
    return some_path.replace('/', '\\')


def save_sales_to_avro(raw_dir:str, stg_dir:str) -> None:
    raw_dir = format_path(raw_dir)
    stg_dir = format_path(stg_dir)
    #current_dir = os.path.dirname(os.path.abspath(__file__))
    #root = os.path.dirname(os.path.dirname(current_dir))
    root = get_root()
    sales_data_path = os.path.join(root,  raw_dir)

    if not os.path.exists(sales_data_path):
        print(f'There is not data in {sales_data_path}. Exit program.')
        return
    
    for file in os.listdir(sales_data_path):
        json_to_avro(sales_data_path, file, stg_dir)
        

def json_to_avro(data_path: str, filename: str, to_folder: str) -> None:
    json_file_path = os.path.join(data_path, filename)
    with open(json_file_path, 'r') as f:
        records = json.load(f)
    
    avro_filename = filename.split('.')[0] + '.avro'
    schema = {
        "type": "record",
        "name": avro_filename,
        "fields": [
            {"name": "client", "type": "string"},
            {"name": "purchase_date", "type": "string"},
            {"name": "product", "type": "string"},
            {"name": "price", "type": "float"},
        ]
    }
    parsed_schema = parse_schema(schema)

    if not os.path.exists(to_folder):
        os.makedirs(to_folder)
        print(f"Directory '{to_folder}' created.")
    else:
        shutil.rmtree(to_folder)
        os.makedirs(to_folder)
        print(f"Cleaned existing directory: {to_folder}")
    
    avro_file_path = os.path.join(to_folder,  avro_filename)
    with open(avro_file_path, 'wb') as out:
        writer(out, parsed_schema, records)

    print(f"Successfully converted JSON to Avro: {avro_file_path}")

        
