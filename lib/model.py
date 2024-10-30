from mistralai import Mistral
import config

api_key = config.api_key

class ModelWrapper():
    def __init__(self):
        self.model = "mistral-large-latest"
        self.client = Mistral(api_key=api_key)
        # self.history: List[dict[str, str]] = []]
        self.history = []

    def get_response(self, request, clear_context=False):
        if clear_context:
            self.reset_context()

        self.history.append({
            "role": "user",
            "content": request,
        })

        print("Send request...")
        chat_response = self.client.chat.complete(
            model = self.model,
            messages = self.history
        )

        message = chat_response.choices[0].message

        # print(f"Response message: {message}")

        self.history.append({
            "role": message.role, # assistant
            "content": message.content,
        })

        return message.content

    def reset_context(self):
        self.history = []


class ExtendedModelWrapper(ModelWrapper):
    def __init__(self):
        super().__init__()

    def enrich(self, filename) -> str:
        with open(filename, 'r', encoding="cp1251", errors='ignore') as f:
            text = f.read()
            print("First lines: ", text.split('\n')[:10])
            text = text[:100000]
            request = "Изучи, пожалуйста, следующую биографию. \n" + text
            return self.get_response(request, clear_context=True)
