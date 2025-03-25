import streamlit as st
import re
import contextlib
import io
import threading
import os
from openai import OpenAI

# Set your OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

st.set_page_config(layout="wide")

# Accessibility: Adjustable font size
font_size = st.sidebar.slider("Adjust Font Size", 10, 24, 14)
st.markdown(f"<style>body{{font-size:{font_size}px;}}</style>", unsafe_allow_html=True)

st.title("🛠️ Advanced Interactive Code Generator")

# Sidebar Chat Assistant
st.sidebar.title("💬 AI Assistant")
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

chat_input = st.sidebar.text_input("Ask the assistant", key="chat_input")
if st.sidebar.button("Send", key="send_button") and chat_input:
    messages = st.session_state['chat_history'] + [{"role": "user", "content": chat_input}]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500
    )
    reply = response.choices[0].message.content
    st.session_state['chat_history'].append({"role": "user", "content": chat_input})
    st.session_state['chat_history'].append({"role": "assistant", "content": reply})

for message in st.session_state['chat_history']:
    st.sidebar.markdown(f"**{message['role'].capitalize()}**: {message['content']}")

# Main Tabs
tab1, tab2 = st.tabs(["Generate Code", "Code Review"])

with tab1:
    prompt = st.text_area("Enter your code prompt:", height=120, key="prompt")
    category = st.selectbox("Categorize your problem:", ["Algorithms", "Data Structures", "Machine Learning", "Web Development", "Database", "Other"], key="category")
    language = st.selectbox("Select programming language:", ["Python", "JavaScript", "Java", "C++", "HTML", "CSS", "SQL", "Go", "Ruby"], key="language")
    model = st.selectbox("Select GPT Model:", ["gpt-3.5-turbo", "gpt-4"], key="model")
    temperature = st.slider("Creativity (Temperature):", 0.0, 1.0, 0.2, key="temperature")
    max_tokens = st.slider("Max Tokens:", 100, 4000, 1500, key="max_tokens")
    explain = st.checkbox("Include detailed explanation with complexity analysis", key="explain")

    examples = st.text_area("Enter test input examples (comma-separated):", height=100, key="examples")

    output_format = st.selectbox("Select output format:", ["Raw", "Markdown"], key="output_format")
    execution_timeout = st.slider("Execution Timeout (seconds):", 1, 10, 5, key="execution_timeout")

    if 'history' not in st.session_state:
        st.session_state['history'] = []

    if st.button("Generate Code", key="generate_code"):
        if not prompt.strip():
            st.warning("Please enter a prompt.")
        else:
            with st.spinner("Generating solutions..."):
                difficulty_response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": f"Rate the difficulty of this problem as Easy, Medium, or Hard: {prompt}"}],
                    temperature=0.0,
                    max_tokens=10
                )
                difficulty = difficulty_response.choices[0].message.content.strip()
                st.info(f"Estimated Difficulty: {difficulty}")

                solutions_types = ["Brute force", "Improved", "Optimal"]
                results = []

                for sol in solutions_types:
                    response = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": f"Provide a {sol.lower()} solution in {language} with detailed comments and explicit time and space complexity."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=temperature,
                        max_tokens=max_tokens
                    )
                    solution_code = response.choices[0].message.content
                    results.append((sol, solution_code))

                def extract_code(content):
                    match = re.search(r"```[a-zA-Z]*\n(.*?)```", content, re.DOTALL)
                    return match.group(1) if match else content

                for sol_type, content in results:
                    st.subheader(f"{sol_type} Solution")

                    code = extract_code(content)

                    if output_format == "Markdown":
                        st.markdown(f"```{language.lower()}\n{code}\n```")
                    else:
                        st.code(code, language=language.lower())

                    complexity_info = re.findall(r"Time Complexity:.*?Space Complexity:.*?(?=\n|$)", content, re.DOTALL)
                    if complexity_info:
                        st.info(complexity_info[0])

with tab2:
    review_code = st.text_area("Paste your code for review:", height=250, key="review_code")

    if st.button("Review Code", key="review_button"):
        if not review_code.strip():
            st.warning("Please paste your code for review.")
        else:
            with st.spinner("Reviewing your code..."):
                review_response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Perform a detailed code review, highlighting improvements, potential issues, and suggesting best practices."},
                        {"role": "user", "content": review_code}
                    ],
                    temperature=0.0,
                    max_tokens=1000
                )
                review = review_response.choices[0].message.content
                st.markdown(review)
