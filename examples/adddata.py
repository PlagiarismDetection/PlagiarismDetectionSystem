from pds.database.document import Document
from pds.database.connection import Connection

database = Connection('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000', 'Documents').getDatabase()
Document.push(database, '../../../data/eng', 'eng')
Document.push(database, '../../../data/vie', 'vie')
