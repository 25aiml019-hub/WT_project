<?php
/**
 * StudentHub - Password Change Processor
 * Course: AIUE203 - Web Development Fundamentals
 * Author: Anshika Badala (25AIML002)
 */

require_once __DIR__ . '/../app/config/config.php';
require_once __DIR__ . '/../app/config/security.php';
require_once __DIR__ . '/../app/services/user_service.php';

initSession();

$isAjax = (!empty($_SERVER['HTTP_X_REQUESTED_WITH']) && strtolower($_SERVER['HTTP_X_REQUESTED_WITH']) === 'xmlhttprequest') ||
          (isset($_SERVER['HTTP_ACCEPT']) && strpos($_SERVER['HTTP_ACCEPT'], 'application/json') !== false);

function sendChangePasswordResponse(int $statusCode, bool $success, string $message, array $extra = [], bool $isAjax = true): void {
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
        $redirect = $extra['redirect'] ?? 'login.html?password_changed=1';
        header("Location: {$redirect}");
    } else {
        $_SESSION['flash_error'] = $message;
        header('Location: pages/change-password.php?error=1');
    }
    exit;
}

if ($_SERVER['REQUEST_METHOD'] !== 'POST') {
    header('Allow: POST');
    sendChangePasswordResponse(405, false, 'Method Not Allowed. Only HTTP POST submissions are accepted.', [], $isAjax);
}

// Ensure user is authenticated
if (empty($_SESSION['user_id'])) {
    sendChangePasswordResponse(401, false, 'You must be logged in to change your password.', [
        'redirect' => 'pages/login.html?error=unauthorized'
    ], $isAjax);
}

// CSRF Verification
$csrfToken = $_POST['csrf_token'] ?? $_SERVER['HTTP_X_CSRF_TOKEN'] ?? '';
if (!validateCsrfToken($csrfToken)) {
    sendChangePasswordResponse(403, false, 'CSRF verification failed. Please refresh and try again.', [], $isAjax);
}

$currentPassword = $_POST['current_password'] ?? '';
$newPassword     = $_POST['new_password'] ?? '';
$confirmPassword = $_POST['confirm_password'] ?? '';

if (empty($currentPassword) || empty($newPassword) || empty($confirmPassword)) {
    sendChangePasswordResponse(422, false, 'All fields are required.', [], $isAjax);
}

if ($newPassword !== $confirmPassword) {
    sendChangePasswordResponse(422, false, 'New password and confirmation password do not match.', [], $isAjax);
}

if (strlen($newPassword) < 6) {
    sendChangePasswordResponse(422, false, 'New password must be at least 6 characters long.', [], $isAjax);
}

$userId = (int)$_SESSION['user_id'];
$result = UserService::changePassword($userId, $currentPassword, $newPassword);

if (!$result['success']) {
    sendChangePasswordResponse(400, false, $result['message'], [], $isAjax);
}

// Clear mandatory password change flag in session
$_SESSION['must_change_password'] = 0;
if (isset($_SESSION['user'])) {
    $_SESSION['user']['must_change_password'] = 0;
}

$role = $_SESSION['role'] ?? 'student';
$targetRedirect = ($role === 'admin') ? '../admin/index.php' : '../student/index.php';

sendChangePasswordResponse(200, true, 'Password changed successfully! Welcome to your portal.', [
    'redirect' => $targetRedirect
], $isAjax);
