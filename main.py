# main.py

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
import openai
import pyttsx3
import speech_recognition as sr

# Set your OpenAI GPT-3 API key
# openai.api_key = "YOUR_API_KEY"
openai.api_key = "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"

class VirtualAssistantApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.text_input = TextInput()
        self.conversation_log = TextInput(readonly=True, multiline=True)
        self.start_button = Button(text="Start Conversation", on_press=self.start_conversation)
        self.stop_button = Button(text="Stop Conversation", on_press=self.stop_conversation)
        self.listen_button = Button(text="Listen", on_press=self.listen_and_reply)
        self.layout.add_widget(self.conversation_log)
        self.layout.add_widget(self.text_input)
        self.layout.add_widget(self.start_button)
        self.layout.add_widget(self.stop_button)
        self.layout.add_widget(self.listen_button)
        return self.layout

    def start_conversation(self, instance):
        # Reset the conversation log
        self.conversation_log.text = "Virtual Assistant: How can I assist you today?\n"
    
    def stop_conversation(self, instance):
        self.conversation_log.text += "Conversation stopped.\n"

    def on_text_input(self, instance, value):
        user_input = value.strip()
        if user_input:
            # Send user input to the GPT-3 model
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=f"User: {user_input}\nVirtual Assistant:",
                max_tokens=50  # Adjust as needed
            )
            assistant_reply = response.choices[0].text.strip()
            self.conversation_log.text += f"User: {user_input}\nVirtual Assistant: {assistant_reply}\n"
            self.text_input.text = ""

    def listen_and_reply(self, instance):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            audio = recognizer.listen(source)
            print("Recognizing...")
            try:
                user_input = recognizer.recognize_google(audio)
                self.conversation_log.text += f"User (voice): {user_input}\n"
                self.on_text_input(self.text_input, user_input)
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")

if __name__ == "__main__":
    VirtualAssistantApp().run()
