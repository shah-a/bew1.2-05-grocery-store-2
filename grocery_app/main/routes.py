from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.main.forms import GroceryStoreForm, GroceryItemForm
from grocery_app import db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    return render_template('home.html', all_stores=all_stores)

@main.route('/new_store', methods=['GET', 'POST'])
@login_required
def new_store():
    form = GroceryStoreForm()

    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,
            address=form.address.data,
            added_by=current_user
        )

        db.session.add(new_store)
        db.session.commit()

        flash("New store was successfully added.")
        return redirect(url_for('main.store_detail', store_id=new_store.id))

    return render_template('new_store.html', form=form)

@main.route('/new_item', methods=['GET', 'POST'])
@login_required
def new_item():
    form = GroceryItemForm()

    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            added_by=current_user
        )

        db.session.add(new_item)
        db.session.commit()

        flash("New item successfully added.")
        return redirect(url_for('main.item_detail', item_id=new_item.id))

    return render_template('new_item.html', form=form)

@main.route('/store/<store_id>', methods=['GET', 'POST'])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)

    if form.validate_on_submit():
        form.populate_obj(store)
        db.session.add(store)
        db.session.commit()

        flash("Store was successfully updated.")
        return redirect(url_for('main.store_detail', store_id=store.id))

    return render_template('store_detail.html', store=store, form=form)

@main.route('/item/<item_id>', methods=['GET', 'POST'])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)

    if form.validate_on_submit():
        form.populate_obj(item)
        db.session.add(item)
        db.session.commit()

        flash("Item was successfully updated.")
        return redirect(url_for('main.item_detail', item_id=item.id))

    return render_template('item_detail.html', item=item, form=form)

@main.route('/shopping_list')
@login_required
def shopping_list():
    return render_template('shopping_list.html')

@main.route('/add_to_shopping_list/<item_id>', methods=['POST'])
@login_required
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)

    current_user.shopping_list_items.append(item)
    db.session.commit()

    flash("Item added to shopping list.")
    return redirect(url_for('main.item_detail', item_id=item_id))

@main.route('/remove_from_shopping_list/<item_id>', methods=['POST'])
@login_required
def remove_from_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)

    current_user.shopping_list_items.remove(item)
    db.session.commit()

    flash("Item removed from shopping list.")
    return redirect(request.referrer)
