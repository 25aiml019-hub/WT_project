<?php
/**
 * StudentHub - Course Enrollment (Authenticated Student Portal)
 * Course: AIUE203 - Web Development Fundamentals
 * Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT
 */

require_once __DIR__ . '/../../app/config/config.php';
require_once __DIR__ . '/../../app/config/db.php';
require_once __DIR__ . '/../../app/config/security.php';
require_once __DIR__ . '/../../app/includes/auth_check.php';
require_once __DIR__ . '/../../app/services/course_service.php';
require_once __DIR__ . '/../../app/services/student_service.php';

// Strict Authentication Enforcement
if (!isAuthenticated()) {
    header('Location: login.html?error=unauthorized&redirect=course-enrollment.php');
    exit;
}

$currentUser = currentUser();
$userId = (int)($currentUser['id'] ?? 0);
$student = StudentService::findByUserId($userId);
if (!$student && ($currentUser['role'] ?? '') === 'admin') {
    $student = StudentService::findById(1);
}

if (!$student) {
    header('Location: login.html?error=unauthorized');
    exit;
}

$studentId = (int)$student['id'];
$message = '';
$messageType = '';

// Handle Enrollment POST Action
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $action = $_POST['action'] ?? '';
    $courseId = (int)($_POST['course_id'] ?? 0);

    if ($action === 'enroll' && $courseId > 0) {
        $res = CourseService::enrollStudent($studentId, $courseId, 3);
        $message = $res['message'];
        $messageType = $res['success'] ? 'success' : 'error';
    } elseif ($action === 'drop' && $courseId > 0) {
        $res = CourseService::dropEnrollment($studentId, $courseId);
        $message = $res['message'];
        $messageType = $res['success'] ? 'success' : 'error';
    }
}

$allCourses = CourseService::getAllCourses();
$enrollments = CourseService::getStudentEnrollments($studentId);
$enrolledIds = array_map(function($e) { return (int)$e['course_id']; }, $enrollments);

$totalCredits = 0;
foreach ($enrollments as $e) {
    $totalCredits += (int)($e['credits'] ?? 0);
}

$pageTitle = 'Course Enrollment';
$currentPage = 'course-enrollment';
$basePath = '../';
$extraCss = ['course-enrollment.css'];

require_once __DIR__ . '/../../app/includes/header.php';
require_once __DIR__ . '/../../app/includes/nav.php';
?>

    <main class="courses-container content-card">
        <div style="margin-bottom: 20px;">
            <a href="../student/index.php" style="text-decoration:none; color: var(--accent-color, #2563EB); font-weight: 600;">&larr; Back to Student Portal</a>
        </div>

        <div class="enrollment-header-summary">
            <div>
                <h2 style="margin: 0 0 6px; color: var(--primary-color, #1E3A8A);">Course Enrollment — Semester 3</h2>
                <p style="margin: 0; color: var(--text-muted, #64748B); font-size: 14px;">
                    Enrolled Student: <strong><?= htmlspecialchars($student['name'] ?? 'Student') ?></strong> (<?= htmlspecialchars($student['student_id'] ?? '25AIML002') ?>) &bull; <?= htmlspecialchars($student['course'] ?? 'B.Tech') ?>
                </p>
            </div>
            <div class="credit-counter-badge">
                Total Enrolled Credits: <strong><?= $totalCredits ?></strong> / 24 max
            </div>
        </div>

        <?php if ($message): ?>
            <div class="alert <?= $messageType === 'success' ? 'alert-success' : 'alert-danger' ?>" style="margin-bottom: 20px; padding: 12px 16px; border-radius: 6px; font-weight: 600;">
                <?= htmlspecialchars($message) ?>
            </div>
        <?php endif; ?>

        <!-- Active Enrollments Section -->
        <h3 style="color: var(--primary-color, #1E3A8A); margin: 24px 0 12px;">My Registered Courses (<?= count($enrollments) ?>)</h3>
        <?php if (empty($enrollments)): ?>
            <p style="color: #64748B;">You have not enrolled in any courses yet. Select courses from the catalog below.</p>
        <?php else: ?>
            <div class="table-responsive">
                <table class="data-table courses-table">
                    <thead>
                        <tr>
                            <th>Code</th>
                            <th>Course Title</th>
                            <th>Department</th>
                            <th>Credits</th>
                            <th>Status</th>
                            <th>Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($enrollments as $enr): ?>
                            <tr>
                                <td><strong><?= htmlspecialchars($enr['course_code']) ?></strong></td>
                                <td><?= htmlspecialchars($enr['course_name']) ?></td>
                                <td><?= htmlspecialchars($enr['department']) ?></td>
                                <td><?= (int)$enr['credits'] ?></td>
                                <td><span class="enrolled-badge">&#10003; Enrolled</span></td>
                                <td>
                                    <form method="POST" action="course-enrollment.php" style="display:inline;" onsubmit="return confirm('Are you sure you want to drop <?= htmlspecialchars($enr['course_code']) ?>?');">
                                        <input type="hidden" name="action" value="drop">
                                        <input type="hidden" name="course_id" value="<?= (int)$enr['course_id'] ?>">
                                        <button type="submit" class="btn-drop-action">Drop Course</button>
                                    </form>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        <?php endif; ?>

        <!-- Available Catalog Section -->
        <h3 style="color: var(--primary-color, #1E3A8A); margin: 35px 0 12px;">Available Semester 3 Curriculum</h3>
        <div class="table-responsive">
            <table class="data-table courses-table">
                <thead>
                    <tr>
                        <th>Code</th>
                        <th>Course Title</th>
                        <th>Credits</th>
                        <th>Description</th>
                        <th>Status / Action</th>
                    </tr>
                </thead>
                <tbody>
                    <?php foreach ($allCourses as $c): ?>
                        <?php $isEnrolled = in_array((int)$c['id'], $enrolledIds, true); ?>
                        <tr>
                            <td><strong><?= htmlspecialchars($c['course_code']) ?></strong></td>
                            <td><?= htmlspecialchars($c['course_name']) ?></td>
                            <td><?= (int)$c['credits'] ?></td>
                            <td style="max-width: 320px; font-size: 13px; color: #475569;"><?= htmlspecialchars($c['description'] ?? 'Curriculum core subject') ?></td>
                            <td>
                                <?php if ($isEnrolled): ?>
                                    <span class="enrolled-badge">&#10003; Enrolled</span>
                                <?php else: ?>
                                    <form method="POST" action="course-enrollment.php" style="display:inline;">
                                        <input type="hidden" name="action" value="enroll">
                                        <input type="hidden" name="course_id" value="<?= (int)$c['id'] ?>">
                                        <button type="submit" class="btn-enroll-action">Enroll in Course</button>
                                    </form>
                                <?php endif; ?>
                            </td>
                        </tr>
                    <?php endforeach; ?>
                </tbody>
            </table>
        </div>
    </main>

<?php
require_once __DIR__ . '/../../app/includes/footer.php';
?>
