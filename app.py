import streamlit as st
import openai
import base64

st.set_page_config(page_title="eFootball Rival Counter AI", page_icon="⚽", layout="centered")
st.title("⚽ eFootball Rival Counter AI")
st.write("Upload your rival's formation screenshot to get instant tactical counters.")

# Automatically read the secret key from Streamlit Settings
if "OPENAI_API_KEY" in st.secrets:
    openai.api_key = st.secrets["OPENAI_API_KEY"]
else:
    st.error("Please configure your OPENAI_API_KEY in the Streamlit Secrets settings.")
    st.stop()

def encode_image(uploaded_file):
    return base64.b64encode(uploaded_file.read()).decode("utf-8")

uploaded_file = st.file_uploader("Upload Rival Formation Screenshot (PNG/JPG)", type=["png", "jpg", "jpeg"])

if uploaded_file:
    with st.spinner("🧠 AI is analyzing rival formation and calculating counter-tactics..."):
        try:
            base64_image = encode_image(uploaded_file)
            
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an elite eFootball Mobile tactical analyst. Your sole purpose is to "
                            "look at a screenshot of an opponent's squad lineup, accurately extract their "
                            "tactical configuration, and output an immediate, highly effective counter-strategy."
                        )
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "content": (
                                    "Analyze this eFootball Mobile squad screenshot and provide a 4-part tactical breakdown:\n\n"
                                    "1. **Rival Formation Identified**: State exactly what formation they are running (e.g., 4-2-2-2, 4-1-2-3) and their apparent Playstyle if visible (Quick Counter, Possession, Long Ball Counter, Out Wide).\n"
                                    "2. **Rival Weakness**: Pinpoint the exact space or positioning flaw exposed by their setup.\n"
                                    "3. **Your Counter-Formation**: Recommend the exact best meta formation to switch to in order to exploit their setup.\n"
                                    "4. **Actionable In-Game Adjustments**: Provide 3 quick mobile adjustments (e.g., individual player instructions or playstyle tips).\n\n"
                                    "Keep the output clean, highly actionable, and easy to read mid-game."
                                )
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=600,
                temperature=0.3
            )
            
            st.success("📊 Tactical Analysis Complete!")
            st.markdown(response.choices.message.content)
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
