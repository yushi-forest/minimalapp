from flask import Flask, render_template, url_for,request, current_app, g, redirect

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello, Flaskbook"

@app.route("/hello/<name>",methods=['GET','POST'],endpoint="hello-endpoint")
def hello(name):
    return f"Hello, {name}!"

@app.route("/name/<name>")
def show_name(name):
    return render_template("index.html",name=name)

with app.test_request_context():
    #/
    print(url_for("index"))
    #/hello/world
    print(url_for("hello-endpoint", name="world"))
    #/name/ichiro?page=1
    print(url_for("show_name", name="ichiro", page=1))


#ここで呼び出すとエラーになる
#print(current_app)

#アプリケーションコンテキストを取得してスタックにpushする
ctx = app.app_context()
ctx.push()

with app.test_request_context("/uses?updated=ture"):
    #tureが出力される
    print(request.args.get("updated"))

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
    if request.method == "POST":
        #メールを送る

       #contactエンドポイントへリダイレクトする
       return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")

   
