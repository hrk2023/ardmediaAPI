import os
import jwt
import datetime
from functools import wraps
from flask import Flask,request,jsonify,make_response
from conStrings import db1
from config import DevelopmentConfig

app=Flask(__name__)
app.config.from_object(DevelopmentConfig())

#------------------DECORATOR------------------------
def token_required(f):
    @wraps(f)
    def token_inner(*args,**kwargs):
        token=request.args.get('token')

        if not token:
            return jsonify({"message":"Token is Missing"})
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'])
        except:
            return jsonify({'message':'Invalid Token'})
        return f(*args,**kwargs)
    return token_inner

#----------------DECORATOR END----------------------

#-----------------GET METHODS-----------------------
@token_required
@app.route('/contact',methods=['GET'])
def contact_get():
    response=db1.contact.find()
    if response is  None:
        return jsonify({"message":"No Data Found"})
    output=[]
    for data in response:
        obj={"firstname":data['firstname'],"lastname":data['lastname'],"email":data['email'],"message":data['message']}
        output.append(obj)
    return jsonify({'result':output})

@token_required
@app.route('/landing',methods=['GET'])
def landing_get():
    response=db1.landing.find()
    if response is None:
        return jsonify({"message":"No Data Found"})
    output=[]
    for data in response:
        obj={"firstname":data['firstname'],"email":data['email']}
        output.append(obj)
    return jsonify({'result':output})

@token_required
@app.route('/subscribe',methods=['GET'])
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

#-----------------------TOKEN GENERATE-----------------------
@app.route('/gen_token')
def gen_token():
    auth=request.authorization
    if auth and auth.username=='adminAdm' and auth.password=='Nydqqzuy1324':
        token=jwt.encode({'user':auth.username, 'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=48)},app.config['SECRET_KEY'])
        return jsonify({'token':token.decode('UTF-8')})
    return make_response("COULD NOT VERIFY!",401,{'WWW-Authenticate':'Basic realm="Login Required"'})

#-----------------------TOKEN GENERATE END-------------------

if __name__=="__main__":
    app.run(debug=True)
