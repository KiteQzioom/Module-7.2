import requests
import csv
import json
from flask import Flask
from flask import request, redirect
from flask import render_template

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
data_dict = data[0]
rates = data_dict.get('rates')
keys=rates[0].keys()

codes = []
for data in rates:
    codes.append(data.get('code'))
print(codes)

with open('output.csv', 'w', newline='', encoding="utf-8") as a_file:
    dict_writer = csv.DictWriter(a_file, keys, delimiter=';')
    dict_writer.writeheader()
    dict_writer.writerows(rates)
    a_file.close()

@app.route("/calculator", methods=['GET', "POST"])
def calculate():
    if request.method == 'GET':
        print("We received GET")
        return render_template("/calculator.html", codes=codes)
    elif request.method == 'POST':
        data=request.form
        currency = request.form['code']
        amount = int(data.get('amount'))
        x=0
        for data in rates:
            if data.get('code') == currency:
                rate = data.get('ask')
                break
        print("rate", rate)
        result = round(rate * amount,2)
        result = str(result)
        print("We received POST")
        return render_template('/calculator.html', result=result, codes=codes)
