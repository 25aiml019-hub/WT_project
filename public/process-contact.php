<?php
/**
 * Contact Us Form Processor
 * StudentHub - CSPIT, CHARUSAT
 * Course: AIUE203 - Web Development Fundamentals (Practical 7 & 8)
 * Author: Anshika Badala (25AIML002)
 */

require_once __DIR__ . '/../app/config/config.php';
require_once __DIR__ . '/../app/config/security.php';
require_once __DIR__ . '/../app/config/db.php';

initSession();

$isAjax = (!empty($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest') ||
          (isset($_SERVER['HTTP_ACCEPT']) && strpos($_SERVER['HTTP_ACCEPT'], 'application/json') !== false) ||
          (isset($_SERVER['CONTENT_TYPE']) && strpos($_SERVER['CONTENT_TYPE'], 'application/json') !== false);

function sendContactResponse(int $statusCode, bool $success, string $message, array $extra = [], bool $isAjax = true): void {
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
        $_SESSION['contact_success'] = $message;
        unset($_SESSION['contact_errors'], $_SESSION['contact_old']);
        header('Location: pages/contact.html?success=1');
    } else {
        $_SESSION['contact_errors'] = $extra['errors'] ?? [$message];
        $_SESSION['contact_old'] = $extra['old'] ?? [];
        header('Location: pages/contact.html?error=1');
    }
    exit;
}

// -------------------------------------------------------------
// 1. HTTP Method Enforcement (Must be POST)
// -------------------------------------------------------------
if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Allow: POST');
    sendContactResponse(405, false, 'Method Not Allowed. Only HTTP POST submissions are accepted.', [], $isAjax);
}

// -------------------------------------------------------------
// 2. CSRF Token Verification
// -------------------------------------------------------------
$csrfToken = $_POST['csrf_token'] ?? $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
if (!empty($csrfToken) || !empty($_SESSION['csrf_token'])) {
    if (!validateCsrfToken($csrfToken)) {
        sendContactResponse(403, false, 'CSRF verification failed. Form submission rejected.', [], $isAjax);
    }
}

// -------------------------------------------------------------
// 3. Extract & Sanitize Fields
// -------------------------------------------------------------
$name    = sanitizeString($_POST['name'] ?? '');
$email   = sanitizeEmail($_POST['email'] ?? '');
$subject = sanitizeString($_POST['subject'] ?? '');
$message = sanitizeString($_POST['message'] ?? '');

// -------------------------------------------------------------
// 4. Server-Side Validation Rules
// -------------------------------------------------------------
$errors = [];

if (empty($name)) {
    $errors['name'] = 'Name is required.';
} elseif (strlen($name) < 2 || strlen($name) > 100) {
    $errors['name'] = 'Name must be between 2 and 100 characters.';
}

if (empty($email)) {
    $errors['email'] = 'Email is required.';
} elseif (!validateEmail($email)) {
    $errors['email'] = 'Please enter a valid email address.';
}

if (empty($subject)) {
    $errors['subject'] = 'Subject is required.';
} elseif (strlen($subject) < 3 || strlen($subject) > 150) {
    $errors['subject'] = 'Subject must be between 3 and 150 characters.';
}

if (empty($message)) {
    $errors['message'] = 'Message is required.';
} elseif (strlen($message) < 5) {
    $errors['message'] = 'Message must be at least 5 characters long.';
}

if (!empty($errors)) {
    sendContactResponse(422, false, 'Validation failed. Please correct the highlighted errors.', [
        'errors' => $errors,
        'old'    => [
            'name'    => $name,
            'email'   => $email,
            'subject' => $subject,
            'message' => $message
        ]
    ], $isAjax);
}

// -------------------------------------------------------------
// 5. Safe JSON File Storage with File Locking (flock)
// -------------------------------------------------------------
$dataDir  = defined('DATA_PATH') ? DATA_PATH : (ROOT_PATH . '/storage/data');
$jsonFile = $dataDir . '/messages.json';

if (!is_dir($dataDir)) {
    if (!@mkdir($dataDir, 0755, true)) {
        error_log("Failed to create storage directory: " . $dataDir);
        sendContactResponse(500, false, 'Storage initialization error. Directory cannot be created.', [], $isAjax);
    }
}

if (!is_writable($dataDir)) {
    error_log("Storage directory is not writable: " . $dataDir);
    sendContactResponse(500, false, 'Storage permission error. Data directory is not writable.', [], $isAjax);
}

$fp = @fopen($jsonFile, 'c+');
if (!$fp) {
    error_log("Failed to open messages.json: " . $jsonFile);
    sendContactResponse(500, false, 'Storage failure: Unable to open JSON storage file.', [], $isAjax);
}

if (!flock($fp, LOCK_EX)) {
    fclose($fp);
    error_log("Failed to acquire lock on: " . $jsonFile);
    sendContactResponse(500, false, 'Storage concurrency failure: Could not obtain file lock.', [], $isAjax);
}

$fileSize = filesize($jsonFile);
$messages = [];
if ($fileSize > 0) {
    $content = fread($fp, $fileSize);
    $decoded = json_decode($content, true);
    if (is_array($decoded)) {
        $messages = $decoded;
    }
}

$nextId = count($messages) > 0 ? (max(array_column($messages, 'id') ?: [0]) + 1) : 1;
$clientIp = getClientIp();
$createdAt = date('Y-m-d H:i:s');

$newMessage = [
    'id'         => $nextId,
    'name'       => $name,
    'email'      => $email,
    'subject'    => $subject,
    'message'    => $message,
    'ip_address' => $clientIp,
    'status'     => 'unread',
    'created_at' => $createdAt
];

$messages[] = $newMessage;

// Truncate file and write updated JSON
ftruncate($fp, 0);
rewind($fp);
$jsonOutput = json_encode($messages, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE);
$writeSuccess = fwrite($fp, $jsonOutput);
fflush($fp);
flock($fp, LOCK_UN);
fclose($fp);

if ($writeSuccess === false) {
    error_log("fwrite returned false when writing messages.json");
    sendContactResponse(500, false, 'Storage failure: Failed to write contact message to JSON storage.', [], $isAjax);
}

// -------------------------------------------------------------
// 6. MySQL Database Persistence (Practical 8 Prepared Statement)
// -------------------------------------------------------------
$dbInsertId = null;
try {
    $mysqli = getMySQLi();
    $stmt = $mysqli->prepare("INSERT INTO contact_messages (name, email, subject, message, ip_address, status) VALUES (?, ?, ?, ?, ?, 'unread')");
    if ($stmt) {
        $stmt->bind_param("sssss", $name, $email, $subject, $message, $clientIp);
        $stmt->execute();
        $dbInsertId = $stmt->insert_id;
        $stmt->close();
    }
} catch (Throwable $e) {
    error_log("Database contact message insert bypassed: " . $e->getMessage());
}

// -------------------------------------------------------------
// 7. Success Response
// -------------------------------------------------------------
sendContactResponse(201, true, 'Thank you! Your message has been sent successfully.', [
    'data' => [
        'id'         => $nextId,
        'db_id'      => $dbInsertId,
        'name'       => $name,
        'email'      => $email,
        'subject'    => $subject,
        'created_at' => $createdAt
    ]
], $isAjax);
