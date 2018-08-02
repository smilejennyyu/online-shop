from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)

from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Store, FashionItem


#Connect to Database and create database session
engine = create_engine('sqlite:///onlineshopping.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#JSON APIs to view Restaurant Information
# @app.route('/store/<int:store_id>/item/JSON')
# def storeItemJSON(store_id):
#     store = session.query(Store).filter_by(id = store_id).one()
#     items = session.query(FashionItem).filter_by(store_id = store_id).all()
#     return jsonify(FashionItems=[i.serialize for i in items])


# @app.route('/store/<int:store_id>/item/<int:item_id>/JSON')
# def menuItemJSON(store_id, item_id):
#     Menu_Item = session.query(MenuItem).filter_by(id = menu_id).one()
#     return jsonify(Menu_Item = Menu_Item.serialize)

# @app.route('/restaurant/JSON')
# def restaurantsJSON():
#     restaurants = session.query(Restaurant).all()
#     return jsonify(restaurants= [r.serialize for r in restaurants])


#Show all restaurants
@app.route('/')
@app.route('/store/')
def showStores():
  stores = session.query(Store).order_by(asc(Store.name))
  return render_template('stores.html', stores = stores)

#Create a new restaurant
@app.route('/store/new/', methods=['GET','POST'])
def newStore():
  if request.method == 'POST':
      newStore = Store(name = request.form['name'])
      session.add(newStore)
      flash('New Store %s Successfully Created' % newStore.name)
      session.commit()
      return redirect(url_for('showStores'))
  else:
      return render_template('newStore.html')

#Edit a restaurant
@app.route('/store/<int:store_id>/edit/', methods = ['GET', 'POST'])
def editStore(store_id):
  editedStore = session.query(Store).filter_by(id = store_id).one()
  if request.method == 'POST':
      if request.form['name']:
        editedStore.name = request.form['name']
        flash('Store Successfully Edited %s' % editedStore.name)
        return redirect(url_for('showStores'))
  else:
    return render_template('editStore.html', store = editedStore)


#Delete a restaurant
@app.route('/store/<int:store_id>/delete/', methods = ['GET','POST'])
def deleteStore(store_id):
  storeToDelete = session.query(Store).filter_by(id = store_id).one()
  if request.method == 'POST':
    session.delete(storeToDelete)
    flash('%s Successfully Deleted' % storeToDelete.name)
    session.commit()
    return redirect(url_for('showStores', store_id = store_id))
  else:
    return render_template('deleteStore.html',store = storeToDelete)

#Show a restaurant menu
@app.route('/store/<int:store_id>/')
# @app.route('/store/<int:store_id>/item/')
def showItem(store_id):
    store = session.query(Store).filter_by(id = store_id).one()
    items = session.query(FashionItem).filter_by(store_id = store_id).all()
    return render_template('item.html', items = items, store = store)
     


# #Create a new menu item
# @app.route('/restaurant/<int:restaurant_id>/menu/new/',methods=['GET','POST'])
# def newMenuItem(restaurant_id):
#   restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
#   if request.method == 'POST':
#       newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
#       session.add(newItem)
#       session.commit()
#       flash('New Menu %s Item Successfully Created' % (newItem.name))
#       return redirect(url_for('showMenu', restaurant_id = restaurant_id))
#   else:
#       return render_template('newmenuitem.html', restaurant_id = restaurant_id)

# #Edit a menu item
# @app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET','POST'])
# def editMenuItem(restaurant_id, menu_id):

#     editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
#     restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
#     if request.method == 'POST':
#         if request.form['name']:
#             editedItem.name = request.form['name']
#         if request.form['description']:
#             editedItem.description = request.form['description']
#         if request.form['price']:
#             editedItem.price = request.form['price']
#         if request.form['course']:
#             editedItem.course = request.form['course']
#         session.add(editedItem)
#         session.commit() 
#         flash('Menu Item Successfully Edited')
#         return redirect(url_for('showMenu', restaurant_id = restaurant_id))
#     else:
#         return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)


# #Delete a menu item
# @app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods = ['GET','POST'])
# def deleteMenuItem(restaurant_id,menu_id):
#     restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
#     itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one() 
#     if request.method == 'POST':
#         session.delete(itemToDelete)
#         session.commit()
#         flash('Menu Item Successfully Deleted')
#         return redirect(url_for('showMenu', restaurant_id = restaurant_id))
#     else:
#         return render_template('deleteMenuItem.html', item = itemToDelete)




if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
