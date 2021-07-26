class EclipseStats:
    def __init__(self, d = None):
        self.comments = None
        self.favourites = None
        if d is not None and type(d) is dict:
            self.from_dict(d)

    def from_dict(self, d):
        if 'comments' in d: self.comments = d['comments']
        if 'favourites' in d: self.favourites = d['favourites']
