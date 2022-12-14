import jsons

class JsonSerializable(object):
    def toJson(self):
        return jsons.dumps(self)

    def __repr__(self):
        return self.toJson()

    def __str__(self):
        return self.toJson()

    def toJSON(self):
        return self.toJson()