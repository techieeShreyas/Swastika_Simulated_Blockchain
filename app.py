from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from utils import get_blockchain, find_match, notify_hospital, notify_recipient
from models import Hospital, db
from validators import (
    validate_name, validate_age, validate_blood_type,
    validate_medical_urgency, validate_hospital_name
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "your_secret_key"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///hospitals.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database
db.init_app(app)

# Initialize login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(Hospital, int(user_id))

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/recipient", methods=["GET", "POST"])
def recipient_form():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        age = request.form.get("age")
        blood_type = request.form.get("blood_type")
        medical_urgency = request.form.get("medical_urgency")

        # Validate form data
        errors = {}
        errors["name"] = validate_name(name)
        errors["age"] = validate_age(age)
        errors["blood_type"] = validate_blood_type(blood_type)
        errors["medical_urgency"] = validate_medical_urgency(medical_urgency)

        # Check if there are any errors
        if any(errors.values()):
            return render_template("recipient_form.html", errors=errors)

        # Create a data dictionary for the recipient
        recipient_data = {
            "name": name,
            "age": age,
            "blood_type": blood_type,
            "medical_urgency": medical_urgency
        }

        # Add recipient to the recipient blockchain
        recipient_chain = get_blockchain("recipient")
        recipient_chain.add_block(recipient_data)  # Pass as a dictionary

        # Find a matching donor
        donor_chain = get_blockchain("donor")
        matched_donor = find_match(recipient_data, donor_chain)

        if matched_donor:
            # Record the transplant
            transplant_chain = get_blockchain("transplant")
            transplant_chain.add_transplant(matched_donor, recipient_data)

            # Mark the donor as "used"
            matched_donor["used"] = True
            donor_chain.add_block(matched_donor)  # Pass as a dictionary

            # Mark the recipient as "transplanted"
            recipient_data["transplanted"] = True
            recipient_chain.add_block(recipient_data)  # Update the recipient record

            # Notify the hospital and recipient
            notify_hospital(matched_donor["hospital"], recipient_data["name"])
            notify_recipient(recipient_data["name"])

            flash("Match found! Transplant recorded.", "success")
        else:
            flash("No matching donor found. Recipient added to the waiting list.", "info")

        return redirect(url_for("home"))

    return render_template("recipient_form.html", errors={})

@app.route("/donor", methods=["GET", "POST"])
@login_required
def donor_form():
    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        age = request.form.get("age")
        blood_type = request.form.get("blood_type")
        hospital = request.form.get("hospital")

        # Validate form data
        errors = {}
        errors["name"] = validate_name(name)
        errors["age"] = validate_age(age)
        errors["blood_type"] = validate_blood_type(blood_type)
        errors["hospital"] = validate_hospital_name(hospital)

        # Check if there are any errors
        if any(errors.values()):
            return render_template("donor_form.html", errors=errors)

        # Create a data dictionary
        data = {
            "name": name,
            "age": age,
            "blood_type": blood_type,
            "hospital": hospital
        }

        # Add data to the donor blockchain
        donor_chain = get_blockchain("donor")
        donor_chain.add_block(data)

        # Redirect to home page
        flash("Donor data added successfully!", "success")
        return redirect(url_for("home"))

    return render_template("donor_form.html", errors={})

@app.route("/view/<chain_name>")
def view_chain(chain_name):
    # Get the blockchain
    blockchain = get_blockchain(chain_name)

    # Get all blocks in the chain
    blocks = blockchain.get_all_blocks()

    # Render the view_data template
    return render_template("view_data.html", chain_name=chain_name.capitalize(), blocks=blocks)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hospital_name = request.form.get("hospital_name")

        # Check if the username already exists
        hospital = Hospital.query.filter_by(username=username).first()
        if hospital:
            flash("Username already exists. Please choose a different one.", "error")
            return redirect(url_for("register"))

        # Create a new hospital
        new_hospital = Hospital(username=username, password=password, hospital_name=hospital_name)
        db.session.add(new_hospital)
        db.session.commit()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Check if the hospital exists
        hospital = Hospital.query.filter_by(username=username).first()
        if hospital and hospital.password == password:
            login_user(hospital)
            flash("Login successful.", "success")
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password.", "error")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("home"))

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        search_term = request.form.get("search_term")
        chain_name = request.form.get("chain_name")

        # Get the blockchain
        blockchain = get_blockchain(chain_name)

        # Search for blocks containing the search term
        results = blockchain.search_blocks(search_term)

        # Render the search results template
        return render_template("search_results.html", chain_name=chain_name.capitalize(), search_term=search_term, results=results)

    return render_template("home.html")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)