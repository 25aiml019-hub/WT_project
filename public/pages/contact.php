<?php
/**
 * StudentHub - Modular Contact Page (PHP)
 * Course: AIUE203 - Web Development Fundamentals (Practical 7 & 8)
 * Author: Anshika Badala (25AIML002)
 */

require_once __DIR__ . '/../../app/config/config.php';
require_once __DIR__ . '/../../app/config/security.php';

initSession();

$pageTitle = 'Contact Us';
$currentPage = 'contact';
$basePath = '../';
$extraCss = ['contact.css'];

$csrfToken = getCsrfToken();
$successMessage = $_SESSION['contact_success'] ?? null;
$errorMessages = $_SESSION['contact_errors'] ?? [];
$old = $_SESSION['contact_old'] ?? [];

unset($_SESSION['contact_success'], $_SESSION['contact_errors'], $_SESSION['contact_old']);

require_once __DIR__ . '/../../app/includes/header.php';
require_once __DIR__ . '/../../app/includes/nav.php';
?>

    <main class="contact-container">
        <h2>We'd Love to Hear From You</h2>

        <p class="intro">
            Have a question, suggestion or any concern regarding Student Hub?
            Feel free to contact us. We are happy to help you with your queries
            and feedback.
        </p>

        <!-- Contact Information Grid -->
        <div class="contact-info-grid">
            <div>
                <h3>Email</h3>
                <p>anshikabadala2@gmail.com</p>
            </div>

            <div>
                <h3>Phone</h3>
                <p>7043100708</p>
            </div>

            <div>
                <h3>Office</h3>
                <p>CHARUSAT Campus</p>
            </div>

            <div>
                <h3>Office Timing</h3>
                <p>
                    Monday - Friday<br>
                    9:00 AM - 5:00 PM
                </p>
            </div>
        </div>

        <hr class="small-line">

        <!-- Contact Form -->
        <h2>Send Us a Message</h2>

        <form id="contactForm" class="contact-form" method="POST" action="../process-contact.php" onsubmit="return submitMessage(event)">
            <div id="contactAlert" class="alert-box" style="<?= empty($successMessage) && empty($errorMessages) ? 'display: none;' : '' ?>" role="alert">
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

            <label for="subject">Subject:</label>
            <input type="text" id="subject" name="subject" placeholder="Enter subject" value="<?= e($old['subject'] ?? '') ?>" required>

            <label for="message">Message:</label>
            <textarea id="message" name="message" rows="5" placeholder="Enter your message" required><?= e($old['message'] ?? '') ?></textarea>

            <div class="buttons">
                <input type="submit" value="Send Message" class="btn">
                <input type="button" value="Reset" class="btn" onclick="resetMessage()">
            </div>
        </form>

        <hr class="small-line">

        <!-- FAQ Link -->
        <div class="faq-link-box">
            <h2>Have More Questions?</h2>
            <p>
                Check our Frequently Asked Questions section to find answers
                to common questions about Student Hub.
            </p>
            <a href="faq.html">Visit FAQ</a>
        </div>
    </main>

    <!-- JavaScript Handlers -->
    <script src="../assets/js/contact.js"></script>
    <script src="../assets/js/main.js"></script>

<?php
require_once __DIR__ . '/../../app/includes/footer.php';
?>
