from flask import Flask, request, render_template, session, url_for, redirect
from flask_mysqldb import MySQL
import secrets

app = Flask(__name__)
secret = secrets.token_urlsafe(32)
app.secret_key = secret

app.config['MYSQL_USER'] = 'uhUuFFGoce'
app.config['MYSQL_PASSWORD'] = 'SFf0Ovd4Xf'
app.config['MYSQL_DB'] = 'uhUuFFGoce'
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['DEBUG'] = True

mysql = MySQL(app)