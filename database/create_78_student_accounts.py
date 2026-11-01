"""
StudentHub - Script to create and link user accounts for all 78 AIML students.
Course: AIUE203 - Web Development Fundamentals
Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT
"""

import pymysql
import bcrypt

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "",
    "database": "studenthub",
    "autocommit": False
}

def main():
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Disambiguate legacy test row 73 / user 58 so official roster student 25AIML064 gets clean email
    cur.execute("UPDATE users SET email = 'legacy_25aiml064@charusat.edu.in' WHERE id = 58 AND email = '25aiml064@charusat.edu.in'")
    cur.execute("UPDATE students SET email = 'legacy_25aiml064@charusat.edu.in' WHERE id = 73 AND email = '25aiml064@charusat.edu.in'")
    conn.commit()

    cur.execute("""
        SELECT id, student_id, name, email, user_id 
        FROM students 
        WHERE student_id IS NOT NULL 
        ORDER BY student_id ASC
    """)
    students = cur.fetchall()
    print(f"Found {len(students)} students with official student_id.")

    created = 0
    updated = 0

    for s_id, roll_no, name, s_email, existing_user_id in students:
        roll_no = roll_no.strip()
        default_email = f"{roll_no.lower()}@charusat.edu.in"
        initial_password = roll_no

        if roll_no == "25AIML002":
            # Anshika Badala - preserve user id 2 (username 'anshika', email 'anshikabadala2@gmail.com')
            cur.execute("SELECT id FROM users WHERE id = 2 OR username = 'anshika'")
            u_row = cur.fetchone()
            if u_row:
                uid = u_row[0]
                cur.execute("UPDATE students SET user_id = %s WHERE id = %s", (uid, s_id))
                print(f"[PRESERVE] {roll_no} -> User ID {uid} ('anshika')")
            continue

        # Generate bcrypt hash for roll_no (e.g. $2y$10$...)
        hashed = bcrypt.hashpw(initial_password.encode('utf-8'), bcrypt.gensalt(10)).decode('utf-8')
        if hashed.startswith("$2b$"):
            hashed = "$2y$" + hashed[4:]

        # Check if user with username == roll_no or email == default_email already exists
        cur.execute("SELECT id FROM users WHERE username = %s OR email = %s", (roll_no, default_email))
        existing_u = cur.fetchone()

        if existing_u:
            uid = existing_u[0]
            cur.execute("""
                UPDATE users 
                SET username = %s, email = %s, password = %s, role = 'student', status = 'active', must_change_password = 1
                WHERE id = %s
            """, (roll_no, default_email, hashed, uid))
            cur.execute("UPDATE students SET user_id = %s, email = %s WHERE id = %s", (uid, default_email, s_id))
            updated += 1
        else:
            cur.execute("""
                INSERT INTO users (username, email, password, role, status, must_change_password)
                VALUES (%s, %s, %s, 'student', 'active', 1)
            """, (roll_no, default_email, hashed))
            uid = cur.lastrowid
            cur.execute("UPDATE students SET user_id = %s, email = %s WHERE id = %s", (uid, default_email, s_id))
            created += 1

    conn.commit()
    print(f"Account setup complete: {created} users created, {updated} users updated.")

    # Verification: check total active student users
    cur.execute("SELECT count(*) FROM users WHERE role = 'student'")
    tot_student_users = cur.fetchone()[0]
    print(f"Total student accounts in users table: {tot_student_users}")

    # Check students linked
    cur.execute("SELECT count(*) FROM students WHERE student_id IS NOT NULL AND user_id IS NOT NULL")
    tot_linked = cur.fetchone()[0]
    print(f"Total roster students linked to user accounts: {tot_linked}/78")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
