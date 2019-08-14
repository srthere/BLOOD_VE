from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
#from data import Articles
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer,SignatureExpired
from forms import loginform,RegisterForm,ArticleForm
app= Flask(__name__)
#app.config.from_pyfile('config.cfg')
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
#config EMAIL

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USE_SSL']=True
#add a email and password
app.config['MAIL_USERNAME'] = ''
app.config['MAIL_PASSWORD'] = ''
mail=Mail(app)
s=URLSafeTimedSerializer(app.secret_key)

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '9334178140'
app.config['MYSQL_DB'] = 'BLOOD_VE'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
#init MySQL
mysql = MySQL(app)
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap
#Articles = Articles()
@app.route('/')
def index():
    return render_template('home.html')

#for sending mail
@app.route('/send/',methods=['GET','post'])
@is_logged_in
def send():
    if request.method == 'POST':
        #Get Form FIelds
        CITY = request.form['CITY']
        BLOOD_GROUP=request.form['BLOOD_GROUP']
        cur = mysql.connection.cursor()
        xpcounter = "SELECT * FROM users WHERE CITY = %s AND BLOOD_GROUP=%s"
        result=cur.execute(xpcounter, (CITY, BLOOD_GROUP))
        if result > 0:
            result=cur.execute("SELECT * FROM users WHERE CITY=%s",[CITY])
            search = cur.fetchall()
            recipients=[]
            for i in search:
                if(i['USERNAME']!=session['USERNAME']):
                    recipients.append(i['EMAIL'])
            body='Hello!!\n'
            k=cur.execute("SELECT * FROM users WHERE USERNAME=%s",[session['USERNAME']])
            search=cur.fetchall()
            for i in search:
                if(i['NAME']):
                    body=body+i['NAME']
                    body+=' has requested a type of blood group that matched with yours.'
                if(i['PHONE_NUMBER']):
                    body+='\n'+'You can also contact to the one who is in need by dialing the below mentioned phone number.\n'
                    body+=i['PHONE_NUMBER']
                    body+='\n'+"Thank You!!"
     #add a sender email
            msg = mail.send_message('Requirement of Blood in Your City',sender='',recipients=recipients,body=body)
            l="msg sent"
            return render_template('home.html',msg=l)
        else:
            msg='No Donors Found in this City'
            return render_template('confirm.html',msg=msg)
        cur.close()
    return render_template('confirm.html')





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




@app.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        NAME = form.NAME.data
        USERNAME = form.USERNAME.data
        PASSWORD = form.PASSWORD.data
        PASSWORD = sha256_crypt.encrypt(str(form.PASSWORD.data))
        EMAIL = form.EMAIL.data
        BLOOD_GROUP = form.BLOOD_GROUP.data
        PHONE_NUMBER = form.PHONE_NUMBER.data
        ADDRESS = form.ADDRESS.data
        CITY = form.CITY.data
        #Create DictCursor
        cur = mysql.connection.cursor()
        # Execute query
        cur.execute("INSERT INTO users(NAME, USERNAME, PASSWORD, EMAIL, BLOOD_GROUP, PHONE_NUMBER, ADDRESS,CITY) VALUES(%s, %s, %s, %s, %s, %s, %s,%s)", (NAME, USERNAME, PASSWORD, EMAIL, BLOOD_GROUP, PHONE_NUMBER, ADDRESS,CITY))

        cur.execute("INSERT INTO cities(EMAIL,CITY) VALUES(%s,%s)",(EMAIL,CITY))
        #for email confirmation
        token=s.dumps(EMAIL,salt='email-confirm')
        msg=Message('Confirm Email',sender='mi.manishpathak@gmail.com',recipients=[EMAIL])
        link=url_for('confirm_email',token=token,_external=True)
        msg.body='Your link is {}'.format(link)
        mail.send(msg)
        # commit to DB
        mysql.connection.commit()
        # Close connection
        cur.close()
        flash('You are now registered and can log in and verify your email address', 'success')

        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form)
#showing confirmation Message
@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email=s.loads(token,salt='email-confirm',max_age=120)
    except SignatureExpired:
        return '<h1>The link is expired</h1>'
    return 'Email Verified'

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form=loginform()
    if form.validate_on_submit():
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
                error = 'Invalid Password'
                app.logger.info('PASSWORD not MATCHED')
                return render_template('login.html',error=error,form=form)
        else:
            error = 'Username not found'
            return render_template('login.html',error=error,form=form)
    return render_template('login.html',form=form)

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

#Search Bar
@app.route('/Search/',methods = ['GET','POST'])
def Search():
    if request.method == 'POST':
        #Get Form FIelds
        CITY = request.form['CITY']
        cur = mysql.connection.cursor()
        result=cur.execute("SELECT * FROM cities WHERE CITY = %s",[CITY])

        if result > 0:
            result=cur.execute("SELECT * FROM users WHERE CITY=%s",[CITY])
            search = cur.fetchall()
            return render_template('setter.html',search=search)
        else:
            msg='No Donors Found in this City'
            return render_template('search.html',msg=msg)
        cur.close()
        #cur2.close()
    return render_template('search.html')




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
@app.route('/edit_article/<string:id>/', methods = ['GET', 'POST'])
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
@app.route('/delete_article/<string:id>/', methods=['post'])
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

    app.run(debug=True)
