document.getElementById("updateButton").addEventListener("click", async function () {
  try {
    const response = await fetch("https://y0vkz8x2w2.execute-api.eu-central-1.amazonaws.com/stage/attendance", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ date: "2024-08-07" })  // این تاریخ به طور مثال است، می‌توانید آن را تغییر دهید
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();

    // بررسی کنید که data آرایه باشد
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
