
import os
import hmac
from functools import wraps
from datetime import datetime
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
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per hour"],
    storage_uri="memory://"
)

# Secret key configuration
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError("SECRET_KEY environment variable is required")

# Temporary admin setup token configuration
app.config["ADMIN_SETUP_TOKEN"] = os.environ.get("ADMIN_SETUP_TOKEN")

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
    role = db.Column(
        db.String(20),
        nullable=False,
        default="owner"
    )


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


# Document sharing permissions
class DocumentPermission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document_id = db.Column(
        db.Integer,
        db.ForeignKey("document.id"),
        nullable=False
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )
    permission = db.Column(db.String(10), nullable=False, default="read")
    __table_args__ = (
        db.UniqueConstraint(
            "document_id",
            "user_id",
            name="unique_document_user_permission"
        ),
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
@limiter.limit("5 per minute")
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


# Audit log database model
class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True
    )
    document_id = db.Column(
        db.Integer,
        db.ForeignKey("document.id"),
        nullable=True
    )
    action = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(255), nullable=True)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )


# Record audit events
def record_audit(action, document_id=None, details=None):
    try:
        entry = AuditLog(
            user_id=(
                current_user.id
                if current_user.is_authenticated
                else None
            ),
            document_id=document_id,
            action=action,
            details=details
        )
        db.session.add(entry)
        db.session.commit()
    except Exception:
        db.session.rollback()
        app.logger.exception("Audit logging failed")


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

        record_audit(
            "upload",
            document.id,
            f"Uploaded {original_filename}"
        )

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
    shared_ids = db.session.query(
        DocumentPermission.document_id
    ).filter_by(user_id=current_user.id).subquery()

    documents = Document.query.filter(
        db.or_(
            Document.owner_id == current_user.id,
            Document.id.in_(shared_ids)
        )
    ).order_by(Document.uploaded_at.desc()).all()

    return render_template(
        "dashboard.html",
        username=current_user.username,
        documents=documents
    )


# Share a document with a registered user
@app.route("/documents/<int:document_id>/share", methods=["POST"])
@login_required
def share_document(document_id):
    document = db.session.get(Document, document_id)

    if document is None:
        abort(404)

    if document.owner_id != current_user.id:
        abort(403)

    username = request.form.get("username", "").strip()
    permission = request.form.get("permission", "read").strip().lower()

    if permission not in {"read", "edit"}:
        abort(400)

    recipient = User.query.filter_by(username=username).first()

    if recipient is None:
        flash("User not found.")
        return redirect(url_for("dashboard"))

    if recipient.id == current_user.id:
        flash("You already own this document.")
        return redirect(url_for("dashboard"))

    existing = DocumentPermission.query.filter_by(
        document_id=document.id,
        user_id=recipient.id
    ).first()

    if existing:
        existing.permission = permission
    else:
        db.session.add(
            DocumentPermission(
                document_id=document.id,
                user_id=recipient.id,
                permission=permission
            )
        )

    db.session.commit()

    record_audit(
        "share",
        document.id,
        f"Shared with username: {username}; permission: {permission}"
    )

    flash("Document access granted.")
    return redirect(url_for("dashboard"))


# Revoke a user's access to an owned document
@app.route("/documents/<int:document_id>/revoke", methods=["POST"])
@login_required
def revoke_document_access(document_id):
    document = db.session.get(Document, document_id)

    if document is None:
        abort(404)

    if document.owner_id != current_user.id:
        abort(403)

    username = request.form.get("username", "").strip()
    recipient = User.query.filter_by(username=username).first()

    if recipient is None:
        flash("User not found.")
        return redirect(url_for("dashboard"))

    permission = DocumentPermission.query.filter_by(
        document_id=document.id,
        user_id=recipient.id
    ).first()

    if permission:
        db.session.delete(permission)
        db.session.commit()

        record_audit(
            "revoke",
            document.id,
            f"Revoked access for username: {username}"
        )

        flash("Document access revoked.")
    else:
        flash("No sharing permission found for that user.")

    return redirect(url_for("dashboard"))


# Secure document download route
@app.route("/documents/<int:document_id>")
@login_required
def download_document(document_id):
    document = db.session.get(Document, document_id)

    if document is None:
        abort(404)

    # Owners can download their own documents.
    # Other users need an explicit sharing permission.
    if document.owner_id != current_user.id:
        permission = DocumentPermission.query.filter_by(
            document_id=document.id,
            user_id=current_user.id
        ).first()

        if (
            permission is None
            or permission.permission not in {"read", "edit"}
        ):
            abort(403)

    response = send_from_directory(
        app.config["UPLOAD_FOLDER"],
        document.filename,
        as_attachment=True,
        download_name=document.original_filename
    )

    record_audit(
        "download",
        document.id,
        f"Downloaded {document.original_filename}"
    )

    return response


# User logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out.")
    return redirect(url_for("home"))


# Restrict audit logs to administrators
def admin_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if current_user.role != "admin":
            abort(403)

        return view(*args, **kwargs)

    return wrapped


@app.route("/admin/audit")
@admin_required
def admin_audit():
    logs = AuditLog.query.order_by(
        AuditLog.created_at.desc()
    ).limit(200).all()

    return render_template("admin_audit.html", logs=logs)


# TEMPORARY ADMIN SETUP ROUTE
# Remove this route after the account role has been updated.
@app.route("/admin/setup", methods=["POST"])
def temporary_admin_setup():
    token = app.config.get("ADMIN_SETUP_TOKEN")

    if not token:
        abort(404)

    provided_token = request.headers.get(
        "X-Admin-Setup-Token",
        ""
    )

    if not hmac.compare_digest(provided_token, token):
        abort(403)

    username = request.form.get("username", "").strip()

    if not username:
        abort(400)

    user = User.query.filter_by(username=username).first()

    if user is None:
        abort(404)

    user.role = "admin"
    db.session.commit()

    # Disable the token in this application process.
    app.config["ADMIN_SETUP_TOKEN"] = None

    app.logger.warning(
        "Temporary admin setup used for username: %s",
        username
    )

    return (
        "Admin role updated. Remove the temporary setup route "
        "and ADMIN_SETUP_TOKEN environment variable, then redeploy."
    )


# Create database tables
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
