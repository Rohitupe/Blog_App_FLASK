from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import  SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# database setup
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///blogs.db'
db = SQLAlchemy(app)

# database model
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), default='N/A')
    date_created = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"{self.title} {self.id}"

# show data on the index page
@app.route('/')
def index():
    blogs = BlogPost.query.order_by(BlogPost.date_created.desc())[:5]
    return render_template('index.html',blogs = blogs)

# add new post
@app.route("/newpost",methods = ['GET','POST'])
def NewPost():
    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        if title and content != "":
            if author == "":
                author = "N/A"
            newBolg = BlogPost(title=title, author=author, content=content, date_created=datetime.now())
            db.session.add(newBolg)
            db.session.commit()
        else:
            return render_template('message.html')

        return redirect(url_for('index'))
    else:
        allBlogs = BlogPost.query.order_by(BlogPost.date_created)
        return render_template('newPost.html',blogs = allBlogs)

# delete post
@app.route('/delete/<int:id>')
def delete(id):
    data = BlogPost.query.get_or_404(id)
    try:
        db.session.delete(data)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "No Blog Found"

# update post
@app.route('/update/<int:id>',methods=["GET","POST"])
def update(id):
    data = BlogPost.query.get_or_404(id)

    if request.method == "POST":
        title = request.form['title']
        author = request.form['author']
        content = request.form['content']

        if title and content != "":
            if author == "":
                author = "N/A"
            data.title = title
            data.author = author
            data.content = content
            data.date_created = datetime.now()
            db.session.commit()
        else:
            return render_template('message.html')
        return redirect(url_for('index'))

    else:
        updateBlog = BlogPost.query.get_or_404(id)
        return render_template('update.html',blogs = updateBlog)

# View complete single blog
@app.route('/blog/<int:id>/')
def blogView(id):
    myBlog = BlogPost.query.get_or_404(id)
    return render_template('ViewBlog.html',myBlog = myBlog)

# all blogs Page
@app.route('/allblogs')
def allblogs():
    allBlog = BlogPost.query.order_by(BlogPost.date_created.desc()).all()
    return render_template('allblogs.html',allBlog = allBlog)

if __name__ == '__main__':
    app.run()