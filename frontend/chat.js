
async function sendMessage() {

    const messageInput = document.getElementById("message");
    const language = document.getElementById("language").value;
    const chatBox = document.getElementById("chat-box");

    const message = messageInput.value.trim();

    if (!message) {
        alert("Please enter your question.");
        return;
    }

    // Display student question
    const userMessage = document.createElement("p");
    userMessage.innerText = "You: " + message;
    chatBox.appendChild(userMessage);

    messageInput.value = "";

    // Display loading message
    const loading = document.createElement("p");
    loading.innerText = "AI is thinking...";
    chatBox.appendChild(loading);

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/chat",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: message,
                    language: language
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Chat failed.");
        }

        loading.innerText = "LearnMitra-AI: " + data.answer;

    } catch (error) {

        loading.innerText = "Error: " + error.message;

    }
}
