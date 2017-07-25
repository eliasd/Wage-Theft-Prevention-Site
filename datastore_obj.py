from google.appengine.ext import ndb
#marital status code:
#1: Dual Income or Single: 1.315%
#2: Married (1 income): 0%
#3: Head of Household: 1.315%

class User(ndb.Model):
    user_id = ndb.StringProperty()
    time_worked = ndb.FloatProperty()
    marital_status = ndb.IntegerProperty()
    total_california_tax = ndb.FloatProperty()
