from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///friends.db'
# Initialize the database
db = SQLAlchemy(app)

# Create db model
class Friends(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<Name %r>' % self.id



@app.route('/home')

def index():
    return render_template("index.html")

@app.route('/about')
def about():
    names = ["A", "B", "C"]
    return render_template("about.html", names = names)

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/form', methods = ["POST"])
def form():
    users = []
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")

    if not first_name or not last_name or not email:
        error_statement = "All form fields required!"
        return render_template("contact.html", error_statement = error_statement,
                               first_name = first_name,
                               last_name = last_name,
                               email=email)
    users.append(f"{first_name} {last_name} | {email}")
    title = "Thank You!"
    return render_template("form.html", title = title, users = users)


@app.route('/users', methods=['POST','GET'])
def users():
    title = "user list"
    if request.method == 'POST':
        user_name = request.form['name']
        new_user = Friends(name=user_name)

        # Push to database
        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/users')
        except:
            return "There was an error adding new user"
    else:
        users = Friends.query.order_by(Friends.date_created)
        return render_template("users.html", title = title, users = users)

@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):
    user_to_update = Friends.query.get_or_404(id)
    if request.method == "POST":
        user_to_update.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/users')
        except:
            return "There was a problem updating users"
    else:
        return render_template("update.html", user_to_update = user_to_update)


@app.route('/hk-ocean-park')
def ocean_park():
    title = "HK Ocean Park"
    return render_template("hk-ocean-park.html", title = title)

if __name__ == '__main__':
    app.run()