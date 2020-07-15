import os
import jwt
import secrets
import datetime
from passlib.hash import pbkdf2_sha256
from functools import wraps
from flask import Flask,request,jsonify,make_response
from conStrings import db1
from config import DevelopmentConfig

app=Flask(__name__)
app.config.from_object(DevelopmentConfig())

#------------------DECORATOR------------------------
def apiKey_required(f):
    @wraps(f)
    def apiKey_inner(*args,**kwargs):
        apiKey=request.args.get('api_key')
        if not apiKey:
            return jsonify({"message":"Api Key is Missing"}),403
        response=db1.apiKey.find_one({"api_key":apiKey})
        if response:
            return f(*args,**kwargs)
        else:
            return jsonify({"message":"Invalid API KEY"}),403
    return apiKey_inner

#----------------DECORATOR END----------------------

#-----------------GET METHODS-----------------------

@app.route('/contact',methods=['GET'])
@apiKey_required
def contact_get():
    response=db1.contact.find()
    if response is  None:
        return jsonify({"message":"No Data Found"}),200
    output=[]
    for data in response:
        obj={"firstname":data['firstname'],"lastname":data['lastname'],"email":data['email'],"message":data['message']}
        output.append(obj)
    return jsonify({'result':output}),200


@app.route('/landing',methods=['GET'])
@apiKey_required
def landing_get():
    response=db1.landing.find()
    if response is None:
        return jsonify({"message":"No Data Found"})
    output=[]
    for data in response:
        obj={"firstname":data['firstname'],"email":data['email']}
        output.append(obj)
    return jsonify({'result':output})


@app.route('/subscribe',methods=['GET'])
@apiKey_required
def subscribe_get():
    response=db1.subscribe.find()
    if response is None:
        return jsonify({"message":"No Data Found"})
    output=[]
    for data in response:
        obj={"email":data['email']}
        output.append(obj)
    return jsonify({'result':output})
#-----------------------GET METHODS END----------------------

#-----------------------POST METHODS-------------------------
@app.route('/contact',methods=['POST'])
@apiKey_required
def contact_post():
    try:
        arg=request.get_json()
    except:
        return jsonify({"message":"Invalid Request"})
    output=[]
    obj={"firstname":arg['firstname'],"lastname":arg['lastname'],"email":arg['email'],"message":arg['message']}
    send_status=db1.contact.insert_one(obj)
    if send_status:
        return jsonify({'message':"Success"})
    return jsonify({"message":"Failure"})

@app.route('/landing',methods=['POST'])
@apiKey_required
def landing_post():
    try:
        arg=request.get_json()
    except:
        return jsonify({"message":"Invalid Request"})
    output=[]
    obj={"firstname":arg['firstname'],"email":arg['email']}
    send_status=db1.landing.insert_one(obj)
    if send_status:
        return jsonify({'message':"Success"})
    return jsonify({"message":"Failure"})

@app.route('/subscribe',methods=['POST'])
@apiKey_required
def subscribe_post():
    try:
        arg=request.get_json()
    except:
        return jsonify({"message":"Invalid Request"})
    output=[]
    obj={"email":arg['email']}
    send_status=db1.subscribe.insert_one(obj)
    if send_status:
        return jsonify({'message':"Success"})
    return jsonify({"message":"Failure"})
#-----------------------POST METHODS END---------------------

#-----------------------DELETE METHODS-----------------------

@app.route('/landing/<string:firstname>',methods=['DELETE'])
@apiKey_required
def landing_del_one():
    res = db1.landing.find('firstname')
    if res is None:
        return jsonify({"message":"No Data Found"})
    status = db1.landing.remove(res[0])
    if status:
        return jsonify({"message":"Success"})
    return jsonify({"message":"Failure"})


@app.route('/landing',methods=['DELETE'])
@apiKey_required
def landing_del():
    res=db1.landing.find()
    if res is None:
        return jsonify({"message":"No Data Found"})
    status = db1.landing.remove()
    if status:
        return jsonify({"message":"Success"})
    return jsonify({"message":"Failure"})


@app.route('/contact',methods=['DELETE'])
@apiKey_required
def contact_del():
    res=db1.contact.find()
    if res is None:
        return jsonify({"message":"No Data Found"})
    status = db1.contact.remove()
    if status:
        return jsonify({"message":"Success"})
    return jsonify({"message":"Failure"})


@app.route('/contact/<string:firstname>',methods=['DELETE'])
@apiKey_required
def contact_del_one():
    res=db1.contact.find('firstname')
    if res is None:
        return jsonify({"message":"No Data Found"})
    status = db1.contact.remove(res[0])
    if status:
        return jsonify({"message":"Success"})
    return jsonify({"message":"Failure"})


@app.route('/subscribe/<string:email>',methods=['DELETE'])
@apiKey_required
def subscribe_del_one():
    res=db1.subscribe.find('email')
    if res is None:
        return jsonify({"message":"No Data Found"})
    status = db1.subscribe.remove(res[0])
    if status:
        return jsonify({"message":"Success"})
    return jsonify({"message":"Failure"})


@app.route('/subscribe',methods=['DELETE'])
@apiKey_required
def subscribe_del():
    res=db1.subscribe.find()
    if res is None:
        return jsonify({"message":"No Data Found"})
    status = db1.subscribe.remove()
    if status:
        return jsonify({"message":"Success"})
    return jsonify({"message":"Failure"})

#--------------------DELETE METHODS END---------------------

#-----------------------API KEY GENERATE-----------------------
@app.route('/gen_token')
def gen_token():
    auth=request.authorization
    if auth:
        username=db1.apiAuth.find_one({"username":auth.username})
        if pbkdf2_sha256.verify(auth.password,username['password']):
            key = secrets.token_hex()
            res=db1.apiKey.insert({"api_key":key})
            if res:
                return jsonify({'api_key':key}),200
            else:
                return jsonify({"message":"Internal Server Error"}),500
    return make_response("COULD NOT VERIFY!",401,{'WWW-Authenticate':'Basic realm="Login Required"'})
#---------------------API KEY GENERATE END---------------------

@app.route('/user/esc/priv/to/admin',methods=['POST'])
def add_user():
    res=request.json
    password=res["password"]
    hsh=pbkdf2_sha256.hash(password)
    res2=db1.apiAuth.insert({"username":res['username'],"password":hsh})
    if res2:
        return jsonify({'message':"new user insertion successful"}),200
    else:
        return jsonify({'message':"new user insertion failed"}),500



if __name__=="__main__":
    app.run(debug=True)
