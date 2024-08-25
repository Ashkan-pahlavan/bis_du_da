// document.getElementById("pauseButton").addEventListener("click", function () {
//   const now = new Date();
//   const localTime = now.toLocaleString(); // ذخیره زمان محلی کاربر
//   localStorage.setItem("pauseTime", localTime);
//   alert("Pause time has been saved.");
// });

document.getElementById("pauseButton").addEventListener("click", function () {
  const now = new Date();
  localStorage.setItem("pauseTime", now.toISOString());
  alert("Pause time has been saved.");
});

document
  .getElementById("updateButton")
  .addEventListener("click", async function () {
    try {
      const dateInput = document.getElementById("dateInput").value;
      let selectedDate;

      if (dateInput) {
        selectedDate = dateInput; // استفاده از تاریخ وارد شده توسط معلم
      } else {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, "0");
        const dd = String(today.getDate()).padStart(2, "0");
        selectedDate = `${yyyy}-${mm}-${dd}`;
      }

      const response = await fetch(
        "https://y0vkz8x2w2.execute-api.eu-central-1.amazonaws.com/stage/attendance",
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

      const data = await response.json();

      if (!Array.isArray(data)) {
        console.error("Received data is not an array:", data);
        throw new Error("Data is not an array");
      }

      const tableBody = document.querySelector("#attendance-table tbody");
      tableBody.innerHTML = "";

      const storedPauseTime = localStorage.getItem("pauseTime");
      const storedPauseDate = storedPauseTime
        ? new Date(storedPauseTime)
        : null;

      data.forEach((item) => {
        const row = document.createElement("tr");

        const truePercentage = parseFloat(item.true_percentage);
        const pauseStart = new Date(item.pause_start);

        // شرط برای تغییر رنگ ردیف اگر درصد حضور کمتر از 80 باشد
        if (truePercentage < 80) {
          row.style.backgroundColor = "red";
        }

        // شرط برای تغییر رنگ زمان شروع پاز اگر تفاوت بیشتر از 3 دقیقه باشد
        if (storedPauseDate) {
          const timeDifference = Math.abs(pauseStart - storedPauseDate) / 60000; // اختلاف زمانی به دقیقه
          if (timeDifference > 3) {
            row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.date}</td>
            <td>${item.true_percentage}</td>
            <td>${item.false_percentage}</td>
            <td style="background-color: yellow;">${item.pause_start}</td>
            <td>${item.pause_end}</td>
          `;
          } else {
            row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.date}</td>
            <td>${item.true_percentage}</td>
            <td>${item.false_percentage}</td>
            <td>${item.pause_start}</td>
            <td>${item.pause_end}</td>
          `;
          }
        } else {
          row.innerHTML = `
          <td>${item.name}</td>
          <td>${item.date}</td>
          <td>${item.true_percentage}</td>
          <td>${item.false_percentage}</td>
          <td>${item.pause_start}</td>
          <td>${item.pause_end}</td>
        `;
        }

        tableBody.appendChild(row);
      });

      console.log("Success:", data);
    } catch (error) {
      console.error("Error:", error);
    }
  });

document
  .getElementById("todayButton")
  .addEventListener("click", async function () {
    try {
      const today = new Date();
      const yyyy = today.getFullYear();
      const mm = String(today.getMonth() + 1).padStart(2, "0");
      const dd = String(today.getDate()).padStart(2, "0");
      const currentDate = `${yyyy}-${mm}-${dd}`;

      const response = await fetch(
        "https://y0vkz8x2w2.execute-api.eu-central-1.amazonaws.com/stage/attendance",
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

      const data = await response.json();

      if (!Array.isArray(data)) {
        console.error("Received data is not an array:", data);
        throw new Error("Data is not an array");
      }

      const tableBody = document.querySelector("#attendance-table tbody");
      tableBody.innerHTML = "";

      const storedPauseTime = localStorage.getItem("pauseTime");
      const storedPauseDate = storedPauseTime
        ? new Date(storedPauseTime)
        : null;

      data.forEach((item) => {
        const row = document.createElement("tr");

        const truePercentage = parseFloat(item.true_percentage);
        const pauseStart = new Date(item.pause_start);

        if (truePercentage < 80) {
          row.style.backgroundColor = "red";
        }

        if (storedPauseDate) {
          const timeDifference = Math.abs(pauseStart - storedPauseDate) / 60000;
          if (timeDifference > 3) {
            row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.date}</td>
            <td>${item.true_percentage}</td>
            <td>${item.false_percentage}</td>
            <td style="background-color: yellow;">${item.pause_start}</td>
            <td>${item.pause_end}</td>
          `;
          } else {
            row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.date}</td>
            <td>${item.true_percentage}</td>
            <td>${item.false_percentage}</td>
            <td>${item.pause_start}</td>
            <td>${item.pause_end}</td>
          `;
          }
        } else {
          row.innerHTML = `
          <td>${item.name}</td>
          <td>${item.date}</td>
          <td>${item.true_percentage}</td>
          <td>${item.false_percentage}</td>
          <td>${item.pause_start}</td>
          <td>${item.pause_end}</td>
        `;
        }

        tableBody.appendChild(row);
      });

      console.log("Success:", data);
    } catch (error) {
      console.error("Error:", error);
    }
  });

document
  .getElementById("yesterdayButton")
  .addEventListener("click", async function () {
    try {
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1); // تنظیم تاریخ به روز گذشته
      const yyyy = yesterday.getFullYear();
      const mm = String(yesterday.getMonth() + 1).padStart(2, "0");
      const dd = String(yesterday.getDate()).padStart(2, "0");
      const yesterdayDate = `${yyyy}-${mm}-${dd}`;

      const response = await fetch(
        "https://y0vkz8x2w2.execute-api.eu-central-1.amazonaws.com/stage/attendance",
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

      const data = await response.json();

      if (!Array.isArray(data)) {
        console.error("Received data is not an array:", data);
        throw new Error("Data is not an array");
      }

      const tableBody = document.querySelector("#attendance-table tbody");
      tableBody.innerHTML = "";

      const storedPauseTime = localStorage.getItem("pauseTime");
      const storedPauseDate = storedPauseTime
        ? new Date(storedPauseTime)
        : null;

      data.forEach((item) => {
        const row = document.createElement("tr");

        const truePercentage = parseFloat(item.true_percentage);
        const pauseStart = new Date(item.pause_start);

        if (truePercentage < 80) {
          row.style.backgroundColor = "red";
        }

        if (storedPauseDate) {
          const timeDifference = Math.abs(pauseStart - storedPauseDate) / 60000;
          if (timeDifference > 3) {
            row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.date}</td>
            <td>${item.true_percentage}</td>
            <td>${item.false_percentage}</td>
            <td style="background-color: yellow;">${item.pause_start}</td>
            <td>${item.pause_end}</td>
          `;
          } else {
            row.innerHTML = `
            <td>${item.name}</td>
            <td>${item.date}</td>
            <td>${item.true_percentage}</td>
            <td>${item.false_percentage}</td>
            <td>${item.pause_start}</td>
            <td>${item.pause_end}</td>
          `;
          }
        } else {
          row.innerHTML = `
          <td>${item.name}</td>
          <td>${item.date}</td>
          <td>${item.true_percentage}</td>
          <td>${item.false_percentage}</td>
          <td>${item.pause_start}</td>
          <td>${item.pause_end}</td>
        `;
        }

        tableBody.appendChild(row);
      });

      console.log("Success:", data);
    } catch (error) {
      console.error("Error:", error);
    }
  });

  document.getElementById("pauseCheckButton").addEventListener("click", function () {
    const storedPauseTime = localStorage.getItem("pauseTime");

    if (!storedPauseTime) {
        alert("No pause time found in local storage.");
        return;
    }

    // Convert stored time to local time
    const storedPauseDateUTC = new Date(storedPauseTime);
    const storedPauseDateLocal = new Date(storedPauseDateUTC);

    const rows = document.querySelectorAll("#attendance-table tbody tr");

    rows.forEach((row, index) => {
        const pauseStartCell = row.querySelector("td:nth-child(5)");
        const pauseStartTime = pauseStartCell.textContent;

        // Parse Pause Start Time from table (HH:MM:SS) and combine with the stored date
        const [hours, minutes, seconds] = pauseStartTime.split(":");
        const pauseDate = new Date(storedPauseDateLocal);
        pauseDate.setHours(parseInt(hours), parseInt(minutes), parseInt(seconds), 0);

        const timeDifference = Math.abs((pauseDate - storedPauseDateLocal) / (1000 * 60)); // تفاوت زمانی به دقیقه

        if (timeDifference > 3) {
            pauseStartCell.style.color = "yellow"; // تغییر رنگ نوشته به زرد
        } else {
            pauseStartCell.style.color = ""; // بازگرداندن رنگ به حالت عادی
        }
    });
});

