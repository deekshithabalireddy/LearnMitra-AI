
async function translateText() {

    const input = document.getElementById("inputText").value;
    const source = document.getElementById("sourceLanguage").value;
    const target = document.getElementById("targetLanguage").value;

    const output = document.getElementById("outputText");
    const status = document.getElementById("status");

    if (!input.trim()) {
        status.textContent = "Please enter some text.";
        return;
    }

    if (source === target) {
        status.textContent = "Please select two different languages.";
        return;
    }

    status.textContent = "Connecting to AI translation service...";
    output.textContent = "";

    try {
        const response = await fetch("http://127.0.0.1:8000/translate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: input,
                source_language: source,
                target_language: target
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Translation failed.");
        }

        output.textContent = data.translation;
        status.textContent = "Translation completed successfully!";

    } catch (error) {
        status.textContent = error.message;
    }
}

function copyTranslation() {

    const text = document.getElementById("outputText").textContent;

    navigator.clipboard.writeText(text)
        .then(() => {
            document.getElementById("status").textContent =
                "Translation copied!";
        })
        .catch(() => {
            document.getElementById("status").textContent =
                "Unable to copy text.";
        });
}
