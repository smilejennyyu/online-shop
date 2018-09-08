from flask import (Flask, render_template, request,
                   redirect, jsonify, url_for, flash)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Store, FashionItem, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "Online Fashion Application"


# Connect to Database and create database session
database = 'sqlite:///onlineshopping.db'
engine = create_engine(database, connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create login
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return the login page
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate the state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    request.get_data()
    code = request.data.decode('utf-8')

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Validate access token.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token, abort it.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify if the access token is used or not.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Validate the token for this specific app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session so that we can use it later.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('User not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % \
        login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    # delete the token
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        flash("Logged out successfully.")

        # logout and go to the store page
        return redirect(url_for('showStores'))
    else:
        response = make_response(json.dumps('Failed to logout.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# JSON APIs to view Store Information
@app.route('/store/<int:store_id>/item/JSON')
def storeItemJSON(store_id):
    store = session.query(Store).filter_by(id=store_id).one()
    items = session.query(FashionItem).filter_by(store_id=store_id).all()
    return jsonify(FashionItems=[i.serialize for i in items])


@app.route('/store/<int:store_id>/item/<int:item_id>/JSON')
def fashionItemJSON(store_id, item_id):
    Fashion_Item = session.query(FashionItem).filter_by(id=item_id).one()
    return jsonify(Fashion_Item=Fashion_Item.serialize)


@app.route('/store/JSON')
def storesJSON():
    stores = session.query(Store).all()
    return jsonify(stores=[r.serialize for r in stores])


# Show all stores
@app.route('/')
@app.route('/store/')
def showStores():
    stores = session.query(Store).order_by(asc(Store.name))
    if 'username' not in login_session:
        return render_template('publicstores.html', stores=stores)
    else:
        return render_template('stores.html', stores=stores,
                               logged_in=('username' in login_session))


# Create a new store
@app.route('/store/new/', methods=['GET', 'POST'])
def newStore():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newStore = Store(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newStore)
        flash('New Store %s Successfully Created' % newStore.name)
        session.commit()
        return redirect(url_for('showStores'))
    else:
        return render_template('newStore.html',
                               logged_in=('username' in login_session))


# Edit a store
@app.route('/store/<int:store_id>/edit/', methods=['GET', 'POST'])
def editStore(store_id):
    editedStore = session.query(Store).filter_by(id=store_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedStore.user_id != login_session['user_id']:
        return """<script>function myFunction()
                  {alert('You are not authorized to edit this store.
                  Please create your own store in order to edit.');}
                  </script><body onload='myFunction()''>"""
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            if request.form['name']:
                editedStore.name = request.form['name']
                flash('Store Successfully Edited %s' % editedStore.name)
                return redirect(url_for('showStores'))
        elif request.form['submit'] == 'cancel':
            flash('Change Cancelled')
            return redirect(url_for('showStores'))
    else:
        return render_template('editStore.html', store=editedStore,
                               logged_in=('username' in login_session))


# Delete a store
@app.route('/store/<int:store_id>/delete/', methods=['GET', 'POST'])
def deleteStore(store_id):
    storeToDelete = session.query(Store).filter_by(id=store_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if storeToDelete.user_id != login_session['user_id']:
        return """<script>function myFunction()
                  {alert('You are not authorized to delete this store.
                  Please create your own store in order to delete.');}
                  </script><body onload='myFunction()''>"""
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            session.delete(storeToDelete)
            flash('%s Successfully Deleted' % storeToDelete.name)
            session.commit()
            return redirect(url_for('showStores', store_id=store_id))
        elif request.form['submit'] == 'cancel':
            flash('Deletion cancelled')
            return redirect(url_for('showStores', store_id=store_id))
    else:
        return render_template('deleteStore.html', store=storeToDelete,
                               logged_in=('username' in login_session))


# Show the store items
@app.route('/store/<int:store_id>/')
@app.route('/store/<int:store_id>/item/')
def showItem(store_id):
    store = session.query(Store).filter_by(id=store_id).one()
    creator = getUserInfo(store.user_id)
    items = session.query(FashionItem).filter_by(
        store_id=store_id).all()
    if ('username' not in login_session) or \
       (creator.id != login_session['user_id']):
        return render_template('publicitems.html', items=items,
                               store=store, creator=creator)
    else:
        return render_template('item.html', items=items, store=store,
                               creator=creator,
                               logged_in=('username' in login_session))


# Create a new item
@app.route('/store/<int:store_id>/item/new/', methods=['GET', 'POST'])
def newItem(store_id):
    store = session.query(Store).filter_by(id=store_id).one()
    if 'username' not in login_session:
        return redirect('/login')
        store = session.query(Store).filter_by(id=store_id).one()
    if login_session['user_id'] != store.user_id:
        return """<script>function myFunction()
        {alert('You are not authorized to add fashion items to this store.
        Please create your own store in order to add items.');}
        </script><body onload='myFunction()''>"""
    if request.method == 'POST':
        if (request.form['name'] == '') or \
           (request.form['price'] == ''):
            flash('Need to fill all the fields!')
            return render_template('newItem.html', store_id=store_id,
                                   logged_in=('username' in login_session))
        else:
            newItem = FashionItem(name=request.form['name'],
                                  price=request.form['price'],
                                  category=request.form['category'],
                                  store_id=store_id)
            session.add(newItem)
            session.commit()
            flash('New Fashion %s Item Successfully Created' % (newItem.name))
            return redirect(url_for('showItem', store_id=store_id))
    else:
        return render_template('newItem.html', store_id=store_id,
                               logged_in=('username' in login_session))


# Edit an item
@app.route('/store/<int:store_id>/item/<int:item_id>/edit',
           methods=['GET', 'POST'])
def editItem(store_id, item_id):
    editedItem = session.query(FashionItem).filter_by(id=item_id).one()
    store = session.query(Store).filter_by(id=store_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    editedItem = session.query(FashionItem).filter_by(id=item_id).one()
    store = session.query(Store).filter_by(id=store_id).one()
    if login_session['user_id'] != store.user_id:
        return """<script>function myFunction()
        {alert('You are not authorized to edit fashion items to this store.
        Please create your own store in order to edit items.');}
        </script><body onload='myFunction()''>"""
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            if request.form['name']:
                editedItem.name = request.form['name']
            if request.form['price']:
                editedItem.price = request.form['price']
            if request.form['category']:
                editedItem.category = request.form['category']
            session.add(editedItem)
            session.commit()
            flash('Fashion Item Successfully Edited')
            return redirect(url_for('showItem', store_id=store_id))
        elif request.form['submit'] == 'cancel':
            flash('Fashion Item Cancelled')
            return redirect(url_for('showItem', store_id=store_id))
    else:
        return render_template('editItem.html', store_id=store_id,
                               item_id=item_id, item=editedItem,
                               logged_in=('username' in login_session))


# Delete an item
@app.route('/store/<int:store_id>/item/<int:item_id>/delete',
           methods=['GET', 'POST'])
def deleteItem(store_id, item_id):
    store = session.query(Store).filter_by(id=store_id).one()
    itemToDelete = session.query(FashionItem).filter_by(id=item_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    store = session.query(Store).filter_by(id=store_id).one()
    itemToDelete = session.query(FashionItem).filter_by(id=item_id).one()
    if login_session['user_id'] != store.user_id:
        return """<script>function myFunction()
        {alert('You are not authorized to delete fashion items to this store.
        Please create your own store in order to delete items.');}
        </script><body onload='myFunction()''>"""
    if request.method == 'POST':
        if request.form['submit'] == 'submit':
            session.delete(itemToDelete)
            session.commit()
            flash('Fashion Item Successfully Deleted')
            return redirect(url_for('showItem', store_id=store_id))
        elif request.form['submit'] == 'cancel':
            flash('Fashion Item Deletion Cancelled')
            return redirect(url_for('showItem', store_id=store_id))
    else:
        return render_template('deleteItem.html',
                               item=itemToDelete,
                               logged_in=('username' in login_session))


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
