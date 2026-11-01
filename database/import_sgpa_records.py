"""
StudentHub - SGPA & Academic Records Import & CGPA Calculation
Course: AIUE203 - Web Development Fundamentals
Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT
"""

import csv
import os
import pymysql

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "",
    "database": "studenthub",
    "autocommit": False
}

SEM1_CSV = r"C:\Users\Manan1\.gemini\antigravity\brain\43fb5d3b-4265-4945-95f5-a9a4d32ea9c5\.user_uploaded\media_1793426910138_239d1f0d.csv"
SEM2_CSV = r"C:\Users\Manan1\.gemini\antigravity\brain\43fb5d3b-4265-4945-95f5-a9a4d32ea9c5\.user_uploaded\media_1793426910133_e875a499.csv"

def main():
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()

    # Build mapping of roster student_id to database student table id
    cur.execute("SELECT id, student_id FROM students WHERE student_id IS NOT NULL")
    roster_map = {row[1].strip(): row[0] for row in cur.fetchall()}
    print(f"Loaded {len(roster_map)} students in official roster map.")

    # Clear prior semester_results & unassigned_academic_records for clean idempotent import
    cur.execute("DELETE FROM semester_results")
    cur.execute("DELETE FROM unassigned_academic_records")
    conn.commit()

    # -------------------------------------------------------------
    # 1. Process Semester 1 (File: media_1793426910138_239d1f0d.csv)
    # -------------------------------------------------------------
    sem1_imported = 0
    with open(SEM1_CSV, mode="r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if not row or len(row) < 3:
                continue
            roll_no = row[0].strip()
            try:
                sgpa = float(row[1].strip())
            except ValueError:
                continue
            credits = float(row[2].strip()) if row[2].strip() else 19.00

            if roll_no in roster_map:
                s_id = roster_map[roll_no]
                cur.execute("""
                    INSERT INTO semester_results (student_id, roll_no, semester, sgpa, credits, is_missing, remarks)
                    VALUES (%s, %s, 1, %s, %s, 0, NULL)
                """, (s_id, roll_no, sgpa, credits))
                sem1_imported += 1
            else:
                cur.execute("""
                    INSERT INTO unassigned_academic_records (roll_no, semester, sgpa, credits, quarantine_reason)
                    VALUES (%s, 1, %s, %s, 'Outside official 78-student FYAIML roster')
                """, (roll_no, sgpa, credits))

    # Explicitly flag 25AIML011 as missing in Semester 1
    if "25AIML011" in roster_map:
        s11_id = roster_map["25AIML011"]
        cur.execute("""
            INSERT INTO semester_results (student_id, roll_no, semester, sgpa, credits, is_missing, remarks)
            VALUES (%s, '25AIML011', 1, NULL, 19.00, 1, 'Official Semester 1 result record pending')
        """, (s11_id,))
        print("Flagged 25AIML011 as missing in Semester 1.")

    print(f"Semester 1 import: {sem1_imported} roster records inserted.")

    # -------------------------------------------------------------
    # 2. Process Semester 2 (File: media_1793426910133_e875a499.csv)
    # -------------------------------------------------------------
    sem2_imported = 0
    unassigned_sem2 = 0
    with open(SEM2_CSV, mode="r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader)
        for row in reader:
            if not row or len(row) < 3:
                continue
            roll_no = row[0].strip()
            try:
                sgpa = float(row[1].strip())
            except ValueError:
                continue
            credits = float(row[2].strip()) if row[2].strip() else 22.00

            if roll_no in roster_map:
                s_id = roster_map[roll_no]
                cur.execute("""
                    INSERT INTO semester_results (student_id, roll_no, semester, sgpa, credits, is_missing, remarks)
                    VALUES (%s, %s, 2, %s, %s, 0, NULL)
                """, (s_id, roll_no, sgpa, credits))
                sem2_imported += 1
            else:
                cur.execute("""
                    INSERT INTO unassigned_academic_records (roll_no, semester, sgpa, credits, quarantine_reason)
                    VALUES (%s, 2, %s, %s, 'Outside official 78-student FYAIML roster (25AIML079 - 25AIML090)')
                """, (roll_no, sgpa, credits))
                unassigned_sem2 += 1

    print(f"Semester 2 import: {sem2_imported} roster records inserted, {unassigned_sem2} unassigned records quarantined.")

    # -------------------------------------------------------------
    # 3. Compute Mathematically Sound Weighted CGPA
    # -------------------------------------------------------------
    cur.execute("""
        SELECT student_id,
               SUM(CASE WHEN is_missing = 0 THEN (sgpa * credits) ELSE 0 END) AS total_pts,
               SUM(CASE WHEN is_missing = 0 THEN credits ELSE 0 END) AS earned_credits,
               SUM(is_missing) AS missing_count,
               COUNT(*) AS sem_count
        FROM semester_results
        GROUP BY student_id
    """)
    cgpa_rows = cur.fetchall()

    updated_cgpa = 0
    for s_id, total_pts, earned_credits, missing_count, sem_count in cgpa_rows:
        if missing_count > 0 or earned_credits == 0:
            # Student has missing semester (e.g. 25AIML011), leave CGPA as NULL or pending
            cur.execute("UPDATE students SET cgpa = NULL WHERE id = %s", (s_id,))
        else:
            cgpa = round(float(total_pts) / float(earned_credits), 2)
            cur.execute("UPDATE students SET cgpa = %s WHERE id = %s", (cgpa, s_id))
            updated_cgpa += 1

    conn.commit()
    print(f"Weighted CGPA calculated for {updated_cgpa} students.")

    # Check Anshika Badala (25AIML002)
    cur.execute("""
        SELECT s.student_id, s.name, s.cgpa,
               sr1.sgpa AS sem1_sgpa, sr1.credits AS sem1_credits,
               sr2.sgpa AS sem2_sgpa, sr2.credits AS sem2_credits
        FROM students s
        LEFT JOIN semester_results sr1 ON sr1.student_id = s.id AND sr1.semester = 1
        LEFT JOIN semester_results sr2 ON sr2.student_id = s.id AND sr2.semester = 2
        WHERE s.student_id = '25AIML002'
    """)
    anshika_row = cur.fetchone()
    print("Anshika Badala Academic Verification:", anshika_row)

    # Check 25AIML011
    cur.execute("""
        SELECT s.student_id, s.name, s.cgpa,
               sr1.sgpa AS sem1_sgpa, sr1.is_missing AS sem1_missing, sr1.remarks AS sem1_remarks,
               sr2.sgpa AS sem2_sgpa
        FROM students s
        LEFT JOIN semester_results sr1 ON sr1.student_id = s.id AND sr1.semester = 1
        LEFT JOIN semester_results sr2 ON sr2.student_id = s.id AND sr2.semester = 2
        WHERE s.student_id = '25AIML011'
    """)
    s11_row = cur.fetchone()
    print("25AIML011 Academic Verification:", s11_row)

    # Check unassigned quarantine records count
    cur.execute("SELECT count(*) FROM unassigned_academic_records")
    tot_unassigned = cur.fetchone()[0]
    print(f"Total unassigned records in quarantine: {tot_unassigned}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
