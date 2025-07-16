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

def is_emergency(text):
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in emergency_keywords)

def sdg3_message_generator(prompt_text):
    message_prompt = (
        f'''
You are a healthcare communication expert. Using the health problem or topic described here: "{prompt_text}", 
write a clear, professional, and empathetic paragraph that:

- Explains the health issue briefly
- Highlights its importance or impact
- Offers practical advice or encouragement
- Uses formal, respectful language appropriate for a medical or health context
- Avoids hashtags, emojis, and casual social media style

The goal is to inform and support the reader with accurate, trustworthy information.
'''
    )
    response = model.generate_content(message_prompt)
    return response.text.strip()

# Streamlit app UI
st.title("Health & Well-being Message Generator 🌍❤️")

prompt = st.text_area("Enter a health problem or SDG 3 topic:")

if st.button("Generate Message"):
    if prompt.strip():
        if is_emergency(prompt):
            st.error("⚠️ Emergency detected! Please call 108 immediately!")
            st.markdown("[📞 Call 108 Now](tel:108)", unsafe_allow_html=True)
        else:
            with st.spinner("Generating message..."):
                message = sdg3_message_generator(prompt)
                st.success("Here's your message:")
                st.write(message)
                st.markdown("---")
                st.info("💡 **Tip:** If you feel your situation is urgent, please call emergency services immediately.")
    else:
        st.warning("Please enter a prompt first.")
