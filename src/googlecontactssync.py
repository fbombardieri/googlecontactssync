import os
import json
import httplib2

from apiclient.discovery import build
from oauth2client.file import Storage
from oauth2client.client import OAuth2WebServerFlow
from oauth2client import tools

with open("../../_shared/config_contactssync.json") as f:
    data = json.load(f)


FLOW = OAuth2WebServerFlow(
    client_id= data["client_id"],
    client_secret= data["client_secret"],
    # scope= "https://www.googleapis.com/auth/contacts.readonly",
    scope= "https://www.googleapis.com/auth/contacts",
    user_agent= data["user_agent"]
    )

flags = tools.argparser.parse_args(args=[])

storage = Storage("info.dat")
credentials = storage.get()
if credentials is None or credentials.invalid == True:
    credentials = tools.run_flow(FLOW, storage, flags) 
    
http = httplib2.Http()
http = credentials.authorize(http)

people_service = build(serviceName= "people", version= "v1", http= http)

connections = people_service.people().connections().list(resourceName= "people/me", personFields= "names,emailAddresses").execute()