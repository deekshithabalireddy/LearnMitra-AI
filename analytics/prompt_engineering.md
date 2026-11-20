
# LearnMitra-AI – Prompt Engineering Documentation

## 1. Introduction

Prompt Engineering is the process of designing clear instructions for Generative AI models to produce accurate and useful responses.

LearnMitra-AI uses Google Gemini AI to support multilingual education and interactive learning.

## 2. AI Translation Prompt

**Purpose:** Translate text from one language to another.

**Prompt:**

Translate the following text from {source_language} to {target_language}.

Use simple and natural language.

Text: {user_input}

Return only the translated text.

**Expected Output:** Translated text in the selected target language.

## 3. AI Learning Assistant Prompt

**Purpose:** Explain educational topics in the learner's preferred language.

**Prompt:**

Explain the topic '{topic}' in {language}.

Use simple words and student-friendly examples.

**Expected Output:** An easy-to-understand explanation of the selected topic.

## 4. AI Quiz Generation Prompt

**Purpose:** Generate interactive multiple-choice questions.

**Prompt:**

Generate 5 multiple-choice questions about {topic} in {language}.

Return only valid JSON in the following format:

{
    "questions": [
        {
            "question": "Question text",
            "options": ["A", "B", "C", "D"],
            "answer": "Correct option"
        }
    ]
}

**Expected Output:** Five MCQ questions with four options and correct answers.

## 5. AI Chatbot Prompt

**Purpose:** Provide educational assistance through a chatbot.

**Prompt:**

You are LearnMitra-AI, a friendly educational assistant.

Answer in {language}.

Use simple words and student-friendly examples.

Question: {user_message}

**Expected Output:** A relevant educational response in the selected language.

## 6. Prompt Engineering Techniques Used

1. Role-based prompting – Assigning the AI a specific educational role.
2. Contextual prompting – Providing the topic and selected language.
3. Instruction-based prompting – Giving clear instructions.
4. Output formatting – Requesting structured JSON for quizzes.
5. Language-specific prompting – Generating responses in the learner's preferred language.

## 7. Conclusion

Prompt Engineering helps LearnMitra-AI generate simple, relevant and multilingual educational content. It improves the usefulness of translation, explanations, quizzes and chatbot interactions.
