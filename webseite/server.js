const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const app = express();
const port = 3000;

// لیست ایمیل‌های مجاز
const allowedEmails = [
    "ashkoli1988@gmail.com",
    "ashkoli1988@yahoo.com",
    "ashkan.pahlavan@docc.techstarter.de"
];

// مسیر فایل رمز عبور
const passwordFilePath = path.join(__dirname, 'password.json');

// تنظیمات Express
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

// تابع هش کردن رمز عبور
function hashPassword(password) {
    return crypto.createHash('sha256').update(password).digest('hex');
}

// تابع خواندن کاربران از فایل رمز عبور
function readUsers() {
    if (!fs.existsSync(passwordFilePath)) {
        return [];
    }
    const usersData = fs.readFileSync(passwordFilePath, 'utf-8');
    if (!usersData) {
        return [];
    }
    try {
        return JSON.parse(usersData);
    } catch (err) {
        // اگر فایل خالی یا نامعتبر بود، یک آرایه خالی برمی‌گردانیم
        return [];
    }
}

// تابع نوشتن کاربران در فایل رمز عبور
function writeUsers(users) {
    fs.writeFileSync(passwordFilePath, JSON.stringify(users, null, 2), 'utf-8');
}

// API برای ثبت‌نام کاربر
app.post('/register', (req, res) => {
    const { email, password } = req.body;
    if (!allowedEmails.includes(email)) {
        return res.status(400).json({ message: 'This email is not allowed to register.' });
    }

    const users = readUsers();
    const hashedPassword = hashPassword(password);

    if (users.find(user => user.email === email)) {
        return res.status(400).json({ message: 'This email is already registered.' });
    }

    users.push({ email, password: hashedPassword });
    writeUsers(users);

    res.json({ message: 'Registration successful. You can now log in.' });
});

// API برای ورود کاربر
app.post('/login', (req, res) => {
    const { email, password } = req.body;
    const users = readUsers();
    const hashedPassword = hashPassword(password);

    const user = users.find(user => user.email === email && user.password === hashedPassword);
    if (user) {
        res.json({ message: 'Login successful!', success: true });
    } else {
        res.status(400).json({ message: 'Incorrect email or password.' });
    }
});

// شروع سرور
app.listen(port, () => {
    console.log(`Server is running at http://localhost:${port}`);
});
