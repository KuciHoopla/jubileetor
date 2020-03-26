import random

from flask import Flask, render_template, request, url_for, redirect, session
from database.customers_table import insert_customer, get_customer_email_password, get_customer_data, insert_gift, \
    get_customer_name_and_last_gift

app = Flask(__name__)
app.secret_key = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b82'


@app.route('/')
def view_welcome_page():
    customers_data = get_customer_name_and_last_gift()
    if customers_data:
        return render_template("welcome_page.jinja2", customers_data=customers_data)
    return render_template("welcome_page.jinja2")


@app.route("/login/", methods=["GET"])
def view_login():
    return render_template("login.jinja2")


@app.route("/customer/<id_customer>/")
def view_customer(id_customer):
    customer_data = get_customer_data(id_customer)
    gifts = customer_data[2]
    photo_link = f'photos/profile_photos/{id_customer}.jpg'
    if customer_data:
        return render_template("customer.jinja2", customer_data=customer_data,
                               gifts=gifts,
                               id_customer=id_customer,
                               photo_link=photo_link)

    return render_template("customer_not_found.jinja2", id_customer=id_customer)


@app.route("/login/", methods=["POST"])
def login_user():
    try:
        email = request.form["email"]
        password = request.form["password"]
        customer_email = get_customer_email_password(email)[0]
        customer_password = get_customer_email_password(email)[1]
        id_customer = get_customer_email_password(email)[2]
        if email == customer_email and password == customer_password:
            session["logged"] = True
            return redirect(url_for("view_customer", id_customer=id_customer))
        else:
            return redirect(url_for("view_login"))
    except:
        redirect(url_for("view_login"))


@app.route("/register_site/", methods=['GET', 'POST'])
def view_register():
    return render_template("register.jinja2")


@app.route("/register/", methods=['GET', 'POST'])
def register():
    try:
        if request.method == "POST":
            first_name = request.form["name"]
            last_name = request.form["surname"]
            email = request.form["email"]
            password = request.form["password"]
            birthday = request.form["birthday"]
            print(birthday)
            insert_customer(first_name, last_name, email, password, birthday)
            if len(email) < 1 or len(password) < 1:
                print("no email or password")
                return redirect(url_for("view_register"))
            else:
                return redirect(url_for("view_login"))
        else:
            return redirect(url_for("view_register"))

    except:
        return redirect(url_for("view_register"))


@app.route("/customer/<id_customer>/", methods=['GET', 'POST'])
def add_gift(id_customer):
    try:
        if request.method == "POST" and request.files["giftPhoto"] or request.form["link"]:
            gift_photo = request.files["giftPhoto"]
            num = random.randrange(100000000000)
            photo_link = f'photos/gift_photos/{num}.jpg'
            photo_name = f'{num}.jpg'
            photo_directory_link = f'static/photos/gift_photos/{photo_name}'
            if gift_photo:
                gift_photo.save(photo_directory_link)
            link = request.form["link"]
            description = request.form["description"]
            insert_gift(id_customer, photo_link, link, description)
            return redirect(url_for("view_customer", id_customer=id_customer))
    except:
        print("no gift was added")
    try:
        if request.method == "POST" and request.files["inputFile"]:
            photo = request.files["inputFile"]
            photo_link = f'static/photos/profile_photos/{id_customer}.jpg'
            photo.save(photo_link)
            return redirect(url_for("view_customer", id_customer=id_customer))
    except:
        print('no inputed file')
    return redirect(url_for("view_customer", id_customer=id_customer))


@app.route("/", methods=["POST"])
def logout_user():
    session.pop("logged")
    return redirect(url_for("login_user"))


if __name__ == '__main__':
    host = "0.0.0.0"
    app.run(host, debug=True)
