import tkinter as tk
from tkinter import font as tkfont
from tkinter import messagebox
import openai
import google.generativeai as genai
import os
from meta_ai_api import MetaAI
import openai as openai
import anthropic  # Anthropic API import for Claude
from PIL import Image as InternalspilImage,ImageTk as InternalspilImageTk

class SoftwareInterpreter:
    def __init__(self, ai_type="meta", api_key=None, font="Arial", openai_maxtoken=250):
        self.ai_type = ai_type
        self.font = font
        self.api_key = api_key
        self.model = None  # Set model to None initially
        self.configure_ai()
        self.muted = False  # Initialize mute status
        self.openai_maxtoken = openai_maxtoken
        # List of available fonts
        self.fonts_list = self.get_installed_fonts()

    def configure_ai(self):
        if self.ai_type == "gemini":
            genai.configure(api_key=self.api_key)
            self.model = "gemini-1.5-flash"  # Default model for Gemini
        elif self.ai_type == "meta":
            self.meta_ai = MetaAI()
            self.model = "meta-ai-1.0"  # Default model for Meta AI
        elif self.ai_type == "chatgpt":
            openai.api_key = self.api_key
            self.model = "gpt-3.5-turbo"  # Default model for ChatGPT
        elif self.ai_type == "claude":
            self.claude = anthropic.Anthropic(api_key=self.api_key)
            self.model = "claude-3-7-sonnet-20250219"  # Default model for Claude
        else:
            raise ValueError("Unsupported AI type. Choose from 'gemini', 'meta', 'chatgpt', or 'claude'.")

    def get_installed_fonts(self):
        """Returns a list of all installed fonts on the system."""
        fonts = list(tkfont.families())
        return sorted(fonts)
    def search_font(self, search_term):
        """Searches for fonts that contain the search term and returns matching fonts."""
        matching_fonts = [font for font in self.fonts_list if search_term.lower() in font.lower()]
        return "\n".join(matching_fonts) if matching_fonts else f"No fonts found matching '{search_term}'."


    def get_response(self, prompt):
        if self.muted:
            return "The bot is muted. Please unmute to receive responses."
        
        if self.ai_type == "gemini":
            model = genai.GenerativeModel(self.model)
            response = model.generate_content(prompt)
            return response.text
        elif self.ai_type == "meta":
            response = self.meta_ai.prompt(message=prompt)
            return response['message']
        elif self.ai_type == "chatgpt":
            response = openai.Completion.create(
                model=self.model,  # Using self.model here
                prompt=prompt,
                max_tokens=self.openai_maxtoken
            )
            return response.choices[0].text.strip()
        elif self.ai_type == "claude":
            message = self.claude.messages.create(
                model=self.model,  # Using self.model here
                max_tokens=1024,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return message.content

    def toggle_mute(self):
        """Toggles the mute status."""
        self.muted = not self.muted
        return "Bot muted." if self.muted else "Bot unmuted."

    def change_font(self, font_name):
        """Change the font of the chat interface and update the GUI."""
        font_name = font_name.strip('"')
        
        if font_name in self.fonts_list:
            self.font = font_name
            return f"Font changed to {font_name}."
        else:
            return f"Font {font_name} is not available. Available fonts are: {', '.join(self.fonts_list)}"

    def set_api_key(self, api_key):
        """Sets a new API key and reconfigures the AI."""
        self.api_key = api_key
        self.configure_ai()  # Ensure the new API key is used
        return "API key updated successfully."

    def switch_bot(self, bot_type):
        """Switch between bots."""
        if bot_type in ["gemini", "meta", "chatgpt",  "claude"]:
            self.ai_type = bot_type
            self.configure_ai()
            return f"Switched to {bot_type} bot."
        else:
            return "Invalid bot type. Choose from 'gemini', 'meta', 'chatgpt', or 'claude'."

    def set_model(self, model_name):
        """Sets the AI model if it exists."""
        self.model = model_name
        return f"Model changed to {model_name}."

    def show_help(self):
        """Returns general help text."""
        return (
            "/mute - Mute or unmute the bot.\n"
            "/say <message> - Send a custom message without bot processing.\n"
            "/font <set/list/search> - Change, list, or search fonts.\n"
            "/apikey <API_KEY> - Set or view the current API key.\n"
            "/switch <bot_name> - Switch between 'gemini', 'meta', 'chatgpt', or 'claude' bots.\n"
            "/model <set> - Set AI model to the specified model.\n"
            "/help - Show this help message."
        )


class ChatbotApp:
    def __init__(self, root=None, title="ChatBotAi-GUI",icon=os.path.dirname(__file__) + "/defaulticon.png"):
        self.root = root or tk.Tk()  # If root is provided, use it; otherwise create a new Tk instance.
        self.title=title
        self.root.title(self.title)
        self.iconfile=icon
        self.icondata= InternalspilImage.open(self.iconfile)
        photo = InternalspilImageTk.PhotoImage(self.icondata)
        self.root.wm_iconphoto(False, photo)
        # Create the chat area and set it to be non-editable
        self.chat_area = tk.Text(self.root, state=tk.DISABLED, wrap=tk.WORD, height=20, width=50)
        self.chat_area.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)
        
        # Input field for user to type messages
        self.entry = tk.Entry(self.root, font=("Arial", 14))
        self.entry.pack(fill=tk.X, padx=10, pady=10)
        self.entry.bind("<Return>", self.send_message)
        
        self.chatbot = SoftwareInterpreter()

    def display_message(self, message, side="left"):
        """Displays the message in the chat area."""
        self.chat_area.config(state=tk.NORMAL)
        if side == "left":
            self.chat_area.insert(tk.END, f"Bot: {message}\n")
        else:
            self.chat_area.insert(tk.END, f"You: {message}\n")
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END)

    def send_message(self, event):
        """Handles sending the user's message and receiving the bot's response."""
        user_message = self.entry.get().strip()
        
        if user_message:  # Only send non-empty messages
            self.display_message(user_message, side="right")  # Show user's message
            
            # Check for special commands
            if user_message.startswith("/mute"):
                bot_response = self.chatbot.toggle_mute()
            elif user_message.startswith("/say"):
                bot_response = user_message[5:].strip() if len(user_message) > 5 else "Usage: /say <message>"
            elif user_message.startswith("/font set"):
                font_name = user_message[9:].strip()
                bot_response = self.chatbot.change_font(font_name)
                # Update the font in the input field and chat area after the font change
                self.entry.config(font=(self.chatbot.font, 14))
                self.chat_area.config(font=(self.chatbot.font, 14))
            elif user_message.startswith("/font list"):
                bot_response = "\n".join(self.chatbot.fonts_list)
            elif user_message.startswith("/font search"):
                search_term = user_message[13:].strip()
                bot_response = self.chatbot.search_font(search_term)
            elif user_message.startswith("/font"):
                bot_response = self.chatbot.show_font_help()
            elif user_message.startswith("/apikey"):
                new_api_key = user_message[8:].strip()
                if new_api_key:
                    bot_response = self.chatbot.set_api_key(new_api_key)
                else:
                    bot_response = f"Current API key: {self.chatbot.api_key if self.chatbot.api_key else 'Not set'}"
            elif user_message.startswith("/switch"):
                bot_type = user_message[8:].strip()
                bot_response = self.chatbot.switch_bot(bot_type)
            elif user_message.startswith("/model set"):
                model_name = user_message[10:].strip()
                bot_response = self.chatbot.set_model(model_name)
            elif user_message.startswith("/model"):
                bot_response = self.chatbot.show_help()
            elif user_message.startswith("/help"):
                bot_response = self.chatbot.show_help()
            else:
                bot_response = self.chatbot.get_response(user_message)  # Get bot response
            
            self.display_message(bot_response, side="left")  # Show bot's response
        
        self.entry.delete(0, tk.END)  # Clear the input field after sending the message

    def run(self):
        """Starts the tkinter GUI main loop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = ChatbotApp()
    app.run()
