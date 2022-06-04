import neo4j
from neo4j import GraphDatabase

uri = "neo4j://34.101.108.134:7687"
user = "neo4j"
password = "poc123"
database = "pythonint"
driver=GraphDatabase.driver(uri=uri,auth=(user,password))


### NODE
def create_node_exptx(driver, id,name, band, role, ssn):
    with driver.session(default_access_mode=neo4j.WRITE_ACCESS, database=database) as session:
        tx = session.begin_transaction()
        
        try:
            create_person_node(tx, id, name)
            set_person_role(tx, id, role)
            set_person_band(tx, id, band)
            set_person_ssn(tx, id, ssn)


            tx.commit()
            print("SUCCESS")

        except:
            tx.rollback()
            print("FAIL")

        finally:
            tx.close()


def create_person_node(tx, id, name):
    result = tx.run("MERGE (a:Person {id:$id}) SET a.name = $name RETURN a.name as Name", id=id, name=name)
    record = result.data()
    return print(record)

def set_person_role(tx, id,role):
    query = """
    MATCH (a:Person) where a.id = $id  
    SET a.role = $role 
    RETURN a.id as ID, a.name as Name, a.role as Role
    """
    result = tx.run(query, id=id, role=role)
    record = result.data()
    return print(record)
    #return print("Success on updating role: {record}".format(record=record))

def set_person_band(tx, id, band):
    result = tx.run("MATCH (a:Person) WHERE a.id = $id SET a.band = $band RETURN a.id as ID, a.name as Name, a.role as Role, a.band as Band", id=id, band=band)
    record = result.data()
    return print(record)

def set_person_ssn(tx, id, ssn):
    result = tx.run("MATCH (a:Person) WHERE a.id = $id SET a.ssn = $ssn RETURN a.id as ID, a.name as Name, a.role as Role, a.band as Band, a.ssn as SSN", id=id, ssn=ssn)
    record = result.data()
    return print(record)


create_node_exptx(driver=driver, id='1', name='Paul', role='Bassist', band='The Beatles', ssn=1010)
create_node_exptx(driver=driver, id='2', name='Ringo', role='Drummer', band='The Beatles', ssn=1010)