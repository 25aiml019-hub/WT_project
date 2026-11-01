-- =======================================================
-- StudentHub Database Seeds
-- Course: AIUE203 - Web Development Fundamentals (WDF)
-- Student: Anshika Badala (25AIML002), CSPIT, CHARUSAT
-- =======================================================

USE `studenthub`;

-- -------------------------------------------------------
-- 1. Seed Users (passwords hashed with bcrypt for 'admin123' and 'student123')
-- -------------------------------------------------------
-- Note: 'admin123' hash: $2y$10$wE9f3M... standard PHP password_hash compatible
-- Fallback test user passwords can also be verified via PHP password_verify()
INSERT IGNORE INTO `users` (`id`, `username`, `email`, `password`, `role`, `status`) VALUES
(1, 'admin', 'admin@studenthub.com', '$2y$10$4aoZ5jm4FCNUPT62s9iSte4Qmr46gyt0OT3YhecSQz6nTwZEktsUW', 'admin', 'active'),
(2, 'anshika', 'anshikabadala2@gmail.com', '$2y$10$neO4OofXTK.9yWVd1dzt/.Cq4uXDDdvKjNi3sULxskOM3aD8UMWk.', 'student', 'active'),
(3, 'demo_student', 'student@studenthub.com', '$2y$10$neO4OofXTK.9yWVd1dzt/.Cq4uXDDdvKjNi3sULxskOM3aD8UMWk.', 'student', 'active');

-- -------------------------------------------------------
-- 2. Seed Students (Minimum 20 records required for Practical 11)
-- -------------------------------------------------------
INSERT IGNORE INTO `students` (`id`, `user_id`, `name`, `email`, `mobile`, `course`, `department`, `academic_year`, `gender`, `hobbies`, `address`, `status`) VALUES
(1, 2, 'Anshika Badala', 'anshikabadala2@gmail.com', '6354069434', 'B.Tech', 'Information Technology', '2023-2024', 'Female', 'Reading, Coding', 'CSPIT, CHARUSAT Campus, Changa', 'active'),
(2, NULL, 'Shruti Babariya', 'shruti@gmail.com', '6424633581', 'B.Tech', 'Computer Engineering', '2024-2025', 'Female', 'Dancing, Sports', 'Anand, Gujarat', 'active'),
(3, NULL, 'Disha Ghadiya', 'disha@gmail.com', '9824633581', 'B.Tech', 'Information Technology', '2025-2026', 'Female', 'Travelling, Music', 'Vadodara, Gujarat', 'active'),
(4, NULL, 'Diya Fefar', 'diya.fefar@gmail.com', '9924633582', 'B.Tech', 'Computer Engineering', '2025-2026', 'Female', 'Reading, Travelling', 'Rajkot, Gujarat', 'active'),
(5, NULL, 'Krisha Ghodasar', 'krisha.g@gmail.com', '9924633583', 'B.Tech', 'Information Technology', '2025-2026', 'Female', 'Sports, Coding', 'Ahmedabad, Gujarat', 'active'),
(6, NULL, 'Heshvi Shah', 'heshvi.shah@gmail.com', '9924633584', 'B.Tech', 'Computer Engineering', '2023-2024', 'Female', 'Dancing, Reading', 'Surat, Gujarat', 'active'),
(7, NULL, 'Aarav Patel', 'aarav.patel@charusat.edu.in', '9876500001', 'B.Tech', 'Computer Engineering', '2024-2025', 'Male', 'Sports, Gaming', 'Nadiad, Gujarat', 'active'),
(8, NULL, 'Bhavya Mehta', 'bhavya.mehta@charusat.edu.in', '9876500002', 'B.Tech', 'Information Technology', '2025-2026', 'Male', 'Coding, Music', 'Ahmedabad, Gujarat', 'active'),
(9, NULL, 'Chirag Joshi', 'chirag.joshi@charusat.edu.in', '9876500003', 'B.Tech', 'Mechanical Engineering', '2025-2026', 'Male', 'Travelling, Sports', 'Bhavnagar, Gujarat', 'active'),
(10, NULL, 'Drashti Dave', 'drashti.dave@charusat.edu.in', '9876500004', 'B.Tech', 'Civil Engineering', '2025-2026', 'Female', 'Reading, Art', 'Gandhinagar, Gujarat', 'active'),
(11, NULL, 'Eshan Trivedi', 'eshan.trivedi@charusat.edu.in', '9876500005', 'B.Tech', 'Computer Engineering', '2023-2024', 'Male', 'Coding, Chess', 'Vadodara, Gujarat', 'active'),
(12, NULL, 'Falguni Varma', 'falguni.varma@charusat.edu.in', '9876500006', 'B.Tech', 'Information Technology', '2024-2025', 'Female', 'Dancing, Travelling', 'Surat, Gujarat', 'active'),
(13, NULL, 'Gautam Sharma', 'gautam.sharma@charusat.edu.in', '9876500007', 'B.Tech', 'Mechanical Engineering', '2025-2026', 'Male', 'Sports, Photography', 'Rajkot, Gujarat', 'active'),
(14, NULL, 'Hetvi Rana', 'hetvi.rana@charusat.edu.in', '9876500008', 'B.Tech', 'Computer Engineering', '2025-2026', 'Female', 'Music, Coding', 'Anand, Gujarat', 'active'),
(15, NULL, 'Ishan Bhatt', 'ishan.bhatt@charusat.edu.in', '9876500009', 'B.Tech', 'Civil Engineering', '2025-2026', 'Male', 'Sports, Travelling', 'Ahmedabad, Gujarat', 'active'),
(16, NULL, 'Janvi Solanki', 'janvi.solanki@charusat.edu.in', '9876500010', 'B.Tech', 'Information Technology', '2023-2024', 'Female', 'Reading, Singing', 'Vadodara, Gujarat', 'active'),
(17, NULL, 'Kunal Parekh', 'kunal.parekh@charusat.edu.in', '9876500011', 'B.Tech', 'Computer Engineering', '2024-2025', 'Male', 'Gaming, Coding', 'Surat, Gujarat', 'active'),
(18, NULL, 'Lata Soni', 'lata.soni@charusat.edu.in', '9876500012', 'B.Tech', 'Mechanical Engineering', '2025-2026', 'Female', 'Art, Sports', 'Nadiad, Gujarat', 'active'),
(19, NULL, 'Manav Desai', 'manav.desai@charusat.edu.in', '9876500013', 'B.Tech', 'Computer Engineering', '2025-2026', 'Male', 'Coding, Travelling', 'Ahmedabad, Gujarat', 'active'),
(20, NULL, 'Nidhi Pandya', 'nidhi.pandya@charusat.edu.in', '9876500014', 'B.Tech', 'Civil Engineering', '2025-2026', 'Female', 'Reading, Photography', 'Vadodara, Gujarat', 'active');

-- -------------------------------------------------------
-- 3. Seed Events (from Practical 2 and Practical 12)
-- -------------------------------------------------------
INSERT IGNORE INTO `events` (`id`, `title`, `description`, `category`, `event_date`, `event_time`, `location`, `poster_image`, `status`) VALUES
(1, 'CHARUSAT Annual Hackathon', 'A 24-hour rapid prototyping hackathon focusing on AI and Web applications.', 'Technical', '2026-08-15', '09:00 AM', 'CSPIT Computer Center', 'hackathon.jpg', 'upcoming'),
(2, 'Campus Sports Day', 'Annual inter-department sports tournament covering football, cricket, and athletics.', 'Sports', '2026-08-22', '08:30 AM', 'University Sports Ground', 'sports.jpg', 'upcoming'),
(3, 'Tech Fest 2026', 'Flagship engineering exhibition, technical paper presentations, and robotics showcase.', 'Technical', '2026-09-10', '10:00 AM', 'Auditorium Hall A', 'techfest.jpg', 'upcoming'),
(4, 'Web Development Workshop', 'Hands-on bootcamp on modern PHP, REST APIs, and responsive design frameworks.', 'Workshop', '2026-09-25', '02:00 PM', 'Lab 3, Department of IT', 'web_dev.jpg', 'upcoming'),
(5, 'Cultural Night & Talent Hunt', 'An evening of music, drama, dance, and creative performances by students.', 'Cultural', '2026-10-05', '06:00 PM', 'Open Air Theatre', 'cultural.jpg', 'upcoming');

-- -------------------------------------------------------
-- 4. Seed Registrations
-- -------------------------------------------------------
INSERT IGNORE INTO `registrations` (`event_id`, `student_id`, `registered_at`) VALUES
(1, 1, '2026-08-01 10:00:00'),
(1, 2, '2026-08-01 11:30:00'),
(2, 1, '2026-08-02 14:15:00'),
(2, 3, '2026-08-02 16:45:00'),
(3, 4, '2026-08-05 09:20:00');

-- -------------------------------------------------------
-- 5. Seed Audit Logs
-- -------------------------------------------------------
INSERT IGNORE INTO `audit_logs` (`user_id`, `action`, `details`, `ip_address`, `created_at`) VALUES
(1, 'DATABASE_INITIALIZATION', 'Schema and seed data created successfully for StudentHub Phase 1', '127.0.0.1', CURRENT_TIMESTAMP);

-- -------------------------------------------------------
-- 6. Seed Contact Messages
-- -------------------------------------------------------
INSERT IGNORE INTO `contact_messages` (`id`, `name`, `email`, `subject`, `message`, `ip_address`, `status`) VALUES
(1, 'Pooja Trivedi', 'pooja.t@gmail.com', 'Admission Query for IT', 'Could you please provide the semester 3 elective subject syllabus?', '127.0.0.1', 'read'),
(2, 'Rohit Verma', 'rohit.v@gmail.com', 'Hackathon Registration Help', 'Is there any prerequisite for participating in the CHARUSAT Annual Hackathon?', '127.0.0.1', 'unread');
