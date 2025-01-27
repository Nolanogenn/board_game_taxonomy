import json
from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import SKOS, RDF, FOAF

g = Graph()
g.parse('./templates/taxonomy_base.ttl')
games = json.load(open('data/games.json'))
mechanics = open('data/mechanics').readlines()
types = open('data/subdomains').readlines()
categories = open('data/subdomains').readlines()
families = open('data/families').readlines()

id_to_thing = {}
def handleLine(line):
    name, descr, i = line.split('\t')
    n = name.strip().replace("'s",'s').replace(', ', '-').replace(': ','-').replace(' ', '-').replace('/','')
    id_to_thing[i.strip()] = n
    return n, descr, i.strip()

gm = Namespace("https://www.genn.nolalt.org/ontologies/games")
g.bind("gm", gm)
uriGame = URIRef("https://www.genn.nolalt.org/ontologies/games")
for line in mechanics:
    m, definition, i = handleLine(line)
    g.add((gm[m], RDF.type, gm["mechanic"]))
    g.add((gm[m], SKOS.definition, Literal(definition, lang="en")))
    g.add((gm[m], gm['bggId'], Literal(int(i))))
for line in types:
    t,definition,i  = handleLine(line)
    g.add((gm[t], RDF.type, gm["subDomain"]))
    g.add((gm[t], SKOS.definition, Literal(definition, lang="en")))
    g.add((gm[t], gm['bggId'], Literal(int(i))))
for line in categories:
    c,definition,i = handleLine(line)
    g.add((gm[c], RDF.type, gm['category']))
    g.add((gm[c], SKOS.definition, Literal(definition, lang="en")))
    g.add((gm[c], gm['bggId'], Literal(int(i))))
for line in families:
    f,definition,i = handleLine(line)
    g.add((gm[f], RDF.type, gm['family']))
    g.add((gm[f], SKOS.definition, Literal(definition, lang="en")))
    g.add((gm[f], gm['bggId'], Literal(int(i))))

for game in games:
    g_id = game['name'].replace("'s", 's').replace(', ', '-').replace(': ','-').replace(' ', '-').replace('/','')
    g.add((gm[g_id], RDF.type, gm['boardgame']))

g.serialize(destination="test.ttl")
