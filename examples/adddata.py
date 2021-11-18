from Database.Document import Document
from Database.Connection import Connection

database = Connection('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000', 'Documents').getDatabase()
Document.push(database, '../../data/eng', 'eng')
Document.push(database, '../../data/eng2', 'eng')
Document.push(database, '../../data/vie', 'vie')
Document.push(database, '../../data/vie1', 'vie2')
