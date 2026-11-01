<?php
/**
 * Authentication Middleware
 * StudentHub - CSPIT, CHARUSAT
 */

require_once __DIR__ . '/../includes/auth_check.php';

function checkAuth($redirect = '../25aiml019/login.html') {
    requireLogin($redirect);
}
