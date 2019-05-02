from flask import Flask, render_template, flash, redirect, url_for, session, request
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import mysql.connector
from flask_socketio import SocketIO, send, emit
import threading
from ServerBJ import Sdealer_plays, Snew_deck, Svalue_check

app = Flask(__name__)

# Config MySQL
'''app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'kevin'
app.config['MYSQL_PASSWORD'] = 'Capstone2'
app.config['MYSQL_DB'] = 'blackjack'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'''
# init MYSQL

socketio = SocketIO(app)
mysql = mysql.connector.connect(user='kevin', password='Capstone2', host='localhost', database='blackjack')

'''def background(msg):
    while True:
        if msg == 'yes':
            deck = Snew_deck()
            playerhand = []
            dealerhand = []
            playerhand.append(deck.pop(0))
            dealerhand.append(deck.pop(0))
            playerhand.append(deck.pop(0))
            dealerhand.append(deck.pop(0))
            print(playerhand)
            str1 = [' '.join([str(c) for c in lst]) for lst in playerhand]
            send(str1, broadcast=True)
            print(dealerhand)
            str2 = [' '.join([str(c) for c in lst]) for lst in dealerhand]
            send(str2, broadcast=True)
            dealer = Svalue_check(dealerhand)
            player = Svalue_check(playerhand)
            print(player)
            print(dealer)
            if dealer == 21:
                send("Dealer wins", broadcast=True)
                return "Dealer wins"
            if player == 21:
                send("Players wins", broadcast=True)
                return "Player wins"
            while True:
                if msg == 'Hit' or msg == 'Stand' or 'User has connected!':
                    player = Splayer_plays(playerhand, deck, msg)
                    print(playerhand)
                    if player > 21:
                        send('Dealer wins', broadcast=True)
                        return "Dealer wins"
                    if player == 21:
                        send("Players wins", broadcast=True)
                        return "Player wins"
                    Sdealer_plays(dealerhand, deck)
                    print(dealerhand)
                    if dealer > 21:
                        return "Player wins"
                    if dealer == 21:
                        send('Dealer wins', broadcast=True)
                        return "Dealer wins"
                    if dealer >= player:
                        send('Dealer wins', broadcast=True)
                        return "Dealers wins"
                    if dealer < player:
                        send("Players wins", broadcast=True)
                        return "Players wins"
                else:
                    print('no')
                    send('Try Again', broadcast=True)
        else:
            print('no')
            send('Try Again', broadcast=True)




def Splayer_plays(hand, deck, user):
    while True:
        if user == "Hit":
            hand.append(deck.pop(0))
            str3 = [' '.join([str(c) for c in lst]) for lst in hand]
            send(str, broadcast=True)
            v = Svalue_check(hand)
            if v >= 21:
                return v
        if user == "Stand":
            v = Svalue_check(hand)
            return v
'''


# Index
@app.route('/')
def index():
    return render_template('home.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Register Form Class
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

        # Create cursor
        cur = mysql.cursor()

        # Execute query
        cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)",
                    (name, email, username, password))

        # Commit to DB
        mysql.commit()

        # Close connection
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# User login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # Create cursor
        cur = mysql.cursor(buffered=True)

        # Get user by username
        cur.execute("SELECT * FROM users WHERE username = %s", [username])
        result = cur.fetchone()
        if result is not None:
            # Get stored hash
            data = cur.fetchone()
            password = data[4]

            # Compare Passwords
            if sha256_crypt.verify(password_candidate, password):
                # Passed
                session['logged_in'] = True
                session['username'] = username

                flash('You are now logged in', 'success')
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid login'
                return render_template('login.html', error=error)
            # Close connection

        else:
            error = 'Username not found'
            return render_template('login.html', error=error)

    return render_template('login.html')


# Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))

    return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


#
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')


@app.route('/blackjack')
@is_logged_in
def game():
    '''threading1 = threading.Thread(target=background, args=(quick,))
    threading1.daemon = True
    threading1.start()'''
    return render_template('NewBlackJack.html')


'''@app.route('/wildblackjack')
@is_logged_in
def game():
    return render_template('NewBlackJack.html')


@app.route('/dealornodealblackjack')
@is_logged_in
def game():
    return render_template('NewBlackJack.html')'''


def yes(mess):
    if mess == 'start':
        print('yes')


@socketio.on('message')
def handleMessage(msg):
    print('Message: ' + msg)
    socketio.send(msg, broadcast=True, callback=yes(msg))
    return msg


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True, port=5001)
    socketio.run(app)
