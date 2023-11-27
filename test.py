import json
from datetime import datetime

import streamlit as st
import openai

model = "gpt-3.5-turbo"

def generate_filename():
    # Get the current date and time
    now = datetime.now()

    # Format the string
    formatted_string = now.strftime("%b%d%Y%H%M%S") + str(int(now.microsecond / 1000))

    # Append '.json' to the string
    filename = formatted_string + ".json"

    return filename


def get_key():
    return st.secrets["OPENAI_API_KEY"]

def load_json(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        
    return data

def load_chat(chat):
    conversation = load_json("data/static/prototype.json")
    old_conversation = load_json("data/conversation/old_conversation.json")
    
    # Validate that 'role' is 'user'
    if chat.get('role') == 'user':
        print("Role is 'user', proceeding...")
        old_conversation.append(chat)
        print(old_conversation)
        conversation['messages'].extend(old_conversation)
    else:
        print("Role is not 'user', cannot proceed.")
    return conversation

def adjust_temperature(number):
    if number >= 0 and number <= 1.2:
        prototype = load_json("data/static/prototype.json")
        print(f"Temperature is changing from {prototype['temperature']} to {number}")
        prototype['temperature'] = number
        with open("data/static/prototype.json", "w") as f:
            json.dump(prototype, f)
        print("Saved!")
    else:
        print("Temperature is not valid, should be between 0 and 1.2. Greater 1.2 is not recommend cause it is not Natural and so dumb")

def checking_response(chat):
    # Check if 'content' contains 'As an AI language model'
    if 'As an AI' in chat['content']:
        print("Unable to get answer. Switching to Tuning version...")
        return False;
    else:
        print("Response valid. Continue to using GPT3.5")
        return True;
    
def create_profile(name, resume):
    data = load_json("data/resume/profile.json")
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    name = name +"-"+dt_string
    
    if check_exist(name, data):
        new_json = {"name": name, "resume": resume}
        data.append(new_json)
        with open("data/resume/profile.json", "w") as f:
            json.dump(data,f)
        print("Saved new profile!")
        return True
    else:
        print("Profile exist. Please wait a minute before continue...")
        return False
        
        
def check_exist(name,data):
    for profile in data:
        if(profile["name"] == name):
            return False
    return True

def clear_profile_data():
    empty_array = []
    with open("data/resume/profile.json", "w") as f:
        json.dump(empty_array, f)
    print("Cleared profile")

def delete_profile_by_name(name_to_delete):
    # Load existing data
    profiles = load_json("data/resume/profile.json")
    
    # Find and remove the profile with the matching name
    for profile in profiles:
        if profile['name'] == name_to_delete:
            profiles.remove(profile)
            break  # Important if there are multiple matches
    
    # Save the updated list back to the JSON file
    with open("data/resume/profile.json", "w") as f:
        json.dump(profiles, f)
        
def load_profiles():
    return load_json("data/resume/profile.json")

def get_profiles_name():
    data = load_json("data/resume/profile.json")
    names = [item['name'] for item in data]
    return names

def get_resume_by_name(name):
    data = load_json("data/resume/profile.json")
    for item in data:
        if item['name'] == name:
            return item['resume']
    return False
    
def write_cover_letter(profile_name, job_description, addition_request=""):
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    chat = ""
    
    if addition_request == "":
        chat = "This is my resume: " + get_resume_by_name(profile_name) + "\n\n" + "This is job description: " + job_description + "\n\n" + "Write me a cover letter based on my resume."
    else:
        chat = "This is my resume: " + get_resume_by_name(profile_name) + "\n\n" + "This is job description: " + job_description + "\n\n" + "Write me a cover letter based on my resume and " + addition_request
    
    message = [{
        "role": "user",
        "content": chat
    }]
    
    chat_completion = openai.ChatCompletion.create(model=model, messages=message, temperature=0.2)
    # Your JSON object as a string
    # json_str = '''
    # {
    #     "id": "chatcmpl-7tTiGfkFnz5ovV9O0RHketJoyu1Dm",
    #     "object": "chat.completion",
    #     "created": 1693456612,
    #     "model": "gpt-3.5-turbo-0613",
    #     "choices": [
    #         {
    #             "index": 0,
    #             "message": {
    #                 "role": "assistant",
    #                 "content": "Hello! How can I assist you today?"
    #             },
    #             "finish_reason": "stop"
    #         }
    #     ],
    #     "usage": {
    #         "prompt_tokens": 9,
    #         "completion_tokens": 9,
    #         "total_tokens": 18
    #     }
    # }
    # '''

    # Parse the JSON string to a Python dictionary
    # chat_completion = json.loads(json_str)
    # print(chat_completion['choices'][0]['message']['content'])
    
    return chat_completion['choices'][0]['message']['content']

def answer_question_base_on_resume(profile_name, question, addition_request=""):
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    chat = ""
    
    if addition_request == "":
        chat = "This is my resume: " + get_resume_by_name(profile_name) + "\n\n" + ". This is job description: " + question + "\n\n" + ". Answer the question based on my resume."
    else:
        chat = "This is my resume: " + get_resume_by_name(profile_name) + "\n\n" + ". This is job description: " + question + "\n\n" + ". Answer the question based on my resume and " + addition_request
    
    message = [{
        "role": "user",
        "content": chat
    }]
    
    chat_completion = openai.ChatCompletion.create(model=model, messages=message, temperature=0.2)
    
    return chat_completion['choices'][0]['message']['content']

def suggest_resume(resume):
    openai.api_key = st.secrets["OPENAI_API_KEY"]
    chat = ""
    
    chat = "This is my resume: \n" + resume + "\n" + "Give me some advisor to have better resume!"
    
    message = [{
        "role": "user",
        "content": chat
    }]
    
    chat_completion = openai.ChatCompletion.create(model=model, messages=message, temperature=0.2)
    
    return chat_completion['choices'][0]['message']['content']

    
print(get_key())

# print("TESTING ---")
# # print(load_chat({'role': 'user', 'content': 'Hey Jarvis. can you check my weather?'}))
# # print(checking_response(load_json("test/lastest-not-valid.json")))
# clear_profile_data()
# # Load Json and checking response, decide gpt 3,5 or tuning
# assert checking_response(load_json("test/lastest-not-valid.json")) == False
# assert checking_response(load_json("test/valid-response.json")) == True

# # test load chat to old conversation
# assert load_chat({"role": "user", "content": "Hey Jarvis. Do you know who is president of USA now??"}) == {'model': 'gpt-3.5-turbo', 'messages': [{'role': 'user', 'content': 'My name is Long. I wanna call you Jarvis. remember it'}, {'role': 'assistant', 'content': "Of course, Long! I'll remember that my name is Jarvis. How can I assist you today?"}, {'role': 'user', 'content': 'Hey Jarvis. Do you know who is president of USA now??'}], 'temperature': 0.2}
# # load_chat({"role": "user", "content": "Hey Jarvis. Do you know who is president of USA now??"})

# # test create a new resume profile.
# assert create_profile("hi", "this is a resume") == True
# assert create_profile("hi", "this is a resume") == False

# # delete a profile name
# now = datetime.now()
# dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
# name = "hi" + dt_string
# delete_profile_by_name(name)

# profiles = load_json("data/resume/profile.json")
# assert profiles == []

