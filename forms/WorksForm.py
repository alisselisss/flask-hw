from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms import BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired


class WorksForm(FlaskForm):
    job = StringField('Job', validators=[DataRequired()])
    team_leader = StringField('Id of team leader', validators=[DataRequired()])
    work_size = IntegerField("Work size")
    collaborators = StringField("List id of collaborators")
    is_finished = BooleanField("Finished")
    submit = SubmitField('Submit')