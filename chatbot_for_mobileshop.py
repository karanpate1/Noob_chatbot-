import os
from dotenv import load_dotenv
import requests
from dotenv import load_dotenv
from google import genai
from google.genai import types
from IPython.display import Markdown, display
import json
import gradio as gr

# Point to your .env file
env_path = "/content/drive/MyDrive/LLM/.env"

load_dotenv(dotenv_path=env_path)

# Test: print a variable
GEMINI_KEY=os.getenv("GEMINI_KEY") 

#function to get price of mobile
clients=genai.Client(api_key=GEMINI_KEY)


def get_price(model_name):
  price_dict = {
        "samsung galaxy s25 ultra": 129999,
        "apple iphone 16 pro max": 159999,
        "oneplus 13r": 42999,
        "xiaomi redmi note 14 pro+": 28499,
        "realme gt neo 6": 31999,
        "google pixel 9 pro": 98999,
        "motorola moto edge 50 fusion": 34999,
        "vivo x120 pro": 67999,
        "oppo find x7": 74999,
        "nothing phone 3": 49999
    }
  
  model_lower=model_name.lower().strip()

  if model_lower in price_dict:
    return {
        "model": model_name,
        "price": price_dict[model_lower],
        "formatted_price": f"₹{price_dict[model_lower]:,}",
        "status": "success"
    }
  else:
    return{
        "status": "error",
        "message": f"Model '{model_name}' not found in our store"
    }

price_function={
    "name":"get_price",
    "description":""" this function takes model_name as input and return price of that model.
                      call this function whenever you needed,
                      example what is the price of this model_name.                
                      """,
    "parameters":{
        "type":"object",
        "properties":{
            "model_name":{
                "type":"string",
                "description":"The name of the model (example samsung galaxy s25 ultra )"
            }
        },

        "required":["model_name"],
                
    }
    }



clients=genai.Client(api_key=GEMINI_KEY)

system_instruction = """
You are a sales assistant for "Karan Mobile Store" specializing in mobile phones.
your name is Karan-Ai.
**Products Available:**
📱 Samsung Galaxy S25 Ultra
📱 Apple iPhone 16 Pro Max
📱 OnePlus 13R
📱 Xiaomi Redmi Note 14 Pro+
📱 Realme GT Neo 6
📱 Google Pixel 9 Pro
📱 Motorola Moto Edge 50 Fusion
📱 Vivo X120 Pro
📱 Oppo Find X7
📱 Nothing Phone 3

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
          temperature=1,
          tools=[{
              "function_declarations":[price_function]
          }]
          ),
  )

  if hasattr(response.candidates[0].content,'parts') and response.candidates[0].content.parts:
    for part in response.candidates[0].content.parts:
      if hasattr(part,'function_call') and part.function_call:
        function_name=part.function_call.name
        if function_name == "get_price":
           # Extract parameters
          model_name=part.function_call.args['model_name']
          # Call the actual function
          price_result=get_price(model_name)

          # Create function response message

          function_response={
              "role":"user",
              "parts":[{
                  "function_response":{
                      "name":"get_price",
                      "response":{
                          "price_info":price_result
                      }
                  }
              }]
          }
          print(function_response)
          # Add function response to messages and generate final response
          messages.append(function_response)

          final_response = clients.models.generate_content(
              model="gemini-2.5-flash",
              contents=messages,
              config=types.GenerateContentConfig(
                  system_instruction=system_instruction,
                  temperature=1,
              ),
          )

          return final_response.text

  # message.append({"role":"model","parts":{"text":response.last}})
  return response.text


gr.ChatInterface(fn=chat,title="Karan mobile").launch(debug=True)