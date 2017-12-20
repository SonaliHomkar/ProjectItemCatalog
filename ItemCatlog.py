## import database and sqlalchemy for CRUD operations ##
from database_setup import Base,Category,Item
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask,render_template, request, redirect, url_for,flash, jsonify
app = Flask(__name__)


## create session and connect to database ##
engine = create_engine('sqlite:///ItemCatlog.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def showCategory():
        category = session.query(Category).all()
        items = session.query(Item).order_by(Item.id.desc()).limit(5).all()
        return render_template('category.html',category=category,items=items)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
        restaurantId = session.query(Restaurant).filter_by(id = restaurant_id).one()
        Menuitems = session.query(MenuItem).filter_by(restaurant_id = restaurantId.id).all()
        return render_template('menu.html',restaurant=restaurantId,items=Menuitems)

# Task 1 : Create route for new category function here
@app.route('/ItemCatlog/newCategory/', methods=['GET','POST'])
def newCategory():
        if request.method == 'POST':
                newItem = Category(catName = request.form['category'])
                session.add(newItem)
                session.commit()
                flash("New Category created!!!")
                return redirect(url_for('showCategory'))
        else:
                return render_template('newCategory.html')        

# Task 1 : Create route for editing category function here
@app.route('/ItemCatlog/<int:cat_id>/edit/', methods=['GET','POST'])
def editCategory(cat_id):
        editedItem = session.query(Category).filter_by(id=cat_id).one()
        if request.method == 'POST':
                editedItem.catName = request.form['category']
                session.add(editedItem)
                session.commit()
                flash("Category edited!!!")
                return redirect(url_for('showCategory'))
        else:
                return render_template('editCategory.html',cat_id=cat_id,i=editedItem)
        return "page to edit a menu item ..."

# Task 1 : Create route for newMenuItem function here
@app.route('/ItemCatlog/<int:cat_id>/delete/', methods = ['GET','POST'])
def deleteCategory(cat_id):
        deletedItem = session.query(Category).filter_by(id=cat_id).one()
        if request.method == 'POST':
                session.delete(deletedItem)
                session.commit()
                flash("Category Deleted!!!")
                return redirect(url_for('showCategory'))
        else:
                return render_template('deleteCategory.html',cat_id=cat_id,i=deletedItem)
        return "page to delete a menu item ..."


# Task 1 : Create route for adding new item function here
@app.route('/ItemCatlog/addItem/', methods = ['GET','POST'])
def addItem():
        if request.method == 'POST':
                newItem = Item(itemName = request.form['itemName'],description = request.form['description'],category_id=request.form['ddlCategory'])
                session.add(newItem)
                session.commit()
                flash("New Item created!!")
                return redirect(url_for('showCategory'))
        else:
                category = session.query(Category).all()
                 
                return render_template('addNewItem.html',categories=category)
        

# Task 1 : Create route for adding new item function here
@app.route('/ItemCatlog/<int:cat_id>/displayItem/', methods = ['GET','POST'])
def displayItem(cat_id):
        category = session.query(Category).all()
        items = session.query(Item).filter_by(category_id=cat_id).all()
        return render_template('category.html',category=category,items=items)
        

# Task 1 : Create route for adding new item function here
@app.route('/ItemCatlog/<int:item_id>/displayItemDetail/', methods = ['GET','POST'])
def displayItemDetails(item_id):
        items = session.query(Item.id,Item.description,Item.itemName,Category.catName).join(Category,Category.id==Item.category_id).filter(Item.id==item_id).all()
        return render_template('itemDetails.html',items=items)

# Task 1 : Create route for adding new item function here
@app.route('/ItemCatlog/<int:item_id>/EditItem/', methods = ['GET','POST'])
def editItemDetails(item_id):
        editedItem = session.query(Item).filter_by(id=item_id).one()
        if request.method == 'POST':
                editedItem.itemName =  request.form['itemName']
                editedItem.description = request.form['description']
                editedItem.category_id = request.form['ddlCategory']
                session.add(editedItem)
                session.commit()
                flash("Item edited!!")
                return redirect(url_for('showCategory'))
        else:
                category = session.query(Category).all()
                items = session.query(Item.id,Item.description,Item.itemName,Category.catName,Category.id).join(Category,Category.id==Item.category_id).filter(Item.id==item_id).all()
                return render_template('editItemDetails.html',items=items,category=category)


# Task 1 : Create route for adding new item function here
@app.route('/ItemCatlog/<int:item_id>/DeleteItem/', methods = ['GET','POST'])
def DeleteItem(item_id):
        deletedItem = session.query(Item).filter_by(id=item_id).one()
        if request.method == 'POST':
                session.delete(deletedItem)
                session.commit()
                flash("Item Deleted!!")
                return redirect(url_for('showCategory'))
        else:
                return render_template('DeleteItem.html')



# Making an API endpoint(get request) to get all categories 
@app.route('/ItemCatlog/JSON')
def categoryJason():
        category = session.query(Category).all()
        return jsonify(categories=[i.serialize for i in category])




# Making an API endpoint(get request) to get the menu of spectified restaurant
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJason(restaurant_id):
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
        items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
        return jsonify(MenuItems=[i.serialize for i in items])

# Making an API endpoint to get the single menu ITem
@ app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/menu/JSON')
def menuItemJason(restaurant_id,menu_id):
        items = session.query(MenuItem).filter_by(id=menu_id).one()
        return jsonify(MenuItems=[items.serialize])

if __name__ == "__main__":
        app.secret_key = 'super_secret_key'
        app.debug = True
        app.run(host = '0.0.0.0', port = 5500)
