from flask import Flask, request
from SPARQLWrapper import SPARQLWrapper, JSON
import json

app = Flask(__name__)

# send CORS headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    if request.method == 'OPTIONS':
        response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
        headers = request.headers.get('Access-Control-Request-Headers')
        if headers:
            response.headers['Access-Control-Allow-Headers'] = headers
    return response


@app.route('/peopleInfo', methods=('GET', ))
def getPeopleInfo():
    yearFrom = request.args.get('yearFrom')
    yearTo = request.args.get('yearTo')

    # Получим строку запроса
    queryString = getQueryString(yearFrom, yearTo)

    sparql = SPARQLWrapper("https://dbpedia.org/sparql", returnFormat=JSON, defaultGraph="http://dbpedia.org")
    sparql.setQuery(queryString)
    results = sparql.query().convert()
    # Прерываем программу, если записи отсутсвуют
    if (len(results["results"]["bindings"]) == 0):
        return []

    # Обрабатываем ответ на число уникальных имен
    personList = []
    for el in results["results"]["bindings"]:
        if (el["namePerson"]["value"] in personList):
            continue
        personList.append(el["namePerson"]["value"])
    
    listRes = dict.fromkeys(personList)
    
    for el in results["results"]["bindings"]:
        if (listRes[el["namePerson"]["value"]] == None) or (
                listRes[el["namePerson"]["value"]][1] > el["callret-3"]["value"]):
            listRes[el["namePerson"]["value"]] = list(
                [el["lablePlace"]["value"], el["callret-3"]["value"], el["lat"]["value"], el["long"]["value"]])

    return json.dumps(listRes)


def getQueryString(yearFrom, yearTo):
    # Список префиксов по умолчанию:
    prefStr = """
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
    """

    # Строка-запрос (выводим имя, год рождения, месторождения, и данные места рождения для обработки)
    queryString = prefStr + """
        SELECT  ?namePerson ?year ?lablePlace xsd:integer(?area) ?lat ?long
        WHERE
        {
        ?temp   rdf:type       dbo:Person;
                dbo:director   ?person.

        ?person dbo:birthDate  ?year
                                #FILTER (xsd:date(?year))
                                FILTER (xsd:date(?year) > "DIR1-NAME"^^xsd:dateTime && xsd:date(?year) < "DIR2-NAME"^^xsd:dateTime)
        ?person rdfs:label      ?namePerson
                                FILTER (LANG(?namePerson) = "en")
        ?person dbo:birthPlace  ?place.

        ?place dbo:areaTotal   ?area;
                geo:lat         ?lat;
                geo:long        ?long.
        ?place rdfs:label      ?lablePlace
                                FILTER (LANG(?lablePlace) = "en")
        }"""
        
    queryString = queryString.replace("DIR1-NAME", yearFrom)
    queryString = queryString.replace("DIR2-NAME", yearTo)

    return queryString

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8888)