import os
from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, login_required, current_user
from werkzeug.middleware.proxy_fix import ProxyFix
from database import db
from models import User, Problem, Comment, StudyGuide
from forms import ProblemForm, CommentForm, StudyGuideForm
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
login_manager.login_view = "auth.login"

# Register blueprints
app.register_blueprint(auth)
app.register_blueprint(google_auth)

# Category mapping
CATEGORY_MAP = {
    'algebra': 'Algebra',
    'counting_and_probability': 'Counting & Probability',
    'geometry': 'Geometry',
    'number_theory': 'Number Theory',
    'exponent': 'Exponents',
    'trigonometry': 'Trigonometry',
    'physics': 'Physics',
    'chemistry': 'Chemistry',
    'biology': 'Biology'
}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html', categories=CATEGORY_MAP)

# Study Guide Routes
@app.route('/study-guides')
@login_required
def study_guides():
    guides = StudyGuide.query.filter_by(user_id=current_user.id).order_by(StudyGuide.created_at.desc()).all()
    return render_template('study_guides.html', study_guides=guides, categories=CATEGORY_MAP)

@app.route('/study-guide/new', methods=['GET', 'POST'])
@login_required
def new_study_guide():
    form = StudyGuideForm()
    if form.validate_on_submit():
        guide = StudyGuide(
            title=form.title.data,
            subject=form.subject.data,
            content=form.content.data,
            user_id=current_user.id
        )
        db.session.add(guide)
        db.session.commit()
        flash('Study guide created successfully')
        return redirect(url_for('study_guides'))
    return render_template('study_guide_form.html', form=form)

@app.route('/study-guide/<int:guide_id>')
@login_required
def view_study_guide(guide_id):
    guide = StudyGuide.query.get_or_404(guide_id)
    if guide.user_id != current_user.id:
        abort(403)
    return render_template('study_guide_detail.html', guide=guide, categories=CATEGORY_MAP)

@app.route('/study-guide/<int:guide_id>/delete', methods=['POST'])
@login_required
def delete_study_guide(guide_id):
    guide = StudyGuide.query.get_or_404(guide_id)
    if guide.user_id != current_user.id:
        abort(403)
    db.session.delete(guide)
    db.session.commit()
    flash('Study guide deleted successfully')
    return redirect(url_for('study_guides'))

@app.route('/problem/<int:problem_id>')
def view_problem(problem_id):
    problem = Problem.query.get_or_404(problem_id)
    comment_form = CommentForm()
    return render_template('problem_detail.html', 
                         problem=problem, 
                         comment_form=comment_form,
                         categories=CATEGORY_MAP)

@app.route('/problem/<int:problem_id>/comment', methods=['POST'])
@login_required
def add_comment(problem_id):
    problem = Problem.query.get_or_404(problem_id)
    form = CommentForm()
    
    if form.validate_on_submit():
        comment = Comment(
            content=form.content.data,
            user_id=current_user.id,
            problem_id=problem_id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully')
    return redirect(url_for('view_problem', problem_id=problem_id))

@app.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.user_id != current_user.id:
        abort(403)
    
    problem_id = comment.problem_id
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted successfully')
    return redirect(url_for('view_problem', problem_id=problem_id))

@app.route('/category/<category_name>')
@login_required
def category_view(category_name):
    if category_name not in CATEGORY_MAP:
        abort(404)
    
    problems = Problem.query.filter_by(
        user_id=current_user.id,
        subject=category_name
    ).order_by(Problem.created_at.desc()).all()
    
    return render_template('category.html', 
                         category_name=category_name,
                         category_display_name=CATEGORY_MAP[category_name],
                         problems=problems)

@app.route('/problem/new', methods=['GET', 'POST'])
@login_required
def new_problem():
    form = ProblemForm()
    if request.method == 'GET':
        category = request.args.get('category')
        if category and category in CATEGORY_MAP:
            form.subject.data = category
            
    if form.validate_on_submit():
        filename = None
        if form.image.data:
            filename = save_file(form.image.data)
        
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
        return redirect(url_for('category_view', category_name=form.subject.data))
    return render_template('problem.html', form=form)

@app.route('/problem/<int:problem_id>/delete', methods=['POST'])
@login_required
def delete_problem(problem_id):
    problem = Problem.query.get_or_404(problem_id)
    
    if problem.user_id != current_user.id:
        abort(403)
    
    category = problem.subject
    
    if problem.image_path:
        image_path = os.path.join('static/uploads', problem.image_path)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    db.session.delete(problem)
    db.session.commit()
    flash('Problem deleted successfully')
    return redirect(url_for('category_view', category_name=category))

# Create static/uploads directory if it doesn't exist
os.makedirs('static/uploads', exist_ok=True)

# Initialize database
with app.app_context():
    db.create_all()

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
