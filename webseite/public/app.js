document.getElementById("updateButton").addEventListener("click", async function () {
  try {
    const dateInput = document.getElementById("dateInput").value;
    let selectedDate;

    if (dateInput) {
      selectedDate = dateInput; // استفاده از تاریخ وارد شده توسط معلم
    } else {
      const today = new Date();
      const yyyy = today.getFullYear();
      const mm = String(today.getMonth() + 1).padStart(2, '0');
      const dd = String(today.getDate()).padStart(2, '0');
      selectedDate = `${yyyy}-${mm}-${dd}`;
    }

    const response = await fetch("https://y0vkz8x2w2.execute-api.eu-central-1.amazonaws.com/stage/attendance", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ date: selectedDate })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (!Array.isArray(data)) {
      console.error("Received data is not an array:", data);
      throw new Error("Data is not an array");
    }

    const tableBody = document.querySelector("#attendance-table tbody");
    tableBody.innerHTML = "";

    data.forEach((item) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.name}</td>
        <td>${item.date}</td>
        <td>${item.true_percentage}</td>
        <td>${item.false_percentage}</td>
        <td>${item.pause_start}</td>
        <td>${item.pause_end}</td>
      `;
      tableBody.appendChild(row);
    });

    console.log("Success:", data);
  } catch (error) {
    console.error("Error:", error);
  }
});

document.getElementById("todayButton").addEventListener("click", async function () {
  try {
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0');
    const dd = String(today.getDate()).padStart(2, '0');
    const currentDate = `${yyyy}-${mm}-${dd}`;

    const response = await fetch("https://y0vkz8x2w2.execute-api.eu-central-1.amazonaws.com/stage/attendance", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ date: currentDate })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (!Array.isArray(data)) {
      console.error("Received data is not an array:", data);
      throw new Error("Data is not an array");
    }

    const tableBody = document.querySelector("#attendance-table tbody");
    tableBody.innerHTML = "";

    data.forEach((item) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.name}</td>
        <td>${item.date}</td>
        <td>${item.true_percentage}</td>
        <td>${item.false_percentage}</td>
        <td>${item.pause_start}</td>
        <td>${item.pause_end}</td>
      `;
      tableBody.appendChild(row);
    });

    console.log("Success:", data);
  } catch (error) {
    console.error("Error:", error);
  }
});

document.getElementById("yesterdayButton").addEventListener("click", async function () {
  try {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1); // تنظیم تاریخ به روز گذشته
    const yyyy = yesterday.getFullYear();
    const mm = String(yesterday.getMonth() + 1).padStart(2, '0');
    const dd = String(yesterday.getDate()).padStart(2, '0');
    const yesterdayDate = `${yyyy}-${mm}-${dd}`;

    const response = await fetch("https://y0vkz8x2w2.execute-api.eu-central-1.amazonaws.com/stage/attendance", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ date: yesterdayDate })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    if (!Array.isArray(data)) {
      console.error("Received data is not an array:", data);
      throw new Error("Data is not an array");
    }

    const tableBody = document.querySelector("#attendance-table tbody");
    tableBody.innerHTML = "";

    data.forEach((item) => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${item.name}</td>
        <td>${item.date}</td>
        <td>${item.true_percentage}</td>
        <td>${item.false_percentage}</td>
        <td>${item.pause_start}</td>
        <td>${item.pause_end}</td>
      `;
      tableBody.appendChild(row);
    });

    console.log("Success:", data);
  } catch (error) {
    console.error("Error:", error);
  }
});
