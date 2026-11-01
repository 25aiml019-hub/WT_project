<?php
/**
 * Idempotent Class Roster & Academic Data Importer
 * StudentHub - CSPIT, CHARUSAT
 * Author: Anshika Badala (25AIML002)
 */

require_once __DIR__ . '/../app/config/config.php';
require_once __DIR__ . '/../app/config/db.php';

echo "=======================================================\n";
echo "Starting StudentHub Roster & Academic Data Import...\n";
echo "=======================================================\n";

$mysqli = Database::getMySQLi();

// 1. Seed Counselors
$counselorsData = [
    [
        'name'       => 'Prof. Gaurav Kumar',
        'email'      => 'gauravkumar.aiml@charusat.ac.in',
        'phone'      => '+91-7052082211',
        'department' => 'Department of Artificial Intelligence and Machine Learning',
        'room_no'    => 'Cabin 204'
    ],
    [
        'name'       => 'Prof. Niyati Patel',
        'email'      => 'niyatipatel.aiml@charusat.ac.in',
        'phone'      => '+91-9545396795',
        'department' => 'Department of Artificial Intelligence and Machine Learning',
        'room_no'    => 'Cabin 205'
    ],
    [
        'name'       => 'Prof. Bhargav Sobhana',
        'email'      => 'bhargavsobhana.aiml@charusat.ac.in',
        'phone'      => '+91-9978918349',
        'department' => 'Department of Artificial Intelligence and Machine Learning',
        'room_no'    => 'Cabin 206'
    ],
    [
        'name'       => 'Prof. Gaurang Patel',
        'email'      => 'gaurangpatel.me@charusat.ac.in',
        'phone'      => '+91-8141342100',
        'department' => 'Department of Artificial Intelligence and Machine Learning',
        'room_no'    => 'Cabin 207'
    ]
];

$counselorMap = []; // name => id
foreach ($counselorsData as $c) {
    $stmt = $mysqli->prepare("SELECT id FROM counselors WHERE email = ? LIMIT 1");
    $stmt->bind_param("s", $c['email']);
    $stmt->execute();
    $res = $stmt->get_result();
    if ($row = $res->fetch_assoc()) {
        $counselorMap[$c['name']] = (int)$row['id'];
    } else {
        $insert = $mysqli->prepare("INSERT INTO counselors (name, email, phone, department, room_no) VALUES (?, ?, ?, ?, ?)");
        $insert->bind_param("sssss", $c['name'], $c['email'], $c['phone'], $c['department'], $c['room_no']);
        $insert->execute();
        $counselorMap[$c['name']] = $mysqli->insert_id;
        $insert->close();
    }
    $stmt->close();
}
echo "Counselors seeded: " . count($counselorMap) . "\n";

// 2. Seed Batches
$batchesData = [
    ['batch_name' => 'Batch A', 'start_id' => '25AIML001', 'end_id' => '25AIML020', 'counselor_name' => 'Prof. Gaurav Kumar'],
    ['batch_name' => 'Batch B', 'start_id' => '25AIML021', 'end_id' => '25AIML040', 'counselor_name' => 'Prof. Niyati Patel'],
    ['batch_name' => 'Batch C', 'start_id' => '25AIML041', 'end_id' => '25AIML060', 'counselor_name' => 'Prof. Bhargav Sobhana'],
    ['batch_name' => 'Batch D', 'start_id' => '25AIML061', 'end_id' => '25AIML078', 'counselor_name' => 'Prof. Gaurang Patel']
];

$batchMap = []; // batch_name => id
foreach ($batchesData as $b) {
    $cid = $counselorMap[$b['counselor_name']] ?? null;
    $stmt = $mysqli->prepare("SELECT id FROM batches WHERE batch_name = ? LIMIT 1");
    $stmt->bind_param("s", $b['batch_name']);
    $stmt->execute();
    $res = $stmt->get_result();
    if ($row = $res->fetch_assoc()) {
        $batchMap[$b['batch_name']] = (int)$row['id'];
        $update = $mysqli->prepare("UPDATE batches SET counselor_id = ?, start_id = ?, end_id = ? WHERE id = ?");
        $update->bind_param("issi", $cid, $b['start_id'], $b['end_id'], $row['id']);
        $update->execute();
        $update->close();
    } else {
        $insert = $mysqli->prepare("INSERT INTO batches (batch_name, academic_year, counselor_id, start_id, end_id) VALUES (?, '2025-2026', ?, ?, ?)");
        $insert->bind_param("siss", $b['batch_name'], $cid, $b['start_id'], $b['end_id']);
        $insert->execute();
        $batchMap[$b['batch_name']] = $mysqli->insert_id;
        $insert->close();
    }
    $stmt->close();
}
echo "Batches seeded: " . count($batchMap) . "\n";

// 3. Import 78 AIML Students from JSON
$jsonPath = __DIR__ . '/roster_data.json';
if (!file_exists($jsonPath)) {
    die("Error: roster_data.json not found!\n");
}

$students = json_decode(file_get_contents($jsonPath), true);
if (!is_array($students) || count($students) !== 78) {
    die("Error: roster_data.json does not contain 78 students! Found: " . count($students) . "\n");
}

$counselorByName = [
    'Batch A' => $counselorMap['Prof. Gaurav Kumar'],
    'Batch B' => $counselorMap['Prof. Niyati Patel'],
    'Batch C' => $counselorMap['Prof. Bhargav Sobhana'],
    'Batch D' => $counselorMap['Prof. Gaurang Patel']
];

$importedCount = 0;
$updatedCount = 0;

foreach ($students as $s) {
    $studentId     = $s['student_id'];
    $tempStudentId = $s['temp_student_id'];
    $fullName      = $s['full_name'];
    $batchName     = $s['batch'];
    $batchId       = $batchMap[$batchName] ?? null;
    $counselorId   = $counselorByName[$batchName] ?? null;

    // Special matching for Anshika Badala (25AIML002) to preserve user account link
    if ($studentId === '25AIML002') {
        $stmtAnshika = $mysqli->prepare("SELECT id FROM students WHERE email = 'anshikabadala2@gmail.com' OR name LIKE '%Anshika%' LIMIT 1");
        $stmtAnshika->execute();
        $resAnshika = $stmtAnshika->get_result();
        if ($rowAnshika = $resAnshika->fetch_assoc()) {
            $upd = $mysqli->prepare("UPDATE students SET student_id = ?, temp_student_id = ?, batch_id = ?, counselor_id = ?, department = 'Artificial Intelligence and Machine Learning', course = 'B.Tech', academic_year = '2025-2026', cgpa = 8.77 WHERE id = ?");
            $upd->bind_param("ssiii", $studentId, $tempStudentId, $batchId, $counselorId, $rowAnshika['id']);
            $upd->execute();
            $upd->close();
            $updatedCount++;
            $stmtAnshika->close();
            continue;
        }
        $stmtAnshika->close();
    }

    // Check if student exists by student_id or temp_student_id
    $check = $mysqli->prepare("SELECT id FROM students WHERE student_id = ? OR temp_student_id = ? LIMIT 1");
    $check->bind_param("ss", $studentId, $tempStudentId);
    $check->execute();
    $resCheck = $check->get_result();

    if ($rowCheck = $resCheck->fetch_assoc()) {
        $sid = (int)$rowCheck['id'];
        $upd = $mysqli->prepare("UPDATE students SET student_id = ?, temp_student_id = ?, name = ?, batch_id = ?, counselor_id = ?, department = 'Artificial Intelligence and Machine Learning', course = 'B.Tech', academic_year = '2025-2026' WHERE id = ?");
        $upd->bind_param("sssiii", $studentId, $tempStudentId, $fullName, $batchId, $counselorId, $sid);
        $upd->execute();
        $upd->close();
        $updatedCount++;
    } else {
        // Insert new student record (email left NULL until administrator verifies / student registers)
        $ins = $mysqli->prepare(
            "INSERT INTO students (student_id, temp_student_id, name, course, batch_id, counselor_id, department, academic_year, status, gender) " .
            "VALUES (?, ?, ?, 'B.Tech', ?, ?, 'Artificial Intelligence and Machine Learning', '2025-2026', 'active', 'Other')"
        );
        $ins->bind_param("sssii", $studentId, $tempStudentId, $fullName, $batchId, $counselorId);
        $ins->execute();
        $ins->close();
        $importedCount++;
    }
    $check->close();
}

echo "Students processed: " . count($students) . " (New: {$importedCount}, Updated: {$updatedCount})\n";

// 4. Seed Clubs
$clubsData = [
    [
        'slug'         => 'sports',
        'name'         => 'Sports Club',
        'category'     => 'Athletics & Fitness',
        'lead_name'    => 'Prof. Coach Sharma',
        'banner_image' => 'https://rockytopsportsworld.com/wp-content/uploads/2019/07/sports-balls.jpg',
        'description'  => 'Promotes athletic development, fitness, and team synergy across basketball, football, volleyball, badminton, cricket, and athletics.',
        'objectives'   => 'Promote physical fitness, organize annual sports meets, participate in inter-university championships, and instill values of discipline and sportsmanship.'
    ],
    [
        'slug'         => 'music',
        'name'         => 'Music Club',
        'category'     => 'Performing Arts',
        'lead_name'    => 'Prof. Swara Joshi',
        'banner_image' => 'https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&w=1200&q=80',
        'description'  => 'A vibrant community for singers, musicians, composers, and sound enthusiasts exploring Indian classical, western vocal, and contemporary music.',
        'objectives'   => 'Provide performance platforms, organize live campus jam sessions, participate in university cultural fests, and conduct instrumental workshops.'
    ],
    [
        'slug'         => 'coding',
        'name'         => 'Coding Club',
        'category'     => 'Technology & Innovation',
        'lead_name'    => 'Prof. Niyati Patel',
        'banner_image' => 'https://media.istockphoto.com/id/1484758991/photo/hackathon-concept-the-meeting-at-the-white-office-table.jpg?s=612x612&w=0&k=20&c=ifl2F6QptCk87wh82yIX7HLILdvmoMdJeB92zr4BR6o=',
        'description'  => 'Cultivates high-impact software engineering, competitive programming, AI/ML hackathons, open-source projects, and technical interview preparation.',
        'objectives'   => 'Sharpen problem-solving skills, host 24-hour campus hackathons, facilitate collaborative GitHub projects, and conduct peer-led web and AI bootcamps.'
    ],
    [
        'slug'         => 'photography',
        'name'         => 'Photography Club',
        'category'     => 'Visual Arts & Media',
        'lead_name'    => 'Prof. Darshan Shah',
        'banner_image' => 'https://images.unsplash.com/photo-1452587925148-ce544e77e70d?auto=format&fit=crop&w=1200&q=80',
        'description'  => 'Captures campus moments through digital photography, portraiture, landscape, street photography, photojournalism, and post-processing workshops.',
        'objectives'   => 'Document official university celebrations, organize campus photo walks, host annual visual art galleries, and teach digital photo editing techniques.'
    ]
];

foreach ($clubsData as $cl) {
    $chk = $mysqli->prepare("SELECT id FROM clubs WHERE slug = ? LIMIT 1");
    $chk->bind_param("s", $cl['slug']);
    $chk->execute();
    $chkRes = $chk->get_result();
    if ($rowC = $chkRes->fetch_assoc()) {
        $up = $mysqli->prepare("UPDATE clubs SET name = ?, category = ?, lead_name = ?, banner_image = ?, description = ?, objectives = ? WHERE id = ?");
        $up->bind_param("ssssssi", $cl['name'], $cl['category'], $cl['lead_name'], $cl['banner_image'], $cl['description'], $cl['objectives'], $rowC['id']);
        $up->execute();
        $up->close();
    } else {
        $in = $mysqli->prepare("INSERT INTO clubs (slug, name, category, lead_name, banner_image, description, objectives) VALUES (?, ?, ?, ?, ?, ?, ?)");
        $in->bind_param("sssssss", $cl['slug'], $cl['name'], $cl['category'], $cl['lead_name'], $cl['banner_image'], $cl['description'], $cl['objectives']);
        $in->execute();
        $in->close();
    }
    $chk->close();
}
echo "Clubs seeded: 4\n";

// 5. Seed Courses
$coursesData = [
    [
        'code'   => 'AIUE203',
        'name'   => 'Web Development Fundamentals',
        'dept'   => 'Artificial Intelligence and Machine Learning',
        'degree' => 'B.Tech',
        'sem'    => 3,
        'creds'  => 4,
        'desc'   => 'Covers HTML5 semantic layout, responsive CSS, JavaScript ES6+, Fetch API, PHP form validation, MySQL relational architecture, and secure web development.'
    ],
    [
        'code'   => 'CEUE203',
        'name'   => 'Object Oriented Programming with Java',
        'dept'   => 'Artificial Intelligence and Machine Learning',
        'degree' => 'B.Tech',
        'sem'    => 3,
        'creds'  => 4,
        'desc'   => 'In-depth study of object-oriented paradigms, classes, inheritance, polymorphism, abstract data types, exception handling, multithreading, and Java collections.'
    ],
    [
        'code'   => 'MAUE201',
        'name'   => 'Discrete Mathematics & Graph Theory',
        'dept'   => 'Artificial Intelligence and Machine Learning',
        'degree' => 'B.Tech',
        'sem'    => 3,
        'creds'  => 4,
        'desc'   => 'Set theory, propositional logic, relations, functions, recurrence relations, combinatorics, graph theory, trees, and Boolean algebra for computation.'
    ],
    [
        'code'   => 'AIUC201',
        'name'   => 'Data Structures & Algorithms',
        'dept'   => 'Artificial Intelligence and Machine Learning',
        'degree' => 'B.Tech',
        'sem'    => 3,
        'creds'  => 4,
        'desc'   => 'Arrays, linked lists, stacks, queues, binary search trees, heaps, hashing, graph traversals, greedy methods, dynamic programming, and asymptotic analysis.'
    ],
    [
        'code'   => 'CEUE204',
        'name'   => 'Database Management Systems',
        'dept'   => 'Artificial Intelligence and Machine Learning',
        'degree' => 'B.Tech',
        'sem'    => 3,
        'creds'  => 4,
        'desc'   => 'Relational data modeling, SQL queries, normalization (1NF-BCNF), transaction processing, ACID properties, indexing, concurrency control, and query optimization.'
    ],
    [
        'code'   => 'DCN201',
        'name'   => 'Data Communication & Networking',
        'dept'   => 'Artificial Intelligence and Machine Learning',
        'degree' => 'B.Tech',
        'sem'    => 3,
        'creds'  => 3,
        'desc'   => 'OSI reference model, TCP/IP protocol suite, data link layer framing, error correction, IP addressing, subnetting, routing protocols, and socket programming.'
    ]
];

$courseMap = []; // code => id
foreach ($coursesData as $co) {
    $chk = $mysqli->prepare("SELECT id FROM courses WHERE course_code = ? LIMIT 1");
    $chk->bind_param("s", $co['code']);
    $chk->execute();
    $chkRes = $chk->get_result();
    if ($rowCo = $chkRes->fetch_assoc()) {
        $courseMap[$co['code']] = (int)$rowCo['id'];
    } else {
        $in = $mysqli->prepare("INSERT INTO courses (course_code, course_name, department, degree, semester, credits, description) VALUES (?, ?, ?, ?, ?, ?, ?)");
        $in->bind_param("sssssis", $co['code'], $co['name'], $co['dept'], $co['degree'], $co['sem'], $co['creds'], $co['desc']);
        $in->execute();
        $courseMap[$co['code']] = $mysqli->insert_id;
        $in->close();
    }
    $chk->close();
}
echo "Courses seeded: " . count($courseMap) . "\n";

// 6. Enroll Anshika Badala (Student #1/25AIML002) in Semester 3 Courses
$stmtAnshikaId = $mysqli->prepare("SELECT id FROM students WHERE student_id = '25AIML002' OR email = 'anshikabadala2@gmail.com' LIMIT 1");
$stmtAnshikaId->execute();
$anshikaRes = $stmtAnshikaId->get_result();
if ($aRow = $anshikaRes->fetch_assoc()) {
    $aStudentId = (int)$aRow['id'];
    foreach ($courseMap as $cCode => $cId) {
        $enr = $mysqli->prepare("INSERT IGNORE INTO course_enrollments (student_id, course_id, semester, academic_year, status) VALUES (?, ?, 3, '2025-2026', 'enrolled')");
        $enr->bind_param("ii", $aStudentId, $cId);
        $enr->execute();
        $enr->close();
    }
    echo "Enrolled Anshika Badala in " . count($courseMap) . " semester courses.\n";
}
$stmtAnshikaId->close();

// 7. Seed Teachers & Subjects
$teachersData = [
    ['emp' => 'T-AIML-01', 'name' => 'Prof. Gaurav Kumar', 'email' => 'gauravkumar.aiml@charusat.ac.in', 'desig' => 'Assistant Professor & Counselor', 'cabin' => 'Cabin 204'],
    ['emp' => 'T-AIML-02', 'name' => 'Prof. Niyati Patel', 'email' => 'niyatipatel.aiml@charusat.ac.in', 'desig' => 'Assistant Professor & Counselor', 'cabin' => 'Cabin 205'],
    ['emp' => 'T-AIML-03', 'name' => 'Prof. Bhargav Sobhana', 'email' => 'bhargavsobhana.aiml@charusat.ac.in', 'desig' => 'Assistant Professor & Counselor', 'cabin' => 'Cabin 206'],
    ['emp' => 'T-AIML-04', 'name' => 'Prof. Gaurang Patel', 'email' => 'gaurangpatel.me@charusat.ac.in', 'desig' => 'Assistant Professor & Counselor', 'cabin' => 'Cabin 207'],
    ['emp' => 'T-AIML-05', 'name' => 'Dr. Amit Ganatra', 'email' => 'amitganatra.it@charusat.ac.in', 'desig' => 'Dean & Professor', 'cabin' => 'Dean Office 101']
];

$teacherMap = [];
foreach ($teachersData as $t) {
    $chk = $mysqli->prepare("SELECT id FROM teachers WHERE employee_id = ? LIMIT 1");
    $chk->bind_param("s", $t['emp']);
    $chk->execute();
    $resT = $chk->get_result();
    if ($rowT = $resT->fetch_assoc()) {
        $teacherMap[$t['name']] = (int)$rowT['id'];
    } else {
        $in = $mysqli->prepare("INSERT INTO teachers (employee_id, name, email, designation, cabin) VALUES (?, ?, ?, ?, ?)");
        $in->bind_param("sssss", $t['emp'], $t['name'], $t['email'], $t['desig'], $t['cabin']);
        $in->execute();
        $teacherMap[$t['name']] = $mysqli->insert_id;
        $in->close();
    }
    $chk->close();
}
echo "Teachers seeded: " . count($teacherMap) . "\n";

// 8. Seed Subjects
$subjectsData = [
    ['code' => 'AIUE203', 'name' => 'Web Development Fundamentals', 'creds' => 4, 'sem' => 3],
    ['code' => 'CEUE203', 'name' => 'Object Oriented Programming with Java', 'creds' => 4, 'sem' => 3],
    ['code' => 'MAUE201', 'name' => 'Discrete Mathematics & Graph Theory', 'creds' => 4, 'sem' => 3],
    ['code' => 'AIUC201', 'name' => 'Data Structures & Algorithms', 'creds' => 4, 'sem' => 3],
    ['code' => 'CEUE204', 'name' => 'Database Management Systems', 'creds' => 4, 'sem' => 3],
    ['code' => 'DCN201', 'name' => 'Data Communication & Networking', 'creds' => 3, 'sem' => 3]
];

$subjectMap = [];
foreach ($subjectsData as $sub) {
    $chk = $mysqli->prepare("SELECT id FROM subjects WHERE subject_code = ? LIMIT 1");
    $chk->bind_param("s", $sub['code']);
    $chk->execute();
    $resSub = $chk->get_result();
    if ($rowSub = $resSub->fetch_assoc()) {
        $subjectMap[$sub['code']] = (int)$rowSub['id'];
    } else {
        $in = $mysqli->prepare("INSERT INTO subjects (subject_code, subject_name, credits, semester) VALUES (?, ?, ?, ?)");
        $in->bind_param("ssii", $sub['code'], $sub['name'], $sub['creds'], $sub['sem']);
        $in->execute();
        $subjectMap[$sub['code']] = $mysqli->insert_id;
        $in->close();
    }
    $chk->close();
}
echo "Subjects seeded: " . count($subjectMap) . "\n";

// 9. Seed Teacher Assignments & Timetable
$assignmentsData = [
    ['teacher' => 'Prof. Gaurav Kumar', 'subject' => 'AIUE203', 'batch' => 'Batch A', 'day' => 'Monday', 'start' => '09:00:00', 'end' => '10:00:00', 'room' => 'Lab 301'],
    ['teacher' => 'Prof. Niyati Patel', 'subject' => 'CEUE203', 'batch' => 'Batch A', 'day' => 'Monday', 'start' => '10:15:00', 'end' => '11:15:00', 'room' => 'Classroom 204'],
    ['teacher' => 'Prof. Bhargav Sobhana', 'subject' => 'AIUC201', 'batch' => 'Batch A', 'day' => 'Tuesday', 'start' => '09:00:00', 'end' => '10:00:00', 'room' => 'Classroom 204'],
    ['teacher' => 'Prof. Gaurang Patel', 'subject' => 'CEUE204', 'batch' => 'Batch A', 'day' => 'Wednesday', 'start' => '11:30:00', 'end' => '12:30:00', 'room' => 'Classroom 205'],
    ['teacher' => 'Dr. Amit Ganatra', 'subject' => 'DCN201', 'batch' => 'Batch A', 'day' => 'Thursday', 'start' => '02:00:00', 'end' => '03:00:00', 'room' => 'Auditorium A']
];

foreach ($assignmentsData as $asg) {
    $tid = $teacherMap[$asg['teacher']] ?? null;
    $sid = $subjectMap[$asg['subject']] ?? null;
    $bid = $batchMap[$asg['batch']] ?? null;

    if ($tid && $sid) {
        $chk = $mysqli->prepare("SELECT id FROM teacher_assignments WHERE teacher_id = ? AND subject_id = ? AND batch_id = ? LIMIT 1");
        $chk->bind_param("iii", $tid, $sid, $bid);
        $chk->execute();
        $resA = $chk->get_result();
        $assignId = null;
        if ($rowA = $resA->fetch_assoc()) {
            $assignId = (int)$rowA['id'];
        } else {
            $in = $mysqli->prepare("INSERT INTO teacher_assignments (teacher_id, subject_id, batch_id, academic_year) VALUES (?, ?, ?, '2025-2026')");
            $in->bind_param("iii", $tid, $sid, $bid);
            $in->execute();
            $assignId = $mysqli->insert_id;
            $in->close();
        }
        $chk->close();

        if ($assignId) {
            $chkTime = $mysqli->prepare("SELECT id FROM timetable WHERE assignment_id = ? AND day_of_week = ? LIMIT 1");
            $chkTime->bind_param("is", $assignId, $asg['day']);
            $chkTime->execute();
            if ($chkTime->get_result()->num_rows === 0) {
                $inTime = $mysqli->prepare("INSERT INTO timetable (assignment_id, day_of_week, start_time, end_time, room_no) VALUES (?, ?, ?, ?, ?)");
                $inTime->bind_param("issss", $assignId, $asg['day'], $asg['start'], $asg['end'], $asg['room']);
                $inTime->execute();
                $inTime->close();
            }
            $chkTime->close();
        }
    }
}
echo "Teacher assignments & timetable seeded.\n";

// 10. Seed Announcements
$announcements = [
    [
        'title'    => 'Mid-Semester Examination Schedule for FYAIML',
        'content'  => 'The mid-semester theoretical and practical examinations for the 3rd Semester B.Tech (AIML) will commence from November 15, 2026. Students are advised to verify their subject registrations.',
        'category' => 'Examination'
    ],
    [
        'title'    => 'Annual Campus Hackathon Registrations Open',
        'content'  => 'The Coding Club announces the CHARUSAT Annual Hackathon 2026. Teams of 2 to 4 students can register through the Events portal before November 10.',
        'category' => 'Events'
    ],
    [
        'title'    => 'Academic Counseling Session with Assigned Mentors',
        'content'  => 'Counseling meetings for Batch A, B, C, and D students with their respective faculty counselors are scheduled every Friday from 3:30 PM to 4:30 PM.',
        'category' => 'Counseling'
    ]
];

foreach ($announcements as $ann) {
    $chk = $mysqli->prepare("SELECT id FROM announcements WHERE title = ? LIMIT 1");
    $chk->bind_param("s", $ann['title']);
    $chk->execute();
    if ($chk->get_result()->num_rows === 0) {
        $in = $mysqli->prepare("INSERT INTO announcements (title, content, category) VALUES (?, ?, ?)");
        $in->bind_param("sss", $ann['title'], $ann['content'], $ann['category']);
        $in->execute();
        $in->close();
    }
    $chk->close();
}
echo "Announcements seeded: " . count($announcements) . "\n";

echo "=======================================================\n";
echo "SUCCESS: Roster & Academic Data Imported Cleanly!\n";
echo "=======================================================\n";
