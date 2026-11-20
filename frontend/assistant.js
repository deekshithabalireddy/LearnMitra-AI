
async function runAgent() {
    const message = document.getElementById("agentMessage").value;
    const language = document.getElementById("agentLanguage").value;

    const actionOutput = document.getElementById("agentAction");
    const responseOutput = document.getElementById("agentResponse");

    if (!message.trim()) {
        responseOutput.innerText = "Please enter your request.";
        return;
    }

    actionOutput.innerText = "";
    responseOutput.innerText = "LearnMitra AI Agent is processing your request...";

    try {
        const response = await fetch("http://127.0.0.1:8000/agent", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: message,
                language: language
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Something went wrong.");
        }

        actionOutput.innerText = "Selected Task: " + data.selected_action;
        responseOutput.innerText =
            typeof data.response === "object"
                ? JSON.stringify(data.response, null, 2)
                : data.response;

    } catch (error) {
        responseOutput.innerText = "Error: " + error.message;
    }
}
