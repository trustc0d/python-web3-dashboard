# Ethereum Block Explorer

## About:  
The objective of this web application is to fetch input which might be block number, block hash and transaction hash.For that objective 
and I have opted to use Flask is a micro web framework written in Python. It is classified as a microframework because it does not require particular tools or libraries.
For the frontend I have opted for Bootstrap which contains HTML, CSS and JavaScript-based design templates for typography, forms, buttons, navigation, and other interface components.
Also added button to connect web3 dapps wallet such as Metamask,Trustwallet,etc.

## Requirements and Description:

Needed python to be installed in your machine,After python installed please check it is installed or not with help of cli based on you OS.

```
python --version 
```

After that you its better creater virtaul environment ,virtualenv is a tool to create isolated Python environments
This tool is provided by python (3.3+):
```
python -m venv choose_any_environment_name
```

Activation
Use one of the provided shell scripts to activate and deactivate the environment. This example assumes bash is used.

```
source choose_any_environment_name/bin/activate
```

After we needed to install Flask

```
pip install Flask
```

Now our next task is to install  Web3.py  which is a Python library for interacting with Ethereum.

```
pip install web3
```

After all this installation we are ready to build this block explorer ,the reason behind flask becuase of it's lightweight we can build application 
to start our development journey , in virtual env we will create two directory which are templates ,also we will create our app.py by writing in cli

```
touch app.py
```

```
mkdir templates 
```
```
mkdir static
```

## CODE DOCUMENTATION

```


@app.route("/tx/<string:hash>")
def get_transaction_data(hash):
    """_summary_  
    In this our major focus has been on fetching transaction data with the given hash,if the transaction 
    hash present in ethereum ledger then we will get attribute dictionary ,otherwise it will throw error.
    Thus transaction hash we try to fetch may exists or may not , for that purpose we have to handle exception 
    handling.Agenda for this function to get dictionary so that we render in our desire page with the help of 
    Jinja template.

    Args:
        hash (string):  _description_
        The function need following arguement which should be 'string' type. 
        

    Returns:
        Our desired need is to get pass variables as arguments to render_template() to 
        use that variables in a template file such as result.html.
        In our following variable input_data which hold the attribute dictionary ,we have to 
        convert into dictionary format,for that purpose I have used web3.toJSON for that purpose 
        which will return type of JSON format, now json library needed for parsing json string 
        and convert it into a python dictionary,thus I need to modified keys name for more understandable format 
        and information which are relevant for the render_template() copied relevant data.
        
        If it will throw error with the help of render_template we just pass information such that its that request not 
        found please try again later
         
    """ 
    
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
    """_summary_
     In this our major focus has been on fetching block information with the given block number or block hash,for that block
     number is integer data type and it will contain all numbers such as (0-9) and block hash is string data type.For the given 
     block number or block hash present in ethereum ledger then we will get attribute dictionary ,otherwise it will throw error.
    Thus block number or block hash we try to fetch may exists or may not , for that purpose we have to handle exception 
    handling.Agenda for this function to get dictionary so that we render in our desire page with the help of 
    Jinja template.

    Args:
        data (string): _description_
        The function need following arguement which should be string. 
        

    Returns:
        Our desired need is to get pass variables as arguments to render_template() to 
        use that variables in a template file such as result.html.
        
        In our following data arguement we first check its all numeric or alphanumeric ,if its numeric then we will 
        convert numeric into integer data type ,otherwise we use default argument for string data type,
        In variable input_data which hold the attribute dictionary ,we have to 
        convert into dictionary format,for that purpose I have used web3.toJSON for that purpose 
        which will return type of JSON format, now json library needed for parsing json string 
        and convert it into a python dictionary,thus I need to modified keys name for more understandable format 
        and information which are relevant for the render_template() copied relevant data.
        
        If it will throw error with the help of render_template we just pass information such that its that request not 
        found please try again later
    """
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
    """_summary_
    The objective of the this fetch the form through post method get our input field and type of option field.
    As get_block_data() function may fetch any detail which either will be block number of block hash and 
    As get_transaction_data() function may fetch any detail which will be Transaction hash  
    for that purpose in option we have block number or block transaction hash as "0" and other option that is 
    transaction hash as "1". Now after figuring out , I redirect the function based on selection option. 

    """
    if request.method =='POST':
        type_of_data = request.form.get('type_of_data')
        block_data = request.form.get('block')
        
        if type_of_data=="1":
            return redirect(url_for('get_transaction_data',hash=block_data))
        else:
            return redirect(url_for('get_block_data',data=block_data))

    return render_template('index.html')
    

#Do not use below lines in production 
if __name__=="__main__":
    app.run(debug=True)

```

## To Do List:

1. Fetching input field with help of metamask provider
2. Making UI better
3. Improving Readme.md
## 

## WHY IT HAVE USED:
1. I am open to learn new thing but implement with limited understanding of web3 library and python made it to development of these project 
2. With Ongoing Learning of Javascript and MERN stack may convert these into more interactive and best functional  use web3.js which through made web3.py has been developed.
3. As metamask uses infura for there process , I have choice to choose remote node such as infure,alchemy,etc in this project they are my links you may get your too by signing them
4. Sometime remote node does while fetching data might give request not found ,In upcoming commit these bugs will be solved 

## Open to hear feedbacks and any bugs found on that.
 

