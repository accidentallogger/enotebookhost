function resendInvite(button) {
    button.textContent = "Resent";
    button.style.backgroundColor = "#28a745";
    button.style.transform = "scale(1.05)";
    button.disabled = true;
    setTimeout(() => {
        button.style.transform = "scale(1)";
    }, 300);  }
