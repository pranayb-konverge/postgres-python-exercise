from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from send_mail import send_mail

app = Flask(__name__)

ENV = 'prod'

if ENV == 'dev':
    app.debug=True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://pranay:pranay@localhost/test'
else:
    app.debug=False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://reqsxgkubgxzpf:e96fd7c002d4a61ebba2a8bcae963959b4881c516da354b4e13a11316a88efa1@ec2-34-231-63-30.compute-1.amazonaws.com:5432/d7r57ilgoe47qm'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    customer = db.Column(db.String(200), unique=True)
    dealer = db.Column(db.String(200))
    rating = db.Column(db.Integer)
    comments = db.Column(db.Text())

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def submit():
    empty_message = "Please provide the Customer and Dealer name."
    customer_already_submited = "You have already submitted feedback."
    if request.method == 'POST':
        customer_name = request.form['customer']
        dealer = request.form['dealer']
        rating = request.form['rating']
        comments = request.form['comments']
        # print(customer_name, dealer, rating,comments)
        if customer_name == '' or dealer == '':
            return render_template('index.html', message=empty_message)

        if db.session.query(Feedback).filter(Feedback.customer == customer_name).count() == 0:
            data = Feedback(customer_name, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_mail(customer_name, dealer, rating, comments)
            return render_template('success.html')

        return render_template('index.html', message=customer_already_submited)
        

if __name__ == '__main__':
    app.run()