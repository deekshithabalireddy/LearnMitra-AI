
const historyList = document.getElementById("historyList");
const totalRecords = document.getElementById("totalRecords");

async function loadHistory() {
    try {
        const response = await fetch("http://127.0.0.1:8000/history");

        if (!response.ok) {
            throw new Error("Unable to load learning history.");
        }

        const data = await response.json();

        totalRecords.textContent = data.total_records;

        if (data.history.length === 0) {
            historyList.innerHTML = "<p>No learning activities found.</p>";
            return;
        }

        historyList.innerHTML = "";

        data.history.forEach((item) => {
            const card = document.createElement("div");
            card.className = "history-card";

            const title = document.createElement("h3");
            title.textContent = getActivityTitle(item.activity_type);

            const input = document.createElement("p");
            input.textContent = "Input: " + (item.input || "");

            const language = document.createElement("p");
            language.textContent =
                "Language: " +
                (item.language ||
                item.target_language ||
                "Not specified");

            const result = document.createElement("p");
            result.textContent =
                "Result: " + formatResult(item.result);

            const date = document.createElement("p");
            date.textContent =
                "Date: " +
                (item.created_at
                    ? new Date(item.created_at).toLocaleString()
                    : "Not available");

            card.appendChild(title);
            card.appendChild(input);
            card.appendChild(language);
            card.appendChild(result);
            card.appendChild(date);

            historyList.appendChild(card);
        });

    } catch (error) {
        historyList.textContent = error.message;
    }
}

function getActivityTitle(type) {
    const titles = {
        translation: "AI Translation",
        explanation: "AI Learning Explanation",
        quiz: "Quiz Generation",
        chat: "AI Chatbot"
    };

    return titles[type] || "Learning Activity";
}

function formatResult(result) {
    if (typeof result === "object" && result !== null) {
        return JSON.stringify(result, null, 2);
    }

    return result || "No result available";
}

loadHistory();
