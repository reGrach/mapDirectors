from SPARQLWrapper import SPARQLWrapper, JSON

yearLeft = input()
yearRight = input()

# Проверим и удалим существующие переменные
try:
    del results
except NameError:
    print("results не существуют")
try:
    del sparql
except NameError:
    print("sparql не существуют")

# Список префиксов по умолчанию:
prefStr = """
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX dbo: <http://dbpedia.org/ontology/>
PREFIX geo:<http://www.w3.org/2003/01/geo/wgs84_pos#>
"""

# Строка-запрос (выводим имя, год рождения, месторождения, и данные места рождения для обработки)
sparql = SPARQLWrapper("https://dbpedia.org/sparql", returnFormat=JSON, defaultGraph="http://dbpedia.org")
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
queryString = queryString.replace("DIR1-NAME", yearLeft)
queryString = queryString.replace("DIR2-NAME", yearRight)
sparql.setQuery(queryString)
results = sparql.query().convert()
# Прерываем программу, если записи отсутсвуют
if (len(results["results"]["bindings"]) == 0):
    print("No results found.")

# Обрабатываем ответ на число уникальных имен
personList = []
for el in results["results"]["bindings"]:
    if (el["namePerson"]["value"] in personList):
        continue
    personList.append(el["namePerson"]["value"])
print('Всего родилось:', len(personList))
listRes = dict.fromkeys(personList)
#
for el in results["results"]["bindings"]:
    if (listRes[el["namePerson"]["value"]] == None) or (
            listRes[el["namePerson"]["value"]][1] > el["callret-3"]["value"]):
        listRes[el["namePerson"]["value"]] = list(
            [el["lablePlace"]["value"], el["callret-3"]["value"], el["lat"]["value"], el["long"]["value"]])

for el in listRes:
    print(el, listRes[el])