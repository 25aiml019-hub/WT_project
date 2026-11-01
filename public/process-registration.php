<?php
/**
 * Student Registration Form Processor (Practical 9: Secure Registration)
 * StudentHub - CSPIT, CHARUSAT
 * Course: AIUE203 - Web Development Fundamentals (Practical 7, 8 & 9)
 * Author: Anshika Badala (25AIML002)
 */

require_once __DIR__ . '/../app/config/config.php';
require_once __DIR__ . '/../app/config/security.php';
require_once __DIR__ . '/../app/services/user_service.php';
require_once __DIR__ . '/../app/services/student_service.php';

initSession();

// Determine if the client expects a JSON response (Fetch API / AJAX)
$isAjax = (!empty($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest') ||
          (isset($_SERVER['HTTP_ACCEPT']) && strpos($_SERVER['HTTP_ACCEPT'], 'application/json') !== false) ||
          (isset($_SERVER['CONTENT_TYPE']) && strpos($_SERVER['CONTENT_TYPE'], 'application/json') !== false);

/**
 * Send JSON or HTML redirect response
 */
function sendResponse(int $statusCode, bool $success, string $message, array $extra = [], bool $isAjax = true): void {
    http_response_code($statusCode);
    if ($isAjax) {
        header('Content-Type: application/json; charset=utf-8');
        echo json_encode(array_merge([
            'success' => $success,
            'message' => $message,
            'status'  => $statusCode
        ], $extra));
        exit;
    }

    if ($success) {
        $_SESSION['form_success'] = $message;
        unset($_SESSION['form_errors'], $_SESSION['form_old']);
        header('Location: pages/registration.html?success=1');
    } else {
        $_SESSION['form_errors'] = $extra['errors'] ?? [$message];
        $_SESSION['form_old'] = $extra['old'] ?? [];
        header('Location: pages/registration.html?error=1');
    }
    exit;
}

// -------------------------------------------------------------
// 1. HTTP Method Enforcement (Must be POST)
// -------------------------------------------------------------
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Allow: POST');
    sendResponse(405, false, 'Method Not Allowed. Only HTTP POST submissions are accepted.', [], $isAjax);
}

// -------------------------------------------------------------
// 2. CSRF Token Verification
// -------------------------------------------------------------
$csrfToken = $_POST['csrf_token'] ?? $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
if (!empty($csrfToken) || !empty($_SESSION['csrf_token'])) {
    if (!validateCsrfToken($csrfToken)) {
        sendResponse(403, false, 'CSRF verification failed. Form submission rejected.', [], $isAjax);
    }
}

// -------------------------------------------------------------
// 3. Extract & Sanitize Input Fields
// -------------------------------------------------------------
$name            = sanitizeString($_POST['name'] ?? '');
$username        = sanitizeString($_POST['username'] ?? '');
$email           = sanitizeEmail($_POST['email'] ?? '');
$mobile          = sanitizeString($_POST['mobile'] ?? '');
$course          = sanitizeString($_POST['course'] ?? '');
$department      = sanitizeString($_POST['department'] ?? '');
$gender          = sanitizeString($_POST['gender'] ?? '');
$address         = sanitizeString($_POST['address'] ?? '');
$password        = $_POST['password'] ?? '';
$confirmPassword = $_POST['confirm_password'] ?? '';

// Hobbies can come as an array from checkboxes or comma-separated string
$hobbies = [];
if (isset($_POST['hobby'])) {
    if (is_array($_POST['hobby'])) {
        foreach ($_POST['hobby'] as $h) {
            $h = sanitizeString($h);
            if (!empty($h)) {
                $hobbies[] = $h;
            }
        }
    } else {
        $parts = explode(',', $_POST['hobby']);
        foreach ($parts as $p) {
            $p = sanitizeString($p);
            if (!empty($p)) {
                $hobbies[] = $p;
            }
        }
    }
}

// -------------------------------------------------------------
// 4. Server-Side Validation Rules
// -------------------------------------------------------------
$errors = [];

if (empty($name)) {
    $errors['name'] = 'Full name is required.';
} elseif (strlen($name) < 2 || strlen($name) > 100) {
    $errors['name'] = 'Name must be between 2 and 100 characters.';
}

if (!empty($username) && (strlen($username) < 3 || strlen($username) > 50)) {
    $errors['username'] = 'Username must be between 3 and 50 characters.';
}

if (empty($email)) {
    $errors['email'] = 'Email address is required.';
} elseif (!validateEmail($email)) {
    $errors['email'] = 'Please provide a valid email address (e.g. user@example.com).';
}

if (empty($mobile)) {
    $errors['mobile'] = 'Mobile number is required.';
} elseif (!validateMobile($mobile)) {
    $errors['mobile'] = 'Mobile number must be exactly 10 digits.';
}

if (empty($course)) {
    $errors['course'] = 'Course is required.';
}

$validDepts = [
    'Computer Engineering',
    'Information Technology',
    'Mechanical Engineering',
    'Civil Engineering'
];
if (empty($department)) {
    $errors['department'] = 'Department is required.';
} elseif (!in_array($department, $validDepts, true)) {
    $errors['department'] = 'Please select a valid department.';
}

$validGenders = ['Male', 'Female', 'Other'];
if (empty($gender)) {
    $errors['gender'] = 'Gender is required.';
} elseif (!in_array($gender, $validGenders, true)) {
    $errors['gender'] = 'Please select a valid gender option.';
}

if (empty($hobbies)) {
    $errors['hobbies'] = 'At least one hobby must be selected.';
}

if (empty($address)) {
    $errors['address'] = 'Address is required.';
}

// Password validations (Practical 9)
if (empty($password)) {
    $errors['password'] = 'Password is required.';
} elseif (strlen($password) < 6) {
    $errors['password'] = 'Password must be at least 6 characters.';
}

if (empty($confirmPassword)) {
    $errors['confirm_password'] = 'Please confirm your password.';
} elseif ($password !== $confirmPassword) {
    $errors['confirm_password'] = 'Password confirmation does not match.';
}

if (!empty($errors)) {
    sendResponse(422, false, 'Validation failed. Please correct the highlighted errors.', [
        'errors' => $errors,
        'old'    => [
            'name'       => $name,
            'username'   => $username,
            'email'      => $email,
            'mobile'     => $mobile,
            'course'     => $course,
            'department' => $department,
            'gender'     => $gender,
            'hobbies'    => $hobbies,
            'address'    => $address
        ]
    ], $isAjax);
}

// -------------------------------------------------------------
// 5. Database Duplicate Prevention & User Account Creation (Practical 9)
// -------------------------------------------------------------
// MySQL is the authoritative user-account store
$userAccount = null;
try {
    // Check duplicate email in users and students
    if (UserService::findByEmail($email) !== null || StudentService::findByEmail($email) !== null) {
        sendResponse(409, false, 'An account with this email address already exists.', [
            'errors' => ['email' => 'Email address is already registered.']
        ], $isAjax);
    }

    // Check duplicate username if provided
    if (!empty($username) && UserService::findByUsername($username) !== null) {
        sendResponse(409, false, 'This username is already taken. Please choose another.', [
            'errors' => ['username' => 'Username is already taken.']
        ], $isAjax);
    }

    // Securely hash password using bcrypt (password_hash via hashPassword helper)
    $passwordHash = hashPassword($password);

    // Atomically create user account and linked student record
    $userAccount = UserService::registerStudent([
        'name'          => $name,
        'username'      => $username,
        'email'         => $email,
        'mobile'        => $mobile,
        'course'        => $course,
        'department'    => $department,
        'gender'        => $gender,
        'hobbies'       => $hobbies,
        'address'       => $address,
        'password'      => $password,
        'password_hash' => $passwordHash
    ]);
} catch (InvalidArgumentException $e) {
    sendResponse(409, false, $e->getMessage(), ['errors' => ['account' => $e->getMessage()]], $isAjax);
} catch (Throwable $e) {
    error_log("Database registration error: " . $e->getMessage());
    sendResponse(500, false, 'An internal registration error occurred. Please try again later.', [], $isAjax);
}

// -------------------------------------------------------------
// 6. Secondary CSV File Logging (Practical 7 Compatibility)
// -------------------------------------------------------------
// Note: Per Practical 9 rules, user accounts are stored in MySQL.
// Never write plaintext passwords or password hashes to CSV/JSON files.
$csvDir  = defined('DATA_PATH') ? DATA_PATH : (ROOT_PATH . '/storage/data');
$csvFile = $csvDir . '/registrations.csv';

if (is_dir($csvDir) && is_writable($csvDir)) {
    $fp = @fopen($csvFile, 'c+');
    if ($fp && flock($fp, LOCK_EX)) {
        $lines = 0;
        $maxId = 0;
        rewind($fp);
        $headerExists = false;
        while (($row = fgetcsv($fp)) !== false) {
            if ($lines === 0 && isset($row[0]) && $row[0] === 'id') {
                $headerExists = true;
            } elseif (isset($row[0]) && is_numeric($row[0])) {
                $maxId = max($maxId, (int)$row[0]);
            }
            $lines++;
        }

        if (!$headerExists || $lines === 0) {
            fputcsv($fp, [
                'id',
                'name',
                'email',
                'mobile',
                'course',
                'department',
                'gender',
                'hobbies',
                'address',
                'created_at'
            ]);
        }

        $newCsvId = $maxId + 1;
        $createdAt = date('Y-m-d H:i:s');
        $hobbiesString = implode(', ', $hobbies);

        fputcsv($fp, [
            $newCsvId,
            $name,
            $email,
            $mobile,
            $course,
            $department,
            $gender,
            $hobbiesString,
            $address,
            $createdAt
        ]);

        fflush($fp);
        flock($fp, LOCK_UN);
        fclose($fp);
    }
}

// -------------------------------------------------------------
// 7. Success Response
// -------------------------------------------------------------
sendResponse(201, true, 'Registration completed successfully! You can now log in with your credentials.', [
    'data' => [
        'user_id'    => $userAccount['user_id'] ?? null,
        'student_id' => $userAccount['student_id'] ?? null,
        'username'   => $userAccount['username'] ?? $username,
        'name'       => $name,
        'email'      => $email,
        'course'     => $course,
        'department' => $department
    ]
], $isAjax);
