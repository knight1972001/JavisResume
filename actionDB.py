from datetime import datetime
from pymongo import MongoClient
import streamlit as st
import pprint

# mongodb_password = st.secrets["password"]
# uri = f"mongodb+srv://knight1972001:{mongodb_password}@javisresume.8xba08e.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)
    
    
# Initialize connection
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return MongoClient(st.secrets["mongodb_uri"])

def ping():
    try:
        client = init_connection()
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
# @st.cache_data(ttl=600)

def get_profiles_name():
    client = init_connection()
    db = client["javis-resume"]
    resumeDB = db.resume
    # for item in resume.find():
    #     # pprint.pprint(item["name"])
    #     profile_names.append(item["name"])
    names = [item['name'] for item in resumeDB.find()]
    # print(names)
    return names

def create_profile(name, resume):
    # init mongodb connection
    client = init_connection()
    db = client["javis-resume"]
    resumeDB = db.resume
    
    # create unique profile name
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
    name = name +"-"+dt_string
    new_json = {"name": name, "resume": resume}
    
    # Insert to mongodb database
    try:
        resumeDB.insert_one(new_json)
        print("Saved new profile!")
        return True
    except Exception as e:
        # pprint.pprint(e)
        return False

def get_resume_by_name(name):
    # init mongodb connection
    client = init_connection()
    db = client["javis-resume"]
    resumeDB = db.resume
    
    # find One
    resume = resumeDB.find_one({"name": name})
    if (resume):
        # print(resume["resume"])
        return resume["resume"]
    else:
        print("No resume found")
        return False
    
    
def delete_profile_by_name(name):
    # init mongodb connection
    client = init_connection()
    db = client["javis-resume"]
    resumeDB = db.resume
    
    # delete one
    try:
        resumeDB.delete_one({"name": name})
        print("Deleted profile!")
        return True
    except Exception as e:
        # pprint.pprint(e)
        return False
    

# db.mycollection.insertMany([{"name" : "Mary", "pet": "dog"}, {"name" : "John", "pet": "cat"}, {"name" : "Robert", "pet": "bird"}])
    