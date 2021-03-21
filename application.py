import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from datetime import date
from flask_session import Session
from tempfile  import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from other_f import login_required

app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)



db = SQL("sqlite:///bookstore.db")

@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET":
        return render_template("login.html")
    else:
        uname = request.form.get("username")
        passs = request.form.get("password")  
        if not uname or not passs:
            return render_template("apology.html")
        else:
            rows = db.execute("SELECT * FROM users WHERE username=:username", username=uname)
            if len(rows) == 0:
                return render_template("apology.html")
            if not check_password_hash(rows[0]["password"], passs):
                return render_template("apology.html", pas=passs, hashed=rows[0]["password"])
            session["user_id"] = rows[0]["id"]
            return redirect("/")



@app.route("/admin", methods=["GET", "POST"])

def admin():
    ide = "kalra234@gmail.com"
    passs = "varun123"
    if request.method == "GET":
        return render_template("admin.html")
    else:
        username = request.form.get("username")
        pas = request.form.get("password")
        if username != ide or pas != passs:
            return render_template("apology.html")
        session["user_id"] = 100
        rows = db.execute("SELECT * FROM requests")
        return render_template("adminindex.html",row=rows)



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if confirmation != password:
            return render_template("apology.html")
        if not name or not password or not confirmation:
            return render_template("apology.html")
        else:
            rows = db.execute("SELECT * FROM users WHERE username = :username", username = name)
            if len(rows) != 0:
                return render_template("apology.html")
            hashed = generate_password_hash(password)
            db.execute("INSERT INTO users (username, password, cash) VALUES(:username, :password, :cash)", username=name, password=hashed, cash = 200)
    return redirect("/")



@app.route("/", methods=["GET"])
def index():
    rows = db.execute("SELECT * FROM users")
    ebooks = db.execute("SELECT name  FROM books WHERE category = :category", category = "ebook")
    textbooks = db.execute("SELECT name  FROM books WHERE category = :category", category = "textbook")
    
    return render_template("index.html", row=textbooks, cate = ebooks)




@app.route("/addbooks", methods=["GET", "POST"])
@login_required
def add():
    name = request.form.get("name")
    description = request.form.get("descr")
    category = request.form.get("category")
    price = float(request.form.get("price"))
    discount = int(request.form.get("discount"))
    count = int(request.form.get("stock"))
    if not name or not description or not category or not price or not discount or not count:
        return render_template("apology.html")
    else:
        discounted = (price - ((price * discount) / 100))
        db.execute("INSERT INTO books (name, description, category, price, discount, bks) VALUES (:name, :description, :category, :price, :discount, :count)", name = name, description = description, category = category, price = discounted, discount = discount, count = count)
    return render_template("adminindex.html")




@app.route("/delete", methods=["GET","POST"])
@login_required
def delete():
    bookn = request.form.get("bookn")
    if not bookn:
        return render_template("apology.html")
    rows = db.execute("SELECT * FROM books WHERE name = :name", name = bookn)
    if len(rows) == 0:
        return render_template("apology.html")
    db.execute("DELETE * FROM books WHERE name = :name", name = bookn)
    return redirect("/admin")





@app.route("/ban", methods=["POST"])
@login_required
def ban():
    if request.method == "POST":
        usern = request.form.get("usr")
        if not usern:
            return render_template("apology.html")
        else:
            rows = db.execute("SELECT * FROM users WHERE username = :username", username = usern)
            if not rows:
                return render_template("apology.html")
            else:
                db.execute("UPDATE users SET flag = :value WHERE username = :username", username = usern, value = False)
                db.execute("INSERT INTO notify (action, username) VALUES (:action, :username)", action="You are temporarily restricted to use our services ", username=username)
                return redirect("/admin")



@app.route("/subscribe", methods=["GET","POST"])
@login_required
def subscribe():
    if request.method == "GET":
        return render_template("subscribe.html")
    else:
        response = request.form.get("confirm")
        if response == "yes":
            db.execute("INSERT INTO notify (action, username) VALUES (:action, :username)", action="Thanks for subscribing our Newsletters.. Best Regards BOOKSTORE", username=username)
            return redirect("/subscribe")
    return redirect("/subscribe")



@app.route("/ebook", methods=["GET"])
def ebook():
    rows=db.execute("SELECT * FROM books WHERE category = :category", category = "ebook")
    return render_template("list.html", row=rows)

@app.route("/textbook", methods=["GET"])
def text():
    rows=db.execute("SELECT * FROM books WHERE category = :category", category = "textbook")
    return render_template("list.html", row=rows)

@app.route("/offer", methods=["GET"])
def offer():
    rows = db.execute("SELECT * FROM books WHERE discount = :discount", discount=10)
    return render_template("list.html", row=rows)


@app.route("/search", methods=["POST"])
def search():
    query = request.form.get("query")
    if not query:
        return render_template("apology.html")
    rows = db.execute("SELECT * FROM books WHERE name = :name", name = query)
    if not rows:
        return render_template("apology.html")
    return render_template("list.html", row = rows)



@app.route("/buys", methods=["POST"])
def buys():
    bookid=request.form.get("bookid")
    rows = db.execute("SELECT * FROM books WHERE book_id = :bookid", bookid=bookid)
    return render_template("buy.html", row=rows)


@app.route("/buy", methods=["GET","POST"])
@login_required
def buy():
    bookid=request.form.get("bookid")
    address=request.form.get("address")
    price=request.form.get("price")
    username = db.execute("SELECT username FROM users WHERE id = :uide", uide=int(session['user_id']))[0]["username"]
    row = db.execute("SELECT * FROM users WHERE username=:username", username=username)
    rows = db.execute("SELECT * FROM books WHERE book_id = :bookid", bookid=bookid)
    cash=row[0]["cash"]
    prices=rows[0]["price"]
    count = rows[0]["bks"]
    if cash < float(price):
        return render_template("apology.html")
    elif count == 0:
        return render_template("apology.html")
    else:
        db.execute("UPDATE users SET cash=cash- :prices", prices=prices)
        db.execute("UPDATE books SET bks=bks - :value", value=1)
        db.execute("INSERT INTO requests (bookid, username, address) VALUES (:bookid, :username, :address)", bookid=bookid, username=username, address=address)
        db.execute("INSERT INTO buy (book_id, user, price, address) VALUES (:bookid, :username, :price, :address)", bookid=bookid, username=username, price=price, address=address)
        db.execute("INSERT INTO notify (action, username) VALUES (:action, :username)", action="We have recieved your order.. Best Regards BOOKSTORE", username=username)
    return redirect("/")


@app.route("/cart", methods=["GET", "POST"])
@login_required
def cart():
    if request.method == "GET":
        username = db.execute("SELECT username FROM users WHERE id = :uide", uide=int(session['user_id']))[0]["username"]
        rows = db.execute("SELECT * FROM cart WHERE username = :username", username=username)
        row = dict()
        length = len(rows)
        for ro in range(length):
            ids=rows[ro]["book_id"]
            row = db.execute("SELECT * FROM books WHERE book_id = :bookid", bookid=ids)
        return render_template("cart.html", row=row)
    else:
        bookid=request.form.get("bookid")
        username = db.execute("SELECT username FROM users WHERE id = :uide", uide=int(session['user_id']))[0]["username"]
        db.execute("INSERT INTO cart (book_id, username) VALUES (:bookid, :username)", bookid=bookid, username=username)
        rows = db.execute("SELECT * FROM cart ")
        db.execute("INSERT INTO notify (action, username) VALUES (:action, :username)", action="Added an item to the cart... Best Regards BOOKSTORE", username=username)
        return redirect("/")
    return redirect("/")

@app.route("/wishlist", methods=["GET", "POST"])
@login_required
def wishlist():
    if request.method == "GET":
        username = db.execute("SELECT username FROM users WHERE id = :uide", uide=int(session['user_id']))[0]["username"]
        rows = db.execute("SELECT * FROM wishlist WHERE username = :username", username=username)
        row = dict()
        length = len(rows)
        for ro in range(length):
            ids=rows[ro]["book_id"]
            row = db.execute("SELECT * FROM books WHERE book_id = :bookid", bookid=ids)
        return render_template("wishlist.html", row=row)
    else:
        bookid=request.form.get("bookid")
        username = db.execute("SELECT username FROM users WHERE id = :uide", uide=int(session['user_id']))[0]["username"]
        db.execute("INSERT INTO wishlist (book_id, username) VALUES (:bookid, :username)", bookid=bookid, username=username)
        db.execute("INSERT INTO notify (action, username) VALUES (:action, :username)", action="Added an item to the Wishlist... Best Regards BOOKSTORE", username=username)
        
    return redirect("/")





@app.route("/remove_item", methods=["GET","POST"])
@login_required
def remove():
    bookid=request.form.get("bookid")
    username = db.execute("SELECT username FROM users WHERE id = :uide", uide=int(session['user_id']))[0]["username"]
    db.execute("DELETE FROM cart WHERE book_id=:bookid AND username=:username", bookid=bookid, username=username )
    db.execute("INSERT INTO notify (action, username) VALUES (:action, :username)", action="Removed item From cart.. Best Regards BOOKSTORE", username=username)
    return redirect("/")


@app.route("/remove_wish", methods=["GET","POST"])
@login_required
def remove_wish():
    bookid=request.form.get("bookid")
    username = db.execute("SELECT username FROM users WHERE id = :uide", uide=int(session['user_id']))[0]["username"]
    db.execute("DELETE FROM wishlist WHERE book_id=:bookid AND username=:username", bookid=bookid, username=username )
    db.execute("INSERT INTO notify (action, username) VALUES (:action, :username)", action="Removed a book from Wishlist.. Best Regards BOOKSTORE", username=username)
    return redirect("/")



@app.route("/balance", methods=["GET", "POST"])
@login_required
def balance():
    if request.method == "GET":
        username = db.execute("SELECT username FROM users WHERE id = :uide", uide=int(session["user_id"]))[0]["username"]
        row = db.execute("SELECT cash FROM users WHERE username = :username", username=username)
        return render_template("cash.html", row=row)
    else:
        username = db.execute("SELECT username FROM users WHERE id = :uide", uide=int(session["user_id"]))[0]["username"]
        amount = request.form.get("amount")
        db.execute("UPDATE users SET cash = cash + :amount", amount=amount)
        rows = db.execute("SELECT cash FROM users WHERE username=:username", username=username)
        db.execute("INSERT INTO notify (action, username) VALUES (:action, :username)", action="Successfully added cash to the wallet. Enjoy reading with bookstore... Best Regards BOOKSTORE", username=username)
        return render_template("cash.html", row=rows)



@app.route("/profile", methods=["GET"])
@login_required
def profile():
    username=db.execute("SELECT username FROM users WHERE id = :uide", uide=int(session["user_id"]))[0]["username"]
    rows = db.execute("SELECT * FROM users WHERE username=:username", username=username)
    return render_template("myProfile.html", row=rows)



@app.route("/orders", methods=["GET"])
@login_required
def order():
    username = db.execute("SELECT username FROM users WHERE id=:uide", uide = int(session["user_id"]))[0]["username"]
    rows = db.execute("SELECT * FROM buy WHERE user = :username", username=username)
    row = dict()
    length = len(rows)
    for ro in range(length):
        ids=rows[ro]["book_id"]
        row = db.execute("SELECT * FROM books WHERE book_id = :bookid", bookid=ids)
    return render_template("orders.html", row=row)



@app.route("/change_user", methods=["POST"])
@login_required
def change_name():
    username = request.form.get("username")
    usernames = request.form.get("usernames")
    if not usernames:
        return render_template("apology.html")
    rows = db.execute("SELECT * FROM users WHERE username=:username", username=username)
    if not rows:
        return render_template("apology.html")
    else:
        db.execute("UPDATE users SET username = :username", username=usernames)
        nrow = db.execute("SELECT * FROM users WHERE id = :uide", uide = int(session["user_id"]))[0]["username"]
        db.execute("INSERT INTO notify (action, username) VALUES (:action, :username)", action="We have noticed you have changed your username.. Best Regards BOOKSTORE", username=username)
        return render_template("myProfile.html", row=nrow)



@app.route("/change_pass", methods=["POST"])
@login_required
def change_pass():
    current = request.form.get("current")
    new = request.form.get("new")
    confirm = request.form.get("confirm")
    if not current or not new or not confirm:
        return render_template("apology.html")
    if confirm != new:
        return render_template("apology.html")

    rows = db.execute("SELECT password FROM users WHERE id = :uide", uide=int(session["user_id"]))[0]["password"]
    print(rows)
    if not rows:
        return render_template("apology.html")
    else:
        if not check_password_hash(rows, current):
            return render_template("apology.html")
        hashed = generate_password_hash(new)
        db.execute("UPDATE users SET password = :password", password=hashed)
        username = db.execute("SELECT username FROM users WHERE id = uide", uide=int(session["user_id"]))[0]["username"]
        db.execute("INSERT INTO notify (action, username) VALUES (:action, :username)", action="We have noticed you have changed your password.. Best Regards BOOKSTORE", username=username)
        return redirect("/profile")


@app.route("/delreq", methods=["POST"])
@login_required
def req():
    bookid = request.form.get("bookid")
    username = request.form.get("username")
    if not bookid or not username:
        return render_template("apology.html")
    db.execute("DELETE FROM requests WHERE bookid = :bookid AND username=:username", bookid=bookid, username=username)
    db.execute("INSERT INTO notify (action, username) VALUES (:action, :username)", action="Your Order will be delivered soon.. Best Regards BOOKSTORE", username=username)
    rows = db.execute("SELECT * FROM requests")
    return render_template("adminindex.html", row=rows)


@app.route("/notify", methods=["GET"])
@login_required
def notify():
    username = db.execute("SELECT username FROM users WHERE id = :uide", uide = int(session["user_id"]))[0]["username"]
    rows = reversed(db.execute("SELECT * FROM notify WHERE username = :username", username= username))
    return render_template("notification.html", row = rows)


if __name__ == "__main__":
    app.run(debug = True)

#CREATE TABLE IF NOT EXISTS 'users'('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' TEXT NOT NULL, 'password' TEXT NOT NULL, 'flag' BOOLEAN NOT NULL DEFAULT True, 'cash' REAL NOT NULL);
#CREATE TABLE IF NOT EXISTS 'books'('book_id' INTEGER NOT NULL AUTOINCREMENT PRIMARY KEY,'name' TEXT NOT NULL,'description' TEXT NOT NULL, 'category' TEXT NOT NULL, 'price' TEXT NOT NULL, 'discount' TEXT NOT NULL, 'bks' INTEGER NOT  NULL);