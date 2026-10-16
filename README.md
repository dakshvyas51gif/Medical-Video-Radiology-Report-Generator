# **🩺 AI Medical Video & Image Radiology Report Generator**

A Streamlit web app that uses Google's Gemini AI to generate **preliminary radiology reports** from medical images and videos. Upload a file, click a button, and get a structured report in seconds.

> ⚠️ **Medical Disclaimer:** This project is for educational and research purposes only. The generated reports are **not a medical diagnosis** and must always be reviewed and verified by a qualified radiologist or doctor. Do not use this tool for real clinical decisions.

---

## **✨ Features**

- 📁 Upload medical **images** (PNG, JPG, JPEG) or **videos** (MP4, AVI, MOV)
- 🎞️ Automatic video preview with duration and frame count
- 🖼️ Image preview with resolution details
- 🤖 AI-generated structured report powered by Gemini
- 📋 Report sections: Examination Type, Clinical Findings, Impression, Recommendations
- 🧹 Uploaded files are automatically deleted from Gemini servers after processing
- 🌐 Clean, simple web interface built with Streamlit

---

## **🛠️ Tech Stack**

| Technology | Purpose |
|------------|---------|
| Python 3.9+ | Programming language |
| Streamlit | Web user interface |
| Google GenAI SDK (`google-genai`) | Gemini API client |
| OpenCV (`opencv-python`) | Reading video/image metadata |
| python-dotenv | Loading the API key from `.env` |

---

## **📂 Project Structure**

```
radiology-report-generator/
│
├── app.py            # Main Streamlit application
├── .env              # Your secret API key (NOT uploaded to Git)
├── .gitignore        # Files Git should ignore
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
```

---

## **🚀 Getting Started**

### **1. Clone the repository**

```bash
git clone https://github.com/your-username/radiology-report-generator.git
cd radiology-report-generator
```

### **2. Create a virtual environment (recommended)**

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### **3. Install dependencies**

Create a `requirements.txt` file with the following content:

```
streamlit
google-genai
opencv-python
python-dotenv
```

Then run:

```bash
pip install -r requirements.txt
```

### **4. Get a Gemini API key**

1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in and create a new API key
3. Copy the key

### **5. Create the `.env` file**

In the project root, create a file named `.env` and add:

```
GOOGLE_API_KEY=your_api_key_here
```

> 🔒 Never share this key or commit it to GitHub. The included `.gitignore` already protects it.

### **6. Run the app**

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## **📖 How It Works**

1. **Upload** – The user uploads an image or video through the Streamlit file uploader.
2. **Temporary storage** – The file is saved to a temporary file on the local machine.
3. **Preview & metadata** – OpenCV reads the file to show resolution (images) or duration and frame count (videos).
4. **Upload to Gemini** – When the user clicks **Generate Radiology Report**, the file is uploaded using the Gemini Files API.
5. **Video processing** – For videos, the app waits until Gemini finishes processing the file (`PROCESSING` → `ACTIVE`).
6. **Report generation** – The file and a structured radiology prompt are sent to the Gemini model, which returns the report.
7. **Display** – The report is rendered in the app as formatted Markdown.
8. **Cleanup** – The file is deleted from Gemini servers and the local temporary file is removed.

---

## **📝 Sample Report Structure**

The AI is instructed to return the report in this format:

1. **Examination Type / Modality** – e.g., X-ray, CT, MRI, Ultrasound
2. **Clinical Findings / Observations** – What is visible in the image/video
3. **Impression / Conclusion** – Summary of the findings
4. **Recommendations** – Suggested follow-up and radiologist verification

The prompt also tells the model to describe **only visible findings** and **not to guess** unclear details.

---

## **⚙️ Configuration**

| Setting | Location | Description |
|---------|----------|-------------|
| `GOOGLE_API_KEY` | `.env` | Your Gemini API key |
| `model` | `app.py` → `generate_radiology_report()` | Gemini model name. Change it if the default is not available for your account |
| `prompt` | `app.py` → `generate_radiology_report()` | Edit this to change the report format or language |

---

## **🧯 Troubleshooting**

| Problem | Solution |
|---------|----------|
| `GOOGLE_API_KEY was not found` | Make sure the `.env` file exists in the same folder as `app.py` and contains the key |
| Model not found / 404 error | Update the model name in `app.py` to one available in your account |
| Video processing failed | Try a shorter video or a different format (MP4 recommended) |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` inside your virtual environment |
| Large file errors | Streamlit's default upload limit is 200 MB; use a smaller file |

---

## **🔐 Privacy & Security Notes**

- Do **not** upload real patient data containing personal information unless you have proper consent and comply with local regulations (e.g., HIPAA, GDPR).
- Files are sent to Google's Gemini API for analysis. Review Google's data policies before use.
- Keep your `.env` file private and never commit it.

---

## **🔮 Future Improvements**

- Download the report as a PDF
- Support for DICOM files
- Multi-language report output
- Report history and comparison
- Patient detail fields (age, symptoms) for better context

---

## **📄 License**

This project is released under the [MIT License](LICENSE). Feel free to use and modify it for learning purposes.

---

## **🤝 Contributing**

Contributions, issues, and feature requests are welcome! Fork the repo, create a branch, and open a pull request.

---

**Made with ❤️ using Streamlit and Google Gemini**
