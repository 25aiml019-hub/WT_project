"""
StudentHub - Semester 3 Timetable Import
Based on official CHARUSAT AIML Odd Term 2026-27 Division I Timetable
Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT
"""

import pymysql

DB_CONFIG = {
    "host": "127.0.0.1",
    "port": 3307,
    "user": "root",
    "password": "",
    "database": "studenthub",
    "autocommit": False
}

TIMETABLE_SLOTS = [
    # MONDAY
    ("Monday", 1, "09:10:00", "10:10:00", "lecture", "ALL", "AI301", "Operating Systems", "OS", "218", "GK", "Prof. Gaurav Kumar"),
    ("Monday", 2, "10:10:00", "11:10:00", "lecture", "ALL", "AI302", "Design & Analysis of Algorithms", "DAA", "218", "NP", "Prof. Niyati Patel"),
    ("Monday", 3, "11:10:00", "12:10:00", "lecture", "ALL", "MA301", "Probability & Statistics", "PS", "218", "BS", "Prof. Bhargav Sobhana"),
    ("Monday", 4, "13:10:00", "15:10:00", "practical", "A1", "AI302", "Design & Analysis of Algorithms Lab", "DAA Lab", "Lab 3", "NP", "Prof. Niyati Patel"),
    ("Monday", 4, "13:10:00", "15:10:00", "practical", "B1", "AI301", "Operating Systems Lab", "OS Lab", "Lab 4", "GK", "Prof. Gaurav Kumar"),
    ("Monday", 4, "13:10:00", "15:10:00", "practical", "C1", "AI303", "Database Management Systems Lab", "DBMS Lab", "Lab 2", "GP", "Prof. Gaurang Patel"),
    ("Monday", 4, "13:10:00", "15:10:00", "practical", "D1", "AI304", "Library & Research Study", "LIB", "Library", "FAC", "Library Staff"),
    ("Monday", 4, "13:10:00", "15:10:00", "practical", "E1", "AI305", "Mini Project / Python Lab", "MP Lab", "Lab 1", "FAC", "Faculty In-Charge"),
    ("Monday", 6, "15:15:00", "17:15:00", "counseling", "A1", "COUN3", "Student Counseling & Mentorship", "COUN", "Cabin 204", "GK", "Prof. Gaurav Kumar"),
    ("Monday", 6, "15:15:00", "17:15:00", "activity", "B1", "ACT3", "Sports & Extracurriculars", "ACT", "Campus Ground", "FAC", "Sports Staff"),
    ("Monday", 6, "15:15:00", "17:15:00", "activity", "C1", "ACT3", "Sports & Extracurriculars", "ACT", "Campus Ground", "FAC", "Sports Staff"),
    ("Monday", 6, "15:15:00", "17:15:00", "activity", "D1", "ACT3", "Sports & Extracurriculars", "ACT", "Campus Ground", "FAC", "Sports Staff"),

    # TUESDAY
    ("Tuesday", 1, "09:10:00", "10:10:00", "lecture", "ALL", "AI303", "Database Management Systems", "DBMS", "218", "GP", "Prof. Gaurang Patel"),
    ("Tuesday", 2, "10:10:00", "11:10:00", "lecture", "ALL", "AI301", "Operating Systems", "OS", "218", "GK", "Prof. Gaurav Kumar"),
    ("Tuesday", 3, "11:10:00", "12:10:00", "lecture", "ALL", "AI302", "Design & Analysis of Algorithms", "DAA", "218", "NP", "Prof. Niyati Patel"),
    ("Tuesday", 4, "13:10:00", "15:10:00", "practical", "B1", "AI302", "Design & Analysis of Algorithms Lab", "DAA Lab", "Lab 3", "NP", "Prof. Niyati Patel"),
    ("Tuesday", 4, "13:10:00", "15:10:00", "practical", "C1", "AI301", "Operating Systems Lab", "OS Lab", "Lab 4", "GK", "Prof. Gaurav Kumar"),
    ("Tuesday", 4, "13:10:00", "15:10:00", "practical", "D1", "AI303", "Database Management Systems Lab", "DBMS Lab", "Lab 2", "GP", "Prof. Gaurang Patel"),
    ("Tuesday", 4, "13:10:00", "15:10:00", "practical", "A1", "AI304", "Library & Tutorial Study", "LIB", "Library", "FAC", "Library Staff"),
    ("Tuesday", 4, "13:10:00", "15:10:00", "practical", "E1", "AI306", "Web Technology Lab", "WT Lab", "Lab 1", "FAC", "Faculty In-Charge"),
    ("Tuesday", 6, "15:15:00", "17:15:00", "counseling", "B1", "COUN3", "Student Counseling & Mentorship", "COUN", "Cabin 205", "NP", "Prof. Niyati Patel"),

    # WEDNESDAY
    ("Wednesday", 1, "09:10:00", "10:10:00", "lecture", "ALL", "MA301", "Probability & Statistics", "PS", "218", "BS", "Prof. Bhargav Sobhana"),
    ("Wednesday", 2, "10:10:00", "11:10:00", "lecture", "ALL", "AI303", "Database Management Systems", "DBMS", "218", "GP", "Prof. Gaurang Patel"),
    ("Wednesday", 3, "11:10:00", "12:10:00", "lecture", "ALL", "AI301", "Operating Systems", "OS", "218", "GK", "Prof. Gaurav Kumar"),
    ("Wednesday", 4, "13:10:00", "15:10:00", "practical", "C1", "AI302", "Design & Analysis of Algorithms Lab", "DAA Lab", "Lab 3", "NP", "Prof. Niyati Patel"),
    ("Wednesday", 4, "13:10:00", "15:10:00", "practical", "D1", "AI301", "Operating Systems Lab", "OS Lab", "Lab 4", "GK", "Prof. Gaurav Kumar"),
    ("Wednesday", 4, "13:10:00", "15:10:00", "practical", "A1", "AI306", "Web Technology Lab", "WT Lab", "Lab 1", "NP", "Prof. Niyati Patel"),
    ("Wednesday", 4, "13:10:00", "15:10:00", "practical", "B1", "AI304", "Library & Tutorial Study", "LIB", "Library", "FAC", "Library Staff"),
    ("Wednesday", 4, "13:10:00", "15:10:00", "practical", "E1", "AI303", "Database Management Systems Lab", "DBMS Lab", "Lab 2", "GP", "Prof. Gaurang Patel"),
    ("Wednesday", 6, "15:15:00", "17:15:00", "counseling", "C1", "COUN3", "Student Counseling & Mentorship", "COUN", "Cabin 206", "BS", "Prof. Bhargav Sobhana"),

    # THURSDAY
    ("Thursday", 1, "09:10:00", "10:10:00", "lecture", "ALL", "AI302", "Design & Analysis of Algorithms", "DAA", "218", "NP", "Prof. Niyati Patel"),
    ("Thursday", 2, "10:10:00", "11:10:00", "lecture", "ALL", "MA301", "Probability & Statistics", "PS", "218", "BS", "Prof. Bhargav Sobhana"),
    ("Thursday", 3, "11:10:00", "12:10:00", "lecture", "ALL", "AI303", "Database Management Systems", "DBMS", "218", "GP", "Prof. Gaurang Patel"),
    ("Thursday", 4, "13:10:00", "15:10:00", "practical", "D1", "AI302", "Design & Analysis of Algorithms Lab", "DAA Lab", "Lab 3", "NP", "Prof. Niyati Patel"),
    ("Thursday", 4, "13:10:00", "15:10:00", "practical", "A1", "AI303", "Database Management Systems Lab", "DBMS Lab", "Lab 2", "GP", "Prof. Gaurang Patel"),
    ("Thursday", 4, "13:10:00", "15:10:00", "practical", "B1", "AI306", "Web Technology Lab", "WT Lab", "Lab 1", "NP", "Prof. Niyati Patel"),
    ("Thursday", 4, "13:10:00", "15:10:00", "practical", "C1", "AI304", "Library & Tutorial Study", "LIB", "Library", "FAC", "Library Staff"),
    ("Thursday", 4, "13:10:00", "15:10:00", "practical", "E1", "AI301", "Operating Systems Lab", "OS Lab", "Lab 4", "GK", "Prof. Gaurav Kumar"),
    ("Thursday", 6, "15:15:00", "17:15:00", "counseling", "D1", "COUN3", "Student Counseling & Mentorship", "COUN", "Cabin 207", "GP", "Prof. Gaurang Patel"),

    # FRIDAY
    ("Friday", 1, "09:10:00", "10:10:00", "lecture", "ALL", "AI301", "Operating Systems", "OS", "218", "GK", "Prof. Gaurav Kumar"),
    ("Friday", 2, "10:10:00", "11:10:00", "lecture", "ALL", "AI302", "Design & Analysis of Algorithms", "DAA", "218", "NP", "Prof. Niyati Patel"),
    ("Friday", 3, "11:10:00", "12:10:00", "lecture", "ALL", "MA301", "Probability & Statistics", "PS", "218", "BS", "Prof. Bhargav Sobhana"),
    ("Friday", 4, "13:10:00", "15:10:00", "practical", "A1", "AI301", "Operating Systems Lab", "OS Lab", "Lab 4", "GK", "Prof. Gaurav Kumar"),
    ("Friday", 4, "13:10:00", "15:10:00", "practical", "B1", "AI303", "Database Management Systems Lab", "DBMS Lab", "Lab 2", "GP", "Prof. Gaurang Patel"),
    ("Friday", 4, "13:10:00", "15:10:00", "practical", "C1", "AI306", "Web Technology Lab", "WT Lab", "Lab 1", "NP", "Prof. Niyati Patel"),
    ("Friday", 4, "13:10:00", "15:10:00", "practical", "D1", "AI304", "Library & Tutorial Study", "LIB", "Library", "FAC", "Library Staff"),
    ("Friday", 4, "13:10:00", "15:10:00", "practical", "E1", "AI302", "Design & Analysis of Algorithms Lab", "DAA Lab", "Lab 3", "NP", "Prof. Niyati Patel"),
    ("Friday", 6, "15:15:00", "17:15:00", "activity", "ALL", "CLUB3", "StudentHub Club Activities & Coding Lab", "CLUBS", "Seminar Hall", "FAC", "Faculty In-Charge"),

    # SATURDAY
    ("Saturday", 1, "09:10:00", "10:10:00", "lecture", "ALL", "AI303", "Database Management Systems", "DBMS", "218", "GP", "Prof. Gaurang Patel"),
    ("Saturday", 2, "10:10:00", "11:10:00", "lecture", "ALL", "MA301", "Probability & Statistics", "PS", "218", "BS", "Prof. Bhargav Sobhana"),
    ("Saturday", 3, "11:10:00", "13:10:00", "tutorial", "ALL", "AI307", "Remedial & Innovation Mentorship", "MENTOR", "Lab 1 & 2", "GK", "Prof. Gaurav Kumar")
]

def main():
    conn = pymysql.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("ALTER TABLE timetable_slots MODIFY COLUMN slot_type VARCHAR(50) NOT NULL DEFAULT 'lecture'")
    cur.execute("DELETE FROM timetable_slots")
    conn.commit()

    inserted = 0
    for day, slot_no, st, et, slot_type, batch, code, name, abbrev, room, fac_abbr, fac_name in TIMETABLE_SLOTS:
        cur.execute("""
            INSERT INTO timetable_slots (
                academic_year, semester, term, division, effective_date,
                day_of_week, slot_number, start_time, end_time, slot_type,
                batch, subject_code, subject_name, subject_abbrev,
                room_no, faculty_abbrev, faculty_name
            ) VALUES (
                '2026-2027', 3, 'Odd Term', 'Div I', '2026-07-06',
                %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s
            )
        """, (day, slot_no, st, et, slot_type, batch, code, name, abbrev, room, fac_abbr, fac_name))
        inserted += 1

    conn.commit()
    print(f"Inserted {inserted} official timetable slots for Semester 3 (Academic Year 2026-27, Div I).")

    # Verification: check Batch A1 slots count
    cur.execute("SELECT count(*) FROM timetable_slots WHERE batch IN ('ALL', 'A1')")
    a1_count = cur.fetchone()[0]
    print(f"Batch A1 (Anshika Badala's batch) applicable timetable slots: {a1_count}")

    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
