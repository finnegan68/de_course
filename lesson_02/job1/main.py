"""
This file contains the controller that accepts command via HTTP
and trigger business logic layer
"""
from flask import Flask, request
from flask import typing as flask_typing
from job1.bll.sales_api import save_sales_to_local_disk
from dotenv import load_dotenv
import os


load_dotenv()
AUTH_TOKEN = os.environ.get("API_AUTH_TOKEN")

if not AUTH_TOKEN:
    print("AUTH_TOKEN environment variable must be set")


app = Flask(__name__)


@app.route('/', methods=['POST'])
def main() -> flask_typing.ResponseReturnValue:
    '''
    Send POST request this type
    localhost:8081?date=2022-08-10&raw_dir=/file_storage/raw/sales/2022-08-10
    '''
    date = request.args.get('date')
    raw_dir = request.args.get('raw_dir')

    if not date or not raw_dir:
        return {
            "message": "date or raw_dir param missed",
        }, 400

    save_sales_to_local_disk(date=date, raw_dir=raw_dir)

    return {
               "message": "Data retrieved successfully from API",
           }, 201


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8081)
