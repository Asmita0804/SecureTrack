
import sqlite3

# Connect to the database
def connect_db():
    return sqlite3.connect("securetrack.db")


# Create database tables
def create_database():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS risks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            risk_name TEXT,
            likelihood INTEGER,
            impact INTEGER,
            score INTEGER,
            level TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS controls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            control_name TEXT,
            description TEXT,
            status TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mitigation_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            risk_id INTEGER,
            plan TEXT,
            status TEXT,
            FOREIGN KEY (risk_id) REFERENCES risks(id)
        )
    """)

    conn.commit()
    conn.close()


# Add a risk
def add_risk(name, likelihood, impact, score, level):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO risks (risk_name, likelihood, impact, score, level) VALUES (?, ?, ?, ?, ?)",
        (name, likelihood, impact, score, level)
    )
    conn.commit()
    conn.close()


# Get all risks
def get_risks():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM risks")
    data = cursor.fetchall()
    conn.close()
    return data


# Update a risk
def update_risk(risk_id, name, likelihood, impact, score, level):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE risks SET risk_name=?, likelihood=?, impact=?, score=?, level=? WHERE id=?",
        (name, likelihood, impact, score, level, risk_id)
    )
    conn.commit()
    conn.close()


# Delete a risk
def delete_risk(risk_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM risks WHERE id=?", (risk_id,))
    conn.commit()
    conn.close()


# Add a security control
def add_control(name, description, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO controls (control_name, description, status) VALUES (?, ?, ?)",
        (name, description, status)
    )
    conn.commit()
    conn.close()


# Get all security controls
def get_controls():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM controls")
    data = cursor.fetchall()
    conn.close()
    return data


# Add a mitigation plan
def add_mitigation(risk_id, plan, status):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO mitigation_plans (risk_id, plan, status) VALUES (?, ?, ?)",
        (risk_id, plan, status)
    )
    conn.commit()
    conn.close()


# Get all mitigation plans
def get_mitigations():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mitigation_plans")
    data = cursor.fetchall()
    conn.close()
    return data


create_database()

