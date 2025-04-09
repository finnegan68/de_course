import os
import json
from fastavro import writer, parse_schema
from datetime import date as dt_date


def save_sales_to_avro(raw_dir:str, stg_dir:str) -> None:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(os.path.dirname(current_dir))
    file_storage_dir = os.path.join(parent_dir,  'file_storage')

    sales_data_path = file_storage_dir
    for folder in raw_dir.split('/'):
        sales_data_path += folder + '\\'

    if not os.path.exists(sales_data_path):
        print(f'There is not data in {sales_data_path}. Exit program.')
        return
    
    for file in os.listdir(sales_data_path):
        json_path = os.path.join(sales_data_path, file)
        json_to_avro(json_path, stg_dir)
        


def json_to_avro(json_file_path: str, to_folder: str) -> None:
    with open(json_file_path, 'r') as f:
        records = json.load(f)
    filename = json_file_path.split('\\')[-1]

    schema = {
        "type": "record",
        "name": filename,
        "fields": [
            {"name": "client", "type": "string"},
            {"name": "purchase_date", "type": "string"},
            {"name": "product", "type": "string"},
            {"name": "price", "type": "float"},
        ]
    }

    parsed_schema = parse_schema(schema)

    # Generate Avro file path
    date = to_folder.split('/')[-1]
    avro_filename = f"sales_{date}.avro"
    avro_file_path = os.path.join(to_folder,  avro_filename).replace('/', '\\')
    
    avro_file_path = json_file_path.split('file_storage')[0] + 'file_storage' + avro_file_path
    print(avro_file_path)

    os.makedirs(os.path.dirname(avro_file_path), exist_ok=True)
    with open(avro_file_path, 'wb') as out:
        writer(out, parsed_schema, records)

    print(f"Successfully converted JSON to Avro: {avro_file_path}")

        
