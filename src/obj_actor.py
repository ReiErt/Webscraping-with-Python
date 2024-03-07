import sqlite3
from src import obj_actor

class Actor:
   def __init__(self, ActorID, Firstname_Surname, About_info, Actorpage_URL, actoraward_url):
      self.ActorID = ActorID
      self.Firstname_Surname = Firstname_Surname
      self.About_info = About_info
      self.Actorpage_URL = Actorpage_URL
      self.actoraward_url = actoraward_url



