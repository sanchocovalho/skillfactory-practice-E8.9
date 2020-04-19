from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length

class WebsiteForm(FlaskForm):
    address = StringField('address', validators=[DataRequired(), Length(min=5, max=300)])
