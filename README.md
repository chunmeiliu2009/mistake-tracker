# Mistake Tracker

A web platform for students to track and learn from their homework mistakes across various subjects including mathematics, physics, chemistry, and biology.

## Features
- User authentication with email and Google OAuth
- Subject categorization (Algebra, Geometry, Physics, etc.)
- Image upload for problem documentation
- Problem management (add/delete)
- Organized by subject categories
- Responsive design using Bootstrap

## Installation
1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables:
   - FLASK_SECRET_KEY
   - DATABASE_URL
   - GOOGLE_OAUTH_CLIENT_ID
   - GOOGLE_OAUTH_CLIENT_SECRET

## Usage
1. Register an account using email or Google authentication
2. Select a subject category
3. Add problems with images and descriptions
4. Track your progress and review past mistakes

## Technologies Used
- Flask (Python web framework)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Bootstrap (Frontend)
- Google OAuth (Authentication)
- Feather Icons

## Project Structure
- `app.py`: Main application file
- `auth.py`: Authentication routes
- `google_auth.py`: Google OAuth implementation
- `models.py`: Database models
- `forms.py`: Form definitions
- `utils.py`: Utility functions
- `templates/`: HTML templates
- `static/`: Static files

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
MIT License
