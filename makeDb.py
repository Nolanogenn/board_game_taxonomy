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
def handleName(name):
    n = name.strip().replace("'s",'s').replace(', ', '-').replace(': ','-').replace(' ', '-').replace('/','')
    return n
def handleLine(line):
    name, descr, i = line.split('\t')
    n = handleName(name)
    id_to_thing[i.strip()] = n
    return n, descr, i.strip()

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
        print(category)
        g.add((gm[g_id], gm['hasCategory'], gm[handleName(category['name'])]))
    for designer in game['links']["boardgamedesigner"]:
        if designer['objectid'] not in addedIds:
            d_id = designer['objectid']
            d_name = designer['name']
            d_href = designer['href']
            g.add((gm[d_id], RDF.type, gm['designer']))
            g.add((gm[d_id], FOAF.name, Literal(d_name)))
            addedIds.add(d_id)
        g.add((gm[g_id], gm['hasDesigner'], gm[designer['objectid']]))
    for artist in game['links']["boardgameartist"]:
        if artist['objectid'] not in addedIds:
            d_id = artist['objectid']
            d_name = artist['name']
            d_href = artist['href']
            g.add((gm[d_id], RDF.type, gm['artist']))
            g.add((gm[d_id], FOAF.name, Literal(d_name)))
            addedIds.add(d_id)
        g.add((gm[g_id], gm['hasArtist'], gm[artist['objectid']]))
    for publisher in game['links']["boardgamepublisher"]:
        if publisher['objectid'] not in addedIds:
            d_id = publisher['objectid']
            d_name = publisher['name']
            d_href = publisher['href']
            g.add((gm[d_id], RDF.type, gm['publisher']))
            g.add((gm[d_id], SCHEMA.name, Literal(d_name)))
            addedIds.add(d_id)
        g.add((gm[g_id], gm['hasPublisher'], gm[publisher['objectid']]))
    for developer in game['links']["boardgamedeveloper"]:
        if developer['objectid'] not in addedIds:
            d_id = developer['objectid']
            d_name = developer['name']
            d_href = developer['href']
            g.add((gm[d_id], RDF.type, gm['developer']))
            g.add((gm[d_id], FOAF.name, Literal(d_name)))
            addedIds.add(d_id)
        g.add((gm[g_id], gm['hasDeveloper'], gm[developer['objectid']]))
    for graphicDesigner in game['links']["boardgamegraphicdesigner"]:
        if graphicDesigner['objectid'] not in addedIds:
            d_id = graphicDesigner['objectid']
            d_name = graphicDesigner['name']
            d_href = graphicDesigner['href']
            g.add((gm[d_id], RDF.type, gm['graphicDesigner']))
            g.add((gm[d_id], FOAF.name, Literal(d_name)))
            addedIds.add(d_id)
        g.add((gm[g_id], gm['hasGraphicDesigner'], gm[graphicDesigner['objectid']]))
    for honor in game['links']["boardgamehonor"]:
        if honor['objectid'] not in addedIds:
            d_id = honor['objectid']
            d_name = honor['name']
            d_href = honor['href']
            g.add((gm[d_id], RDF.type, gm['honor']))
            g.add((gm[d_id], SCHEMA.name, Literal(d_name)))
            addedIds.add(d_id)
        g.add((gm[g_id], gm['hasHonor'], gm[honor['objectid']]))
