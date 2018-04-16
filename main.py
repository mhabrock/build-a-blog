from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:purplepower@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
#app.secret_key = "purplesecret"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    body = db.Column(db.String(5000))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog', methods=['GET', 'POST'])
def index():
    # check query parameters
    # assign id params to a variable
    blog_id = request.args.get('id')
    if blog_id:
        single_post = Blog.query.filter_by(id = blog_id).all()
        return render_template('main.html', pagetitle ="Blog Posts", main_header = single_post[0].title, blogs = single_post)

    blogs = Blog.query.all()
    main_header = "Welcome to the PURPLE!"
    return render_template('main.html', pagetitle = "Blog Posts", main_header = main_header, blogs = blogs)

@app.route('/newpost', methods = ['GET', 'POST'])
def new_post():

    if request.method == 'POST':

        blog_title = request.form['title']
        blog_content = request.form['blogpost']  
        
        # new post error validation

        if blog_title == '' or blog_content == '':
            if blog_title == '':
                flash("Please enter a title for this blog post!")
            if blog_content == '':
                flash("Please add content to the body of your post!")
             
            return render_template('newpost.html', pagetitle="Add a Blog Post", title = blog_title, blogpost = blog_content)
        
        
        new_post = Blog(blog_title, blog_content)
        db.session.add(new_post)
        db.session.commit()  
        
        return redirect('/blog?id=' + str(new_post.id))

    
    return render_template('newpost.html', pagetitle = "Add a Blog Post")  


if __name__ == '__main__':
    app.run()