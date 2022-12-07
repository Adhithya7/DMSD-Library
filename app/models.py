from peewee import Model, CharField, DateTimeField, BooleanField, DatabaseProxy
import datetime

database_proxy = DatabaseProxy()

class Documents(Model):
    class Meta:
        database = database_proxy

    pkey = CharField(primary_key=True)
    updated_at = DateTimeField(default=datetime.datetime.now)
    created_at = DateTimeField(default=datetime.datetime.now)
    lastmodified = DateTimeField()
    created_ts = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        self.updated_at = datetime.datetime.now()
        return super(Documents, self).save(*args, **kwargs)
