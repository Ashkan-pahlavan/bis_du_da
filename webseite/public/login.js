document.addEventListener('DOMContentLoaded', function() {
    // تابع تغییر وضعیت نمایش رمز عبور
    function togglePassword(inputId) {
        const input = document.getElementById(inputId);
        const icon = document.getElementById(`${inputId}Icon`);
        if (input.type === "password") {
            input.type = "text";
            icon.src = "eye-icon-new.jpg"; // مسیر آیکون چشم باز
        } else {
            input.type = "password";
            icon.src = "eye-icon.jpg"; // مسیر آیکون چشم بسته
        }
    }

    // مدیریت فرم ثبت‌نام
    document.getElementById('registerForm').addEventListener('submit', async function(event) {
        event.preventDefault();
        const email = document.getElementById('registerEmail').value;
        const password = document.getElementById('registerPassword').value;
        const confirmPassword = document.getElementById('confirmPassword').value;

        if (password !== confirmPassword) {
            alert('Passwords do not match.');
            return;
        }

        const response = await fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const result = await response.json();
        alert(result.message);
    });

    // مدیریت فرم ورود
    document.getElementById('loginForm').addEventListener('submit', async function(event) {
        event.preventDefault();
        const email = document.getElementById('loginEmail').value;
        const password = document.getElementById('loginPassword').value;

        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        const result = await response.json();
        if (result.success) {
            window.location.href = "index-tabelle.html";
        } else {
            alert(result.message);
        }
    });

    // اضافه کردن رویداد کلیک به آیکون‌های چشم
    document.getElementById('registerPasswordIcon').addEventListener('click', function() {
        togglePassword('registerPassword');
    });

    document.getElementById('confirmPasswordIcon').addEventListener('click', function() {
        togglePassword('confirmPassword');
    });

    document.getElementById('loginPasswordIcon').addEventListener('click', function() {
        togglePassword('loginPassword');
    });
});
