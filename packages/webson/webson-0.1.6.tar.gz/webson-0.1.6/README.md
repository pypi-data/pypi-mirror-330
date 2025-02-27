# Webson 🕸️

**Turn any webpage into structured outputs!** ⚡️  
*Extract data from any website with the power of AI.*

---

## ✨ Overview

Webson is a cutting-edge tool that transforms webpages into structured data models — all with just a few lines of code. No more manual scraping or complex parsers! With Webson, you can effortlessly convert HTML into meaningful, actionable insights using state-of-the-art Language Models (LLMs) from IntelliBricks and robust automation powered by Playwright.

---

## 🎯 Key Features

- **🦾 Intelligent Data Extraction:**  
  Convert webpages into structured data using your own defined models.  
  *(Say goodbye to messy HTML!)*

- **💬 Chat Casting:**  
  Simply tell Webson what you need in plain language, and it will extract and structure the data for you.  
  *(Example: "Extract product details from https://amazon.com and shopee.com including title, price, and rating.")*

- **⚡️ Seamless Integration:**  
  Built on top of [IntelliBricks](https://arthurbrenno.github.io/intellibricks/) and [Playwright](https://playwright.dev/python/docs/intro) — enjoy a Python-first approach without the boilerplate.

- **📊 Structured Outputs:**  
  Define your output schemas with `msgspec.Struct` and get data back in a ready-to-use, strongly typed format.

---

## 🚀 Installation

Install Webson and its dependencies via pip:

```bash
pip install webson
```

**Important:** Webson relies on [Playwright](https://playwright.dev/python/docs/intro) for web automation. This happens because we all know that many pages rely on things that only happen in a browser, like loading stripts, styles, etc. Follow these steps to install Playwright and its browser dependencies:

1. **Install Playwright:**

    ```bash
    pip install playwright
    ```

2. **Install Browser Binaries:**

    ```bash
    playwright install
    ```

Now you’re all set to transform any webpage into structured intelligence!

---

## 🔧 Usage Examples

### 1. Casting a Webpage into a Structured Model

Define your own data model and cast a webpage’s content into it:

```python
import msgspec
from intellibricks.llms import Synapse
from webson import Webson
from typing import Annotated

# Define your desired structured model
class PageSummary(msgspec.Struct):
    title: str
    summary: Annotated[
      str,
      msgspec.Meta(
        description="A short summary of the page")
    ]

# Initialize your LLM (using IntelliBricks Synapse) and Webson
llm = Synapse.of("google/genai/gemini-pro-experimental")
webson = Webson(llm=llm, timeout=5000)

# Cast the webpage content into your structured model
structured_data = webson.cast(PageSummary, "https://example.com")
print(f"Title: {structured_data.title}")
print(f"Content: {structured_data.summary}")
```

### 2. High-Level Query to Struct

Simply describe what you need and let Webson do the heavy lifting:

```python
from intellibricks.llms import Synapse
from webson import Webson

# Initialize your LLM and Webson instance
llm = Synapse.of("google/genai/gemini-pro-experimental")
webson = Webson(llm=llm, timeout=5000)

# Use natural language to instruct Webson on what data to extract
results = webson.query_to_struct(
    "Extract product info from https://amazon.com and https://www.walmart.com/ including title, price, and rating."
)
for url, output in results:
    print(url, output)
```

---

## ⚙️ How It Works

1. **Webpage Automation:**  
   Webson uses Playwright to open webpages in a headless browser and retrieve the HTML content.

2. **Markdown Conversion:**  
   The raw HTML is converted into Markdown for improved text processing and parsing.

3. **LLM-Powered Casting:**  
   The transformed Markdown is sent to your LLM (via IntelliBricks) which then returns structured data based on your specified schema.

---

## 🤝 Contributing

We welcome contributions to make Webson even more awesome!  
If you encounter any issues or have ideas for new features, please open an issue or submit a pull request on our [GitHub repository](https://github.com/your-repo/webson).

---

## 📜 License

This project is licensed under the [APACHE 2.0 License](LICENSE).

---
