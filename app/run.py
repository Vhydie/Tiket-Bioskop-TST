# Definition
from flask import Flask, request, render_template, redirect, url_for, flash, session
from __init__ import app,mysql
from db_controller import *
from response import *
from authlib.integrations.flask_client import OAuth

# Initialization for OAuth
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='877655369552-4nrhlafr6h9oe1s8fevdcv00b4hb6naq.apps.googleusercontent.com',
    client_secret='NMd1vfzJ0tl5vrZ___az9dLB',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    acess_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid profile email'}
)



# Main code

# API
# API
# API
# API
# API

# Page untuk memesan tiket
@app.route('/tiketbioskop', methods = ['GET','POST'])
def pesan():
    # mengurus id user
    id_daftar = set_index()

    if request.method == "GET":
        return get_data()
    elif request.method == "POST":
        return post_data(id_daftar)


# Page memasukkan email dan password untuk membuka cart
@app.route('/cart', methods = ['GET','POST'])
def check():
    # Setiap kali mengakses ini, akan dihilangkan data orang yang sedang login
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('password', None)
    if request.method == "POST":
        if acc() is None:
            pass
        else:
            session['password'] = acc()[1]
            return post_acc_api()
    if request.method == "GET":
        return get_acc()


# Page untuk melihat cart yang pernah dipesan oleh seseorang
@app.route('/cart/<email>', methods = ['GET'])
@login_required
def cart(email):
    try:
        if request.method == "GET":
            return get_cart_acc(get_ticket_on_cart(email))
    except Exception:
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 302, "Login Required"))
        mysql.connection.commit()
        return (log_req("", '', "Anda harus login terlebih dahulu"))
        

# Page untuk mengubah data pemesanan
@app.route('/cart/ticket/<id>', methods = ['GET','PUT','DELETE'])
@login_required
def ticket(id):
    try:
        if request.method == "GET":
            return get_ticket(get_ticket_details(id,session['email']))
        elif request.method == "PUT":
            return update_ticket(update_ticket_database(id,session['email']), id)
        elif request.method == "DELETE":
            return del_ticket(del_ticket_database(id,session['email']))
    except Exception:
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 302, "Login Required"))
        mysql.connection.commit()
        return (log_req("", '', "Anda harus login terlebih dahulu"))
        




# FRONT END, bila di call akan return HTML template, bukan API
# FRONT END, bila di call akan return HTML template, bukan API
# FRONT END, bila di call akan return HTML template, bukan API
# FRONT END, bila di call akan return HTML template, bukan API
# FRONT END, bila di call akan return HTML template, bukan API

# Mengakses page untuk memesan tiket, hanya sebagai route tambahan demi keperluan frontend (tidak bisa diakses manual melalui postman, karena return html template)
@app.route('/', methods = ['GET','POST'])
def get_single_pesan():
    # mengurus id user
    id_daftar = set_index()

    if request.method == "GET":
        get_data()
        return render_template ("order.html")
    elif request.method == "POST":
        post_data(id_daftar)
        return render_template ("order.html")


# Mengakses page untuk masukkan email dan pass, hanya sebagai route tambahan demi keperluan frontend (tidak bisa diakses manual melalui postman, karena return html template)
@app.route('/cart/get', methods = ['GET','POST'])
def get_single_check():
    # Setiap kali mengakses ini, akan dihilangkan data orang yang sedang login
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('password', None)
    if request.method == "POST":
        if acc() is None:
            flash(f'Maaf, Akun Anda belum terdaftar! Harap masukkan email dan password yang sesuai.', "info")
            pass
        else:
            google = oauth.create_client('google')
            redirect_uri = url_for('authorize', _external=True)
            session['password'] = acc()[1]
            return google.authorize_redirect(redirect_uri)
    if request.method == "GET":
        get_acc()
    return render_template ("cart.html")


# Untuk OAuth, tidak akan mengembalikan API, namun akan redirect ke HTML lain
@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo', token=token)
    user_info = resp.json()
    session['email'] = user_info['email']
    email = session['email']
    if email is None:
        auth_failed()
    else:
        auth_success()
        post_acc(email)
    return (redirect(url_for('get_single_cart', email = email)))


# Mengakses page untuk melihat isi cart, hanya sebagai route tambahan demi keperluan frontend (tidak bisa diakses manual melalui postman, karena return html template)
@app.route('/cart/get/<email>', methods = ['GET'])
def get_single_cart(email):
    try:
        get_cart_acc(get_ticket_on_cart(email))
        return render_template ("ticket.html", data = get_ticket_on_cart(session['email']), email = session['email'])
    except Exception:
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 302, "Login Required"))
        mysql.connection.commit()
        return (log_req("", '', "Anda harus login terlebih dahulu"))


# Mengakses page untuk melihat detail satu tiket, hanya sebagai route tambahan demi keperluan frontend (tidak bisa diakses manual melalui postman, karena return html template)
@app.route('/cart/get/ticket/<id>')
def get_single_ticket(id):
    try:
        get_ticket(get_ticket_details(id,session['email']))
        return render_template ("singleticket.html", data = get_ticket_details(id,session['email']))
    except Exception:
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 302, "Login Required"))
        mysql.connection.commit()
        return (log_req("", '', "Anda harus login terlebih dahulu"))


# Menghapus tiket, hanya sebagai route tambahan untuk menghapus tiket demi keperluan frontend (tidak bisa diakses manual melalui postman, karena return html template)
@app.route('/cart/delete/ticket/<id>')
def delete_single_ticket(id):
    try:
        del_ticket(del_ticket_database(id,session['email']))
        return redirect(url_for('get_single_cart', email = session['email']))
    except Exception:
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 302, "Login Required"))
        mysql.connection.commit()
        return (log_req("", '', "Anda harus login terlebih dahulu"))


# Mengubah data tiket, hanya sebagai route tambahan untuk mengubah tiket demi keperluan frontend (tidak bisa diakses manual melalui postman, karena return html template)
@app.route('/cart/update/ticket/<id>', methods = ['GET','POST'])
def update_single_ticket(id):
    try:
        if request.method == "POST":
            update_ticket(update_ticket_database(id,session['email']), id)
            return redirect(url_for('get_single_ticket', id = id))
        return render_template ("update.html", email = session['email'], data = get_ticket_details(id,session['email']))
    except Exception:
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 302, "Login Required"))
        mysql.connection.commit()
        return (log_req("", '', "Anda harus login terlebih dahulu"))








# Frontend yang bisa menampilkan API
# Frontend yang bisa menampilkan API
# Frontend yang bisa menampilkan API
# Frontend yang bisa menampilkan API
# Frontend yang bisa menampilkan API
# Frontend yang bisa menampilkan API


# Mengakses page untuk memesan tiket, namun setelah memesan tiket dialihkan ke API untuk mengambil data
@app.route('/api', methods = ['GET','POST'])
def get_api_single_pesan():
    # mengurus id user
    id_daftar = set_index()

    if request.method == "GET":
        get_data()
        return render_template ("order_api.html")
    elif request.method == "POST":
        post_data(id_daftar)
        return get_data()


# Mengakses page untuk masukkan email dan pass, hanya sebagai route tambahan demi keperluan frontend (tidak bisa diakses manual melalui postman, karena return html template)
@app.route('/api/cart/get', methods = ['GET','POST'])
def get_api_single_check():
    # Setiap kali mengakses ini, akan dihilangkan data orang yang sedang login
    session.pop('loggedin', None)
    session.pop('email', None)
    session.pop('password', None)
    if request.method == "POST":
        if acc() is None:
            flash(f'Maaf, Akun Anda belum terdaftar! Harap masukkan email dan password yang sesuai.', "info")
            pass
        else:
            google = oauth.create_client('google')
            redirect_uri = url_for('authorize_api', _external=True)
            session['password'] = acc()[1]
            return google.authorize_redirect(redirect_uri)
    if request.method == "GET":
        get_acc()
    return render_template ("cart_api.html")


# Untuk OAuth, tidak akan mengembalikan API, namun akan redirect ke HTML lain
@app.route('/authorize_api')
def authorize_api():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo', token=token)
    user_info = resp.json()
    session['email'] = user_info['email']
    email = session['email']
    if email is None:
        auth_failed()
    else:
        auth_success()
        post_acc(email)
    return (redirect(url_for('get_api_single_cart', email = email)))


# Mengakses page untuk melihat isi cart, hanya sebagai route tambahan demi keperluan frontend (tidak bisa diakses manual melalui postman, karena return html template)
@app.route('/api/cart/get/<email>', methods = ['GET'])
def get_api_single_cart(email):
    try:
        get_cart_acc(get_ticket_on_cart(email))
        return render_template ("ticket_api.html", data = get_ticket_on_cart(session['email']), email = session['email'])
    except Exception:
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 302, "Login Required"))
        mysql.connection.commit()
        return (log_req("", '', "Anda harus login terlebih dahulu"))


# Mengakses page untuk melihat detail satu tiket, hanya sebagai route tambahan demi keperluan frontend (tidak bisa diakses manual melalui postman, karena return html template)
@app.route('/api/cart/get/ticket/<id>')
def get_api_single_ticket(id):
    try:
        get_ticket(get_ticket_details(id,session['email']))
        return render_template ("singleticket_api.html", data = get_ticket_details(id,session['email']))
    except Exception:
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 302, "Login Required"))
        mysql.connection.commit()
        return (log_req("", '', "Anda harus login terlebih dahulu"))


# Menghapus tiket, hanya sebagai route tambahan untuk menghapus tiket demi keperluan frontend (tidak bisa diakses manual melalui postman, karena return html template)
@app.route('/api/cart/delete/ticket/<id>')
def delete_api_single_ticket(id):
    try:
        return del_ticket(del_ticket_database(id,session['email']))
    except Exception:
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 302, "Login Required"))
        mysql.connection.commit()
        return (log_req("", '', "Anda harus login terlebih dahulu"))


# Mengubah data tiket, hanya sebagai route tambahan untuk mengubah tiket demi keperluan frontend (tidak bisa diakses manual melalui postman, karena return html template)
@app.route('/api/cart/update/ticket/<id>', methods = ['GET','POST'])
def update_api_single_ticket(id):
    try:
        if request.method == "POST":
            return update_ticket(update_ticket_database(id,session['email']), id)
        return render_template ("update_api.html", email = session['email'], data = get_ticket_details(id,session['email']))
    except Exception:
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 302, "Login Required"))
        mysql.connection.commit()
        return (log_req("", '', "Anda harus login terlebih dahulu"))






# Untuk menjalankan program
# RUNNER
# RUNNER
# RUNNER
# RUNNER
# RUNNER
if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5000)