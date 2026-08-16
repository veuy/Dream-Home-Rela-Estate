# Dream Home Real Estate

A full-stack web application built for a Database Concepts course project. It provides a back-office admin interface for managing Staff, Branches, and Clients at a real estate agency, backed by an Oracle database with PL/SQL stored procedures and functions.

---

## Tech Stack

- **Backend logic:** Oracle PL/SQL (stored procedures & functions), tested and compiled in Oracle SQL Developer
- **Web framework:** Python 3 + Flask
- **Database driver:** [python-oracledb](https://oracle.github.io/python-oracledb/) (thin mode — no Oracle Instant Client required)
- **Frontend:** HTML, CSS, Jinja2 templates
- **Database schema:** `DH_STAFF`, `DH_BRANCH`, `DH_CLIENT` (provided sample schema)

---

## Features

### Staff Menu
- **Staff Hiring** — `staff_hire_sp` procedure inserts a new staff record from a web form
- **Staff List / Update** — Excel-style editable grid; updates Salary, Telephone, and Email in place

### Branch Menu
- **Branch Address Lookup** — `get_branch_address` function returns a branch's street/city from a branch number
- **Branch List / Update** — Excel-style editable grid for Street, City, and Postcode
- **Open New Branch** — `new_branch` procedure inserts a new branch record

### Client Menu
- **Register New Client** — `register_client_sp` procedure inserts a new client record
- **Client List / Update** — Excel-style editable grid for all client fields except Client No

---

## Project Structure

```
Dream-Home-Rela-Estate/
├── app.py                     # Flask routes and application logic
├── db.py                      # Oracle database connection helper
├── .env                       # Local database credentials (gitignored, not committed)
├── sql/
│   ├── staff_hire_sp.sql
│   ├── new_branch.sql
│   ├── get_branch_address.sql
│   └── register_client_sp.sql
└── templates/
    ├── staff_hire.html
    ├── staff_list.html
    ├── branch_address.html
    ├── branch_list.html
    ├── branch_new.html
    ├── client_register.html
    └── client_list.html
```

---

## Setup & Installation

### 1. Install dependencies
```bash
pip install flask oracledb
```

### 2. Configure your database connection
Create a `.env` file in the project root (this file is gitignored and must **not** be committed):
```
DB_USER=your_username
DB_PASSWORD=your_password
DB_DSN=hostname:port/SID_or_service_name
```

### 3. Set up the database
In Oracle SQL Developer, run each script in the `sql/` folder against your `DH_XXXX` schema:
- `staff_hire_sp.sql`
- `new_branch.sql`
- `get_branch_address.sql`
- `register_client_sp.sql`

Each script includes a test block to confirm it compiles and runs correctly.

### 4. Run the application
```bash
python app.py
```
Then open **http://127.0.0.1:5000** in your browser.

---

## Notes

- All database writes use bind variables and `COMMIT` after each successful operation.
- The `.env` file keeps database credentials out of version control — never commit real credentials.
- The assignment's original task sheet contains a few typos in its sample code (referencing `dh_staff` where `dh_branch` was clearly intended for Branch-related tasks); this implementation follows the correct table based on task context.

