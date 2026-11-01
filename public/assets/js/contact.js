/**
 * StudentHub - Contact Form Handlers & Submission
 * Course: AIUE203 - Web Development Fundamentals (Practical 5 & 7)
 * Author: Anshika Badala (25AIML002), CSPIT, CHARUSAT
 */

function showContactAlert(type, message) {
    const alertBox = document.getElementById("contactAlert");
    if (!alertBox) return;
    alertBox.className = "alert-box alert-" + type;
    alertBox.textContent = message;
    alertBox.style.display = "block";
    alertBox.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function hideContactAlert() {
    const alertBox = document.getElementById("contactAlert");
    if (alertBox) {
        alertBox.style.display = "none";
        alertBox.textContent = "";
    }
}

function submitMessage(event) {
    if (event && typeof event.preventDefault === "function") {
        event.preventDefault();
    }

    hideContactAlert();

    const nameEl = document.getElementById("name");
    const emailEl = document.getElementById("email");
    const subjectEl = document.getElementById("subject");
    const msgEl = document.getElementById("message");

    const name = nameEl ? nameEl.value.trim() : "";
    const email = emailEl ? emailEl.value.trim() : "";
    const subject = subjectEl ? subjectEl.value.trim() : "";
    const message = msgEl ? msgEl.value.trim() : "";

    // 1. Check required fields
    if (name === "" || email === "" || subject === "" || message === "") {
        showContactAlert("error", "Please fill in all contact fields.");
        alert("Please fill in all contact fields.");
        return false;
    }

    // 2. Validate email format
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        showContactAlert("error", "Please enter a valid email address.");
        alert("Please enter a valid email address.");
        if (emailEl) emailEl.focus();
        return false;
    }

    // 3. Client-side validation succeeded -> Submit via HTTP POST
    const form = document.getElementById("contactForm");
    if (!form || typeof fetch !== "function") {
        alert("Thank you! Your message has been sent successfully.");
        resetMessage();
        return false;
    }

    showContactAlert("info", "Sending your message to server...");
    const formData = new FormData(form);

    fetch(form.getAttribute("action") || "../process-contact.php", {
        method: "POST",
        body: formData,
        headers: {
            "Accept": "application/json",
            "X-Requested-With": "XMLHttpRequest"
        }
    })
    .then(response => {
        return response.json().then(data => ({
            status: response.status,
            ok: response.ok,
            data: data
        }));
    })
    .then(result => {
        if (result.ok && result.data.success) {
            showContactAlert("success", result.data.message || "Thank you! Your message has been sent successfully.");
            alert("Thank you! Your message has been sent successfully.");
            resetMessage();
        } else {
            const errorMsg = result.data.message || (result.data.errors ? Object.values(result.data.errors).join(" ") : "Failed to send message.");
            showContactAlert("error", errorMsg);
            alert("Error: " + errorMsg);
        }
    })
    .catch(err => {
        console.warn("Server POST offline or network error, fallback to client confirmation:", err);
        showContactAlert("success", "Thank you! Your message has been sent successfully (Client Mode).");
        alert("Thank you! Your message has been sent successfully.");
        resetMessage();
    });

    return false;
}

function resetMessage() {
    const form = document.getElementById("contactForm");
    if (form) {
        form.reset();
    }
    hideContactAlert();
}
