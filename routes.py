from flask import render_template, flash, redirect, url_for, make_response, request, Markup
from flask_app import app, bid_calculation
from flask_app.forms import UserForm
from flask_app.bid_calculation import bid_calculator, current_prizes, current_leaders
import io, csv
from flask_mysqldb import MySQL
from tabulate import tabulate
import pandas as pd
import mysql.connector as connection

mysql = MySQL(app)

@app.route('/', methods=['GET','POST'])
@app.route('/bid_form', methods=['GET','POST'])
def bid_form():
    data = pd.read_sql('''SELECT * from bids''', mysql.connection)
    form = UserForm()
    #cursor = mysql.connection.cursor()
    #cursor.execute('select * from bids')
    #data = cursor.fetchall()
    #print(data)
    #cur.close()
    if form.validate_on_submit():
        #f = open('bids.csv', 'a')
        #f.write(",".join([now.strftime("%d/%m/%Y %H:%M:%S"), form.name.data, form.email.data, form.team.data, form.bid.data])
        #f.close()


        flash("Bids are closed, but submitting forms sure is fun.") #form=UserForm(formdata=None)


        '''
        cursor = mysql.connection.cursor()
        cursor.execute(INSERT INTO bids (name, email, team, bid) values (%s, %s, %s, %s), (form.name.data, form.email.data, form.team.data, round(form.bid.data,2)))
        mysql.connection.commit()
        cursor.close()
        '''

        #flash("You have placed a bid of {} on {} - see if you're now leading below.".format(form.bid.data, form.team.data)) #form=UserForm(formdata=None)

        data = pd.read_sql('''SELECT * from bids''', mysql.connection)
        form = UserForm(formdata=None)
        return render_template('bid_form.html', title='Bid Page', form=form, data=current_prizes(data), data_2=current_leaders(data)) #return redirect('/bid_form') #
    #cur.execute('SELECT * FROM bids')
    #data = mycursor.fetchall()
    return render_template('bid_form.html', title='Bid Page', form=form, data=current_prizes(data), data_2=current_leaders(data))

@app.route('/current_bids')
def current_bids():
    try:
        #cursor = mysql.connection.cursor()
        #cursor.execute('''SELECT * from bids''')
        #data = cursor.fetchall()
        data = pd.read_sql('''SELECT * from bids''', mysql.connection)
        data = bid_calculator(data)
        return render_template('current_bids.html', data=data.sort_values(by=['Current Bid'], ascending=False))
    except Exception as e:
        return (str(e))

@app.route('/current_bids_seed')
def current_bids_seed():
    try:
        #cursor = mysql.connection.cursor()
        #cursor.execute('''SELECT * from bids''')
        #data = cursor.fetchall()
        data = pd.read_sql('''SELECT * from bids''', mysql.connection)
        data = bid_calculator(data)
        return render_template('current_bids.html', data=data.sort_values(by=['Seed'], ascending=True))
    except Exception as e:
        return (str(e))

@app.route('/current_bids_region')
def current_bids_region():
    try:
        #cursor = mysql.connection.cursor()
        #cursor.execute('''SELECT * from bids''')
        #data = cursor.fetchall()
        data = pd.read_sql('''SELECT * from bids''', mysql.connection)
        data = bid_calculator(data)
        data_e = data[data['Region']=='E'].sort_values(by=['Seed'], ascending=True)
        data_w = data[data['Region']=='W'].sort_values(by=['Seed'], ascending=True)
        data_s = data[data['Region']=='S'].sort_values(by=['Seed'], ascending=True)
        data_mw = data[data['Region']=='MW'].sort_values(by=['Seed'], ascending=True)
        return render_template('current_bids_regional.html', data_east=data_e, data_west=data_w, data_south=data_s, data_midwest=data_mw)
    except Exception as e:
        return (str(e))

@app.route('/current_bids_no_bids')
def current_bids_no_bids():
    try:
        #cursor = mysql.connection.cursor()
        #cursor.execute('''SELECT * from bids''')
        #data = cursor.fetchall()
        data = pd.read_sql('''SELECT * from bids''', mysql.connection)
        data = bid_calculator(data)
        data = data[data['Bid Count']==0]
        return render_template('current_bids.html', data=data.sort_values(by=['Seed'], ascending=True))
    except Exception as e:
        return (str(e))

@app.route('/rules')
def rules():
    return render_template('rules.html', title='Rules')

@app.route('/prizes')
def prizes():
    prizes = pd.read_csv('/home/zachgozlan/flask_app/prizes.csv', encoding='latin-1')
    return render_template('prizes.html', data=prizes)

#@app.route('/index')
#def index():
#    user = {'username': 'Miguel'}
#    posts = [
#        {
#            'author': {'username': 'John'},
#            'body': 'Beautiful day in Portland!'
#        },
#        {
#            'author': {'username': 'Susan'},
#            'body': 'The Avengers movie was so cool!'
#        }
#    ]
#    return render_template('index.html', title='Home', user=user, posts=posts)
#
#@app.route('/index2')
#def index2():
#    user = {'username': 'Josh'}
#    posts = [
#        {
#            'author': {'username': 'Dave'},
#            'body': 'Beautiful day in Seattle!'
#        },
#        {
#            'author': {'username': 'Susan'},
#            'body': 'The Avengers movie was okay!'
#        }
#    ]
#    return render_template('index2.html', title='Home', user=user, posts=posts)
