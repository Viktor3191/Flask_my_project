from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import desc


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myproject.db'
db = SQLAlchemy(app)


class About_Me(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return '<About_Me %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        city = request.form['city']
        text = request.form['text']
        user = About_Me(name=name, age=age, city=city, text=text)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении пользователя произошла ошибка'
    else:
        return render_template('create.html')

@app.route('/posts')
def posts():
    users = About_Me.query.order_by(desc(About_Me.date)).all()
    return render_template('posts.html', users=users)

@app.route('/posts/<int:id>')
def post_detail(id):
    user = About_Me.query.get(id)
    return render_template('post-detail.html', user=user)


@app.route('/posts/<int:id>/delete')
def post_delete(id):
    user = About_Me.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'При удалении произошла ошибка'

@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    user=About_Me.query.get(id)
    if request.method == 'POST':
        user.name = request.form['name']
        user.age = request.form['age']
        user.city = request.form['city']
        user.text = request.form['text']
        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При редактировании пользователя произошла ошибка'
    else:
        user=About_Me.query.get(id)
        return render_template('post-update.html', user=user)


if __name__ == '__main__':
    app.run(debug=True)
