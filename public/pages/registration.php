<?php
/**
 * StudentHub - Modular Registration Page (PHP)
 * Course: AIUE203 - Web Development Fundamentals (Practical 7 & 8)
 * Author: Daksh Harkhani (25AIML019)
 */

require_once __DIR__ . '/../../app/config/config.php';
require_once __DIR__ . '/../../app/config/security.php';

initSession();

$pageTitle = 'Student Registration';
$currentPage = 'registration';
$basePath = '../';
$extraCss = ['registration.css'];

$csrfToken = getCsrfToken();
$successMessage = $_SESSION['form_success'] ?? null;
$errorMessages = $_SESSION['form_errors'] ?? [];
$old = $_SESSION['form_old'] ?? [];

unset($_SESSION['form_success'], $_SESSION['form_errors'], $_SESSION['form_old']);

require_once __DIR__ . '/../../app/includes/header.php';
require_once __DIR__ . '/../../app/includes/nav.php';
?>

    <main>
        <form id="registrationForm" class="registration-form" method="POST" action="../process-registration.php" onsubmit="return registerForm(event)">
            <h2>New Student Registration</h2>

            <div id="registrationAlert" class="alert-box" style="<?= empty($successMessage) && empty($errorMessages) ? 'display: none;' : '' ?>" role="alert">
                <?php if (!empty($successMessage)): ?>
                    <div class="alert-box alert-success"><?= e($successMessage) ?></div>
                <?php endif; ?>
                <?php if (!empty($errorMessages)): ?>
                    <div class="alert-box alert-error">
                        <?php foreach ($errorMessages as $err): ?>
                            <div><?= e($err) ?></div>
                        <?php endforeach; ?>
                    </div>
                <?php endif; ?>
            </div>

            <input type="hidden" name="csrf_token" id="csrf_token" value="<?= e($csrfToken) ?>">

            <label for="name">Name:</label>
            <input type="text" id="name" name="name" placeholder="Enter your name" value="<?= e($old['name'] ?? '') ?>" required>

            <label for="email">Email:</label>
            <input type="email" id="email" name="email" placeholder="Enter your email" value="<?= e($old['email'] ?? '') ?>" required>

            <label for="mobile">Mobile:</label>
            <input type="text" id="mobile" name="mobile" placeholder="Enter your Mobile no" maxlength="10" value="<?= e($old['mobile'] ?? '') ?>" required>

            <label for="course">Course:</label>
            <input type="text" id="course" name="course" placeholder="Enter the course" value="<?= e($old['course'] ?? '') ?>" required>

            <label>Gender:</label>
            <div class="options-group">
                <?php $curGender = $old['gender'] ?? ''; ?>
                <label><input type="radio" name="gender" value="Male" <?= $curGender === 'Male' ? 'checked' : '' ?>> Male</label>
                <label><input type="radio" name="gender" value="Female" <?= $curGender === 'Female' ? 'checked' : '' ?>> Female</label>
                <label><input type="radio" name="gender" value="Other" <?= $curGender === 'Other' ? 'checked' : '' ?>> Other</label>
            </div>

            <label for="department">Department:</label>
            <select id="department" name="department" required>
                <?php $curDept = $old['department'] ?? ''; ?>
                <option value="">Select Department</option>
                <option value="Computer Engineering" <?= $curDept === 'Computer Engineering' ? 'selected' : '' ?>>Computer Engineering</option>
                <option value="Information Technology" <?= $curDept === 'Information Technology' ? 'selected' : '' ?>>Information Technology</option>
                <option value="Mechanical Engineering" <?= $curDept === 'Mechanical Engineering' ? 'selected' : '' ?>>Mechanical Engineering</option>
                <option value="Civil Engineering" <?= $curDept === 'Civil Engineering' ? 'selected' : '' ?>>Civil Engineering</option>
            </select>

            <label>Hobbies:</label>
            <div class="options-group">
                <?php $curHobbies = (array)($old['hobbies'] ?? []); ?>
                <label><input type="checkbox" name="hobby[]" value="Travelling" <?= in_array('Travelling', $curHobbies) ? 'checked' : '' ?>> Travelling</label>
                <label><input type="checkbox" name="hobby[]" value="Dancing" <?= in_array('Dancing', $curHobbies) ? 'checked' : '' ?>> Dancing</label>
                <label><input type="checkbox" name="hobby[]" value="Singing" <?= in_array('Singing', $curHobbies) ? 'checked' : '' ?>> Singing</label>
                <label><input type="checkbox" name="hobby[]" value="Sports" <?= in_array('Sports', $curHobbies) ? 'checked' : '' ?>> Sports</label>
                <label><input type="checkbox" name="hobby[]" value="Reading" <?= in_array('Reading', $curHobbies) ? 'checked' : '' ?>> Reading</label>
                <label><input type="checkbox" name="hobby[]" value="Other" <?= in_array('Other', $curHobbies) ? 'checked' : '' ?>> Other</label>
            </div>

            <label for="username">Username (Optional):</label>
            <input type="text" id="username" name="username" placeholder="Choose a username" value="<?= e($old['username'] ?? '') ?>">

            <label for="password">Password:</label>
            <input type="password" id="password" name="password" placeholder="Create a password (min 6 characters)" minlength="6" required>

            <label for="confirm_password">Confirm Password:</label>
            <input type="password" id="confirm_password" name="confirm_password" placeholder="Confirm your password" minlength="6" required>

            <label for="address">Address:</label>
            <textarea id="address" name="address" rows="5" cols="30" placeholder="Enter your address" required><?= e($old['address'] ?? '') ?></textarea>

            <div class="buttons">
                <input type="submit" value="Register" class="btn">
                <input type="button" value="Reset" class="btn" onclick="resetForm()">
            </div>
        </form>
    </main>

    <!-- JavaScript Validation -->
    <script src="../assets/js/registration.js"></script>
    <script src="../assets/js/main.js"></script>

<?php
require_once __DIR__ . '/../../app/includes/footer.php';
?>
