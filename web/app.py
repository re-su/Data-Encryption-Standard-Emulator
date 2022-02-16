from flask import Flask, render_template, flash, request
from des_core.Des import Des
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired

class EncodeForm(FlaskForm):
    text = StringField('Plain text', validators=[DataRequired()])
    submit = SubmitField('Encode')
    submitDecode = SubmitField('Decode')

app = Flask(__name__)
app.config['SECRET_KEY'] = '12345678901234567890123456789012'
des = Des()

@app.route("/", methods=['POST', 'GET'])
def index():
    des = Des()
    form = EncodeForm()
    return render_template('index.html', form=form, secret=des.keyGenerator.initialKey)

@app.route("/encode", methods=['POST', 'GET'])
def encode():
    text = request.args.get('jsdata')
    text = des.encode(text)
    return render_template('textarea.html', text=text)

@app.route("/decode", methods=['POST', 'GET'])
def decode():
    text = request.args.get('jsdata')
    text = des.decode(text)
    return render_template('textarea.html', text=text)

@app.route("/secret", methods=['POST'])
def newSecret():
    text = des.keyGenerator.newKey()
    return render_template('textarea.html', text=text)

if __name__ == '__main__':
    app.run()