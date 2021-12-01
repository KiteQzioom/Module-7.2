import requests
import csv
from flask import Flask
from flask import request, redirect
from flask import render_template

app = Flask(__name__)

response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
data = response.json()
data_dict = data[0]
rates = data_dict.get('rates')
keys=rates[0].keys()

with open('output.csv', 'w', newline='', encoding="utf-8") as a_file:
    dict_writer = csv.DictWriter(a_file, keys, delimiter=';')
    print("1")
    dict_writer.writeheader()
    print("2")
    dict_writer.writerows(rates)
    a_file.close()

@app.route("/calculator", methods=['GET', "POST"])
def calculate():
    if request.method == 'GET':
        print("We received GET")
        return render_template("/calculator.html")
    elif request.method == 'POST':
        currency = request.form["currency"]
        currency = str(currency)
        x=0
        while currency != rates[x]["code"]:
            x=x+1
            return x
        rate = rates[x]["bid"]
        print("rate", rate)
        amount = request.form["amount"]
        amount = float(amount)
        result = round(rate * amount,2)
        result = str(result)
        print("We received POST")
        return render_template('/calculator.html', result=result)


        
