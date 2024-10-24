from fastapi import FastAPI
import pickle
import json
import random

app = FastAPI()

# Load the trained model and vectorizer
with open('model/chatbot_model.pkl', 'rb') as f:
    best_model = pickle.load(f)

with open('model/vectorizer.pkl', 'rb') as f:
    vectorizer = pickle.load(f)

# Load the intents data
with open('dataset/intents1.json', 'r') as f:
    intents = json.load(f)

def chatbot_response(user_input):
    input_text = vectorizer.transform([user_input])
    predicted_intent = best_model.predict(input_text)[0]

    for intent in intents['intents']:
        if intent['tag'] == predicted_intent:
            response = random.choice(intent['responses'])
            break

    return response

@app.get("/")
def home():
    return {"message": "Welcome to the Chatbot API"}

@app.post("/chat")
async def chat(user_input: str):
    response = chatbot_response(user_input)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
