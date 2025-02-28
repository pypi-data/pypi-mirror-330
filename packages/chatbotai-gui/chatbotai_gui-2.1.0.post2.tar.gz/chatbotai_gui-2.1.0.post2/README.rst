ChatbotAI-GUI
=============

**ChatbotAI-GUI** is a graphical user interface (GUI) chatbot that integrates multiple AI models, including OpenAI, Meta AI, Google Generative AI, and Anthropic Claude. This package allows users to interact with different AI models seamlessly through a single application.

✨ Features
------------
- Supports **OpenAI**, **Meta AI API**, **Google Generative AI**, and **Anthropic Claude**.
- Simple and intuitive GUI for easy interaction.
- Extensible and customizable for different chatbot implementations.

📦 Installation
----------------
Install the package using:

.. code-block:: sh

    pip install chatbotai-gui

🚀 Usage
---------
After installation, you can launch the chatbot GUI using:

.. code-block:: sh

    python -m chatai

Or in a Python script:

.. code-block:: python

    from chatai.chatbotgui import ChatbotApp

    app = ChatbotApp()
    app.run()

📝 Configuration
----------------
The chatbot uses a software interpreter to process API keys and select the AI model on launch.
You can also configure the application's title and icon using the `ChatbotApp` class.

After launching the GUI, you can use the `/help` command to see available commands.

Example configuration:

.. code-block:: python

    from chatai.chatbotgui import ChatbotApp, SoftwareInterpreter

    app = ChatbotApp(title="ExampleTitle", icon="icon.png")
    app.chatbot = SoftwareInterpreter(
        api_key="YOUR_API_KEY_HERE",
        ai_type="GEMINI",  # Choose from "GEMINI", "CHATGPT", "META", or "Claude"
        font="Arial",
        openai_maxtoken=250,
    )
    app.run()

🛠 Commands
------------
Here are the available commands:

.. code-block:: text

    /mute - Mute or unmute the bot.
    /say <message> - Send a custom message without bot processing.
    /font <set/list/search> - Change, list, or search fonts.
    /apikey <API_KEY> - Set or view the current API key.
    /switch <bot_name> - Switch between 'gemini', 'meta', 'chatgpt', or 'claude'.
    /model <set> - Set the AI model to the specified model.
    /help - Show this help message.

⚙️ Advanced Configuration
-------------------------
For advanced users, replacing the root window is allowed:

.. code-block:: python

    import tkinter as tk
    app = ChatbotApp(root=tk.Tk())
    app.run()

📜 License
-----------
This project is licensed under **AGPL-3.0-or-later**. See the `LICENSE` file for more details.
