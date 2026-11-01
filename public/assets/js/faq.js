/**
 * StudentHub - Collapsible FAQ & Dark Theme Switcher
 * Course: AIUE203 - Web Development Fundamentals (Practical 4)
 * Author: Daksh Harkhani (25AIML019), CSPIT, CHARUSAT
 */

// Toggle Dark Theme with localStorage persistence
function theme() {
    document.body.classList.toggle("dark-theme");
    const isDark = document.body.classList.contains("dark-theme");
    try {
        localStorage.setItem("studenthub_theme", isDark ? "dark" : "light");
    } catch (e) {
        // Local storage not available
    }
}

// Restore saved theme on page load
document.addEventListener("DOMContentLoaded", function () {
    try {
        const savedTheme = localStorage.getItem("studenthub_theme");
        if (savedTheme === "dark") {
            document.body.classList.add("dark-theme");
        }
    } catch (e) {
        // Local storage not available
    }
});

// Helper to toggle collapsible question
function toggleFaqAnswer(elementId) {
    const el = document.getElementById(elementId);
    if (!el) return;

    if (el.style.display === "block") {
        el.style.display = "none";
    } else {
        el.style.display = "block";
    }
}

// Named functions preserved for existing HTML onclick handlers
function faq() {
    toggleFaqAnswer("ans");
}

function faq1() {
    toggleFaqAnswer("ans1");
}

function faq2() {
    toggleFaqAnswer("ans2");
}

function faq3() {
    toggleFaqAnswer("ans3");
}

function faq4() {
    toggleFaqAnswer("ans4");
}
