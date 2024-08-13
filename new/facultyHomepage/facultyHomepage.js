const shrink_btn = document.querySelector(".shrink-btn");

const active_tab = document.querySelector(".active-tab");
const shortcuts = document.querySelector(".sidebar-links h4");
const tooltip_elements = document.querySelectorAll(".tooltip-element");

let activeIndex;

const isMobileDevice = () => {
  return /Mobi|Android|iPhone|iPad|iPod/i.test(navigator.userAgent);
};
shrink_btn.addEventListener("click", () => {
  document.body.classList.toggle("shrink");
//   setTimeout(moveActiveTab, 400);

//   shrink_btn.classList.add("hovered");

//   setTimeout(() => {
//     shrink_btn.classList.remove("hovered");
//   }, 500);
});

if (isMobileDevice()) {
  document.body.classList.add("shrink");
}


// function moveActiveTab() {
//   let topPosition = activeIndex * 58 + 2.5;

//   if (activeIndex > 3) {
//     topPosition += shortcuts.clientHeight;
//   }

//   active_tab.style.top = `${topPosition}px`;
// }

// function changeLink() {
//   sidebar_links.forEach((sideLink) => sideLink.classList.remove("active"));
//   this.classList.add("active");

//   activeIndex = this.dataset.active;

//   moveActiveTab();
// }

// sidebar_links.forEach((link) => link.addEventListener("click", changeLink));

// function showTooltip() {
//   let tooltip = this.parentNode.lastElementChild;
//   let spans = tooltip.children;
//   let tooltipIndex = this.dataset.tooltip;

//   Array.from(spans).forEach((sp) => sp.classList.remove("show"));
//   spans[tooltipIndex].classList.add("show");

//   tooltip.style.top = `${(100 / (spans.length * 2)) * (tooltipIndex * 2 + 1)}%`;
// }

// tooltip_elements.forEach((elem) => {
//   elem.addEventListener("mouseover", showTooltip);
// });


document.addEventListener("DOMContentLoaded", () => {
  const profileDropdown = document.querySelector(".profile-dropdown");
  const dropdownMenu = document.querySelector(".dropdown-menu");

  profileDropdown.addEventListener("mouseover", () => {
    dropdownMenu.style.display = "flex";
  });

  profileDropdown.addEventListener("mouseout", (event) => {
    // Check if the mouse is leaving the profileDropdown and entering the dropdownMenu
    if (!dropdownMenu.contains(event.relatedTarget) && event.relatedTarget !== profileDropdown) {
      dropdownMenu.style.display = "none";
    }
  });

  dropdownMenu.addEventListener("mouseover", () => {
    dropdownMenu.style.display = "flex";
  });

  dropdownMenu.addEventListener("mouseout", (event) => {
    // Check if the mouse is leaving the dropdownMenu and entering the profileDropdown
    if (!profileDropdown.contains(event.relatedTarget) && event.relatedTarget !== dropdownMenu) {
      dropdownMenu.style.display = "none";
    }
  });

  profileDropdown.addEventListener("click", () => {
    const isVisible = dropdownMenu.style.display === "flex";
    dropdownMenu.style.display = isVisible ? "none" : "flex";
  });
});
