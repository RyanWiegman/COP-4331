from flask import render_template, url_for, flash, redirect, request
from restaurant import app, db, bcrypt
from restaurant.userForms import registerForm, loginForm, AccountUpdateForm, adjustMenu
from restaurant.databases import User, Order, Menu
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")
def home() :
    #image_icon = url_for('static', filename = 'image/' + current_user.image_icon)
    return render_template("home.html")

@app.route("/about")
def about() :
    return render_template("about.html", title = "aboutpage")

@app.route("/menu", methods= ['GET' , 'POST'])
def menu() :
    food = Menu.query.all()
    if request.method == 'POST':
        order_id = request.form.get('save_order')

        if order_id is not None :
            item = Order(orderName = Menu.query.get(order_id).orderName, description = Menu.query.get(order_id).description, price = Menu.query.get(order_id).price, userID = current_user.username)
            db.session.add(item)
            db.session.commit()
            flash(f'Item added to order.', 'success')
    
    return render_template('menu.html', title = 'Menu', food = food)

@app.route('/register', methods= ['GET', 'POST'])
def register() :
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    
    resForm = registerForm()
    if resForm.validate_on_submit() :
        hashedPassword = bcrypt.generate_password_hash(resForm.password.data).decode('utf-8')
        user = User(username = resForm.username.data, email = resForm.email.data, password = hashedPassword)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', resForm = resForm)

@app.route('/login', methods= ['GET', 'POST'])
def login() :
    if current_user.is_authenticated :
        return redirect(url_for('home'))
    
    login = loginForm()
    if login.validate_on_submit() :
        user = User.query.filter_by(email = login.email.data).first()
        if user and bcrypt.check_password_hash(user.password, login.password.data) :
            login_user(user)
            return redirect(url_for('home'))
        else :
           flash('Logged In', 'danger')
    return render_template('login.html', title = 'Login', login = login)

@app.route('/logout')
def logout() : 
    logout_user()
    return redirect(url_for('home'))

@app.route('/account', methods= ['GET', 'POST'])
@login_required
def account() :
    update = AccountUpdateForm()
    if update.validate_on_submit() :
        current_user.username = update.username.data
        current_user.email = update.email.data
        db.session.commit()
        flash('Account update.', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET' :
        update.username.data = current_user.username
        update.email.data = current_user.email

    image_icon = url_for('static', filename = 'image/' + current_user.image_icon)
    return render_template('account.html', title = 'Account', image_icon = image_icon, update = update)

@app.route('/order', methods= ['GET', 'POST'])
def order() :
    total_price = 0.00
    order = Order.query.all()
    user = current_user.username

    for items in order :
        if items.userID == current_user.username :
            total_price = total_price + float(items.price)
    total_price = round(total_price, 2)

    if request.method == 'POST':
        user_name = request.form.get('complete')

        if user_name is not None :
            for items in order :
                if user_name == items.userID :
                    items.complete = True
                    db.session.commit()
            flash(f'Order Complete.', 'success')
        
    return render_template('order.html', order = order, total_price = total_price, user = user)
 
##admin only
@app.route('/adjustMenu', methods= ['GET', 'POST'])
@login_required
def adjust_menu() :
    adjMenu = adjustMenu()
    if adjMenu.validate_on_submit() :
        item = Menu(orderName = adjMenu.Name.data, description = adjMenu.description.data, price = adjMenu.price.data)
        db.session.add(item)
        db.session.commit()
        flash('Item created', 'success')
        return redirect(url_for('adjust_menu'))
    return render_template('adjust_menu.html', title = 'Adjust Menu', adjMenu = adjMenu)

@app.route('/serve', methods= ['GET', 'POST'])
@login_required
def serve() :
    temp_order = []
    order = Order.query.all()
    name = []
    
    for items in order :
        if items.complete :
            temp_order.append(items)
            name.append(items.userID) 
    name = list(dict.fromkeys(name))

    if request.method == 'POST':
        temp_name = request.form.get('finish')

        if temp_name is not None :
            for items in order :
                if temp_name == items.userID :
                    db.session.delete(items)
                    db.session.commit()
            flash(f'Order ready for pickup!', 'success')
            return redirect(url_for('serve'))

    
    return render_template('serve.html', order = temp_order, name = name)