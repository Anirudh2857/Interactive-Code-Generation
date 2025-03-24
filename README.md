# 🛠️ Advanced Interactive Code Generator

This Streamlit application leverages OpenAI's GPT models to automatically generate and evaluate code solutions based on user-defined prompts. It supports multiple programming languages and provides detailed explanations, complexity analysis, and interactive testing capabilities.

🔗 **Deployed App:** [Access the live application here]([your-deployment-link](https://interactive-code-generation-phuoeuqtiojx2tnrkkmuev.streamlit.app))

---

## 🚀 Features

- **Automatic Code Generation:** Generate brute-force, improved, and optimal solutions for your coding problems.
- **Interactive GPT Assistant:** Clarify your queries directly via a sidebar AI assistant.
- **Complexity Analysis:** Each solution explicitly states its time and space complexity.
- **Problem Difficulty Prediction:** Predicts whether a given problem is Easy, Medium, or Hard.
- **Interactive Code Testing:** Run your own test cases with execution timeout handling.
- **Export Options:** Export solutions in Markdown or HTML formats.
- **Customizable Output:** Choose between Raw or Markdown formatting.
- **Accessibility:** Adjustable font size for better readability.
- **Categorization:** Easily organize and filter problems based on categories (Algorithms, Data Structures, Machine Learning, etc.).

---

## 📦 Requirements

Ensure you have Python installed and set up your environment with:

```bash
pip install -r requirements.txt
```

Your `requirements.txt` should include:

```
streamlit
openai
```

---

## 🔑 Setup

Set your OpenAI API key securely via environment variable:

```bash
export OPENAI_API_KEY="your-secret-key"
```

---

## 🚀 Running the Application

Launch the app locally by running:

```bash
streamlit run app.py
```

---

## 🎯 Usage

1. **Input your prompt** describing the coding problem clearly.
2. **Select desired options** (programming language, GPT model, etc.).
3. **Generate and review solutions** with provided complexity analyses.
4. **Interactively test** generated solutions with custom test cases.
5. **Export solutions** in the desired format.

---

## ⚠️ Important Notes

- Always keep your OpenAI API key private and secure.
- Monitor usage to avoid unexpected charges from the OpenAI API.

---

## 📜 License

This project is available under the MIT License.

