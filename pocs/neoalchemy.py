from neomodel import config, db

config.DATABASE_URL = 'bolt://neo4j:qwert123@localhost:7687'

results, meta = db.cypher_query("RETURN 'Hello World' as message")

print(results, meta)