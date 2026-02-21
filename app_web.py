from flask import Flask, render_template, request, redirect, session
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'kunci_rahasia_untuk_login'

# --- SETTING DATABASE ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'perpustakaan.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# ==========================================
# 1. ROUTE PUBLIK (HALAMAN UTAMA)
# ==========================================
@app.route('/')
def halaman_publik():
    conn = get_db_connection()
    buku_list = conn.execute('SELECT * FROM buku').fetchall()
    conn.close()
    return render_template('index.html', buku=buku_list)

# ==========================================
# 2. ROUTE LOGIN ADMIN
# ==========================================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('logged_in'):
        return redirect('/admin')
        
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'admin':
            session['logged_in'] = True
            return redirect('/admin')
        else:
            return render_template('login.html', error="Username atau Password salah!")
            
    return render_template('login.html')

# ==========================================
# 3. ROUTE DASHBOARD ADMIN
# ==========================================
@app.route('/admin', methods=['GET', 'POST'])
def dashboard_admin():
    if not session.get('logged_in'):
        return redirect('/login')
        
    conn = get_db_connection()
    
    if request.method == 'POST':
        kode = request.form['kode_buku']
        judul = request.form['judul_buku']
        pengarang = request.form['pengarang']
        
        conn.execute('INSERT INTO buku (kode_buku, judul_buku, pengarang) VALUES (?, ?, ?)', 
                     (kode, judul, pengarang))
        conn.commit()
        return redirect('/admin')

    buku_list = conn.execute('SELECT * FROM buku').fetchall()
    conn.close()
    
    return render_template('buku.html', buku=buku_list)

# ==========================================
# 4. ROUTE LOGOUT
# ==========================================
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)