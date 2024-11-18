document.getElementById("pause10Button").addEventListener("click", function () {
  const now = new Date();
  localStorage.setItem("pause10Time", now.toISOString());
  alert("10-minute Pause time has been saved.");
});

document.getElementById("pause20Button").addEventListener("click", function () {
  const now = new Date();
  localStorage.setItem("pause20Time", now.toISOString());
  alert("20-minute Pause time has been saved.");
});

document.getElementById("updateButton").addEventListener("click", async function () {
  try {
    const dateInput = document.getElementById("dateInput").value;
    let selectedDate;

    if (dateInput) {
      selectedDate = dateInput;
    } else {
      const today = new Date();
      const yyyy = today.getFullYear();
      const mm = String(today.getMonth() + 1).padStart(2, "0");
      const dd = String(today.getDate()).padStart(2, "0");
      selectedDate = `${yyyy}-${mm}-${dd}`;
    }

    const response = await fetch(
      "https://j10bhm00v5.execute-api.eu-central-1.amazonaws.com/st/attendify-web",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ date: selectedDate }),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // دریافت پاسخ و پارس کردن body
    const responseBody = await response.json();
    const data = JSON.parse(responseBody.body); // تبدیل استرینگ JSON به آرایه

    const tableBody = document.querySelector("#attendance-table tbody");
    tableBody.innerHTML = ""; // پاک کردن جدول

    data.forEach((item) => {
      const row = document.createElement("tr");

      const truePercentage = parseFloat(item.true_percentage) || 0;
      const falsePercentage = parseFloat(item.false_percentage) || 0;
      const pause10Start = item.pause_10_start || "N/A";
      const pause10End = item.pause_10_end || "N/A";
      const pause20Start = item.pause_20_start || "N/A";
      const pause20End = item.pause_20_end || "N/A";

      row.innerHTML = `
        <td>${item.name || "N/A"}</td>
        <td>${item.date || "N/A"}</td>
        <td>${truePercentage}</td>
        <td>${falsePercentage}</td>
        <td>${pause10Start}</td>
        <td>${pause10End}</td>
        <td>${pause20Start}</td>
        <td>${pause20End}</td>
      `;

      if (truePercentage < 80) {
        row.style.backgroundColor = "red";
      }

      tableBody.appendChild(row);
    });

    console.log("Table updated successfully with data:", data);
  } catch (error) {
    console.error("Error loading data:", error);
  }
});

document.getElementById("todayButton").addEventListener("click", async function () {
  try {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, "0");
    const dd = String(today.getDate()).padStart(2, "0");
    const currentDate = `${yyyy}-${mm}-${dd}`;

    const response = await fetch(
      "https://j10bhm00v5.execute-api.eu-central-1.amazonaws.com/st/attendify-web",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ date: currentDate }),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const responseBody = await response.json();
    const data = JSON.parse(responseBody.body); // تبدیل body به آرایه

    const tableBody = document.querySelector("#attendance-table tbody");
    tableBody.innerHTML = "";

    data.forEach((item) => {
      const row = document.createElement("tr");

      const truePercentage = parseFloat(item.true_percentage) || 0;
      const falsePercentage = parseFloat(item.false_percentage) || 0;
      const pause10Start = item.pause_10_start || "N/A";
      const pause10End = item.pause_10_end || "N/A";
      const pause20Start = item.pause_20_start || "N/A";
      const pause20End = item.pause_20_end || "N/A";

      row.innerHTML = `
        <td>${item.name || "N/A"}</td>
        <td>${item.date || "N/A"}</td>
        <td>${truePercentage}</td>
        <td>${falsePercentage}</td>
        <td>${pause10Start}</td>
        <td>${pause10End}</td>
        <td>${pause20Start}</td>
        <td>${pause20End}</td>
      `;

      if (truePercentage < 80) {
        row.style.backgroundColor = "red";
      }

      tableBody.appendChild(row);
    });

    console.log("Today's data loaded:", data);
  } catch (error) {
    console.error("Error loading today's data:", error);
  }
});

document.getElementById("yesterdayButton").addEventListener("click", async function () {
  try {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1); // تاریخ روز قبل
    const yyyy = yesterday.getFullYear();
    const mm = String(yesterday.getMonth() + 1).padStart(2, "0");
    const dd = String(yesterday.getDate()).padStart(2, "0");
    const yesterdayDate = `${yyyy}-${mm}-${dd}`;

    const response = await fetch(
      "https://j10bhm00v5.execute-api.eu-central-1.amazonaws.com/st/attendify-web",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ date: yesterdayDate }),
      }
    );

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const responseBody = await response.json();
    const data = JSON.parse(responseBody.body); // پارس کردن body به آرایه

    const tableBody = document.querySelector("#attendance-table tbody");
    tableBody.innerHTML = "";

    data.forEach((item) => {
      const row = document.createElement("tr");

      const truePercentage = parseFloat(item.true_percentage) || 0;
      const falsePercentage = parseFloat(item.false_percentage) || 0;
      const pause10Start = item.pause_10_start || "N/A";
      const pause10End = item.pause_10_end || "N/A";
      const pause20Start = item.pause_20_start || "N/A";
      const pause20End = item.pause_20_end || "N/A";

      row.innerHTML = `
        <td>${item.name || "N/A"}</td>
        <td>${item.date || "N/A"}</td>
        <td>${truePercentage}</td>
        <td>${falsePercentage}</td>
        <td>${pause10Start}</td>
        <td>${pause10End}</td>
        <td>${pause20Start}</td>
        <td>${pause20End}</td>
      `;

      if (truePercentage < 80) {
        row.style.backgroundColor = "red";
      }

      tableBody.appendChild(row);
    });

    console.log("Yesterday's data loaded:", data);
  } catch (error) {
    console.error("Error loading yesterday's data:", error);
  }
});
