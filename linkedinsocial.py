import streamlit as st
import google.generativeai as genai
from PIL import Image
import io
import base64

# --- Configure Gemini API Key ---
GEMINI_API_KEY = "AIzaSyCqYb76ycquiCbVQM1pbWsNrc-S-ueA2q8"  # Replace with your actual key
genai.configure(api_key=GEMINI_API_KEY)

# --- App UI ---
st.set_page_config(page_title="🔗 LinkedIn Post Generator", layout="centered")
st.title("🔗 AI LinkedIn Post Generator with Image")

st.markdown("""
Enter your topic or content, upload an image (optional), select a style and tone, and generate a LinkedIn-ready post.
""")

# --- Input Fields ---
input_text = st.text_area("✍️ What's your post about?", height=150)
uploaded_image = st.file_uploader("📷 Upload an image (optional)", type=["jpg", "jpeg", "png"])

# --- Format & Tone Selectors ---
col1, col2 = st.columns(2)
with col1:
    format_choice = st.selectbox("🧾 Post Format", ["Professional", "Motivational", "Storytelling", "Promotional"])
with col2:
    tone_choice = st.selectbox("🎭 Post Tone", ["Inspirational", "Confident", "Friendly", "Formal", "Neutral"])

# --- Session State for Results ---
if "linkedin_text" not in st.session_state:
    st.session_state.linkedin_text = ""
if "generated_image" not in st.session_state:
    st.session_state.generated_image = None

# --- Generate Text from Gemini ---
def generate_post_text(context, format_type, tone_type):
    prompt = f"""
You are a LinkedIn content assistant.
Write a LinkedIn post based on the following details:

Context: {context}
Format: {format_type}
Tone: {tone_type}

Keep it concise and engaging (about 100–150 words). Exclude hashtags and emojis.
"""
    model = genai.GenerativeModel("gemini-2.0-flash")
    response = model.generate_content(prompt)
    return response.text.strip()

# --- Generate Image Caption or Prompt (Optional) ---
def generate_image_from_text(text):
    # This function would ideally generate image prompts or captions
    # Placeholder for real image generation (e.g., if using Gemini multimodal)
    return f"Generate an image representing: {text[:80]}..."

# --- Convert PIL to Downloadable Bytes ---
def image_to_bytes(img: Image.Image):
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

# --- Generate Post Button ---
if st.button("🚀 Generate LinkedIn Post"):
    if not input_text.strip():
        st.warning("Please enter some text for your LinkedIn post.")
    else:
        st.session_state.linkedin_text = generate_post_text(input_text, format_choice, tone_choice)

        if uploaded_image:
            image = Image.open(uploaded_image).convert("RGB")
            st.session_state.generated_image = image
        else:
            # Placeholder: Simulate an image (if no upload)
            st.session_state.generated_image = Image.new("RGB", (512, 512), color="lightgray")

# --- Show Results ---
if st.session_state.linkedin_text:
    st.subheader("📢 Generated LinkedIn Post")
    st.text_area("Your AI Post", st.session_state.linkedin_text, height=200)

    st.subheader("🖼️ Associated Image")
    st.image(st.session_state.generated_image, caption="Generated/Uploaded Image", use_column_width=True)

    # Download button
    img_bytes = image_to_bytes(st.session_state.generated_image)
    st.download_button(
        label="📥 Download Image",
        data=img_bytes,
        file_name="linkedin_image.png",
        mime="image/png"
    )

    # Regenerate
    if st.button("🔁 Regenerate with New Format & Tone"):
        st.session_state.linkedin_text = generate_post_text(input_text, format_choice, tone_choice)

