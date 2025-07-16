import streamlit as st
import google.generativeai as genai

# Load API key securely using Streamlit Secrets
api_key = st.secrets["general"]["api_key"]

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Define severity-related keywords
severe_keywords = [
    "severe", "critical", "urgent", "life-threatening", "intense", "serious"
]

# Check if the input text contains severity keywords
def is_severe_problem(text):
    return any(word in text.lower() for word in severe_keywords)

# Return contact info only if the issue is severe
def get_contact_info_if_severe(text):
    if is_severe_problem(text):
        return [
            "Mental Health Helpline: 100",
            "Women’s Health Helpline: 101",
            "Child Health Helpline: 102",
            "Elderly Care Helpline: 104",
            "Diabetes Support Helpline: 105",
            "TB Helpline: 106",
            "COVID-19 Helpline: 107",
            "General Health Helpline: 103",
            "Emergency Services: 108"
        ]
    else:
        return []

# Generate short health-related message
def generate_health_message(prompt_text):
    message_prompt = f'''
You are a healthcare communication expert. Using the health problem or topic described here: "{prompt_text}", 
write a concise and clear health message in 2-3 sentences that:

- Briefly explains the issue
- Offers simple advice or encouragement
- Uses professional and empathetic language
- Avoids hashtags, emojis, and casual tone
'''
    response = model.generate_content(message_prompt)
    return response.text.strip()

# Streamlit App UI
st.title("Health & Well-being Message Generator 🌍❤️")

prompt = st.text_area("Enter a health problem or related topic:")

if st.button("Generate Message"):
    if prompt.strip():
        with st.spinner("Generating message..."):
            message = generate_health_message(prompt)
            st.success("Here's your message:")
            st.write(message)

            # Only show contact info if the problem is severe
            contacts = get_contact_info_if_severe(prompt)
            if contacts:
                st.markdown("---")
                st.warning("⚠️ Severe health condition detected. Please consider contacting the following helplines:")
                for contact in contacts:
                    st.write(f"- {contact}")
    else:
        st.warning("Please enter a prompt first.")

