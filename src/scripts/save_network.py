from neo4j import GraphDatabase


def save_json(network, path):
    network.save_json(path)


def save_csvs(network, path):
    network.save_csvs(path)


def save_xlsx(network, path):
    network.save_xlsx(path)


def save_neo4j(network, config):
    create_cypher = network.render_create_cypher()

    graphDB_Driver = GraphDatabase.driver(config.uri, auth=(config.username, config.pw))

    with graphDB_Driver.session() as graphDB_Session:
        graphDB_Session.run(create_cypher)
