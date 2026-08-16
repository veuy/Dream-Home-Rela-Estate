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
        <li><a href='/branch/address'>Branch Address Lookup</a></li>
        <li><a href='/branch/list'>Branch List / Update</a></li>
        <li><a href='/branch/new'>Open New Branch</a></li>
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



@app.route("/branch/address", methods=["GET", "POST"])
def branch_address():
    address = None
    searched_branchno = None

    if request.method == "POST":
        searched_branchno = request.form["branchno"]
        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            # Calls the get_branch_address FUNCTION using a bind variable
            # to receive its return value.
            result = cursor.callfunc("get_branch_address", str, [searched_branchno])
            address = result
        except Exception as e:
            address = f"Error: {e}"
        finally:
            cursor.close()
            connection.close()

    return render_template("branch_address.html", address=address, searched_branchno=searched_branchno)


@app.route("/branch/list", methods=["GET"])
def branch_list_page():
    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT branchno, street, city, postcode FROM dh_branch ORDER BY branchno")
    branch_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("branch_list.html", branch_list=branch_list, message=None)


@app.route("/branch/update/<branchno>", methods=["POST"])
def branch_update(branchno):
    new_street = request.form["street"]
    new_city = request.form["city"]
    new_postcode = request.form["postcode"]

    connection = db.get_connection()
    message = None
    try:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE dh_branch
            SET street = :new_street,
                city = :new_city,
                postcode = :new_postcode
            WHERE branchno = :branchno
        """, {
            "new_street": new_street,
            "new_city": new_city,
            "new_postcode": new_postcode,
            "branchno": branchno
        })
        connection.commit()
        message = f"Branch {branchno} updated successfully."
    except Exception as e:
        message = f"Error updating {branchno}: {e}"
    finally:
        cursor.close()
        connection.close()

    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT branchno, street, city, postcode FROM dh_branch ORDER BY branchno")
    branch_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("branch_list.html", branch_list=branch_list, message=message)


@app.route("/branch/new", methods=["GET", "POST"])
def branch_new():
    message = None

    if request.method == "POST":
        p_branchno = request.form["branchno"]
        p_street = request.form["street"]
        p_city = request.form["city"]
        p_postcode = request.form["postcode"]

        connection = db.get_connection()
        try:
            cursor = connection.cursor()
            cursor.callproc("new_branch", [p_branchno, p_street, p_city, p_postcode])
            connection.commit()
            message = f"Branch {p_branchno} opened successfully."
        except Exception as e:
            message = f"Error: {e}"
        finally:
            cursor.close()
            connection.close()

    connection = db.get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT branchno, street, city, postcode FROM dh_branch ORDER BY branchno")
    branch_list = cursor.fetchall()
    cursor.close()
    connection.close()

    return render_template("branch_new.html", message=message, branch_list=branch_list)

if __name__ == "__main__":
    app.run(debug=True)