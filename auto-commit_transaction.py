import neo4j
from neo4j import GraphDatabase

uri = "neo4j://34.101.108.134:7687"
user = "neo4j"
password = "poc123"
database = "pythonint"
driver=GraphDatabase.driver(uri=uri,auth=(user,password))


def create_node_autotx(name, code, role):
    session = driver.session(default_access_mode=neo4j.WRITE_ACCESS,database=database)
    query = """
    MERGE (a:Person {name:$name}) set a.code = $code, a.role = $role, a.source = "Auto TX"
    with a
    MATCH (a) RETURN a.name as Name, a.code as Code, a.role as Role, a.source as Source
    """
    parameter = {
        "name":name,
        "code":code,
        "role":role
    }
    result = session.run(query, parameter)
    data = []
    for result in result:
        dic = {}
        Name = result["Name"]
        Code = result["Code"]
        Role = result["Role"]
        Source = result["Source"]
        dic.update({
            "Name":Name,
            "Code":Code,
            "Role":Role,
            "Source":Source})
        data.append(dic)
        
    return print(data)

def match_node_autotx(name):
    session = driver.session(default_access_mode=neo4j.READ_ACCESS, database=database)
    query = """
    MATCH (a:Person {name:$name}) RETURN a.name as Name, a.code as Code, a.role as Role, a.source as Source
    """
    parameter = {
        "name":name
    }
    results = session.run(query, parameter)
    data = []
    for result in results:
        dic={}
        Name = result["Name"]
        Code = result["Code"]
        Role = result["Role"]
        Source = result["Source"]
        dic.update({
            "Name":Name,
            "Code":Code,
            "Role":Role,
            "Source":Source})
        data.append(dic)
        
    return print(data)


create_node_autotx(name="Name1", code="E01", role="tester1")
match_node_autotx(name="Name1")