import pymysql

conn = pymysql.connect(host="127.0.0.1", port=3307, user="root", password="", database="studenthub")
cur = conn.cursor()

# 1. Check and add columns to users table
cur.execute("SELECT COLUMN_NAME FROM information_schema.columns WHERE table_name = 'users' AND table_schema = 'studenthub'")
user_cols = [r[0] for r in cur.fetchall()]

if 'must_change_password' not in user_cols:
    cur.execute("ALTER TABLE users ADD COLUMN must_change_password TINYINT(1) NOT NULL DEFAULT 0 AFTER status")
    print("Added must_change_password to users")

if 'failed_login_attempts' not in user_cols:
    cur.execute("ALTER TABLE users ADD COLUMN failed_login_attempts INT NOT NULL DEFAULT 0 AFTER must_change_password")
    print("Added failed_login_attempts to users")

if 'lockout_until' not in user_cols:
    cur.execute("ALTER TABLE users ADD COLUMN lockout_until DATETIME NULL DEFAULT NULL AFTER failed_login_attempts")
    print("Added lockout_until to users")

# 2. Create semester_results table
cur.execute("""
CREATE TABLE IF NOT EXISTS semester_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    roll_no VARCHAR(20) NOT NULL,
    semester INT NOT NULL,
    sgpa DECIMAL(4,2) NULL DEFAULT NULL,
    credits DECIMAL(4,2) NOT NULL DEFAULT 0.00,
    is_missing TINYINT(1) NOT NULL DEFAULT 0,
    remarks VARCHAR(255) NULL DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_student_sem (student_id, semester),
    INDEX idx_roll_semester (roll_no, semester),
    CONSTRAINT fk_results_student FOREIGN KEY (student_id) REFERENCES students (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")
print("Created semester_results table")

# 3. Create unassigned_academic_records table
cur.execute("""
CREATE TABLE IF NOT EXISTS unassigned_academic_records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_no VARCHAR(20) NOT NULL,
    semester INT NOT NULL,
    sgpa DECIMAL(4,2) NOT NULL,
    credits DECIMAL(4,2) NOT NULL,
    quarantine_reason VARCHAR(255) NOT NULL DEFAULT 'Outside official 78-student FYAIML roster (25AIML079 - 25AIML090)',
    imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE KEY unique_unassigned_roll_sem (roll_no, semester)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")
print("Created unassigned_academic_records table")

# 4. Create timetable_slots table
cur.execute("""
CREATE TABLE IF NOT EXISTS timetable_slots (
    id INT AUTO_INCREMENT PRIMARY KEY,
    academic_year VARCHAR(20) NOT NULL DEFAULT '2026-27',
    semester INT NOT NULL DEFAULT 3,
    term VARCHAR(20) NOT NULL DEFAULT 'Odd Term',
    division VARCHAR(10) NOT NULL DEFAULT 'I',
    effective_date DATE NOT NULL DEFAULT '2026-07-06',
    day_of_week ENUM('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday') NOT NULL,
    slot_number INT NOT NULL,
    start_time VARCHAR(20) NOT NULL,
    end_time VARCHAR(20) NOT NULL,
    slot_type ENUM('lecture','lab','counselling','break','elective') NOT NULL DEFAULT 'lecture',
    batch ENUM('All','A1','B1','C1','D1','E1') NOT NULL DEFAULT 'All',
    subject_code VARCHAR(20) NULL DEFAULT NULL,
    subject_name VARCHAR(120) NULL DEFAULT NULL,
    subject_abbrev VARCHAR(20) NULL DEFAULT NULL,
    room_no VARCHAR(50) NULL DEFAULT NULL,
    faculty_abbrev VARCHAR(20) NULL DEFAULT NULL,
    faculty_name VARCHAR(120) NULL DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_day_batch (day_of_week, batch),
    INDEX idx_slot_order (day_of_week, slot_number)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
""")
print("Created timetable_slots table")

conn.commit()
conn.close()
print("Migration completed successfully!")
