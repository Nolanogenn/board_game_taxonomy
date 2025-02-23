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

thing_info = json.load(open('data/thing_info.json'))
id_to_thing = {}
def handleName(name):
    n = name.strip().replace("'s",'s').replace(', ', '-').replace(': ','-').replace(' ', '-').replace('/','')
    return n
def handleLine(line):
    name, descr, i = line.split('\t')
    n = handleName(name)
    id_to_thing[i.strip()] = n
    return n, descr, i.strip()

def addThing(g_id,category,thing,addedIds):
    _id = thing['objectid']
    _name = thing['name']
    _href = thing['href']
    _kind = thing_info[category]['kind']
    _rel = thing_info[category]['rel']
    _type = thing_info[category]['type']
    if _id not in addedIds:
        g.add((gm[_id], RDF.type, gm[_kind]))
        if _type == 'person':
            g.add((gm[_id], FOAF.name, Literal(_name)))
        else:
            g.add((gm[_id], SCHEMA.name, Literal(_name)))
        addedIds.add(_id)
    g.add((gm[g_id], gm[_rel], gm[_id]))

addedIds = set()
gm = Namespace("https://www.genn.nolalt.org/ontologies/games#")
SCHEMA = Namespace("http://schema.org/")
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
    g.add((gm[g_id], SCHEMA.name, Literal(game['name'])))
    g.add((gm[g_id], SKOS.definition, Literal(game['description'])))
    for category in game['links']['boardgamecategory']:
        cat_name = handleName(category['name'])
        g.add((gm[g_id], gm['hasCategory'], gm[cat_name]))
    for mechanic in game['links']['boardgamemechanic']:
        mec_name = handleName(mechanic['name'])
        print(mec_name, g_id)
        g.add((gm[g_id], gm['hasMechanic'], gm[mec_name]))
    for thing in thing_info:
        things = game['links'][thing]
        for _thing in things:
            addThing(g_id, thing, _thing,addedIds)
