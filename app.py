from flask import Flask, render_template, request, redirect, url_for, session
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit_info', methods=['POST'])
def submit_info():
    session['name'] = request.form['name']
    session['age'] = request.form['age']
    session['gender'] = request.form['gender']
    session['bio'] = request.form['bio']
    file = request.files['photo']
    if file:
        filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        session['photo'] = filepath
    return redirect(url_for('page2'))

@app.route('/page2')
def page2():
    return render_template('page2.html')

@app.route('/submit_preferences', methods=['POST'])
def submit_preferences():
    session['preferences'] = request.form.to_dict(flat=False)
    return redirect(url_for('page3'))

@app.route('/page3')
def page3():
    return render_template('page3.html', name=session.get('name'), age=session.get('age'),
                           gender=session.get('gender'), bio=session.get('bio'),
                           photo=session.get('photo'), preferences=session.get('preferences'))

@app.route('/chat')
def chat():
    return render_template('chat.html')

if __name__ == '__main__':
    app.run(debug=True)
