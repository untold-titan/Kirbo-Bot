class User(object):

    def __init__(self,id,username,tokens = 0,lastDaily = None,customRole = False):
        self.id = id
        self.username = username
        self.lastDaily = lastDaily
        self.tokens = tokens
        self.customRole = customRole
    
    def to_string(self):
        return "Username: " + self.username + " ID: " + self.id + " Tokens: " + str(self.tokens)

    @staticmethod
    def from_dict(source):
        if "lastDaily" in source:
            return User(source["id"], source["username"],source["tokens"], source["lastDaily"], source["customRole"])
        else:
            return User(source["id"], source["username"],source["tokens"], source["customRole"])

    def to_dict(self):
        data = {
            u"id":self.id,
            u"username":self.username,
            u"tokens":self.tokens,
            u"lastDaily":self.lastDaily,
            u"customRole":self.customRole
        }
        if self.lastDaily == None:
            del data["lastDaily"]
        return data

