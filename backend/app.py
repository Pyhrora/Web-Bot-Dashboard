# app.py

from flask import Flask, redirect, url_for, session, render_template
from discord import OAuth2Session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Discord-OAuth-Konfiguration
CLIENT_ID = 'DEIN_CLIENT_ID'  # Discord-Client-ID
CLIENT_SECRET = 'DEIN_CLIENT_SECRET'  # Discord-Client-Secret
REDIRECT_URI = 'http://127.0.0.1:5000/callback'  # OAuth-Callback-URL

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    discord = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI)
    auth_url, state = discord.authorization_url('https://discord.com/api/oauth2/authorize')
    session['oauth_state'] = state
    return redirect(auth_url)

@app.route('/callback')
def callback():
    discord = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, state=session['oauth_state'])
    token = discord.fetch_token('https://discord.com/api/oauth2/token', client_secret=CLIENT_SECRET)
    session['oauth_token'] = token
    return redirect(url_for('dashboard'))

@app.route('/dashboard')
def dashboard():
    if 'oauth_token' not in session:
        return redirect(url_for('login'))
    
    discord = OAuth2Session(CLIENT_ID, token=session['oauth_token'])
    user_info = discord.get('https://discord.com/api/users/@me').json()
    
    return render_template('dashboard.html', user=user_info)

if __name__ == "__main__":
    app.run(debug=True)
s