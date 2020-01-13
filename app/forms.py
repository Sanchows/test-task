from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FileField
from wtforms.validators import DataRequired

class AddForm(FlaskForm):
    surname = StringField('Фамилия', validators=[DataRequired()])
    first_name = StringField('Имя', validators=[DataRequired()])
    last_name = StringField('Отчество', validators=[DataRequired()])
    file = FileField('Фотография', validators=[DataRequired()],)
    submit = SubmitField('Добавить')