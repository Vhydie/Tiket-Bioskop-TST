from flask import jsonify, make_response

def ok(method,values,message):
    res = {
        'method' : method,
        'status' : 200,
        'desc' : "OK",
        'values' : values,
        'messages' : message
    }
    return make_response(jsonify(res))

def bad(method,values,message):
    res = {
        'method' : method,
        'status' : 400,
        'desc' : "Bad Request",
        'values' : values,
        'messages' : message
    }
    return make_response(jsonify(res))

def log_req(method,values,message):
    res = {
        'method' : method,
        'status' : 302,
        'desc' : "Login Required",
        'values' : values,
        'messages' : message
    }
    return make_response(jsonify(res))