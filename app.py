import streamlit as st
import os
import time
import tempfile
import cv2
from dotenv import load_dotenv
from google import genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

# 1. Page Configuration
st.set_page_config(
    page_title="AI Medical Report Generator",
    page_icon="🩺",
    layout="centered"
)

if not API_KEY:
    st.error("GOOGLE_API_KEY was not found in the .env file.")
    st.stop()

# 2. Initialize Gemini Client
client = genai.Client(api_key=API_KEY)

# 3. Report Generation Function
def generate_radiology_report(file_path, file_extension):
    uploaded_file = client.files.upload(file=file_path)

    try:
        if file_extension in [".mp4", ".avi", ".mov"]:
            while uploaded_file.state.name == "PROCESSING":
                time.sleep(2)
                uploaded_file = client.files.get(
                    name=uploaded_file.name
                )

            if uploaded_file.state.name == "FAILED":
                raise ValueError("Video processing failed.")

        prompt = """
        You are an expert radiology assistant.
        Create a preliminary report for the uploaded medical image or video.
        Respond only in English, using the following structure:

        1. Examination Type / Modality
        2. Clinical Findings / Observations
        3. Impression / Conclusion
        4. Recommendations

        Describe only the visible findings. Do not guess about unclear
        findings. Advise that the report be verified by a qualified
        radiologist.
        """

        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=[uploaded_file, prompt]
        )

        if not response.text:
            raise ValueError("Report could not be generated.")

        return response.text

    finally:
        client.files.delete(name=uploaded_file.name)


# 4. Streamlit User Interface
st.title("🩺 AI Medical Video & Image Radiology Report Generator")
st.write("Upload a medical image or video and get a preliminary report.")

uploaded_file = st.file_uploader(
    "Upload a medical file",
    type=["png", "jpg", "jpeg", "mp4", "avi", "mov"]
)

if uploaded_file is not None:
    ext = os.path.splitext(uploaded_file.name)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_file_path = tmp_file.name

    if ext in [".mp4", ".avi", ".mov"]:
        st.video(uploaded_file)

        cap = cv2.VideoCapture(tmp_file_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = frame_count / fps if fps > 0 else 0
        cap.release()

        st.info(
            f"📊 Duration: {duration:.2f} seconds | "
            f"Total Frames: {frame_count}"
        )

    elif ext in [".png", ".jpg", ".jpeg"]:
        st.image(uploaded_file, caption="Uploaded Medical Image",
                 use_container_width=True)

        img = cv2.imread(tmp_file_path)

        if img is not None:
            h, w = img.shape[:2]
            st.info(f"📊 Image Resolution: {w}x{h} pixels")
        else:
            st.error("Invalid image file.")

    if st.button("Generate Radiology Report"):
        try:
            with st.spinner("Analyzing the medical file... ⏳"):
                report = generate_radiology_report(tmp_file_path, ext)

            st.success("Preliminary report generated!")
            st.markdown("---")
            st.subheader("📋 Generated Radiology Report")
            st.markdown(report)

        except Exception as e:
            st.error(f"An error occurred: {e}")

        finally:
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)