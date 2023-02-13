import json 
from flask import Flask,render_template,request,redirect,url_for
from web3 import Web3
from datetime import datetime

app = Flask(__name__)
aclhemy = "https://eth-mainnet.g.alchemy.com/v2/LhYIWAbhI0NfNR229czelwvmrI_oGXxS" 
infura = "https://mainnet.infura.io/v3/fb861132fe8b44ee9c75d6ab4d239e9d"
w3= Web3(Web3.HTTPProvider(infura))
data={}
data2={}

@app.route("/tx/<string:hash>")
def get_transaction_data(hash):
    try:
        input_data = Web3.toJSON(w3.eth.get_transaction(hash))
        input_data = json.loads(input_data)
        data["Transaction Hash"] = input_data["blockHash"]
        data["Block Height"] = input_data["blockNumber"]
        data["Nonce"] = input_data["nonce"]
        data["From"]=input_data["from"]
        data["To"]=input_data["to"]
        data["Value"]= str(float(w3.fromWei(input_data["value"],'ether'))) + " " + "ETH"
        data["Gas"] = input_data["gas"]
        
        data["Gas Price"] = str(float(w3.fromWei(input_data["gasPrice"],'gwei'))) + " " + "Gwei" 
        
        
        
     
        return render_template("result.html",result=data)
    except:
        return render_template("error.html")
    
@app.route("/block/<string:data>")
def get_block_data(data):
    try:
        if data.isnumeric():
            x=int(data)
            input_data = Web3.toJSON(w3.eth.get_block(x,full_transactions=False))
        else:
            input_data = Web3.toJSON(w3.eth.get_block(data,full_transactions=False))
    
        input_data = json.loads(input_data)
        data2["Block Hash"] = input_data["hash"]
        data2["Block Number"] = input_data["number"]
        data2["Nonce"] = input_data["nonce"]
        data2["Timestamp"] = str(datetime.fromtimestamp(input_data["timestamp"])) + " " + "UTC"
        data2["Transactions"] = len(input_data["transactions"])
        data2["Difficulty"] = input_data["difficulty"]
        data2["Total Difficulty"] = input_data["totalDifficulty"]
        data2["Gas Limit"] = input_data["gasLimit"]
        data2["Gas Used"] = input_data["gasUsed"]
        data2["Miner"] = input_data["miner"]
        data2["Parent Hash"] = input_data["parentHash"]
        data2["Receipts Root"] = input_data["receiptsRoot"]
        data2["State Root"] = input_data["stateRoot"]
        data2["SHA3 Uncles"] = input_data["sha3Uncles"]
        data2["Transaction Root"] = input_data["transactionsRoot"]
        data2["Size"] = input_data["size"]
        return render_template("result.html",result=data2)
    except:
        return render_template("error.html")


  
@app.route("/",methods=['GET','POST'])
def index():
    if request.method =='POST':
        type_of_data = request.form.get('type_of_data')
        block_data = request.form.get('block')
        
        if type_of_data=="1":
            return redirect(url_for('get_transaction_data',hash=block_data))
        else:
            return redirect(url_for('get_block_data',data=block_data))

    return render_template('index.html')
    


if __name__=="__main__":
    app.run(debug=True)


    
    


