class EclipseUser:
    def __init__(self, d):
        self.userId = None
        self.useridUuid = None
        self.username = None
        self.usericon = None
        self.type = None
        self.isWatching = None
        self.isNewDeviant = None
        if d is not None and type(d) is dict:
            self.from_dict(d)

    def __repr__(self):
        return self.userId
    
    def from_dict(self, d):
        if 'userId' in d: self.userId = d['userId']
        if 'useridUuid' in d: self.useridUuid = d['useridUuid']
        if 'username' in d: self.username = d['username']
        if 'usericon' in d: self.usericon = d['usericon']
        if 'type' in d: self.type = d['type']
        if 'isWatching' in d: self.isWatching = d['isWatching']
        if 'isNewDeviant' in d: self.isNewDeviant = d['isNewDeviant']
