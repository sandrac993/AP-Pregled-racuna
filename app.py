from flask import Flask, render_template, request, session
import flask_bootstrap
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)
flask_bootstrap.Bootstrap(app)

# Configure DB
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)
# app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.secret_key = 'sandra123456'

@app.route('/')
def index():
    #prikazivanje početne stranice
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if session.get('username') is None:
            cur = mysql.connection.cursor()
            username = request.form.get('username')
            password = request.form.get('password')
            if cur.execute("SELECT * from korisnik where username = %s and password = %s", [username, password]) > 0:
                user = cur.fetchone()
                session['login'] = True
                session['username'] = user[6]
                session['firstName'] = user[4]
                session['lastName'] = user[5]
                mysql.connection.commit()
                cur.execute("UPDATE korisnik SET active = 1 WHERE username = %s ", [username])
                mysql.connection.commit()
                # fetch all
                result_value = cur.execute("SELECT * from racuni")
                if result_value > 0:
                    racuni = cur.fetchall()
                    return render_template("index.html", racuni=racuni)
                return render_template("index.html")
            else:
                flask.flash('Pogresan username ili password!', 'danger')
                return render_template('login.html')
        else:
            cur = mysql.connection.cursor()
            result_value = cur.execute("SELECT * from racuni")
            if result_value > 0:
                racuni = cur.fetchall()
                return render_template("index.html", racuni=racuni)
            return render_template("index.html")
    else:
        if session.get('username') is not None:
            cur = mysql.connection.cursor()
            result_value = cur.execute("SELECT * from racuni")
            if result_value > 0:
                racuni = cur.fetchall()
                return render_template("racuni.html", racuni=racuni)
        else:
            return render_template("login.html")
    return render_template("login.html")




@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        username = request.form.get('username')
        password = request.form.get('password')
        Ime = request.form.get('Ime')
        Prezime = request.form.get('Prezime')
        email = request.form.get('email')
        password_confirm = request.form.get('passwordConfirm')
        if password == password_confirm:
            if (cur.execute("SELECT * from korisnik where username = %s", [username]) == 0) and len(username) >= 5:
                if cur.execute("SELECT * from korisnik where email = %s", [email]) == 0:
                    cur.execute("INSERT INTO korisnik(Ime,Prezime,email,password,username) VALUES (%s,%s,%s,%s,%s)",
                                [Ime, Prezime, email, password, username])
                    mysql.connection.commit()
                    cur.close()
                    flask.flash('Uspjesno ste se registrovali! Logujte se koristeci vas username i password.', 'success')
                    return redirect(url_for('index'))
                else:
                    flask.flash('Email adresa zauzeta!', 'danger')
                    return render_template("registration.html")
            else:
                flask.flash('Username postoji!', 'danger')
                return render_template("registration.html")
        else:
            flask.flash('Password nepoznat!')
            return render_template("registration.html")
    return render_template("registration.html")


@app.route('/logout/')
def logout():
    if session.get('username') is not None:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE korisnik SET active = 0 WHERE username = %s ", [session['username']])
        mysql.connection.commit()
        session.pop('username')
        return render_template('index.html')
    else:
        return render_template('index.html')

@app.route('/invoices')
def invoices(id):
    if session.get('username') is None:
        return render_template("index.html")
    else:
        cur = mysql.connection.cursor()
        result_value = cur.execute("SELECT * from racuni WHERE idbroj_racuna = %s ", [id])
        if result_value > 0:
            b = cur.fetchone()
            return render_template("invoices.html", invoice=invoice)
        return render_template("index.html")


@app.route('/add_invoice', methods=['GET', 'POST'])
def add_invoice():
    if request.method == 'POST':
        cur = mysql.connection.cursor()
        broj_racuna = request.form.get('broj racuna')
        datum_izdavanja = request.form.get('datum izdavanja')
        zaduzeno_lice= session.get('Ime') + ' ' + session.get('Prezime')
        status = request.form.get('status')
        cur.execute("INSERT INTO racuni (broj racuna,datum izdavanja,zaduzeno_lice,status) VALUES (%s,%s,%s,%s)",
                    [broj_racuna, datum_izdavanja, zaduzeno_lice, status])
        mysql.connection.commit()
        cur.close()
        flask.flash('Racun je uspjesno dodan!', 'success')
        return redirect(url_for('invoices'))
    else:
        return render_template("add_invoice.html")



@app.route('/print_invoice/<int:invoice_id>')
def print_invoice(broj_racuna):
    return render_template('print_invoice.html', invoice=invoice)

if __name__ == '__main__':
    app.run(debug=True)
