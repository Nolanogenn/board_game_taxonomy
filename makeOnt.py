from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import SKOS, RDF

g = Graph()
g.parse('./templates/taxonomy_base.ttl')
mechanics = open('data/mechanics').readlines()
types = open('data/subdomains').readlines()

def handleLine(line):
    name, descr = line.split('\t')
    n = name.strip().replace("'s",'s').replace(', ', '-').replace(': ','-').replace(' ', '-').replace('/','')
    return n, descr.strip()

gm = Namespace("https://www.genn.nolalt.org/ontologies/games")
g.bind("gm", gm)
uriGame = URIRef("https://www.genn.nolalt.org/ontologies/games")
for line in mechanics:
    m, definition = handleLine(line)
    g.add((gm[m], RDF.type, gm["mechanic"]))
    g.add((gm[m], SKOS.definition, Literal(definition, lang="en")))

for line in types:
    t,definition = handleLine(line)
    g.add((gm[t], RDF.type, gm["subDomain"]))
    g.add((gm[t], SKOS.definition, Literal(definition, lang="en")))

g.serialize(destination="test.ttl")
