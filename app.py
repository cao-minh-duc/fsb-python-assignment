from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "F7B4C657489B418623F87EED37382B80"
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
migrate = Migrate(app, db)

class LocationForm(FlaskForm):
    name = StringField('Location Name', validators=[DataRequired(), Length(min=2, max=50)])
    description = StringField('Description', validators=[Length(max=200)])
    submit = SubmitField('Submit')

class DeleteForm(FlaskForm):
    submit = SubmitField('Confirm Delete')
    
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(200))
    

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LocationForm()
    if form.validate_on_submit():
        new_location = Location(name=form.name.data, description=form.description.data)
        db.session.add(new_location)
        db.session.commit()
        return redirect(url_for('index'))
    locations = Location.query.all()
    return render_template('index.html', locations=locations, form=form)

@app.route('/add', methods=['POST'])
def add_location():
    name = request.form['name']
    description = request.form['description']
    new_location = Location(name=name, description=description)
    db.session.add(new_location)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_location(id):
    location = Location.query.get_or_404(id)
    form = LocationForm()
    if form.validate_on_submit():
        location.name = form.name.data
        location.description = form.description.data
        db.session.commit()
        return redirect(url_for('index'))
    elif request.method == 'GET':
        form.name.data = location.name
        form.description.data = location.description
    return render_template('update.html', form=form)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_location(id):
    location = Location.query.get_or_404(id)
    form = DeleteForm()
    if form.validate_on_submit():
        db.session.delete(location)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('delete.html', form=form, location=location)

if __name__ == '__main__':
    app.run(debug=True, port=8001)
