import pymongo
import psycopg2

# Підключення до MongoDB
mongo_client = pymongo.MongoClient(host="mongodb+srv://yaroslavtarnopil:<password>@cluster0.kqcceae.mongodb.net/")
mongo_db = mongo_client["quotes_db"]
mongo_authors = mongo_db["authors"]
mongo_quotes = mongo_db["quotes"]

# Підключення до Postgres
conn = psycopg2.connect("dbname=quotes_db user=yourusername password=yourpassword")
cursor = conn.cursor()

# Міграція авторів
for author in mongo_authors.find():
    cursor.execute("INSERT INTO quotes_author (name, bio) VALUES (%s, %s)", (author['name'], author['bio']))

# Міграція цитат
for quote in mongo_quotes.find():
    cursor.execute("SELECT id FROM quotes_author WHERE name = %s", (quote['author'],))
    author_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO quotes_quote (text, author_id) VALUES (%s, %s)", (quote['text'], author_id))

conn.commit()
cursor.close()
conn.close()
