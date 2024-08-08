document.getElementById("updateButton").addEventListener("click", async function () {
  try {
    // دریافت تاریخ امروز
    const today = new Date();
    const yyyy = today.getFullYear();
    const mm = String(today.getMonth() + 1).padStart(2, '0'); // ماه از 0 شروع می‌شود، بنابراین 1 را اضافه می‌کنیم
    const dd = String(today.getDate()).padStart(2, '0');
    const currentDate = `${yyyy}-${mm}-${dd}`; // فرمت YYYY-MM-DD

    const response = await fetch("https://y0vkz8x2w2.execute-api.eu-central-1.amazonaws.com/stage/attendance", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ date: currentDate }) // استفاده از تاریخ امروز به جای تاریخ ثابت
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
