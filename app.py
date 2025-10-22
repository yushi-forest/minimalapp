from email_validator import validate_email, EmailNotValidError

from flask import (
        Flask, 
        render_template, 
        url_for,
        request, 
        current_app, 
        g, 
        redirect,
        flash,
)
import logging
from flask_debugtoolbar import DebugToolbarExtension 

app = Flask(__name__)
#SERCH_KEYを追加する
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBs"
#ログレベルを設定する
app.logger.setLevel(logging.DEBUG)
#リダイレクトを中断しないようにする
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
#DebugToolbarExtensionにアプリケーションを設定する
toolbar = DebugToolbarExtension(app)

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
        #form属性を使って、フォーム値を取得する
        username = request.form["username"]
        email = request.form["email"]
        description = request.form["description"]

        #入力チェック
        is_valid = True

        if not username:
            flash("ユーザー名は必須です")
            is_valid = False

        if not email:
                  flash("メールアドレスは必須です")
                  is_valid = False

        try:
                  validate_email(email)
        except EmailNotValidError:
                  flash("メールアドレスの形式で入力してください")
                  is_valid = False

        if not description:
                  flash("お問い合わせ内容は必須です")
                  is_valid = False

        if not is_valid:
            return redirect(url_for("contact"))
        #メールを送る

       #contactエンドポイントへリダイレクトする
        flash("お問い合わせ内容はメールにて送信いたしました。お問い合わせありがとうございます。")
        return redirect(url_for("contact_complete"))

    return render_template("contact_complete.html")

   
