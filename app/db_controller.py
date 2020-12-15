# Definition and Initialization
from flask import request, session, flash
from flask_mysqldb import MySQL
from __init__ import mysql
from response import *
from functools import wraps




# PEMESANAN
# PEMESANAN
# PEMESANAN
# PEMESANAN
# PEMESANAN

# Mengatur index yang akan dimasukkan dalam database
def set_index():
    # Mengambil index saat ini
    curid = mysql.connection.cursor()
    curid.execute("SELECT MAX(idpesanan) FROM pemesanan")
    currentid = curid.fetchone()

    # Menambahkan 1 pada indeks
    if currentid[0] is None:
        maxid = 0
    else: 
        maxid = int((str(currentid[0])))
    iddaftar = maxid + 1
    mysql.connection.commit()
    curid.close()

    return(iddaftar)


# Melihat data hasil POST di database
def post_data(iddaftar):
    try:
        # Mengambil data yang telah diisi
        details = request.form
        DataNama = details['name']
        Dataemail= details['email']
        Datapassword = details['password']
        DataKota = details['kota']
        DataBioskop = details['bioskop']
        DataLetak = details['letak']
        DataFilm = details['film']
        DataTgl = details['tgl']
        DataJam = details['jam']
        DataPosisi = details['posisi']

        # Memasukkan data dalam database
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO pemesanan(idpesanan,nama_pemesan,email,password,kota,nama_bioskop,letak,nama_film,tanggal,jam,tempat_duduk,status) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (iddaftar, DataNama, Dataemail, Datapassword, DataKota, DataBioskop, DataLetak, DataFilm, DataTgl, DataJam, DataPosisi, 0))
        mysql.connection.commit()

        # Mengeluarkan API sukses
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("POST", 200, "OK"))
        mysql.connection.commit()
        flash(f'Tiket berhasil dipesan!', "info")
        return (ok("POST", '', "Data pemesanan dengan id " + str(iddaftar) + " berhasil disimpan!"))

    except Exception:
        # Bila ada kesalahan saat menginput data, akan mengeluarkan API kegagalan
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("POST", 400, "Bad Request"))
        mysql.connection.commit()
        flash(f'Maaf, ada kesalahan saat memesan buku. Harap lengkapi semua data atau ganti posisi tempat duduk karena telah ditempati!', "info")
        return (bad("POST", '', "Tidak berhasil memesan!"))


# Mengubah satu record data menjadi sebuah API
def single_transform(data):
    api_single_data = {
        'idpesanan' : data[0],
        'nama_pesanan' : data[1],
        'status' : data[2]
    }
    return api_single_data


# Mengubah semua hasil fetching data menjadi API yang utuh
def transform(data):
    array = []
    for i in data:
        array.append(single_transform(i))
    return array


# Melihat seluruh data pemesanan tiket
def get_data():
    try:
        # Mengambil semua data yang dibutuhkan dari database
        cur = mysql.connection.cursor()
        cur.execute("SELECT idpesanan,nama_pemesan,status FROM pemesanan")
        data = cur.fetchall()
        data_api = transform(data)
        mysql.connection.commit()
        cur.close()

        # Mengirimkan API
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 200, "OK"))
        mysql.connection.commit()
        if (data_api == []):
            return (ok("GET", data_api, "Tidak ada data pesanan yang ada dalam database!"))
        else:
            return (ok("GET", data_api, "Berikut adalah data pesanan yang ada dalam database!"))
    except Exception:
        # Bila ada kesalahan saat mengambil data, akan mengeluarkan API kegagalan
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 400, "Bad Request"))
        mysql.connection.commit()
        return (bad("GET", '', "Tidak berhasil mengambil data!"))




# CART
# CART
# CART
# CART
# CART

# Mengubah satu record data pesanan menjadi sebuah API
def single_transform_cart(data):
    api_single_data = {
        'nama_pesanan' : data[0],
        'kota' : data[1],
        'nama_bioskop' : data[2],
        'letak' : data[3],
        'nama_film' : data[4],
        'tanggal' : str(data[5]),
        'jam' : str(data[6]),
        'tempat_duduk' : data[7],
        'status' : data[8],
        'idpesanan' : data[9]
    }
    return api_single_data


# Mengubah semua hasil fetching data menjadi API yang utuh
def transform_cart(data):
    array = []
    for i in data:
        array.append(single_transform_cart(i))
    return array

# Mengubah satu record data pesanan menjadi sebuah API
def single_transform_all_cart(data):
    api_single_data = {
        'nama_pesanan' : data[0],
        'nama_film' : data[4],
        'tanggal' : str(data[5]),
        'tempat_duduk' : data[7],
        'status' : data[8],
        'idpesanan' : data[9]
    }
    return api_single_data


# Mengubah semua hasil fetching data menjadi API yang utuh
def transform_all_cart(data):
    array = []
    for i in data:
        array.append(single_transform_all_cart(i))
    return array


# Mengambil data masukan email dan password
def acc():
    # Mengambil masukan user
    details = request.form
    Dataemail= details['email']
    Datapassword = details['password']

    # Mengambil data dari database untuk dicocokkan
    cur = mysql.connection.cursor()
    cur.execute("SELECT email,password FROM pemesanan WHERE email = %s AND password = %s", (Dataemail, Datapassword))
    data = cur.fetchone()

    mysql.connection.commit()
    cur.close()
    return data


# Melihat seluruh data pemesanan tiket
def get_acc():
    try:
        # Mengirimkan API
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 200, "OK"))
        mysql.connection.commit()
        return (ok("GET", "", "Anda dapat login ke akun Anda! Silahkan masukkan email dan password Anda yang telah terdaftar dalam Google"))
    except Exception:
        # Bila ada kesalahan saat mengambil data, akan mengeluarkan API kegagalan
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 400, "Bad Request"))
        mysql.connection.commit()
        return (bad("GET", '', "Anda tidak dapat login karena halaman tidak tersedia!"))


# Melihat apakah email dan password telah sesuai
def post_acc(email):
    try:
        # Mengambil data
        data = [email,session['password']]

        # Melihat apakah masukan sesuai atau tidak
        # Bila tidak dimasukkan, akan error
        done = mysql.connection.cursor()
        if data is None and email is None:
            # Setiap belum di authorize, dia akan terhitung sebagai bad request, namun akan berhasil bila pada log ada "AUTH 200 - OK"
            done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("POST", 400, "Bad Request"))
            mysql.connection.commit()
            return (bad("POST","", "Masukan email dan password Anda salah!"))
        else:
            done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("POST", 200, "OK"))
            mysql.connection.commit()
            return (ok("POST", "", "Anda dapat melihat isi Cart Anda!"))
    except Exception:
        # Bila ada kesalahan saat menginput data, akan mengeluarkan API kegagalan
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("POST", 400, "Bad Request"))
        mysql.connection.commit()
        return (bad("POST", '', "Tidak berhasil melihat tiket!"))


# Melihat apakah email dan password telah sesuai
def post_acc_api():
    try:
        # Mengambil data
        data = acc()
        session['email'] = data[0]
        
        # Melihat apakah masukan sesuai atau tidak
        done = mysql.connection.cursor()
        if data is None:
            done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("POST", 400, "Bad Request"))
            mysql.connection.commit()
            return (bad("POST","", "Masukan email dan password Anda salah!"))
        else:
            done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("POST", 200, "OK"))
            mysql.connection.commit()
            return (ok("POST", "", "Pastikan Anda telah memasukkan token yang benar dan tidak expired. Jika sudah, segala isi cart akan terbuka. Namun, jika belum, Anda tidak bisa melihat isi cart!"))
    except Exception:
        # Bila ada kesalahan saat menginput data, akan mengeluarkan API kegagalan
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("POST", 400, "Bad Request"))
        mysql.connection.commit()
        return (bad("POST", '', "Tidak berhasil melihat tiket!"))



# Melihat isi cart dari suatu akun
def get_cart_acc(data):
    try:
        # Mengubah data
        data_api = transform_all_cart(data)

        # Mengirimkan API
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 200, "OK"))
        mysql.connection.commit()
        if data_api == []:
            return (ok("GET", data_api, "Anda tidak dapat melihat isi cart ini!"))
        else:
            return (ok("GET", data_api, "Berikut adalah data pesanan Anda!"))
    except Exception:
        # Bila ada kesalahan saat mengambil data, akan mengeluarkan API kegagalan
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 400, "Bad Request"))
        mysql.connection.commit()
        return (bad("GET", '', "Tidak berhasil mengambil data!"))



# Mengambil data tiket dalam satu akun dari mamsukan melalui frontend dan API
def get_ticket_on_cart(email):
    if email == session['email']:
        pass
    else:
        email = None
    cur = mysql.connection.cursor()
    cur.execute("SELECT nama_pemesan,kota,nama_bioskop,letak,nama_film,tanggal,jam,tempat_duduk,status,idpesanan FROM pemesanan WHERE email = %s AND password = %s", (email,session['password']))
    data = cur.fetchall()
    mysql.connection.commit()
    cur.close()
    return data


# Mengambil email pemesan tiket
def get_email(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT email FROM pemesanan WHERE idpesanan = %s AND password = %s", (id,session['password']))
    data = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return data


# Melihat tiket pesanan
def get_ticket(data):
    try:
        # Mengambil data
        data_api = single_transform_cart(data)

        # Mengirimkan API
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 200, "OK"))
        mysql.connection.commit()
        if data_api is None:
            return (ok("GET", data_api, "Tidak ada tiket"))
        else:
            return (ok("GET", data_api, "Berikut adalah data tiket pesanan Anda!"))
    except Exception:
        # Bila ada kesalahan saat mengambil data, akan mengeluarkan API kegagalan
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 400, "Bad Request"))
        mysql.connection.commit()
        return (bad("GET", '', "Tidak berhasil mengambil data!"))


# Mengambil data satu tiket saja
def get_ticket_details(id,email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT nama_pemesan,kota,nama_bioskop,letak,nama_film,tanggal,jam,tempat_duduk,status,idpesanan FROM pemesanan WHERE idpesanan = %s AND email = %s AND password = %s", (id, email, session['password']))
    data = cur.fetchone()
    mysql.connection.commit()
    cur.close()
    return data


# Mengubah data suatu tiket pesanan
def update_ticket(data,id):
    try:
        # Mengeluarkan API sukses
        done = mysql.connection.cursor()
        if data is None:
            done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("PUT", 400, "Bad Request"))
            mysql.connection.commit()
            flash(f'Maaf, ada kesalahan saat mengubah data tiket. Harap lengkapi semua data atau ubah posisi tempat duduk karena bisa saja telah ditempati.', "info")
            return (bad("PUT", '', "Tidak berhasil mengubah data tiket!"))
        else:
            done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("PUT", 200, "OK"))
            mysql.connection.commit()
            flash(f'Data tiket berhasil diubah, lihat perubahannya!', "info")
            return (ok("PUT",'', "Data tiket dengan id " + str(id) + " berhasil diubah!"))
    except Exception:
        # Bila ada kesalahan saat mengubah data, akan mengeluarkan API kegagalan
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("PUT", 400, "Bad Request"))
        mysql.connection.commit()
        flash(f'Maaf, ada kesalahan saat mengubah data tiket. Harap lengkapi semua data atau ubah posisi tempat duduk karena bisa saja telah ditempati.', "info")
        return (bad("PUT", '', "Tidak berhasil mengubah data tiket!"))


# Memasukkan data dalam database dari frontend
def update_ticket_database(id,email):
    try:
        # Mengambil data yang telah diisi
        details = request.form
        DataNama = details['name']
        DataKota = details['kota']
        DataBioskop = details['bioskop']
        DataLetak = details['letak']
        DataFilm = details['film']
        DataTgl = details['tgl']
        DataJam = details['jam']
        DataPosisi = details['posisi']
        
        # Mengubah isi data
        cur = mysql.connection.cursor()
        cur.execute("UPDATE pemesanan SET nama_pemesan = %s, kota = %s, nama_bioskop = %s, letak = %s, nama_film = %s, tanggal = %s, jam = %s, tempat_duduk = %s WHERE idpesanan = %s AND email = %s AND password = %s", (DataNama, DataKota, DataBioskop, DataLetak, DataFilm, DataTgl, DataJam, DataPosisi, id, email, session['password']))
        cur.execute("SELECT * FROM pemesanan WHERE nama_pemesan = %s AND kota = %s AND nama_bioskop = %s AND letak = %s AND nama_film = %s AND tanggal = %s AND jam = %s AND tempat_duduk = %s AND idpesanan = %s AND email = %s AND password = %s", (DataNama, DataKota, DataBioskop, DataLetak, DataFilm, DataTgl, DataJam, DataPosisi, id, email, session['password']))
        data = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        return data
    except Exception:
        return None


# Menghapus pemesanan tiket dari suatu akun
def del_ticket(data):
    try:
        # Mengeluarkan API sukses
        done = mysql.connection.cursor()
        if data is None:
            done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("DELETE", 400, "Bad Request"))
            mysql.connection.commit()
            flash(f'Maaf, ada kesalahan yang membuat tiket tidak berhasil dihapus. Mohon coba kembali.', "info")
            return (bad("DELETE", '', "Tidak berhasil menghapus tiket!"))
        else:
            done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("DELETE", 200, "OK"))
            mysql.connection.commit()
            flash(f'Tiket berhasil dihapus.', "info")
            return (ok("DELETE", "", "Tiket Berhasil Dihapus!"))
    except Exception:
        # Bila ada kesalahan saat menghapus data, akan mengeluarkan API kegagalan
        done = mysql.connection.cursor()
        done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("DELETE", 400, "Bad Request"))
        mysql.connection.commit()
        flash(f'Maaf, ada kesalahan yang membuat tiket tidak berhasil dihapus. Mohon coba kembali.', "info")
        return (bad("DELETE", '', "Tidak berhasil menghapus tiket!"))


# Menghapus data tiket jika request dari frontend
def del_ticket_database(id,email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM pemesanan WHERE idpesanan = %s AND email = %s AND password = %s", (id, email, session['password']))
    data = cur.fetchone()
    cur.execute("DELETE FROM pemesanan WHERE idpesanan = %s AND email = %s AND password = %s", (id, email, session['password']))
    mysql.connection.commit()
    cur.close()
    return data





# Authorization
# Authorization
# Authorization
# Authorization
# Authorization

# Success
def auth_success():
    done = mysql.connection.cursor()
    done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("AUTH", 200, "OK"))
    mysql.connection.commit()
    return (ok("AUTH", '', "Authorization Success!"))

# Success
def auth_failed():
    done = mysql.connection.cursor()
    done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("AUTH", 400, "Bad Request"))
    mysql.connection.commit()
    return (bad("AUTH", '', "Authorization Failed!"))


# Mewajibkan Login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        headers = request.headers
        token = headers.get('Authorization')

        if token:
            return f(*args, **kwargs)
        else:
            user = dict(session).get('profile', None)
            if user:
                return f(*args, **kwargs)
            done = mysql.connection.cursor()
            done.execute("INSERT INTO log(log_method,status,message) VALUES (%s,%s,%s)", ("GET", 302, "Login Required"))
            mysql.connection.commit()
            return (log_req("", '', "Anda harus login terlebih dahulu"))
    return decorated_function