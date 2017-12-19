from google.appengine.ext import ndb


class Member(ndb.Model):
    full_name = ndb.StringProperty()
    birth_date = ndb.StringProperty()
    hometown = ndb.StringProperty()
    primary_family = ndb.StringProperty()
    picture = ndb.StringProperty()
    input_time = ndb.DateTimeProperty(auto_now_add=True)