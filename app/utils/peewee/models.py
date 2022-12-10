from peewee import *
import datetime

class Documents(Model):
    class Meta:
        database = database_proxy

    docid = AutoField(primary_key=True)
    title = CharField()
    pdate = DateTimeField()
    publisherid = CharField()

    def save(self, *args, **kwargs):
        return super(Documents, self).save(*args, **kwargs)

class Publisher(Model):
    class Meta:
        database = database_proxy

    publisherid = ForeignKeyField(Documents, field='publisherid' ,primary_key=True)
    pubname = CharField()
    address = CharField()

    def save(self, *args, **kwargs):
        return super(Publisher, self).save(*args, **kwargs)
