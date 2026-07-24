import streamlit as st
import google.generativeai as genai
from PIL import Image

st.set_page_config(page_title="eFootball Rival Counter AI", page_icon="⚽", layout="centered")
st.title("⚽ eFootball Rival Counter AI (Gemini Edition)")
st.write("Upload your rival's formation screenshot to get instant tactical counters.")

# Automatically read the Gemini key from Streamlit Settings
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Please configure your GEMINI_API_KEY in the Streamlit Secrets settings.")
    st.stop()

uploaded_file = st.file_uploader("Upload Rival Formation Screenshot (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    with st.spinner("🧠 Gemini AI is analyzing rival formation and calculating counter-tactics..."):
        try:
            # Open the uploaded image file
            img = Image.open(uploaded_file)
            
            # Use the fast, powerful multimodal model
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = (
                "You are an elite eFootball Mobile tactical analyst. Your sole purpose is to "
                "look at this screenshot of an opponent's squad lineup, accurately extract their "
                "tactical configuration, and output an immediate, highly effective counter-strategy.\n\n"
                "Provide a 4-part tactical breakdown:\n\n"
                "1. **Rival Formation Identified**: State exactly what formation they are running (e.g., 4-2-2-2, 4-1-2-3) and their apparent Playstyle if visible (Quick Counter, Possession, Long Ball Counter, Out Wide).\n"
                "2. **Rival Weakness**: Pinpoint the exact space or positioning flaw exposed by their setup.\n"
                "3. **Your Counter-Formation**: Recommend the exact best meta formation to switch to in order to exploit their setup.\n"
                "4. **Actionable In-Game Adjustments**: Provide 3 quick mobile adjustments (e.g., individual player instructions or playstyle tips).\n\n"
                "Keep the output clean, highly actionable, and easy to read mid-game."
            )
            
            # Generate the tactical feedback
            response = model.generate_content([prompt, img])
            
            st.success("📊 Tactical Analysis Complete!")
            st.markdown(response.text)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
