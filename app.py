from logging import debug
from flask import Flask, render_template, request, session, redirect, url_for, g
import utils
from utils import preprocessdata
import os


class User:
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password


users = []
users.append(User(id=1, email='test@test.com', password='wgu'))

app = Flask(__name__)
app.secret_key = 'somesecretkey'


@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        email = request.form['email']
        password = request.form['password']

        wrong_cred = "The email and/or password entered is not valid!  Please try again."
        for x in users:
            if x.email != email:
                return render_template('login.html', wrong_credentials=wrong_cred)
                # return redirect(url_for('login'))
            user = [x for x in users if x.email == email][0]

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('apply'))

        return render_template('login.html', wrong_credentials=wrong_cred)
        # return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/apply', methods=['POST', 'GET'])
def apply():
    return render_template('application.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        Gender = request.form.get('Gender')
        Married = request.form.get('Married')
        Dependents = request.form.get('Dependents')
        Education = request.form.get('Education')
        Self_Employed = request.form.get('Self_Employed')
        ApplicantIncome = request.form.get('ApplicantIncome')
        CoapplicantIncome = request.form.get('CoapplicantIncome')
        LoanAmount = request.form.get('LoanAmount')
        Loan_Amount_Term = request.form.get('Loan_Amount_Term')
        Credit_History = request.form.get('Credit_History')
        Property_Area = request.form.get('Property_Area')

    prediction = utils.preprocessdata(Gender, Married, Dependents, Education, Self_Employed, ApplicantIncome,
                                      CoapplicantIncome, LoanAmount, Loan_Amount_Term, Credit_History,
                                      Property_Area)

    return render_template('result.html', prediction=prediction)


port = int(os.environ.get("PORT", 5000))
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
