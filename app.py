from flask import request, render_template, Flask
from flask_sqlalchemy import SQLAlchemy
from send_email import send_email
from sqlalchemy.sql import func
import pandas
import heights_plot


app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/height_collector'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://wdlpdymrblkhtf:9866128995f638c2be926bf34d0f4b15b884d4ab22eeb51dabc26f5a16fd42c0@ec2-52-200-48-116.compute-1.amazonaws.com:5432/d1rpm6uoboom6j?sslmode=require'

db = SQLAlchemy(app)


class Data(db.Model):
    __tablename__ = "data"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Integer)

    def __init__(self, email, height):
        self.email = email
        self.height = height


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/success/", methods=["POST"])
def success():
    if request.method == "POST":
        email = request.form['email_name']
        height = request.form['height_name']
        if not db.session.query(Data).filter(Data.email == email).count():
            db_row = Data(email, height)
            db.session.add(db_row)
            db.session.commit()
            average_height = db.session.query(func.avg(Data.height)).scalar()
            average_height = round(average_height, 1)
            people_count = db.session.query(Data).count()

            # trying to send email with height data to user
            if not send_email(email, height, average_height, people_count):
                db.session.query(Data).filter(Data.email == email).delete()
                db.session.commit()
                return render_template("index.html", text="Can't find the given email to send a message")


            return render_template("success.html")
        else:
            return render_template("index.html", text="Only one height data from each email")


@app.route("/plot/")
def show_plot():
    # build a plot with height_statistic
    df = pandas.read_sql_table("data", db.engine)
    height = int(df.tail(1)["height"])
    script_plot, div_plot, cdn_js, cdn_css = heights_plot.build_plot(df, height)

    return render_template("plot.html",
                           script_plot=script_plot,
                           div_plot=div_plot,
                           cdn_js=cdn_js,
                           test_height=height)


# =================== a page for another porgram - FastFood Map ==============
@app.route("/fastfood")
def fastfood():
    return render_template("rest_map.html")
# ============================================================================


if __name__ == '__main__':
    app.run(debug=True)
