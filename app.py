import streamlit as st
import google.generativeai as genai

# Load API key securely using Streamlit Secrets
api_key = st.secrets["general"]["api_key"]

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# Emergency keywords list
emergency_keywords = [
    "emergency", "heart attack", "accident", "unconscious",
    "severe bleeding", "stroke", "choking", "collapse", "loss of consciousness"
]

# Severe problem keywords list (broader)
severe_keywords = [
    "severe", "critical", "urgent", "life-threatening", "extreme", "intense"
]

def is_emergency(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in emergency_keywords)

def is_severe_problem(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in severe_keywords)

def get_contact_info(text):
    text_lower = text.lower()
    contacts = []

    if any(word in text_lower for word in ["mental health", "depression", "anxiety", "suicide", "stress"]):
        contacts.append("Mental Health Helpline: 100")
    if any(word in text_lower for word in ["women", "pregnancy", "maternal"]):
        contacts.append("Women’s Health Helpline: 101")
    if any(word in text_lower for word in ["child", "pediatric", "newborn"]):
        contacts.append("Child Health Helpline: 102")
    if any(word in text_lower for word in ["elderly", "senior", "old age"]):
        contacts.append("Elderly Care Helpline: 104")
    if any(word in text_lower for word in ["diabetes", "blood sugar"]):
        contacts.append("Diabetes Support Helpline: 105")
    if any(word in text_lower for word in ["tuberculosis", "tb"]):
        contacts.append("TB Helpline: 106")
    if any(word in text_lower for word in ["covid", "coronavirus", "pandemic"]):
        contacts.append("COVID-19 Helpline: 107")

    # General health helpline as default suggestion
    if not contacts:
        contacts.append("General Health Helpline: 103")

    return contacts

def sdg3_message_generator(prompt_text):
    message_prompt = (
        f'''
You are a healthcare communication expert. Using the health problem or topic described here: "{prompt_text}", 
write a concise and clear health message in 2-3 sentences that:

- Briefly explains the issue
- Offers simple advice or encouragement
- Uses professional and empathetic language
- Avoids hashtags, emojis, and casual tone

Keep the message informative and supportive.
'''
    )
    response = model.generate_content(message_prompt)
    return response.text.strip()

# Streamlit app UI
st.title("Health & Well-being Message Generator 🌍❤️")

prompt = st.text_area("Enter a health problem or related topic:")

if st.button("Generate Message"):
    if prompt.strip():
        if is_emergency(prompt):
            st.error("⚠️ Emergency detected! Please call 108 immediately!")
            st.markdown("[📞 Call 108 Now](tel:108)", unsafe_allow_html=True)
        elif is_severe_problem(prompt):
            st.warning("⚠️ Severe health issue detected. Please consider contacting emergency services at 108.")
            contacts = get_contact_info(prompt)
            st.markdown("---")
            st.info("You may find the following contact numbers helpful:")
            for contact in contacts:
                st.write(f"- {contact}")
        else:
            with st.spinner("Generating message..."):
                message = sdg3_message_generator(prompt)
                st.success("Here's your message:")
                st.write(message)

                contacts = get_contact_info(prompt)
                if contacts:
                    st.markdown("---")
                    st.info("You may find the following contact numbers helpful:")
                    for contact in contacts:
                        st.write(f"- {contact}")

                st.markdown("---")
                st.info("💡 **Tip:** If you feel your situation is urgent, please call emergency services immediately.")
    else:
        st.warning("Please enter a prompt first.")

