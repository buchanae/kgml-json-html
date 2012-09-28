from collections import defaultdict
import json

from lxml import objectify




if __name__ == '__main__':
    content = open('rn00250.xml').read()

    graphics = defaultdict(dict)

    xml = objectify.fromstring(content)
    for entry in getattr(xml, 'entry', []):

        ID = entry.get('id')
        t = entry.get('type')
        g = entry.graphics[0]

        graphics[t][ID] = {
            'type': t,
            'x': int(g.get('x')),
            'y': int(g.get('y')),
            'width': int(g.get('width')),
            'height': int(g.get('height')),
            'name': g.get('name'),
        }

    links_reaction = defaultdict(list)
    for reaction_xml in getattr(xml, 'reaction', []):

        reversible = reaction_xml.get('type') == 'reversible'
        substrates = tuple(x.get('id') for x in getattr(reaction_xml, 'substrate', []))
        products = tuple(x.get('id') for x in getattr(reaction_xml, 'product', []))

        key = (reversible, substrates, products)
        ID = reaction_xml.get('id')
        links_reaction[key].append(ID)

    # TODO gawd this code is getting ugly
    #      and largely untested

    reactions = {}
    for (reversible, substrates, products), IDs in links_reaction.items():

        ID = IDs[0]
        reaction = graphics['reaction'][ID]
        reaction.update({
            'substrates': substrates,
            'products': products,
            'reversible': reversible,
            'related-reactions': IDs[1:],
        })
        reactions[ID] = reaction

    json.dump({
        'compounds': graphics['compound'],
        'reactions': reactions,
    }, open('out.json', 'w'))
