![Alt text](logo.png)
-----

# Gennaro - Your AI Shopping Assistant 🛒

Meet **Gennaro**, a friendly and intelligent conversational AI designed to enhance your e-commerce experience. Gennaro acts as your personal shopping assistant, helping you find products, discover similar items, and manage your shopping cart with ease, all through a natural chat interface.

This project demonstrates how to build a powerful AI agent using a Large Language Model (LLM) with custom tools for a specific domain, like e-commerce.

## ✨ Features

  * **🗣️ Natural Conversation:** Interact with Gennaro using everyday language.
  * **🔍 Smart Product Search:** Describe what you're looking for, and Gennaro will find similar items from the product catalog.
  * **🛒 Effortless Cart Management:** Add or remove items from your cart with simple commands.
  * **🤖 LLM-Powered:** Utilizes the OpenAI API (`gpt-4o-mini`) for intelligent conversation and tool usage.
  * **🚀 Vector Search:** Employs a **ChromaDB** vector database for fast and accurate similarity searches.
  * **💻 Rich CLI:** A beautiful and user-friendly command-line interface powered by the `rich` library.

-----

## ⚙️ How It Works

Gennaro leverages a Large Language Model to understand user requests. The core logic is built around an agentic workflow where the LLM can decide to call external tools to fulfill a request.

1.  **User Interaction:** You chat with Gennaro through the command-line interface.
2.  **LLM Interpretation:** The model processes your request, understands your intent, and maintains the context of the conversation.
3.  **Tool Invocation:** When you ask to find a product or modify the cart, the LLM intelligently decides to call one of the available custom Python functions:
      * `get_similar_items`: This tool queries a **ChromaDB** vector database. It takes your text description, converts it into a vector embedding using the OpenAI API, and performs a similarity search to find the closest matching products in the catalog.
      * `manage_shopping_cart`: This tool directly modifies the state of your shopping cart by adding or removing specified items.
4.  **Response Generation:** The result from the tool is sent back to the LLM, which then formulates a friendly, human-readable response.

This cycle of `User -> LLM -> Tool -> LLM -> User` allows for a dynamic, responsive, and powerful interaction.

-----

## 🛠️ Technology Stack

  * **Language:** Python 3.x
  * **LLM & Embeddings:** [OpenAI API](https://platform.openai.com/) (`gpt-4o-mini`, `text-embedding-3-small`)
  * **Vector Database:** [ChromaDB](https://www.trychroma.com/)
  * **CLI:** [Rich](https://github.com/Textualize/rich)
  * **Environment Management:** `python-dotenv`

-----

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

### Prerequisites

  * Python 3.8+
  * An OpenAI API Key

### Installation

1.  **Clone the Repository**

    ```bash
    git clone https://github.com/your-username/gennaro-shopping-agent.git
    cd gennaro-shopping-agent
    ```

2.  **Create and Activate a Virtual Environment**

    ```bash
    # For macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # For Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Install Dependencies**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up Environment Variables**
    Create a `.env` file in the root directory by copying the example file.

    ```bash
    cp .env.example .env
    ```

    Open the `.env` file and add your OpenAI API key:

    ```
    OPENAI_API_KEY="sk-..."
    ```

5.  **Populate the Vector Database**
    Before you can search for items, you need to populate the ChromaDB database with your product catalog. *(Note: You will need to implement a script to embed your product data and add it to the collection defined in `vector_db.py`)*.

### Usage

To start chatting with Gennaro, simply run the main script:

```bash
python run.py
```

Gennaro will greet you, and you can start shopping\! To exit the application, type `quit`.

#### Example Interaction

```
$ python run.py
AI: Hello! I’m Gennaro — how can I help you build your cart today?
You: I am looking for a blue jacket for the winter
AI: Of course! Based on your description, I found this:
    Product: 'Warm Winter Puffer Jacket'
    Description: 'A stylish and warm blue puffer jacket, perfect for cold weather. Water-resistant and filled with premium insulation.'
    [An image of the jacket would be displayed here]
You: Great, add it to my cart
AI: You got it! I've added the "Warm Winter Puffer Jacket" to your cart. Is there anything else I can help you with?
You: remove it
AI: No problem, I have removed "Warm Winter Puffer Jacket" from your cart.
```

-----

## 📂 Project Structure

```
.
├── .env.example        # Example environment variables file
├── README.md           # This file
├── requirements.txt    # Python dependencies
├── prompts.py          # Contains the agent's system prompt
├── tools.py            # Defines the functions (tools) for the agent
├── vector_db.py        # Manages the ChromaDB vector database
└── run.py              # Main script to run the chat application
```

-----

