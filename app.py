from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
app= Flask(__name__)
#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '9334178140'
app.config['MYSQL_DB'] = 'BLOOD_VE'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MySQL
mysql = MySQL(app)
#Articles = Articles()
@app.route('/')
def index():
    return render_template('home.html')
@app.route('/about/')
def about():
    return render_template('about.html')
@app.route('/articles/')
def articles():
    cur =mysql.connection.cursor()
    #Get Aricle
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result>0:
        return render_template('articles.html', articles=articles)
    else:
        msg= 'No article found'
        return render_template('articles.html',msg =msg)
    #close conection
    cur.close()
@app.route('/article/<string:id>/')
def article(id):
    cur =mysql.connection.cursor()
    #Get Aricle
    result = cur.execute("SELECT * FROM articles WHERE id = %s", [id])
    article = cur.fetchone()
    return render_template('article.html',article = article)
class RegisterForm(Form):
    NAME = StringField('Name', [validators.Length(min=1, max=50)])
    USERNAME =StringField('Username', [validators.Length(min=4, max=30)])
    EMAIL =StringField('Email', [validators.Length(min=6, max=50)])
    PASSWORD =PasswordField('Password', [
    validators.DataRequired(),validators.EqualTo('confirm',message='Password do not match')
    ])
    confirm = PasswordField('Confirm Password')
    BLOOD_GROUP =StringField('BLOOD_GROUP', [validators.Length(min=2, max=4)])
    EMAIL =StringField('Email', [validators.Length(min=6, max=50)])
    PHONE_NUMBER =StringField('PHONE_NUMBER', [validators.Length(min=10, max=50)])
    ADDRESS =StringField('ADDRESS', [validators.Length(min=2, max=200)])
@app.route('/register/', methods=['GET', 'post'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        NAME = form.NAME.data
        USERNAME = form.USERNAME.data
        PASSWORD = form.PASSWORD.data
        PASSWORD = sha256_crypt.encrypt(str(form.PASSWORD.data))
        EMAIL = form.EMAIL.data
        BLOOD_GROUP = form.BLOOD_GROUP.data
        PHONE_NUMBER = form.PHONE_NUMBER.data
        ADDRESS = form.ADDRESS.data

        #Create DictCursor
        cur = mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO users(NAME, USERNAME, PASSWORD, EMAIL, BLOOD_GROUP, PHONE_NUMBER, ADDRESS) VALUES(%s, %s, %s, %s, %s, %s, %s)", (NAME, USERNAME, PASSWORD, EMAIL, BLOOD_GROUP, PHONE_NUMBER, ADDRESS))
        # commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash('You are now registere and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Get Form FIelds
        USERNAME = request.form['USERNAME']
        PASSWORD_CANDIDATE = request.form['PASSWORD']
        #Create DictCursor
        cur = mysql.connection.cursor()
        result = cur.execute("SELECT * FROM users WHERE USERNAME = %s",[USERNAME])
        if result > 0:
            data = cur.fetchone()
            PASSWORD = data['PASSWORD']
            if sha256_crypt.verify(PASSWORD_CANDIDATE, PASSWORD):
                session['logged_in'] = True
                session['USERNAME'] = USERNAME
                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                app.logger.info('PASSWORD not MATCHED')
                return render_template('login.html',error=error)
        else:
            error = 'Username not found'
            return render_template('login.html',error)
    return render_template('login.html')
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
@app.route('/logout/')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))


@app.route('/dashboard/')
@is_logged_in
def dashboard():
    #cursor
    cur =mysql.connection.cursor()
    #Get Aricle
    result = cur.execute("SELECT * FROM articles")
    articles = cur.fetchall()
    if result>0:
        return render_template('dashboard.html', articles=articles)
    else:
        msg= 'No article found'
        return render_template('dashboard.html',msg =msg)
    #close conection
    cur.close()

# Aricle form class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=500)])
    body =TextAreaField('Body', [validators.Length(min=30)])

@app.route('/add_article/', methods = ['GET', 'POST'])
@is_logged_in
def add_article():
    form =ArticleForm(request.form)
    if request.method == 'POST' and form.validate():
        title = form.title.data
        body= form.body.data

        #create cursor
        cur = mysql.connection.cursor()
        #Execute
        cur.execute("INSERT INTO articles(title, body, author)VALUES(%s, %s, %s)",(title, body, session['USERNAME']))
        #commit to DB
        mysql.connection.commit()
        #close connection
        cur.close()
        flash('Article created', 'success')
        return redirect(url_for('dashboard'))
    return render_template('add_article.html', form =form)
#edit article
@app.route('/edit_article/<string:id>', methods = ['GET', 'POST'])
@is_logged_in
def edit_article(id):
    #Create Cursor
    cur = mysql.connection.cursor()
    # get article by id
    result = cur.execute("SELECT * FROM articles WHERE id = %s",[id])
    article = cur.fetchone()
    form =ArticleForm(request.form)
    form.title.data = article['title']
    form.body.data =  article['body']
    if request.method == 'POST' and form.validate():
        title = request.form['title']
        body= request.form['body']

        #create cursor
        cur = mysql.connection.cursor()
        app.logger.info(title)
        #Execute
        #cur.execute ("UPDATE articles SET name =%s, body=%s WHERE id =%s" (name, body, id))
        cur.execute ("UPDATE articles SET title=%s, body=%s WHERE id=%s",(title, body, id))
        #commit to DB
        mysql.connection.commit()
        #close connection
        cur.close()
        flash('Article updated', 'success')
        return redirect(url_for('dashboard'))
    return render_template('edit_article.html', form =form)
#delete_article
@app.route('/delete_article/<string:id>', methods=['post'])
@is_logged_in
def delete_article(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM articles WHERE ID =%s", [id])
    mysql.connection.commit()
    #close connection
    cur.close()
    flash('Article Deleted', 'success')
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.secret_key='secret123'
    app.run(debug=True)
