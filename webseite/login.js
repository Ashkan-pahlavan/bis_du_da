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
        body: JSON.stringify({ body: JSON.stringify(data) }),
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
          "https://el5t5k2kq0.execute-api.eu-central-1.amazonaws.com/st/register",
          { email, password }
        );

        if (
          result.body === '{"message": "Login successful!", "success": true}'
        ) {
          // بررسی موفقیت لاگین
          window.location.href = "index-tabelle.html";
          alert(result.message || "Register successful!");
        } else {
          alert(result.message || "Login failed");
        }
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
          "https://el5t5k2kq0.execute-api.eu-central-1.amazonaws.com/st/login",
          { email, password }
        );

        if (
          result.body === '{"message": "Login successful!", "success": true}'
        ) {
          // بررسی موفقیت لاگین
          window.location.href = "index-tabelle.html"; // انتقال به صفحه‌ی index-tabelle.html
          alert(result.message || "Login successful!");
        } else {
          alert(result.message || "Login failed");
        }
      } catch (error) {
        alert("Login failed");
        console.error("Error:", error);
      }
    });

  // مدیریت کلیک روی "Hier klicken" برای نمایش فرم ثبت‌نام
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

  // Toggle forms visibility
  document
    .getElementById("showRegisterForm")
    .addEventListener("click", function (event) {
      event.preventDefault();
      document.getElementById("loginContainer").style.display = "none";
      document.getElementById("registerContainer").style.display = "block";
    });

  document
    .getElementById("showLoginForm")
    .addEventListener("click", function (event) {
      event.preventDefault();
      document.getElementById("registerContainer").style.display = "none";
      document.getElementById("loginContainer").style.display = "block";
    });
});
