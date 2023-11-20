from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL, ValidationError
from flask_ckeditor import CKEditorField

class CreateCafeForm(FlaskForm):
    name = StringField("Cafe Name", validators=[DataRequired()])
    map_url = StringField("Map URL", validators=[DataRequired(), URL()])
    img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    location = StringField("Location", validators=[DataRequired()])
    has_sockets = BooleanField("Has Sockets")
    has_toilet = BooleanField("Has Toilet")
    has_wifi = BooleanField("Has WiFi")
    can_take_calls = BooleanField("Can Take Calls")
    seats = StringField("Number of Seats", validators=[DataRequired()])
    coffee_price = StringField("Coffee Price")
    submit = SubmitField("Add Cafe")

    def validate_seats(self, field):
        try:
            int(field.data)
        except ValueError:
            raise ValidationError("Seats must be a number.")
