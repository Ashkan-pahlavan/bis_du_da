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

document
  .getElementById("updateButton")
  .addEventListener("click", async function () {
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

      data.forEach((item) => {
        const row = document.createElement("tr");

        const truePercentage = parseFloat(item.true_percentage) || 0;
        const falsePercentage = parseFloat(item.false_percentage) || 0;
        const pause10Start = item.pause_start || "N/A"; // Name corrected
        const pause10End = item.pause_end || "N/A"; // Name corrected
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

      const storedPause10Time = localStorage.getItem("pause10Time");
      const storedPause20Time = localStorage.getItem("pause20Time");
      const storedPause10Date = storedPause10Time
        ? new Date(storedPause10Time)
        : null;
      const storedPause20Date = storedPause20Time
        ? new Date(storedPause20Time)
        : null;

      data.forEach((item) => {
        const row = document.createElement("tr");

        const truePercentage = parseFloat(item.true_percentage);
        const pause10Start = item.pause_start || "N/A";
        const pause10End = item.pause_end || "N/A";
        const pause20Start = item.pause_20_start || "N/A";
        const pause20End = item.pause_20_end || "N/A";

        if (truePercentage < 80) {
          row.style.backgroundColor = "red";
        }

        row.innerHTML = `
              <td>${item.name}</td>
              <td>${item.date}</td>
              <td>${item.true_percentage}</td>
              <td>${item.false_percentage}</td>
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

      const storedPause10Time = localStorage.getItem("pause10Time");
      const storedPause20Time = localStorage.getItem("pause20Time");
      const storedPause10Date = storedPause10Time
        ? new Date(storedPause10Time)
        : null;
      const storedPause20Date = storedPause20Time
        ? new Date(storedPause20Time)
        : null;

      data.forEach((item) => {
        const row = document.createElement("tr");

        const truePercentage = parseFloat(item.true_percentage);
        const pause10Start = item.pause_start || "N/A";
        const pause10End = item.pause_end || "N/A";
        const pause20Start = item.pause_20_start || "N/A";
        const pause20End = item.pause_20_end || "N/A";

        if (truePercentage < 80) {
          row.style.backgroundColor = "red";
        }

        row.innerHTML = `
              <td>${item.name}</td>
              <td>${item.date}</td>
              <td>${item.true_percentage}</td>
              <td>${item.false_percentage}</td>
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

      console.log("Success:", data);
    } catch (error) {
      console.error("Error:", error);
    }
  });

  document.getElementById("pauseCheckButton").addEventListener("click", function () {
    const storedPause10Time = localStorage.getItem("pause10Time");
    const storedPause20Time = localStorage.getItem("pause20Time");

    if (!storedPause10Time && !storedPause20Time) {
        alert("Keine Pausenzeit im lokalen Speicher gefunden.");
        return;
    }

    const rows = document.querySelectorAll("#attendance-table tbody tr");

    rows.forEach((row, index) => {
        const pause10StartCell = row.querySelector("td:nth-child(5)");
        const pause20StartCell = row.querySelector("td:nth-child(7)");

        const pause10StartTime = pause10StartCell.textContent;
        const pause20StartTime = pause20StartCell.textContent;

        if (storedPause10Time && pause10StartTime !== "N/A") {
            const storedPause10Date = new Date(storedPause10Time);
            const [hours10, minutes10, seconds10] = pause10StartTime.split(":");
            const pause10Date = new Date(storedPause10Date);
            pause10Date.setHours(
                parseInt(hours10),
                parseInt(minutes10),
                parseInt(seconds10),
                0
            );

            const timeDifference10 = Math.abs(
                (pause10Date.getTime() - storedPause10Date.getTime()) / (1000 * 60)
            );

            if (timeDifference10 > 3) {
                pause10StartCell.style.color = "yellow";
            } else {
                pause10StartCell.style.color = "";
            }
        }

        if (storedPause20Time && pause20StartTime !== "N/A") {
            const storedPause20Date = new Date(storedPause20Time);
            const [hours20, minutes20, seconds20] = pause20StartTime.split(":");
            const pause20Date = new Date(storedPause20Date);
            pause20Date.setHours(
                parseInt(hours20),
                parseInt(minutes20),
                parseInt(seconds20),
                0
            );

            const timeDifference20 = Math.abs(
                (pause20Date.getTime() - storedPause20Date.getTime()) / (1000 * 60)
            );

            if (timeDifference20 > 3) {
                pause20StartCell.style.color = "yellow";
            } else {
                pause20StartCell.style.color = "";
            }
        }
    });
});
