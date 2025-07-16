# -*- coding: utf-8 -*-
import streamlit as st
import google.generativeai as genai

# Load API key securely using Streamlit Secrets
api_key = st.secrets["general"]["api_key"]

# Configure Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('models/gemini-1.5-flash')

def sdg3_message_generator(prompt_text):
    message_prompt = (
        f'''

You are a creative social media expert dedicated to highlighting critical health issues under SDG 3. Using the problem described here: {prompt_text}, craft a short, impactful social media message (up to 250 characters) that informs or motivates.

The message should:
    • Grab attention right away with a strong opening
    • Use a warm, relatable, and encouraging tone
    • Be brief but meaningful and impactful
    • Include 1 to 3 relevant, trending hashtags focused on health, well-being, or SDG 3

Keep the message genuine and powerful—avoid clichés and generic language. Make sure it educates, inspires, or drives awareness about the health challenge.
'''
    )

    response = model.generate_content(message_prompt)
    return response.text.strip()

# Streamlit app UI
st.title("SDG 3 Message Generator 🌍❤️")

prompt = st.text_area("Enter a health problem or SDG 3 topic:", "")

if st.button("Generate Message"):
    if prompt.strip():
        with st.spinner("Generating message..."):
            message = sdg3_message_generator(prompt)
            st.success("Here's your message:")
            st.write(message)
    else:
        st.warning("Please enter a prompt first.")
