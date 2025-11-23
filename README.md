# 🤖 Multi-Modal AI Chatbot

A sleek, dark-themed chatbot powered by Google Gemini AI that supports both text and image inputs.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.29+-red.svg)

## ✨ Features

- 💬 Text conversations with AI
- 🖼️ Image analysis and understanding
- 🔄 Combined text + image inputs
- 🎨 Beautiful dark theme UI
- ⚙️ Customizable settings (temperature, models)
- 💾 Session chat history

## 🚀 Quick Start

### Installation

```bash
# Clone the repo
git clone https://github.com/jaysharamesh11-commits/Multimodel-chatbot
cd multimodal-chatbot

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

### Requirements

```txt
streamlit==1.29.0
google-generativeai==0.3.2
pillow==10.1.0
python-dotenv==1.0.0
```

### Setup

1. Get your API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Enter it in the sidebar when you run the app
3. Start chatting!

## 🎮 Usage

- **Text only**: Type your message and send
- **Image only**: Upload an image for analysis
- **Combined**: Upload image + add text for context

## 🛠️ Available Models

- `gemini-2.5-flash` - ⚡ Fastest
- `gemini-2.5-pro` - 🧠 Most powerful
- `gemini-flash-latest` - 🔄 Latest version

## 🐛 Troubleshooting

**API Key Error**: Verify your key at [Google AI Studio](https://makersuite.google.com/app/apikey)

**Model Not Found**: Use the "Check Available Models" button in sidebar

**Image Too Large**: Keep images under 4MB

## 📝 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

Built with [Google Gemini AI](https://deepmind.google/technologies/gemini/) and [Streamlit](https://streamlit.io/)

---

⭐ Star this repo if you find it helpful!