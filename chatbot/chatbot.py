# chatbot.py
from dotenv import load_dotenv
import openai
import os
from kaggle_fetcher import KaggleDatasetFetcher

load_dotenv()

class AIChatbot:
    def __init__(self, kaggle_fetcher: KaggleDatasetFetcher, openai_api_key=None):
        self.fetcher = kaggle_fetcher
        openai.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

    def handle_message(self, message: str) -> str:
        # Basic routing
        if "dataset" in message.lower():
            return self._handle_dataset_request(message)
        return self._respond_with_gpt(message)

    def _handle_dataset_request(self, message: str) -> str:
        topic = self._extract_topic_with_gpt(message)
        if not topic:
            return "❌ Sorry, I couldn't understand your dataset request."

        datasets = self.fetcher.search_datasets(topic)
        if not datasets or "error" in datasets[0]:
            return f"❌ Couldn't find datasets for '{topic}'. Try a simpler keyword."

        response = f"🔍 Found datasets for **{topic}**:\n\n"
        for d in datasets:
            response += f"- **{d['title']}** (`{d['ref']}`)\n"
        response += "\nUse the full reference (e.g. `zynicide/wine-reviews`) to download."

        return response

    def _extract_topic_with_gpt(self, prompt: str) -> str:
        system_msg = "Extract a short search keyword from user input about datasets. Only return the keyword."
        try:
            result = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ]
            )
            return result.choices[0].message.content.strip().lower()
        except Exception as e:
            return None

    def _respond_with_gpt(self, prompt: str) -> str:
        system_msg = "You're a helpful AI tutor for beginner data scientists. Respond clearly and briefly."

        try:
            result = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": prompt}
                ]
            )
            return result.choices[0].message.content.strip()
        except Exception as e:
            return f"❌ GPT error: {str(e)}"
