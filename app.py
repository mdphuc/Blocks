from flask import Flask, make_response, redirect, url_for, render_template,request, session, flash, jsonify
from flask_login.utils import logout_user
from flask_migrate import Migrate, migrate
from datetime import  timedelta, datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, current_user, login_user
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from sqlalchemy.sql import func
import hashlib
import os






ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.secret_key = hashlib.sha512("hello".encode()).hexdigest()
app.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=3)
app.config['suppress_callback_exception'] = True

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

db = SQLAlchemy(app)

migrate = Migrate(app, db)

s = URLSafeTimedSerializer(app.secret_key)



#database

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    username = db.Column(db.String(30))
    email = db.Column(db.String(40)) 
    password = db.Column(db.String(30))
    pic = db.relationship("Profile", backref="user",uselist = False)

    post = db.relationship("Post", backref = "user", uselist = False)
    about = db.relationship("About", backref = "user", uselist = False)
    friendrequest = db.relationship("FriendRequest", backref = "user", uselist = False)
    friend = db.relationship("Friend", backref = "user", uselist = False)
    like = db.relationship("Like", backref = "user", uselist = False)
    notification = db.relationship("Notification", backref = "user", uselist = False)

    def __init__(self, username, email, password):
        super().__init__()
        self.username = username
        self.email = email
        self.password = password
  
    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.password}')"

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique=True)
    img_path = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id' , ondelete= "CASCADE"))

    def __init__(self, img_path, user_id):
        super().__init__()
        self.img_path = img_path
        self.user_id = user_id
        
  
    def __repr__(self):
        return f"Profile('{self.img_path}','{self.user_id}')"





class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    text = db.Column(db.Text)
    image = db.Column(db.Text)
    date_created = db.Column(db.String(20))
    author = db.Column(db.String(30))
    author_img_path = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"))
    comment = db.relationship("Comment", backref = "post")
    like =  db.relationship("Like", backref = "post")

    def __init__(self, text, image, date_created, author, author_img_path, author_id):
        super().__init__()
        self.text = text
        self.image = image
        self.date_created = date_created
        self.author = author
        self.author_img_path = author_img_path
        self.author_id = author_id
    
    def __repr__(self):
        return f"Post('{self.text}','{self.image}', '{self.date_created}','{self.author}', '{self.author_img_path}','{self.author_id}')"

class About(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    text = db.Column(db.Text)
    date_created = db.Column(db.String(20))
    author = db.Column(db.String(30))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"))

    def __init__(self, text, date_created, author, author_id):
        super().__init__()
        self.text = text
        self.date_created = date_created
        self.author = author
        self.author_id = author_id
    
    def __repr__(self):
        return f"About('{self.text}', '{self.date_created}','{self.author}','{self.author_id}')"

class FriendRequest(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    date_created = db.Column(db.Text)
    receiver = db.Column(db.String(20))
    receiver_id = db.Column(db.Integer)
    receiver_img_path = db.Column(db.Text)
    author = db.Column(db.String(20))
    author_img_path = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"))

    def __init__(self, date_created,  receiver, receiver_id, receiver_img_path, author, author_img_path, author_id):
        super().__init__()
        self.date_created = date_created
        self.receiver = receiver
        self.receiver_id = receiver_id
        self.receiver_img_path = receiver_img_path
        self.author = author
        self.author_img_path = author_img_path
        self.author_id = author_id
    
    def __repr__(self):
        return f"FriendRequest('{self.date_created}', '{self.receiver}','{self.receiver_id}','{self.receiver_img_path}','{self.author}','{self.author_img_path}','{self.author_id}')"

class Friend(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    date_created = db.Column(db.Text)
    friend = db.Column(db.String(20))
    friend_id = db.Column(db.Integer)
    friend_img_path = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"))

    def __init__(self, date_created,  friend, friend_id, friend_img_path, user_id):
        super().__init__()
        self.date_created = date_created
        self.friend = friend
        self.friend_id = friend_id
        self.friend_img_path = friend_img_path
        self.user_id = user_id
    
    def __repr__(self):
        return f"Friend('{self.date_created}', '{self.friend}','{self.friend_id}','{self.friend_img_path}','{self.user_id}')"

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    text = db.Column(db.Text)
    date_created = db.Column(db.String(20))
    author = db.Column(db.String(30))
    author_img_path = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete = "CASCADE"))

    def __init__(self, text, date_created, author, author_img_path, author_id, post_id):
        super().__init__()
        self.text = text
        self.date_created = date_created
        self.author = author
        self.author_id = author_id
        self.author_img_path = author_img_path
        self.post_id = post_id

    def __repr__(self):
        return f"Comment('{self.text}', '{self.date_created}','{self.author}','{self.author_img_path}','{self.author_id}','{self.post_id}')"

class Like(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    date_created = db.Column(db.String(20))
    author = db.Column(db.String(30))
    author_img_path = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete = "CASCADE"))

    def __init__(self, date_created, author, author_img_path, author_id, post_id):
        super().__init__()
        self.date_created = date_created
        self.author = author
        self.author_img_path = author_img_path
        self.author_id = author_id
        self.post_id = post_id

    def __repr__(self):
        return f"Like('{self.text}', '{self.date_created}','{self.author}', '{self.author_img_path}', '{self.author_id}','{self.post_id}')"

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key = True, unique = True)
    text = db.Column(db.Text)
    date_created = db.Column(db.String(20))
    author = db.Column(db.String(30))
    author_img_path = db.Column(db.Text)
    author_id = db.Column(db.Integer)
    state = db.Column(db.String(10))
    post_id = db.Column(db.Integer)
    comment_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = "CASCADE"))

    def __init__(self,text, date_created, author, author_img_path, author_id, state, post_id, comment_id, user_id):
        super().__init__()
        self.text = text
        self.date_created = date_created
        self.author = author
        self.author_img_path = author_img_path
        self.author_id = author_id
        self.state = state
        self.post_id = post_id
        self.comment_id = comment_id
        self.user_id = user_id

    def __repr__(self):
        return f"Notification('{self.text}', '{self.date_created}','{self.author}', '{self.author_img_path}', '{self.author_id}', '{self.state}','{self.post_id}','{self.comment_id}', '{self.user_id}')"



#back-end
def notification_def(text, id, post_id, category, comment_id):
  if current_user.is_authenticated and current_user.id == id:
    if category == "post":
      now = datetime.now()
      date_created = now.strftime("%Y %D %H:%M:%S")

      friends = Friend.query.filter_by(user_id = id).all()
      for friend in friends:
        notification = Notification(text=f"{text}", date_created=date_created, author=current_user.username, author_img_path= current_user.pic.img_path, author_id=current_user.id, state="unseen", post_id=post_id , comment_id = comment_id, user_id= friend.friend_id)
        
        db.session.add(notification)

      db.session.commit()
    elif category == "comment" or category == "like":
      now = datetime.now()
      date_created = now.strftime("%Y %D %H:%M:%S")
      user = User.query.filter_by(id = id).first()
      post = Post.query.filter_by(id = post_id).first()
      comment = Comment.query.filter_by(id = comment_id).first()

      if post is not None:
        if post.author_id != id and user is not None:
          if category == "like":
            notification = Notification(text=f"{text}", date_created=date_created, author=user.username, author_img_path= user.pic.img_path, author_id=user.id, state="unseen", post_id=post.id, comment_id = comment_id, user_id= post.author_id)
          elif comment is not None:
            notification = Notification(text=f"{text}", date_created=date_created, author=user.username, author_img_path= user.pic.img_path, author_id=user.id, state="unseen", post_id=post.id, comment_id= comment.id, user_id= post.author_id)
          db.session.add(notification)
          db.session.commit()

@app.route("/notification_seen/<int:id>", methods = ['POST'])
def notification_seen(id):
  if current_user.id == id:
    notifications = Notification.query.filter_by(user_id = id).all()
    for notification in notifications:
      notification.state = "seen"
    db.session.commit()
  
  return "thank"
    


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))




@app.route("/")
def home():
  if not current_user.is_authenticated:
    return render_template("base.html")

  if current_user.is_authenticated:
    img_path = url_for('static', filename = current_user.pic.img_path)
    notifications = Notification.query.filter_by(user_id = current_user.id).all()
    new_notifications = Notification.query.filter_by(user_id = current_user.id, state = "unseen").all()
    if len(notifications) == 0:
      return render_template("base.html", img_path = img_path, notification_check = 'no')
    else:
      return render_template("base.html", img_path = img_path, new_notifications = len(new_notifications), notifications = notifications, notification_check = 'yes')




@app.route("/login", methods = ["POST","GET"])
def login():
  if request.method == "POST":
    session.permanent = True
    username = request.form.get("uname")
    password = request.form.get("psw")
    remember = True if request.form.get("remember") is not None else False
    
    user1 = User.query.filter_by(username = username, password = hashlib.sha512(password.encode()).hexdigest()).first()
    user2 = User.query.filter_by(email = username, password = hashlib.sha512(password.encode()).hexdigest()).first()



    if user1 is not None or user2 is not None:
      try:
        login_user(user1, remember=remember)   
      except:
        login_user(user2, remember=remember)  
      return redirect(url_for("home"))
    else:
      flash("Invalid Credentials!", 'error')
      return redirect(url_for("login"))
  

  elif request.method == "GET":
    if 'remember' in session:
      username = session["username"]
      password = session["password"]
      remember = session["remember"]
      user = User.query.filter_by(username = username, password = hashlib.sha512(password.encode()).hexdigest()).first()
      login_user(user, remember=remember)

    return render_template("login.html")

@app.route("/register", methods = ["POST","GET"])
def register():
  if request.method == "POST":
    username = request.form.get("uname")
    email = request.form.get("email")
    password = request.form.get("psw")

    session["username"] = username
    session["email"] = email
    session["password"] = password
    
    user1 = User.query.filter_by(username = username).first()
    user2 = User.query.filter_by(email = email).first()

    if user1 is None and user2 is None:

      usr = User(username=username, email=email,password=hashlib.sha512(password.encode()).hexdigest())
      db.session.add(usr)
      db.session.commit()
      usr_check = User.query.filter_by(username=username).first()

      image = Profile(img_path = "images/profile_pics/default.png", user_id=usr_check.id)
      db.session.add(image)
      db.session.commit()

      about = About(text = "", date_created=0, author=username, author_id=usr_check.id)
      db.session.add(about)
      db.session.commit()


      flash("Sign up successfully!", category='info')
      session.pop("username", None)
      session.pop("password", None)
      session.pop("remember", None)
      session.pop("code", None)
      session.pop("allow", None)
      return redirect(url_for("register"))

    elif user1 is not None or user2 is not None:
      flash("Credentials existed!", category= 'error')
      return redirect(url_for("register"))
     
  else:
    return render_template("register.html")

@app.route("/recovery", methods = ["POST","GET"])
def recovery():
  return "This is recovery page"

@app.route("/verified/<token>", methods = ["POST","GET"])
def verified(token):
  try: 
    email_token = s.loads(token, salt='email-confirm', max_age=600)
    if request.method == "POST":
      code = request.form.get("code")
      code_ = session["code"]
      username = session["username"]
      email = session["email"]
      password = session["password"]

      if code == code_:
        usr = User(username=username, email=email,password=hashlib.sha512(password.encode()).hexdigest())
        db.session.add(usr)
        db.session.commit()
        usr_check = User.query.filter_by(username=username).first()

        image = Profile(img_path = "images/profile_pics/default.png", user_id=usr_check.id)
        db.session.add(image)
        db.session.commit()



        flash("Sign up successfully!", category='info')
        session.pop("username", None)
        session.pop("password", None)
        session.pop("remember", None)
        session.pop("code", None)
        session.pop("allow", None)
        return redirect(url_for("register"))
      else:
        flash("Invalid code!", 'error')
        return redirect(url_for("verified"))
    else:
      path = f'http:127.0.0.1/resend/{token}'
      return render_template('verified.html', path=path)

  except SignatureExpired or BadTimeSignature:
    return redirect(url_for("/"))

@app.route("/dashboard/<int:id>")
def dashboard(id):
  if current_user.id == id:
    posts = Post.query.filter_by(author_id = current_user.id).all()
    user_img_path = current_user.pic.img_path 
    user_name = current_user.username
    user_id = current_user.id
    about = About.query.filter_by(author_id = id).first()
    friends = Friend.query.filter_by(user_id = current_user.id).all()

    if len(friends) == 0:
      return render_template("dashboard.html", posts= posts, friend_check_ = 'false', user_id = user_id,  name = user_name, image_path = user_img_path, check = 'true', about = about.text)
    else:
      return render_template("dashboard.html", posts= posts, friend_check_ = "true", user_id = user_id, friends1 = friends, name = user_name, image_path = user_img_path, check = 'true', about = about.text)
  else:
    user = User.query.filter_by(id = id).first()
    if user is not None:

      user_img_path = user.pic.img_path 
      user_name = user.username
      user_id = user.id
      posts = Post.query.filter_by(author_id = id).all()

      friend_request1 = FriendRequest.query.filter_by(receiver_id = user.id, author_id = current_user.id).first()
      friends1 = Friend.query.filter_by(user_id = user.id).all()
      friends = Friend.query.filter_by(user_id = current_user.id).all()
        

      if len(friends1) == 0:
        friend_check = 'false'
      else:
        friend_check = "true"

      friend = ""

      if len(friends) != 0:
        for friend_ in friends:
          if friend_.friend_id ==  user_id:
            friend = "true"
          else:
            friend = "false"
      else:
        friend = "false"
      
      if friend_request1 is not None:
        return render_template("dashboard.html" , friend_request_check = "true" , friend = friend,  status = "sender" , posts= posts , friends1 = friends1 , friend_check_ = friend_check,  user_id = user_id, name = user_name, image_path = user_img_path, check = 'false')
      else:
        friend_request2 = FriendRequest.query.filter_by(receiver_id = current_user.id, author_id = user.id).first()
        if friend_request2 is not None:
          return render_template("dashboard.html" , friend_request_check = "true", friend = friend, status = "receiver" , friend_check_ = friend_check , friends1 = friends1,  friend_request = friend_request2,  posts= posts, user_id = user_id, name = user_name, image_path = user_img_path, check = 'false')
        else:
          return render_template("dashboard.html" , friend_request_check = "false", friend = friend,  posts= posts, friend_check_ = friend_check , friends1 = friends1, user_id = user_id, name = user_name, image_path = user_img_path, check = 'false')
        

    else:
      return redirect(url_for("/"))

@app.route("/add_friend/<int:user_id>/<name>", methods=['POST', 'GET'])
def add_friend(user_id, name):
  if current_user.is_authenticated:
    if current_user.id == user_id:
      if request.method == "POST":
        user = User.query.filter_by(username = name).first()
        if user is not None:
          now = datetime.now()
          date_created = now.strftime("%Y %D %H:%M:%S")
          friend_request_check = FriendRequest.query.filter_by(receiver_id = user.id, author_id = current_user.id).first()
          friend_request_check2 = FriendRequest.query.filter_by(receiver_id = current_user.id, author_id = user.id).first()
          
          if friend_request_check is None and friend_request_check2 is None:
            friend_request = FriendRequest(date_created=date_created, receiver=name, receiver_id=user.id, receiver_img_path=user.pic.img_path, author=current_user.username, author_img_path=current_user.pic.img_path, author_id= current_user.id)
            notification = Notification(text=" sent you a friend request", date_created= date_created, author = current_user.username, author_img_path= current_user.pic.img_path, author_id=current_user.id, state="unseen", post_id = 'none', comment_id=0, user_id=user.id)

            db.session.add(friend_request)
            db.session.add(notification)
            
            db.session.commit()


  return 'Finish'

@app.route("/unfriend/<int:current_user_id>/<int:user_id>", methods=['POST', 'GET'])
def unfriend(current_user_id, user_id):
  if current_user.is_authenticated:
    if current_user.id == current_user_id:
      if request.method == "POST":
        user = User.query.filter_by(id = user_id).first()
        if user is not None:
          friend_request = Friend.query.filter_by(friend_id = user_id, user_id = current_user_id).first()
          friend_request2 = Friend.query.filter_by(friend_id = current_user_id, user_id = user_id).first()
          
          if friend_request is not None and friend_request2 is not None:

            db.session.delete(friend_request)
            db.session.delete(friend_request2)
            
            db.session.commit()


  return 'Finish'

@app.route('/unsent_friend_request/<int:author_id>/<int:user_id>', methods = ['POST', 'GET'])
def unsent(author_id, user_id):
  if current_user.is_authenticated:
    if current_user.id == author_id:
      if request.method == "POST":
        notification = Notification.query.filter_by(author_id = author_id, user_id = user_id, text = " sent you a friend request").first()
        user = User.query.filter_by(id = user_id).first()
        friend_request_check = FriendRequest.query.filter_by(receiver_id = user.id, author_id = current_user.id).first()

        if friend_request_check is not None:
          db.session.delete(friend_request_check)

        if notification is not None:
          db.session.delete(notification)
        
        db.session.commit()
  
  return "Finish"

@app.route("/decline/<int:receiver_id>/<int:sender_id>", methods = ["POST" , "GET"])
def decline(receiver_id, sender_id):
  if current_user.is_authenticated:
    if current_user.id == receiver_id:
      if request.method == "POST":
        user = User.query.filter_by(id = receiver_id).first()
        friend_request = FriendRequest.query.filter_by(receiver_id = receiver_id, author_id = sender_id).first()
        notification_check = Notification.query.filter_by(text = " accepted your friend request", author_id = receiver_id, user_id = sender_id).first()

        if friend_request is not None and notification_check is None:
          db.session.delete(friend_request)

          notification = Notification.query.filter_by(author_id = sender_id, user_id = receiver_id, text = " sent you a friend request").first()
          if notification is not None:
            db.session.delete(notification)

          now = datetime.now()
          date_created = now.strftime("%Y %D %H:%M:%S")

          new_notification = Notification(text=" declined your friend request", date_created = date_created, author= user.username, author_img_path=user.pic.img_path, author_id=user.id, state="unseen", post_id='none', comment_id=0, user_id= sender_id)
          db.session.add(new_notification)

          db.session.commit()
  
  return "Finish"

@app.route("/accept/<int:receiver_id>/<int:sender_id>", methods = ["POST" , "GET"])
def accept(receiver_id, sender_id):
  if current_user.is_authenticated:
    if current_user.id == receiver_id:
      if request.method == "POST":
        user = User.query.filter_by(id = sender_id).first()
        user2 = User.query.filter_by(id = receiver_id).first()
        
        friend1_check = Friend.query.filter_by(friend_id = user.id, user_id = user2.id).first()
        friend2_check = Friend.query.filter_by(friend_id = user2.id, user_id = user.id).first()
        friend_request = FriendRequest.query.filter_by(receiver_id = receiver_id, author_id = sender_id).first()

        now = datetime.now()
        date_created = now.strftime("%Y %D %H:%M:%S")
        friend1 = Friend(date_created=date_created, friend= user.username, friend_id= user.id, friend_img_path=user.pic.img_path, user_id= user2.id)
        friend2 = Friend(date_created=date_created, friend= user2.username, friend_id= user2.id, friend_img_path=user2.pic.img_path, user_id= user.id)
        notification_check = Notification.query.filter_by(text = " declined your friend request", author_id = receiver_id, user_id = sender_id ).first()

        if friend1_check is None and friend2_check is None and friend_request is not None and notification_check is None:
          db.session.delete(friend_request)
          db.session.add(friend1)
          db.session.add(friend2)

          notification = Notification.query.filter_by(author_id = sender_id, user_id = receiver_id, text = " sent you a friend request").first()
          
          now = datetime.now()
          date_created = now.strftime("%Y %D %H:%M:%S")

          new_notification = Notification(text= " accepted your friend request", date_created=date_created, author=user2.username, author_img_path= user2.pic.img_path, author_id= user2.id, state="unseen", post_id = 'none', comment_id = 0, user_id= user.id)
          db.session.add(new_notification)

          if notification is not None:
            db.session.delete(notification)
          
  
          db.session.commit()
  
  return "Finish"

@app.route('/post/<int:post_id>/<int:comment_id>')
def post_(post_id, comment_id):
  user_id = current_user.id
  posts = Post.query.filter_by(id = post_id).all()
  if comment_id != 0:
    return render_template("post.html", posts = posts, post_id = post_id, comment_id = comment_id, scrollable = "yes", user_id = user_id)
  else:
    return render_template("post.html", posts = posts, post_id = post_id, scrollable = "yes", user_id = user_id)
 

@app.route("/post")
def post():
    user_id = current_user.id
    posts = Post.query.all()
    return render_template('post.html', posts = posts, user_id = user_id)

@app.route("/like/<int:post_id>/<int:user_id>",methods=["POST"])
def like(post_id, user_id):
  if current_user.id == user_id:
    post = Post.query.filter_by(id = post_id).first()
    like = Like.query.filter_by(author_id = current_user.id, post_id = post_id).first()

    notification = Notification.query.filter_by(text="liked your post!",author=current_user.username, author_img_path= current_user.pic.img_path, author_id=current_user.id, user_id= post_id).first()
    if post is not None:
      if like is not None and notification is not None:
        
        db.session.delete(like)
        db.session.delete(notification)
        db.session.commit()
        isliked = "already"
      elif like is not None and notification is None:
        
        db.session.delete(like)
        db.session.commit()
        isliked = "already"
      else:
        isliked = "notyet"
        now = datetime.now()
        date_created = now.strftime("%Y %D %H:%M:%S")
        like = Like(date_created=date_created, author=current_user.username, author_img_path= current_user.pic.img_path,author_id=current_user.id, post_id= post_id)
        db.session.add(like)
        notification_def(text = "liked your post!", post_id=post_id , id = current_user.id, category="like", comment_id=0)        

        db.session.commit()
    
    likes = Like.query.filter_by(post_id = post_id).all()
  if isliked == "already":
    res = make_response(jsonify({"isliked" : isliked , "likes" : len(likes)}))
  else:
    res = make_response(jsonify({"isliked" : isliked , "likes" : len(likes), "author" : like.author, "author_id" : like.author_id, "date_created" : like.date_created, "author_img_path" : like.author_img_path}))


  return res
 

@app.route("/create_post/<int:id>", methods = ["POST"])
@login_required
def create_post(id):
  if current_user.id == id:
    caption = request.form.get("caption")
    pic = request.files["pic"] 

    if len(pic.filename) != 0:
      filename = secure_filename(pic.filename)

      if allowed_file(filename):
        now = datetime.now()
        date_created = now.strftime("%Y %D %H:%M:%S")
        img_path = 'images/post/' + filename
        pic.save(os.path.join('static/' , img_path))
        post = Post(text = caption, image = img_path, date_created= date_created, author= current_user.username, author_img_path=current_user.pic.img_path , author_id= current_user.id)

        db.session.add(post)
        db.session.commit()

        filename_split = os.path.splitext(filename)
        filename_split_list = list(filename_split)
        filename_split_list[0] = str(current_user.id) + str(post.id)
        filename = filename_split_list[0] + filename_split_list[1]

        img_path2 = 'images/post/' + filename
        
        post.image = img_path2
        now = datetime.now()
        date_created = now.strftime("%Y %D %H:%M:%S")
       

        notification_def(text = "has just posted something!", post_id=post.id , id = id, category="post", comment_id=0)        

        db.session.commit()

        os.rename(f'static/{img_path}', f'static/{img_path2}')

        return redirect(url_for('post'))
      else:
        return redirect(url_for('post'))

    else:
      now = datetime.now()
      date_created = now.strftime("%Y %D %H:%M:%S")
      post1 = Post(text = caption, image = "no",date_created=date_created , author= current_user.username, author_img_path=current_user.pic.img_path , author_id = current_user.id)
      db.session.add(post1)


      
      db.session.commit()
      notification_def(text = "has just posted something!", post_id=post1.id , id = id, category="post", comment_id=0)        

      return redirect(url_for('post'))
  else:
    return redirect(url_for('post'))
  

@app.route('/create_comment/<int:id>' , methods = ["POST"])
def create_comment(id):
  req = request.get_json()
  now = datetime.now()
  date_created = now.strftime("%Y %D %H:%M:%S")

  cmt = Comment(text= req["text"], date_created = date_created, author=current_user.username, author_img_path=current_user.pic.img_path ,author_id=current_user.id, post_id=id)
  db.session.add(cmt)

  cmt2 = Comment.query.filter_by(date_created = date_created).first()
  notification_def(text = "commented on your post!", post_id=id , id = current_user.id, category="comment", comment_id=cmt2.id)
  db.session.commit()
  
  
  res = make_response(jsonify({"id": cmt2.id, "date_created" : cmt2.date_created,  "text":req["text"], "author":cmt2.author, "author_img_path": cmt2.author_img_path, "author_id" : cmt2.author_id, "post_id" : id}), 200)
 
  return res

   
@app.route('/delete_comment/<int:post_id>/<int:comment_id>', methods=["POST"])
@login_required
def delete_comment(post_id, comment_id):
  
  comment = Comment.query.filter_by(id = comment_id, post_id = post_id).first()
  if current_user.id == comment.author_id:
    db.session.delete(comment)  
    db.session.commit()
      
  res = make_response(jsonify({}))
  return res



@app.route('/delete_notification/<int:id>', methods=["POST"])
@login_required
def delete_notification(id):
  notification = Notification.query.filter_by(id = id).first()
  if current_user.id == notification.user_id:
    db.session.delete(notification)  
    db.session.commit()
    notifications = Notification.query.all()
    res = make_response(jsonify({"noti_id" : id, "notis" : len(notifications), "state" : "authorized"}), 200)
  else:
    res = make_response(jsonify({"state" : "unauthorized"}), 200)
  
  return res



@app.route('/edit_comment/<int:post_id>/<int:comment_id>', methods=["POST"])
@login_required
def edit_comment(post_id, comment_id):
  req = request.get_json()  
  cmt = Comment.query.filter_by(id = comment_id).first()
  cmt.text = req["text"]
  db.session.commit()

  res = make_response(jsonify({"id": cmt.id, "date_created" : cmt.date_created,  "text":req["text"], "author":cmt.author, "author_img_path": cmt.author_img_path, "author_id" : cmt.author_id, "post_id" : post_id}), 200)
  return res



@app.route('/delete_post/<int:id>', methods=["POST"])
@login_required
def delete_post(id):
  
  post = Post.query.filter_by(id = id).first()

  if current_user.id == post.author_id:
    comments = Comment.query.filter_by(post_id = post.id).all()
    likes = Like.query.filter_by(post_id = post.id).all()
    db.session.delete(post)
    for comment in comments:
      db.session.delete(comment)
    for like in likes:
      db.session.delete(like)
    db.session.commit()
    if post.image != 'no':
      os.remove(f'static/{post.image}')
  
  res = make_response(jsonify({}))

  
  return res

@app.route('/view/<int:id>')
@login_required
def get_img(id):
  user = User.query.filter_by(id = id).first()
  
  img_path = url_for('static',filename=user.pic.img_path)
  return render_template('view.html', img_path = img_path)

@app.route("/logout")
@login_required
def logout():
  if 'remember' not in session:
    try:
      session.pop('username')
      session.pop('password')
      session.pop('remember')
    except:
      pass

  logout_user()
  return redirect(url_for("home")) 

@app.route("/passchange", methods = ["POST","GET"])
@login_required
def passchange():
  if request.method == "POST":
    current_pass = request.form.get("currpsw")
    newpass = request.form.get("psw")
    renewpass = request.form.get("repsw")

    current_pass_check = User.query.filter_by(password = hashlib.sha512(current_pass.encode()).hexdigest()).first()
    if current_pass_check is None:
      flash("Invalid current password", category='error')
      return redirect(url_for("passchange"))
    elif current_pass_check is not None:
      if newpass != renewpass:
        flash("New Password not match", category='error')
        return redirect(url_for("passchange"))
      else:
        current_user.password = hashlib.sha512(newpass.encode()).hexdigest()
        try:
          db.session.commit()
          flash("Change password successfully", category='info')
          return redirect(url_for("passchange"))
        except:
          pass
  else:
    return render_template("passchange.html")

def allowed_file(filename):
  return '.' in filename and \
          filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/about/<int:id>" , methods = ["POST"])
@login_required
def about(id):
  if current_user.id == id:
    now = datetime.now()
    date_created = now.strftime("%Y %D %H:%M:%S")
    req = request.get_json()  
    about = About.query.filter_by(author_id = id).first()
    about.text = req["text"]
    about.date_created = date_created
    db.session.commit()

    res = make_response(jsonify({"date_created" : date_created,  "text":req["text"]}), 200)
    # return res
    return res


@app.route("/profilepict/<int:id>", methods=["POST","GET"])
@login_required
def profilepict(id):
  if current_user.id == id:
    if request.method == "POST":

      pic = request.files["pic"] 

      if len(pic.filename) == 0:
        flash("No file selected!", 'error')
        return redirect(url_for('profilepict'))  
      else:
        filename = secure_filename(pic.filename)

        img_check = Profile.query.filter_by(user_id = current_user.id).first()

        filename_split = os.path.splitext(filename)
        filename_split_list = list(filename_split)
        filename_split_list[0] = str(current_user.id)
        filename_split_list[1] = ".png"
        filename = filename_split_list[0] + filename_split_list[1]

        if allowed_file(filename):
          pic.save(os.path.join('static/images/profile_pics' , filename))
          path = 'images/profile_pics/' + filename
          if img_check is None:
            img_path = Profile(img_path = path, user_id=current_user.id)
            posts = Post.query.filter_by(author_id = current_user.id).all()
            friends = Friend.query.filter_by(friend_id = current_user.id).all()
            comments = Comment.query.filter_by(author_id = current_user.id).all()
            likes = Like.query.filter_by(author_id = current_user.id).all()
            notifications = Notification.query.filter_by(author_id = current_user.id).all()

            for post in posts:
              post.author_img_path = path
              db.session.commit()

            for friend in friends:
              friend.author_img_path = path
              db.session.commit()

            for comment in comments:
              comment.author_img_path = path
              db.session.commit()

            for like in likes:
              like.author_img_path = path
              db.session.commit()

            for notification in notifications:
              notification.author_img_path = path
              db.session.commit()            
            
            

            db.session.add(img_path)
            db.session.commit()

            flash("Change successfully!", 'info')
            return redirect(url_for('profilepict'))
          else:
            img_check.img_path = path
            try:
              posts = Post.query.filter_by(author_id = current_user.id).all()
              for post in posts:
                post.author_img_path = path
            except:
              pass

            db.session.commit()   

            flash("Upload successfully!", 'info')
            return redirect(url_for("profilepict", id = current_user.id))
        else:
          flash("Invalid file extension!", 'error')
          return redirect(url_for("profilepict"))

     
  return render_template("profilepict.html")
  


@app.route("/delete/<int:id>")
@login_required
def delete(id):
    if current_user.id == id:
      if current_user.pic.img_path != 'images/profile_pics/default.png':
        os.remove(f"static/{current_user.pic.img_path}")

      session.pop("username", None)
      session.pop("password", None)
      session.pop("remember", None)
      user = User.query.filter_by(id = current_user.id).first()
      posts = Post.query.filter_by(author_id = user.id).all()
      profile = Profile.query.filter_by(user_id = id).first()
      about = About.query.filter_by(author_id = id).first()
      friends = Friend.query.filter_by(user_id = id).all()
      for post in posts:
        for comment in post.comment:
          db.session.delete(comment)
        for like in post.like:
          db.session.delete(like)
        db.session.delete(post)

      db.session.delete(user)
      db.session.delete(profile)
      try: 
        db.session.delete(about)
      except:
        pass
      for friend in friends:
        db.session.delete(friend)      
      db.session.commit()
      

      flash('Delete user successfully!', 'info')
      return redirect(url_for('login'))
    else:
      return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
