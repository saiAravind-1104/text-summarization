# Text Summarization App 🔍📄

A Streamlit-based web application that generates concise summaries from web URLs and YouTube videos using LangChain and Groq's LLaMA model.

## Features

- 📝 Summarize content from any web URL
- 🎥 Extract and summarize YouTube video transcripts
- 🤖 Powered by Groq's LLaMA 3.1 model
- 🎯 Generates focused 200-word summaries
- 🔒 Secure API key handling
- ⚡ Fast dependency management with `uv`

## Prerequisites

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) package manager
- Groq API key ([Get it here](https://console.groq.com))

## Installation

### 1. Install uv (if not already installed)

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or via pip
pip install uv
```

### 2. Clone the repository

```bash
git clone <your-repo-url>
cd <your-repo-name>
```

### 3. Install dependencies using uv

```bash
# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install all dependencies
uv pip install streamlit python-dotenv validators langchain langchain-groq langchain-community youtube-transcript-api unstructured
```

### 4. Set up environment (optional)

```bash
# Create a .env file for storing your API key
echo "GROQ_API_KEY=your_api_key_here" > .env
```

## Project Structure

```
.
├── src\app.py                 # Main application file
├── pyproject.toml         # Project configuration and dependencies
├── .env                   # Environment variables (optional)
└── README.md              # This file
```


## Usage

### 1. Run the application

```bash
# Activate virtual environment
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Run the app
streamlit run app.py
```

### 2. In the web interface

1. Enter your **Groq API key** in the sidebar (password field)
2. Paste a **URL** in the input field:
   - Web article URL (e.g., news, blog, documentation)
   - YouTube video URL (e.g., `https://youtube.com/watch?v=...`)
3. Click **"Summarize"** button
4. Wait for processing (spinner will indicate progress)
5. View the generated 200-word summary

## How It Works

### Architecture

1. **Input Validation**
   - Validates the provided URL format using the `validators` library
   - Checks for Groq API key presence

2. **Content Loading**
   - **YouTube URLs**: Uses `YoutubeLoader` to extract video transcripts
   - **Web URLs**: Uses `UnstructuredURLLoader` to scrape and parse web content

3. **LLM Summarization**
   - Initializes ChatGroq with LLaMA 3.1 8B Instant model
   - Uses LangChain's `load_summarize_chain` with "stuff" strategy
   - Applies custom prompt template for 200-word summaries

4. **Display Results**
   - Shows success message with generated summary
   - Displays errors for invalid inputs or processing failures

### Components Breakdown

```python
# LLM Configuration
llm = ChatGroq(
    api_key=st.session_state.key,
    model_name="llama-3.1-8b-instant"  # Fast, efficient model
)

# Summarization Chain
chain = load_summarize_chain(
    llm=llm,
    chain_type="stuff",  # Passes all docs at once
    prompt=prompt        # Custom 200-word summary template
)
```

## Configuration

### Model Settings
- **LLM Provider**: Groq
- **Model**: `llama-3.1-8b-instant`
- **Chain Type**: `stuff` (best for single-document summarization)
- **Summary Length**: ~200 words

### Customization

**Adjust summary length or style:**
```python
template = '''
Summarize this text and give a 200-word response:

{text}
'''
```

You can modify:
- Word count (change "200-word")
- Style (add "in bullet points", "technical summary", etc.)
- Language (add "in Spanish", "in Hindi", etc.)

## Supported URL Types

| Type | Example | Notes |
|------|---------|-------|
| ✅ YouTube | `youtube.com/watch?v=...` | Requires transcript availability |
| ✅ News Articles | `nytimes.com/article/...` | Most news sites supported |
| ✅ Blogs | `medium.com/@user/post` | Works with most blogging platforms |
| ✅ Documentation | `docs.python.org/...` | Technical documentation pages |
| ✅ Wikipedia | `en.wikipedia.org/wiki/...` | All Wikipedia articles |

## Error Handling

The app handles various error scenarios:

| Error | Cause | Solution |
|-------|-------|----------|
| "Please enter Groq key and URL" | Missing API key or URL | Provide both inputs |
| "Please provide a valid URL" | Invalid URL format | Check URL format (must include http/https) |
| "Unable to extract content" | Content loading failed | Try different URL or check internet connection |

## Development

### Using uv for dependency management

```bash
# Add a new dependency
uv pip install <package-name>

# Update dependencies
uv pip install --upgrade <package-name>

# Freeze dependencies
uv pip freeze > requirements.txt

# Sync dependencies from pyproject.toml
uv pip sync
```

### Running in development mode

```bash
# With auto-reload
streamlit run app.py --server.runOnSave true
```

## Security Best Practices

- ✅ API keys stored in session state (not logged)
- ✅ Password-type input for API key (not visible)
- ⚠️ SSL verification disabled (consider enabling for production)
- ✅ No API key stored in code or version control

**Recommendation**: Use `.env` file for API key storage:

```bash
# .env file
GROQ_API_KEY=your_actual_api_key_here
```

```python
# In app.py
load_dotenv()
default_key = os.getenv("GROQ_API_KEY", "")
```

## Future Enhancements

- [ ] Support for multiple URLs in batch
- [ ] Adjustable summary length slider
- [ ] Export summaries (PDF, TXT, Markdown)
- [ ] Support for local file uploads (PDF, DOCX, TXT)
- [ ] Multi-language summary support
- [ ] Token usage tracking and cost estimation
- [ ] Summary history and session management
- [ ] Support for other LLM providers (OpenAI, Anthropic)
- [ ] Advanced summarization strategies (map-reduce, refine)

## Troubleshooting

### Common Issues

**1. ModuleNotFoundError**
```bash
# Reinstall dependencies
uv pip install -r requirements.txt
```

**2. Streamlit import errors**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate
```

**3. YouTube loader fails**
```bash
# Install youtube-transcript-api separately
uv pip install --upgrade youtube-transcript-api
```

**4. Groq API errors**
- Check API key validity
- Verify internet connection
- Check Groq service status

## Performance

- **Average processing time**: 3-10 seconds (depends on content length)
- **Model latency**: ~1-2 seconds (Groq's LLaMA 3.1 is optimized for speed)
- **Supported content length**: Up to ~8K tokens (model context limit)


## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Author

K. Sai Aravind

## Acknowledgments

- **LangChain** - Framework for LLM applications
- **Groq** - Fast LLM inference platform
- **Streamlit** - Web app framework
- **uv** - Fast Python package manager by Astral

---

**Made with ❤️ using LangChain, Streamlit, and uv**

## Quick Start

```bash
# Complete setup in 3 commands
uv venv && source .venv/bin/activate
uv pip install streamlit python-dotenv validators langchain langchain-groq langchain-community youtube-transcript-api unstructured
streamlit run app.py
```