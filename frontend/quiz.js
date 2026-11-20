
async function generateQuiz() {

    const topic = document.getElementById("topic").value;
    const language = document.getElementById("language").value;
    const questionsDiv = document.getElementById("questions");

    if (!topic.trim()) {
        questionsDiv.innerText = "Please enter a topic.";
        return;
    }

    questionsDiv.innerText = "Generating quiz...";

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/generate-quiz",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    topic: topic,
                    language: language
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Quiz generation failed.");
        }

        questionsDiv.innerHTML = "";

        data.questions.forEach((question, index) => {

            const questionBox = document.createElement("div");
            questionBox.style.marginBottom = "25px";

            const heading = document.createElement("h3");
            heading.innerText = (index + 1) + ". " + question.question;

            questionBox.appendChild(heading);

            question.options.forEach(option => {

                const label = document.createElement("label");
                const radio = document.createElement("input");

                radio.type = "radio";
                radio.name = "question" + index;
                radio.value = option;

                label.appendChild(radio);
                label.appendChild(document.createTextNode(" " + option));

                questionBox.appendChild(label);
                questionBox.appendChild(document.createElement("br"));
            });

            questionsDiv.appendChild(questionBox);
        });

        const submitButton = document.createElement("button");
        submitButton.innerText = "Submit Quiz";
        submitButton.onclick = () => checkAnswers(data.questions);

        questionsDiv.appendChild(submitButton);

    } catch (error) {

        questionsDiv.innerText = "Error: " + error.message;

    }
}


function checkAnswers(questions) {

    let score = 0;

    questions.forEach((question, index) => {

        const selected = document.querySelector(
            'input[name="question' + index + '"]:checked'
        );

        if (selected && selected.value === question.answer) {
            score++;
        }

    });

    document.getElementById("questions").innerText =
        "Your Score: " + score + " / " + questions.length;
}
