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


#JSON APIs to view Store Information
@app.route('/store/<int:store_id>/item/JSON')
def storeItemJSON(store_id):
    store = session.query(Store).filter_by(id = store_id).one()
    items = session.query(FashionItem).filter_by(store_id = store_id).all()
    return jsonify(FashionItems=[i.serialize for i in items])


@app.route('/store/<int:store_id>/item/<int:item_id>/JSON')
def fashionItemJSON(store_id, item_id):
    Fashion_Item = session.query(FashionItem).filter_by(id = item_id).one()
    return jsonify(Fashion_Item = Fashion_Item.serialize)

@app.route('/store/JSON')
def storesJSON():
    stores = session.query(Store).all()
    return jsonify(stores= [r.serialize for r in stores])


#Show all stores
@app.route('/')
@app.route('/store/')
def showStores():
  stores = session.query(Store).order_by(asc(Store.name))
  return render_template('stores.html', stores = stores)

#Create a new store
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

#Edit a store
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


#Delete a store
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

#Show a store items
@app.route('/store/<int:store_id>/')
@app.route('/store/<int:store_id>/item/')
def showItem(store_id):
    store = session.query(Store).filter_by(id = store_id).one()
    items = session.query(FashionItem).filter_by(store_id = store_id).all()
    return render_template('item.html', items = items, store = store)
     


# #Create a new item
@app.route('/store/<int:store_id>/item/new/',methods=['GET','POST'])
def newItem(store_id):
  store = session.query(Store).filter_by(id = store_id).one()
  if request.method == 'POST':
      newItem = FashionItem(name = request.form['name'], price = request.form['price'], category = request.form['category'], store_id = store_id)
      session.add(newItem)
      session.commit()
      flash('New Fashion %s Item Successfully Created' % (newItem.name))
      return redirect(url_for('showItem', store_id = store_id))
  else:
      return render_template('newItem.html', store_id = store_id)

# #Edit a item
@app.route('/store/<int:store_id>/item/<int:item_id>/edit', methods=['GET','POST'])
def editItem(store_id, item_id):

    editedItem = session.query(FashionItem).filter_by(id = item_id).one()
    store = session.query(Store).filter_by(id = store_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['category']:
            editedItem.category = request.form['category']
        session.add(editedItem)
        session.commit() 
        flash('Fahion Item Successfully Edited')
        return redirect(url_for('showItem', store_id = store_id))
    else:
        return render_template('editItem.html', store_id = store_id, item_id = item_id, item = editedItem)


# #Delete a item
@app.route('/store/<int:store_id>/item/<int:item_id>/delete', methods = ['GET','POST'])
def deleteItem(store_id,item_id):
    store = session.query(Store).filter_by(id = store_id).one()
    itemToDelete = session.query(FashionItem).filter_by(id = item_id).one() 
    if request.method == 'POST':
        session.delete(itemToDelete)
        session.commit()
        flash('Fashion Item Successfully Deleted')
        return redirect(url_for('showItem', store_id = store_id))
    else:
        return render_template('deleteItem.html', item = itemToDelete)




if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
