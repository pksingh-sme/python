from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.validators import DataRequired, URL
import csv

'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class RideForm(FlaskForm):
    ride = StringField('Ride name', validators=[DataRequired()])
    destination = StringField("Destination", validators=[DataRequired()])
    location = StringField("Location on google Maps (URL)", validators=[DataRequired(), URL()])
    ride_date = StringField("Ride Date", validators=[DataRequired()])
    duration = StringField("Ride Duration (in Days)", validators=[DataRequired()])
    rider_rating = SelectField("Energy level", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    bike_rating = SelectField("Bike condition", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    power_rating = SelectField("Power Availability", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌", DataRequired()])
    riders = StringField("Rider Name(s)", validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET","POST"])
def add_ride():
    form = RideForm()
    if form.validate_on_submit():
        with open("ride-data.csv", mode="a", encoding="utf-8") as csv_file:
            csv_file.write(
                f"\n\"{form.ride.data}\","
                f"\"{form.destination.data}\","
                f"\"{form.location.data}\","
                f"\"{form.ride_date.data}\","
                f"\"{form.duration.data}\","
                f"{form.rider_rating.data},"
                f"{form.bike_rating.data},"
                f"{form.power_rating.data},"
                f"\"{form.riders.data}\""
            )
        return redirect(url_for("rides"))
    # Exercise:
    # Make the form write a new row into ride-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/rides')
def rides():
    with open('ride-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('rides.html', rides=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
