/**
 * DadBods Multi-Step Application Wizard
 * Robust 6-step client-side wizard with instant validation,
 * back/forward navigation, draft persistence, and clean Django integration.
 */

document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("coachingApplicationForm");
  if (!form) return;

  const totalSteps = 6;
  let currentStep = 1;

  const stepCards = document.querySelectorAll(".form-step-section");
  const stepCounterText = document.getElementById("stepCounterText");
  const stepHeadingText = document.getElementById("stepHeadingText");
  const stepBadges = document.querySelectorAll(".step-badge");
  const btnPrev = document.getElementById("btnStepPrev");
  const btnNext = document.getElementById("btnStepNext");
  const btnSubmit = document.getElementById("btnStepSubmit");

  const stepLabels = [
    "01 / 06 • ABOUT YOU",
    "02 / 06 • YOUR GOAL",
    "03 / 06 • TRAINING",
    "04 / 06 • LIFESTYLE",
    "05 / 06 • COMMITMENT",
    "06 / 06 • FINAL DETAILS",
  ];

  const stepHeadings = [
    "LET'S GET TO KNOW YOU.",
    "PHYSIQUE & TARGET GOAL.",
    "TRAINING BACKGROUND.",
    "LIFESTYLE & NUTRITION.",
    "HEALTH & COMMITMENT.",
    "READINESS TO START.",
  ];

  // 1. Setup conditional health disclosure toggles
  setupConditionalDisclosures();

  // 2. Restore saved draft if not re-rendered with server errors
  const hasServerErrors = form.querySelectorAll(".field-error-text[data-server-error]").length > 0;
  if (!hasServerErrors) {
    restoreFormData();
  }

  // 3. Save progress on user input
  form.addEventListener("input", saveFormData);
  form.addEventListener("change", saveFormData);

  // 4. Determine initial step (if server returned errors on a later step, jump there)
  let initialStep = 1;
  const firstServerError = form.querySelector(".field-error-text");
  if (firstServerError) {
    const parentStep = firstServerError.closest(".form-step-section");
    if (parentStep && parentStep.id) {
      const match = parentStep.id.match(/\d+/);
      if (match) initialStep = parseInt(match[0], 10);
    }
  }

  goToStep(initialStep);

  // 5. Button Listeners
  btnNext?.addEventListener("click", (e) => {
    e.preventDefault();
    if (validateStep(currentStep)) {
      if (currentStep < totalSteps) {
        goToStep(currentStep + 1);
      }
    }
  });

  btnPrev?.addEventListener("click", (e) => {
    e.preventDefault();
    if (currentStep > 1) {
      goToStep(currentStep - 1);
    }
  });

  // 6. Step tracker clickable badges
  stepBadges.forEach((badge) => {
    badge.style.cursor = "pointer";
    badge.addEventListener("click", () => {
      const targetStep = parseInt(badge.getAttribute("data-step"), 10);
      if (isNaN(targetStep)) return;

      if (targetStep < currentStep) {
        goToStep(targetStep);
      } else if (targetStep > currentStep) {
        // Validate intermediate steps before jumping forward
        let canAdvance = true;
        for (let s = currentStep; s < targetStep; s++) {
          if (!validateStep(s)) {
            canAdvance = false;
            goToStep(s);
            break;
          }
        }
        if (canAdvance) {
          goToStep(targetStep);
        }
      }
    });
  });

  // 7. Final Form Submission
  form.addEventListener("submit", (e) => {
    for (let s = 1; s <= totalSteps; s++) {
      if (!validateStep(s)) {
        e.preventDefault();
        goToStep(s);
        return false;
      }
    }

    if (btnSubmit) {
      btnSubmit.disabled = true;
      btnSubmit.textContent = "SUBMITTING APPLICATION...";
    }

    try {
      sessionStorage.removeItem("dadbods_application_draft");
    } catch {
      // sessionStorage might be restricted
    }
  });

  // =========================================================================
  // CORE FUNCTIONS
  // =========================================================================

  function goToStep(stepNumber) {
    if (stepNumber < 1 || stepNumber > totalSteps) return;
    currentStep = stepNumber;

    stepCards.forEach((sec, idx) => {
      const stepIdx = idx + 1;
      if (stepIdx === stepNumber) {
        sec.style.display = "block";
        sec.classList.add("active-step");
      } else {
        sec.style.display = "none";
        sec.classList.remove("active-step");
      }
    });

    // Update step tracker badges
    stepBadges.forEach((badge, idx) => {
      const stepIdx = idx + 1;
      if (stepIdx === stepNumber) {
        badge.classList.add("active");
        badge.classList.remove("completed");
      } else if (stepIdx < stepNumber) {
        badge.classList.remove("active");
        badge.classList.add("completed");
      } else {
        badge.classList.remove("active");
        badge.classList.remove("completed");
      }
    });

    // Update counter & heading
    if (stepCounterText) {
      stepCounterText.textContent = stepLabels[stepNumber - 1];
    }
    if (stepHeadingText) {
      stepHeadingText.textContent = stepHeadings[stepNumber - 1];
    }

    // Update buttons
    if (btnPrev) {
      btnPrev.style.display = stepNumber === 1 ? "none" : "inline-flex";
    }

    if (btnNext && btnSubmit) {
      if (stepNumber === totalSteps) {
        btnNext.style.display = "none";
        btnSubmit.style.display = "inline-flex";
      } else {
        btnNext.style.display = "inline-flex";
        btnSubmit.style.display = "none";
      }
    }

    // Smooth scroll back to form section if scrolled down
    const formSection = document.querySelector(".apply-form-section");
    if (formSection && window.scrollY > formSection.offsetTop) {
      window.scrollTo({
        top: formSection.offsetTop - 70,
        behavior: "smooth",
      });
    }
  }

  function validateStep(stepNumber) {
    const activeSection = document.getElementById(`formStep${stepNumber}`);
    if (!activeSection) return true;

    // Clear previous client-side errors
    activeSection.querySelectorAll(".field-error-text:not([data-server-error])").forEach((el) => {
      el.remove();
    });

    const requiredFields = activeSection.querySelectorAll(
      "input[required], select[required], textarea[required]"
    );

    let isValid = true;
    let firstInvalid = null;

    requiredFields.forEach((field) => {
      let fieldValid = true;
      let errorMsgText = "This field is required.";

      if (field.type === "checkbox") {
        if (!field.checked) {
          fieldValid = false;
          errorMsgText = "Please check this box to continue.";
        }
      } else {
        const val = field.value.trim();
        if (!val) {
          fieldValid = false;
          errorMsgText = "This field is required.";
        } else if (field.type === "email") {
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(val)) {
            fieldValid = false;
            errorMsgText = "Please enter a valid email address.";
          }
        } else if (field.name === "age") {
          const ageNum = parseInt(val, 10);
          if (isNaN(ageNum) || ageNum < 16 || ageNum > 85) {
            fieldValid = false;
            errorMsgText = "Age must be between 16 and 85.";
          }
        } else if (field.name === "whatsapp_number") {
          const digits = val.replace(/\D/g, "");
          if (digits.length < 7) {
            fieldValid = false;
            errorMsgText = "Please enter a valid WhatsApp number (minimum 7 digits).";
          }
        } else if (field.name === "follow_through_score") {
          const num = parseInt(val, 10);
          if (isNaN(num) || num < 1 || num > 10) {
            fieldValid = false;
            errorMsgText = "Please enter a score between 1 and 10.";
          }
        }
      }

      if (!fieldValid) {
        isValid = false;
        field.style.borderColor = "#ff6b6b";
        if (!firstInvalid) firstInvalid = field;

        const errMsg = document.createElement("p");
        errMsg.className = "field-error-text";
        errMsg.textContent = errorMsgText;

        const container = field.closest(".field-group") || field.parentElement;
        container.appendChild(errMsg);

        const clearError = () => {
          field.style.borderColor = "";
          errMsg.remove();
        };

        field.addEventListener("input", clearError, { once: true });
        field.addEventListener("change", clearError, { once: true });
      } else {
        field.style.borderColor = "";
      }
    });

    if (!isValid && firstInvalid) {
      firstInvalid.focus();
    }

    return isValid;
  }

  function setupConditionalDisclosures() {
    const toggles = [
      { check: "id_previous_injury", box: "box_injury_description" },
      { check: "id_medical_condition", box: "box_medical_condition_description" },
      { check: "id_medication", box: "box_medication_description" },
    ];

    toggles.forEach(({ check, box }) => {
      const chkEl = document.getElementById(check);
      const boxEl = document.getElementById(box);
      if (chkEl && boxEl) {
        const updateBox = () => {
          boxEl.style.display = chkEl.checked ? "block" : "none";
        };
        chkEl.addEventListener("change", updateBox);
        updateBox();
      }
    });
  }

  function saveFormData() {
    try {
      const formData = new FormData(form);
      const dataObj = {};
      formData.forEach((val, key) => {
        if (key !== "csrfmiddlewaretoken" && key !== "website" && key !== "form_load_timestamp") {
          dataObj[key] = val;
        }
      });
      // Also explicitly capture unchecked checkboxes
      form.querySelectorAll("input[type='checkbox']").forEach((chk) => {
        if (chk.name && chk.name !== "website") {
          dataObj[chk.name] = chk.checked;
        }
      });
      sessionStorage.setItem("dadbods_application_draft", JSON.stringify(dataObj));
    } catch {
      // sessionStorage might be restricted
    }
  }

  function restoreFormData() {
    try {
      const saved = sessionStorage.getItem("dadbods_application_draft");
      if (!saved) return;
      const dataObj = JSON.parse(saved);

      Object.entries(dataObj).forEach(([key, val]) => {
        const field = form.elements[key];
        if (!field) return;

        if (field.type === "checkbox") {
          field.checked = val === true || val === "on" || val === "true";
        } else if (field.value !== undefined && !field.value) {
          field.value = val;
        }
      });

      // Refresh conditional disclosure visibility after restoring checkboxes
      setupConditionalDisclosures();
    } catch {
      // ignore parse errors
    }
  }
});
