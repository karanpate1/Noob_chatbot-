import os
from dotenv import load_dotenv

# Point to your .env file
env_path = "/content/drive/MyDrive/LLM/.env"

load_dotenv(dotenv_path=env_path)

# Test: print a variable
GEMINI_KEY=os.getenv("GEMINI_KEY")

import os
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from IPython.display import Markdown, display
import json
import gradio as gr

clients=genai.Client(api_key=GEMINI_KEY)

system_instruction = """
You are a sales assistant for "Karan Mobile Store" specializing in mobile phones. 
your name is Karan-Ai.
**Products Available:**
📱 Samsung Galaxy S25 Ultra: ₹129,999
📱 Apple iPhone 16 Pro Max: ₹159,999  
📱 OnePlus 13R: ₹42,999
📱 Xiaomi Redmi Note 14 Pro+: ₹28,499
📱 Realme GT Neo 6: ₹31,999
📱 Google Pixel 9 Pro: ₹98,999
📱 Motorola Moto Edge 50 Fusion: ₹34,999
📱 Vivo X120 Pro: ₹67,999
📱 Oppo Find X7: ₹74,999
📱 Nothing Phone 3: ₹49,999

**Guidelines:**
1. Greet warmly and ask about budget/brand preference
2. Recommend phones based on customer needs
3. We ONLY sell mobiles - politely redirect other requests
4. Offer 10% discount when customer selects a model: "Special 10% offer for you! 🎉"
5. Be helpful, professional and use Indian price formatting

Focus on understanding needs and providing the best mobile solution! 😊
"""

def chat(message,history):
  messages=[]
  for user_message,assistant_message in history:
    messages.append({"role":"user","parts":[{"text":user_message}]})
    messages.append({"role":"model","parts":[{"text":assistant_message}]})
  messages.append({"role":"user","parts":[{"text":message}]})
  # system_instruction="you are healpful assistant of a mobile store called 'Tushar mobile'. we have following products {(Samsung, Galaxy S25 Ultra, 129999), (Apple, iPhone 16 Pro Max, 159999), (OnePlus, OnePlus 13R, 42999), (Xiaomi, Redmi Note 14 Pro+, 28499), (Realme, Realme GT Neo 6, 31999), (Google, Pixel 9 Pro, 98999), (Motorola, Moto Edge 50 Fusion, 34999), (Vivo, Vivo X120 Pro, 67999), (Oppo, Oppo Find X7, 74999), (Nothing, Nothing Phone 3, 49999)},all price are in rupees , first of ask customer about budget or specif brand he or she ois looking for, we only sales mobile so if customer ask for any other product replay as we only sales mobile , if customer select any model to buy tell them we have special 10% offer for you."
  
  response = clients.models.generate_content(
      model="gemini-2.5-flash", contents=messages,
      config=types.GenerateContentConfig(
          system_instruction=system_instruction,
          temperature=1
          ),
  )

  # message.append({"role":"model","parts":{"text":response.last}})
  return response.text

gr.ChatInterface(fn=chat,title="Karan mobile").launch(debug=True)