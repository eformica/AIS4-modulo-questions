from neo4j import GraphDatabase

def init_driver(uri, username, password):
    # Create an instance of the driver
    driver = GraphDatabase.driver(uri, auth=(username, password))

    # Verify Connectivity
    driver.verify_connectivity()

    return driver

driver = init_driver("bolt://localhost:7687", "neo4j", "qwert123")

# Unit of work
def get_actors(tx, movie): # (1)
    result = tx.run("""
        MATCH (p:Person)-[:ACTED_IN]->(:Movie {title: $title})
        RETURN p
    """, title=movie)

    # Access the `p` value from each record
    return [ record["p"] for record in result ]


# Open a Session
with driver.session() as session:
    # Run the unit of work within a Read Transaction
    actors = session.execute_read(get_actors, movie="The Green Mile") # (2)

    for record in actors:
        print(record["p"])

    session.close()
