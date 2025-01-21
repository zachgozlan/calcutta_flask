from flask import Markup
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, DecimalField, BooleanField, validators
from wtforms.validators import DataRequired, Email
from wtforms.fields import EmailField
from decimal import ROUND_HALF_UP
import pandas as pd

opening = pd.read_csv('/home/zachgozlan/flask_app/opening_bids.csv', encoding='latin-1')
current = pd.read_csv('/home/zachgozlan/flask_app/current_bids.csv', encoding='latin-1', index_col=0)

def dropdown_generator(team, table):
    value = team

    seed = table.loc[team]['Seed']
    region = table.loc[team]['Region']
    #current_price = table.loc[team]['Current Bid']
    display = "{} | Seed: {}{}".format(value, seed, region)
    return tuple([value, display])

value_list = [('', '---')]

for team in list(opening.Team):
    value_list.append(dropdown_generator(team, current))


class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), validators.Length(min=1,max=20,message="Keep names below 20 characters")])
    email = StringField('Email', validators=[DataRequired(), validators.Email()])
    team = SelectField('Team',choices=value_list, validators=[validators.Length(min=1,message="Please pick a team.")])
    bid = DecimalField('Bid', places=2, rounding=ROUND_HALF_UP, validators=[DataRequired()])
    confirm = BooleanField("I have read and I understand the rules. I did not accidentally pick the wrong team or put the wrong number in the boxes. I am willing to pay up to the amount I provided for the rights to this team.", validators=[DataRequired()])
    submit = SubmitField('Submit Bid')