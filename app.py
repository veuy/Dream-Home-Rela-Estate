from flask import Flask, render_template, request
import db

app = Flask(__name__)


@app.route("/")
def home():
    return """
    <h1>Dream Home Real Estate</h1>
    <ul>
        <li><a href='/staff/hire'>Staff Hiring</a></li>
        <li><a href='/staff/list'>Staff List / Update</a></li>
    </ul>
    """


@app.route("/staff/hire", methods=["GET", "POST"])
def staff_hire():
    message = None

    if request.method == "POST":
        # Grab the values the user typed into the form fields.
        # These names must match the "name" attributes in staff_hire.html
        p_staffno = request.form["staffno"]
        p_fname = request.form["fname"]
        p_lname = request.form["lname"]
        p_position = request.form["position"]
        p_sex = request.form["sex"]
        p_dob = request.form["dob"]          # expects format YYYY-MM-DD
        p_salary = request.form["salary"]
        p_branchno = request.form["branchno"]
        p_telephone = request.form["telephone"]

        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc("staff_hire_sp", [
                p_staffno, p_fname, p_lname, p_position,
                p_sex, p_dob, p_salary, p_branchno, p_telephone
            ])
            connection.commit()
            message = f"Staff member {p_fname} {p_lname} ({p_staffno}) hired successfully."
        except Exception as e:
            message = f"Error: {e}"
        finally:
            cursor.close()
            connection.close()

    # Always show the current staff list below the form, whether GET or POST
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT staffno, fname, lname, position, branchno FROM dh_staff ORDER BY staffno")
    staff_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("staff_hire.html", message=message, staff_list=staff_list)


@app.route("/staff/list", methods=["GET"])
def staff_list_page():
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT staffno, fname, lname, position, salary, telephone, email
        FROM dh_staff
        ORDER BY staffno
    """)
    staff_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("staff_list.html", staff_list=staff_list, message=None)


@app.route("/staff/update/<staffno>", methods=["POST"])
def staff_update(staffno):
    new_salary = request.form["salary"]
    new_telephone = request.form["telephone"]
    new_email = request.form["email"]

    connection = db.get_connection()
    message = None
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE dh_staff
            SET salary = :new_salary,
                telephone = :new_telephone,
                email = :new_email
            WHERE staffno = :staffno
        """, {
            "new_salary": new_salary,
            "new_telephone": new_telephone,
            "new_email": new_email,
            "staffno": staffno
        })
        connection.commit()
        message = f"Staff {staffno} updated successfully."
    except Exception as e:
        message = f"Error updating {staffno}: {e}"
    finally:
        cursor.close()
        connection.close()

    # Reload the full list so the page shows the updated value
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute("""
        SELECT staffno, fname, lname, position, salary, telephone, email
        FROM dh_staff
        ORDER BY staffno
    """)
    staff_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("staff_list.html", staff_list=staff_list, message=message)


if __name__ == "__main__":
    app.run(debug=True)