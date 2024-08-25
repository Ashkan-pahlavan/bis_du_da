document.addEventListener("DOMContentLoaded", function () {
  // تابع تغییر وضعیت نمایش رمز عبور
  function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const icon = document.getElementById(`${inputId}Icon`);
    if (input.type === "password") {
      input.type = "text";
      icon.src = "eye-icon-new.jpg";
    } else {
      input.type = "password";
      icon.src = "eye-icon.jpg";
    }
  }

  // ارسال درخواست به سرور
  async function sendRequest(url, data) {
    try {
      console.log("Request Body:", data);
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      const result = await response.json();
      console.log("Received response:", result);

      if (!response.ok) {
        throw new Error(result.message || "An error occurred");
      }

      return result;
    } catch (error) {
      console.error("Error:", error);
      alert(`Error: ${error.message}`);
      throw error;
    }
  }

  // مدیریت فرم ثبت‌نام
  document
    .getElementById("registerForm")
    .addEventListener("submit", async function (event) {
      event.preventDefault();
      const email = document.getElementById("registerEmail").value;
      const password = document.getElementById("registerPassword").value;
      const confirmPassword = document.getElementById("confirmPassword").value;

      if (password !== confirmPassword) {
        alert("Passwords do not match.");
        return;
      }

      try {
        const result = await sendRequest(
          "https://1pnb7lz9ql.execute-api.eu-central-1.amazonaws.com/prod/st/register",
          { email, password }
        );
        alert(result.message);
      } catch (error) {
        // خطا قبلاً لاگ شده است
      }
    });

  // مدیریت فرم ورود
  document
    .getElementById("loginForm")
    .addEventListener("submit", async function (event) {
      event.preventDefault();
      const email = document.getElementById("loginEmail").value;
      const password = document.getElementById("loginPassword").value;

      try {
        const result = await sendRequest(
          "https://1pnb7lz9ql.execute-api.eu-central-1.amazonaws.com/prod/st/login",
          { email, password }
        );

        if (result.success) {
          window.location.href = "index-tabelle.html";
        } else {
          alert(result.message);
        }
      } catch (error) {
        // خطا قبلاً لاگ شده است
      }
    });

  document
    .getElementById("registerPasswordIcon")
    .addEventListener("click", function () {
      togglePassword("registerPassword");
    });

  document
    .getElementById("confirmPasswordIcon")
    .addEventListener("click", function () {
      togglePassword("confirmPassword");
    });

  document
    .getElementById("loginPasswordIcon")
    .addEventListener("click", function () {
      togglePassword("loginPassword");
    });
});
