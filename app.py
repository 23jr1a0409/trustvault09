
import os
import uuid

from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, send_from_directory, abort
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Secret key configuration
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY environment variable is required")

# SQLite database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///trustvault.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Secure upload configuration
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "uploads")
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB

# Create upload folder if it does not exist
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

db = SQLAlchemy(app)

# Login manager configuration
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# User database model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)


# Document database model
class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    uploaded_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Home page
@app.route("/")
def home():
    return render_template("index.html")


# User registration
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or not password:
            flash("Please enter both username and password.")
            return redirect(url_for("register"))

        if len(password) < 8:
            flash("Password must contain at least 8 characters.")
            return redirect(url_for("register"))

        existing_user = User.query.filter_by(username=username).first()

        if existing_user:
            flash("Username already exists.")
            return redirect(url_for("register"))

        user = User(
            username=username,
            password_hash=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration successful. Please log in.")
        return redirect(url_for("login"))

    return render_template("register.html")


# User login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for("dashboard"))

        flash("Invalid username or password.")

    return render_template("login.html")


# Allowed document file types
ALLOWED_EXTENSIONS = {"pdf", "txt", "png", "jpg", "jpeg"}


def allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


# Secure document upload route
@app.route("/upload", methods=["POST"])
@login_required
def upload_document():
    if "file" not in request.files:
        flash("Please select a file.")
        return redirect(url_for("dashboard"))

    file = request.files["file"]

    if not file or file.filename == "":
        flash("Please select a file.")
        return redirect(url_for("dashboard"))

    if not allowed_file(file.filename):
        flash("Only PDF, TXT, PNG, JPG and JPEG files are allowed.")
        return redirect(url_for("dashboard"))

    original_filename = secure_filename(file.filename)

    if not original_filename:
        flash("Invalid filename.")
        return redirect(url_for("dashboard"))

    extension = original_filename.rsplit(".", 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        unique_filename
    )

    try:
        file.save(file_path)

        document = Document(
            filename=unique_filename,
            original_filename=original_filename,
            owner_id=current_user.id
        )

        db.session.add(document)
        db.session.commit()

    except Exception:
        db.session.rollback()

        if os.path.exists(file_path):
            os.remove(file_path)

        app.logger.exception("Document upload failed")
        flash("Upload failed. Please try again.")
        return redirect(url_for("dashboard"))

    flash("Document uploaded successfully.")
    return redirect(url_for("dashboard"))

# Protected dashboard

@app.route("/dashboard")
@login_required
def dashboard():
    documents = Document.query.filter_by(
        owner_id=current_user.id
    ).order_by(Document.uploaded_at.desc()).all()

    return render_template(
        "dashboard.html",
        username=current_user.username,
        documents=documents
    )


# Secure document download route
@app.route("/documents/<int:document_id>")
@login_required
def download_document(document_id):
    document = db.session.get(Document, document_id)

    if document is None:
        abort(404)

    # Only the document owner can download it
    if document.owner_id != current_user.id:
        abort(403)

    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        document.filename,
        as_attachment=True,
        download_name=document.original_filename
    )


# User logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home"))


# Create database tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=False)
