const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");
const regForm = document.getElementById("regForm");
const loginForm = document.querySelector(".login-form");
var pw = document.getElementById("password").value;
var pw2 = document.getElementById("confirmPassword").value;
// Landing page is login so registration page is hidden by default
regForm.style.display = "none";

// Event listener for sign-up button
sign_up_btn.addEventListener("click", () => {
  container.classList.add("sign-up-mode");
  setTimeout(() => {
    regForm.style.display = "block";
    loginForm.style.display = "none";
  }, 1000);


});

// Event listener for sign-in button
sign_in_btn.addEventListener("click", () => {
  container.classList.remove("sign-up-mode");
  setTimeout(() => {
    regForm.style.display = "none";
    loginForm.style.display = "flex";
  }, 1000);
});

// Initialize the first tab
var currentTab = 0;
showTab(currentTab);

// Function to display the specified tab
function showTab(n) {
  var tabs = document.getElementsByClassName("tab");
  tabs[n].style.display = "block";

  // Handle Previous button visibility
  if (n === 0) {
    document.getElementById("prevBtn").style.display = "none";
  } else {
    document.getElementById("prevBtn").style.display = "inline";
  }

  // Handle Next/Submit button text
  if (n === (tabs.length - 1)) {
    document.getElementById("nextBtn").innerHTML = "Submit";
  } else {
    document.getElementById("nextBtn").innerHTML = "Next";
  }

  // Update step indicator
  fixStepIndicator(n);
}

// Function to handle navigation between tabs
function nextPrev(n) {
  var tabs = document.getElementsByClassName("tab");
  // Exit if form is invalid
  if (n === 1 && !validateForm()) return false;

  // Hide the current tab
  tabs[currentTab].style.display = "none";

  // Update current tab
  currentTab = currentTab + n;

  // Submit the form if it's the last tab
  if (currentTab >= tabs.length) {
    document.getElementById("regForm").submit();
    return false;
  }

  // Show the new tab
  showTab(currentTab);
}

// Function to validate form fields in the current tab
function validateForm() {
  var tabs, inputs, i, valid = true;
  tabs = document.getElementsByClassName("tab");
  inputs = tabs[currentTab].getElementsByTagName("input");

  // Validate each input field
  for (i = 0; i < inputs.length; i++) {
    var errorIcon = inputs[i].nextElementSibling;
    var errorMessage = errorIcon.nextElementSibling;

    if (inputs[i].value === "") {
      inputs[i].classList.add("invalid");
      errorIcon.style.display = "inline";
      errorMessage.style.display = "inline";
      valid = false;
    } else {
      inputs[i].classList.remove("invalid");
      errorIcon.style.display = "none";
      errorMessage.style.display = "none";
    }
  }

  // Mark step as finished if valid
  if (valid) {
    document.getElementsByClassName("step")[currentTab].className += " finish";
  }

  return valid;
}

// Function to update step indicators
function fixStepIndicator(n) {
  var i, steps = document.getElementsByClassName("step");
  // Remove active class from all steps
  for (i = 0; i < steps.length; i++) {
    steps[i].className = steps[i].className.replace(" active", "");
  }
  // Add active class to the current step
  steps[n].className += " active";
}
