/**
 * CineFlow - Cinema Production Management
 * Interactive Dashboard & Frontend Enhancements
 */

document.addEventListener('DOMContentLoaded', function () {
  // 1. Mobile Menu Toggle
  const mobileToggle = document.getElementById('mobileToggle');
  const navMenu = document.getElementById('navMenu');
  if (mobileToggle && navMenu) {
    mobileToggle.addEventListener('click', function () {
      navMenu.classList.toggle('show');
    });
  }

  // 2. Auto-dismiss Flash Alerts
  const alerts = document.querySelectorAll('.alert');
  alerts.forEach(function (alert) {
    // Dismiss button
    const closeBtn = alert.querySelector('.alert-close');
    if (closeBtn) {
      closeBtn.addEventListener('click', function () {
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 250);
      });
    }

    // Auto fade after 6 seconds
    setTimeout(function () {
      if (document.body.contains(alert)) {
        alert.style.transition = 'opacity 0.4s ease';
        alert.style.opacity = '0';
        setTimeout(() => alert.remove(), 400);
      }
    }, 6000);
  });

  // 3. Confirm Delete Actions
  const deleteForms = document.querySelectorAll('form[data-confirm]');
  deleteForms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
      const msg = form.getAttribute('data-confirm') || 'Are you sure you want to proceed?';
      if (!confirm(msg)) {
        e.preventDefault();
      }
    });
  });

  // 4. Dynamic Scene & Location Autofill in Schedule Creation
  const sceneSelect = document.getElementById('scene_id');
  const locationInput = document.getElementById('location');
  if (sceneSelect && locationInput) {
    sceneSelect.addEventListener('change', function () {
      const selectedOption = sceneSelect.options[sceneSelect.selectedIndex];
      const defaultLoc = selectedOption.getAttribute('data-location');
      if (defaultLoc && (!locationInput.value || locationInput.dataset.touched !== 'true')) {
        locationInput.value = defaultLoc;
      }
    });

    locationInput.addEventListener('input', function () {
      locationInput.dataset.touched = 'true';
    });
  }

  // 5. Department Filter & Cast Role Character Logic
  const deptSelect = document.getElementById('department');
  const characterGroup = document.getElementById('character-group');
  if (deptSelect && characterGroup) {
    function toggleCharacterField() {
      const isCast = deptSelect.value === 'Cast';
      const charInput = characterGroup.querySelector('input');
      if (isCast) {
        characterGroup.style.display = 'flex';
        if (charInput && charInput.value === 'N/A') charInput.value = '';
      } else {
        if (charInput && !charInput.value) charInput.value = 'N/A';
      }
    }
    deptSelect.addEventListener('change', toggleCharacterField);
    toggleCharacterField();
  }

  // 6. Production Dashboard Progress Rings / Mini Visualizer
  const ringElements = document.querySelectorAll('.donut-progress');
  ringElements.forEach(function (el) {
    const val = parseFloat(el.getAttribute('data-value') || '0');
    const circle = el.querySelector('.donut-circle-val');
    if (circle) {
      const radius = circle.r.baseVal.value;
      const circumference = 2 * Math.PI * radius;
      circle.style.strokeDasharray = `${circumference} ${circumference}`;
      const offset = circumference - (val / 100) * circumference;
      circle.style.strokeDashoffset = offset;
    }
  });
});
