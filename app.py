import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
from database import db
from models import User, Problem
from forms import ProblemForm
from utils import save_file
from auth import auth
from google_auth import google_auth

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(google_auth)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
@login_required
def dashboard():
    problems = Problem.query.filter_by(user_id=current_user.id).order_by(Problem.created_at.desc()).all()
    return render_template('dashboard.html', problems=problems, config=app.config, os=os)

@app.route('/problem/new', methods=['GET', 'POST'])
@login_required
def new_problem():
    form = ProblemForm()
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = save_file(form.image.data)
            if not filename:
                flash('Error uploading image. Please try again.', 'error')
                return render_template('problem.html', form=form)
        
        problem = Problem(
            title=form.title.data,
            subject=form.subject.data,
            description=form.description.data,
            image_path=filename,
            user_id=current_user.id
        )
        db.session.add(problem)
        db.session.commit()
        flash('Problem added successfully')
        return redirect(url_for('dashboard'))
    return render_template('problem.html', form=form)

# Create static/uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize database
with app.app_context():
    db.create_all()

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
