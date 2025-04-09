from flask import Flask, request
from flask import typing as flask_typing
from job2.bll.sales import save_sales_to_avro
import os


app = Flask(__name__)

@app.route('/', methods=['POST'])
def main() -> flask_typing.ResponseReturnValue:
    '''
    Send POST request this type
    localhost:8081?raw_dir=/raw/sales/2022-08-10&stg_dir=/stg/sales/2022-08-10
    '''
    stg_dir = request.args.get('stg_dir')
    raw_dir = request.args.get('raw_dir')

    if not stg_dir or not raw_dir:
        return {
            "message": "raw or stg param missed",
        }, 400

    save_sales_to_avro(raw_dir=raw_dir, stg_dir=stg_dir)

    return {
               "message": "Data saved to Avro format successfully",
           }, 201


if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8082)
