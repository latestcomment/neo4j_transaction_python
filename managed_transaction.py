import neo4j
from neo4j import GraphDatabase

uri = "neo4j://34.101.108.134:7687"
user = "neo4j"
password = "poc123"
database = "pythonint"
driver=GraphDatabase.driver(uri=uri,auth=(user,password))


def create_person(driver,name, code, role):
    with driver.session(database=database) as session:
        session.write_transaction(create_person_tx, name, code, role)
    

def create_person_tx(tx, name, code, role):
    query = """
    MERGE (a:Person {name:$name}) set a.code = $code, a.role = $role, a.source = "Managed TX"
    with a
    MATCH (a) RETURN a.name as Name, a.code as Code, a.role as Role, a.source as Source
    """
    parameter = {
        "name":name,
        "code":code,
        "role":role
    }
    results = tx.run(query, parameter)
    record = results.data()
    return print(record)

def match_person(driver,name):
    with driver.session(database=database) as session:
        session.read_transaction(match_person_tx, name)
    

def match_person_tx(tx, name):
    query = """
    MATCH (a:Person {name:$name}) RETURN a.name as Name, a.code as Code, a.role as Role, a.source as Source
    """
    parameter = {
        "name":name
    }
    results = tx.run(query, parameter)
    record = results.data()
    return print(record)

create_person(driver,name="Queen", code="B01", role="Entertainer")
match_person(driver,name="Queen")