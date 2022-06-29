import couchdb
import os

from couchdb.mapping import Document, TimeField, IntegerField
from dotenv import load_dotenv

load_dotenv()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


class Transaction(Document):
    timestamp = IntegerField()
    amount = IntegerField()


couch = couchdb.Server(os.getenv("COUCHDB_URL"))

db = couch["blockchain"]

tr = Transaction(timestamp=2421, amount=2)
tr.store(db)
