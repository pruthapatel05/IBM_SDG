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
You are a social media content expert focused on Sustainable Development Goal 3 (Good Health and Well-being). 
Using the health problem or topic described here: "{prompt_text}", craft a **short, catchy, and friendly social media message** (max 250 characters) that:

- Grabs attention immediately
- Uses clear, simple, and positive language
- Includes 1 to 3 relevant, trending hashtags (related to health, well-being, or SDG3)
- May include 1 or 2 emojis to add warmth and friendliness
- Encourages awareness or action in a motivational tone

Example style:  
"Breathe easy! Clean air = healthy lungs. Let's fight air pollution for better respiratory health. Join the movement! #CleanAir #HealthyLungs #SDG3"

Create a message like that.
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
                st.success("Here's your social media message:")
                st.write(message)
                st.markdown("---")
                st.info("💡 **Tip:** If you feel your situation is urgent, please call emergency services immediately.")
    else:
        st.warning("Please enter a prompt first.")
