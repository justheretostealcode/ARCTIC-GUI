
from PIL import Image
from PIL.ImageDraw import ImageDraw, Draw

import json
from typing import TypedDict

class Node(TypedDict):
    type:str
    sources:list[str]
    targets:list[str]
    __box:tuple[int, int, int, int]
    __pos:tuple[int, int]

class Edge(TypedDict):
    _in:tuple[int, int]
    outs:list[tuple[int, int]]
    posX:int

rgb = tuple[int, int, int]

test_data = '''{
  "truthtable" : "11010000",
  "gate_truthtables" : {
    "NOR2_2" : "00010001",
    "b" : "11001100",
    "OUTPUT_BUFFER_5" : "11010000",
    "NOT_1" : "00001111",
    "NOR2_3" : "00100010",
    "a" : "11110000",
    "c" : "10101010",
    "NOR2_4" : "11010000"
  },
  "graph" : {"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"NOT_1","type":"NOT"},{"id":"a","type":"INPUT"},{"id":"NOR2_2","type":"NOR2"},{"id":"b","type":"INPUT"},{"id":"c","type":"INPUT"},{"id":"NOR2_3","type":"NOR2"},{"id":"NOR2_4","type":"NOR2"},{"id":"OUTPUT_BUFFER_5","type":"OUTPUT_BUFFER"}],"edges":[{"id":"1","source":"a","target":"NOT_1","variable":"x"},{"id":"2","source":"b","target":"NOR2_2","variable":"x"},{"id":"3","source":"c","target":"NOR2_2","variable":"y"},{"id":"4","source":"NOR2_2","target":"NOR2_3","variable":"x"},{"id":"5","source":"b","target":"NOR2_3","variable":"y"},{"id":"6","source":"NOT_1","target":"NOR2_4","variable":"x"},{"id":"7","source":"NOR2_3","target":"NOR2_4","variable":"y"},{"id":"8","source":"NOR2_4","target":"OUTPUT_BUFFER_5","variable":"x"}]}
}'''

def _not_connections(pos:tuple[float, float], size:int)->list[tuple[int, int]|None]:
    return [(pos[0], pos[1]+4*size), (pos[0]+10*size, pos[1]+4*size)]
def _nor_connections(pos:tuple[float, float], size:int)->list[tuple[int, int]|None]:
    from math import pi, sin, cos
    x = 4*size*cos(pi/6)
    y = 8*size*sin(pi/6)
    return [(pos[0]+x, pos[1]+8*size-y), (pos[0]+x, pos[1]+8*size+y), (pos[0]+18*size, pos[1]+8*size)]
def _in_connections(pos:tuple[float, float], size:int)->list[tuple[int, int]|None]:
    return [None, (pos[0]+16*size, pos[1]+4*size)]
def _out_connections(pos:tuple[float, float], size:int)->list[tuple[int, int]|None]:
    return [(pos[0], pos[1]+4*size), None]
def _connections(node:Node, size:int)->list[tuple[int, int]|None]:
    funs = {'INP':_in_connections,'NOT':_not_connections, 'NOR':_nor_connections, 'OUT':_out_connections, 'BYP':lambda pos, size:[pos, pos]}
    return funs[node['type'][:3]](node['__pos'], size)

def _not_box(size:int)->tuple[int, int]:
    return 10*size, 8*size
def _nor_box(size:int)->tuple[int, int]:
    return 18*size, 16*size
def _in_box(size:int)->tuple[int, int]:
    return 16*size, 8*size
def _out_box(size:int)->tuple[int, int]:
    return 16*size, 8*size
def _box(node:Node, size:int)->tuple[int, int]:
    funs = {'INP':_in_box,'NOT':_not_box, 'NOR':_nor_box, 'OUT':_out_box, 'BYP':lambda size:(0, 0)}
    return funs[node['type'][:3]](size)

def _not(draw:ImageDraw, pos:tuple[float, float], size:int, fill:rgb, outline:rgb, background:rgb)->None:
    draw.polygon((pos, (pos[0]+8*size, pos[1]+4*size), (pos[0], pos[1]+8*size), pos), outline=outline, fill=fill, width=WIDTH)
    draw.ellipse((pos[0]+8*size, pos[1]+3*size, pos[0]+10*size, pos[1]+5*size), outline=outline, fill=fill, width=WIDTH)
def _nor(draw:ImageDraw, pos:tuple[float, float], size:int, fill:rgb, outline:rgb, background:rgb)->None:
    from math import sin, cos, pi
    draw.polygon((pos, (pos[0]+16*size, pos[1]+8*size), (pos[0], pos[1]+16*size), pos), outline=fill, fill=fill, width=WIDTH)
    x = 16*size/sin(pi/3)
    y = 8*size/(1-cos(pi/3))
    box = (pos[0]-x, pos[1], pos[0]+x, pos[1]+2*y)
    draw.chord(box, start=270, end=330, outline=None, fill=fill, width=WIDTH)
    draw.arc(box, start=270, end=330, fill=outline, width=WIDTH)
    box = (pos[0]-x, pos[1]-2*y+16*size, pos[0]+x, pos[1]+16*size)
    draw.chord(box, start=30, end=90, outline=None, fill=fill, width=WIDTH)
    draw.arc(box, start=30, end=90, fill=outline, width=WIDTH)
    x = 4*size/(1-cos(pi/4))
    y = 8*size/sin(pi/4)
    box = (pos[0]+4*size-2*x, pos[1]-y+8*size, pos[0]+4*size, pos[1]+y+8*size)
    draw.chord(box, start=-45, end=45, outline=None, fill=background, width=WIDTH)
    draw.arc(box, start=-45, end=45, fill=outline, width=WIDTH)
    draw.ellipse((pos[0]+16*size, pos[1]+7*size, pos[0]+18*size, pos[1]+9*size), outline=outline, fill=fill, width=WIDTH)
def _in(draw:ImageDraw, pos:tuple[float, float], size:int, fill:rgb, outline:rgb, background:rgb)->None:
    draw.polygon((pos, (pos[0]+12*size, pos[1]), (pos[0]+16*size, pos[1]+4*size), (pos[0]+12*size, pos[1]+8*size), (pos[0], pos[1]+8*size), pos), outline=outline, fill=fill, width=WIDTH)
def _out(draw:ImageDraw, pos:tuple[float, float], size:int, fill:rgb, outline:rgb, background:rgb)->None:
    draw.polygon(((pos[0], pos[1]+4*size), (pos[0]+4*size, pos[1]), (pos[0]+16*size, pos[1]), (pos[0]+16*size, pos[1]+8*size), (pos[0]+4*size, pos[1]+8*size), (pos[0], pos[1]+4*size)), outline=outline, fill=fill, width=WIDTH)
def _draw(draw:ImageDraw, node:Node, size:int, fill:rgb, outline:rgb, background:rgb)->None:
    funs = {'INP':_in,'NOT':_not, 'NOR':_nor, 'OUT':_out, 'BYP':lambda draw, pos, size, fill, ol, bg:None}
    funs[node['type'][:3]](draw, node['__pos'], size, fill, outline, background)

def gen(data:str, color:dict[str, tuple[int, int, int]|str])->Image.Image:
    graph = json.loads(data)['graph']
    match graph['version']:
        case "1":
            return _v1(graph, color)
        case _:
            raise Exception("unknown graph version")

V_SPACING = 5
H_SPACING = 10
SIZE = 10
DEFCOLOR = 'white'
WIDTH = 2

def _v1(graph:list[dict[str, str]], colorMap:dict[str, tuple[int, int, int]|str])->Image.Image:
    # restructure nodes
    nodes:dict[str,  node] = {node['id']:{'type':node['type'], 'sources':[], 'targets':[]} for node in graph['nodes']}
    # add edges to node
    for edge in graph['edges']:
        nodes[edge['target']]['sources'].append(edge['source'])
        nodes[edge['source']]['targets'].append(edge['target'])
    # rank nodes by edge dependency
    rankedNodes:list[dict[str,  node]] = []
    rankBox:list[tuple[int, int, int, int]] = []
    while len(nodes)>0:
        newRankIds = []
        for nodeID, node in nodes.items():
            if all(node not in nodes for node in node['sources']):
                newRankIds.append(nodeID)
        newRank = {id:nodes[id] for id in newRankIds}
        for id in newRankIds:
            del nodes[id]
        # insert bypass nodes for connection with prior nodes
        if len(rankedNodes) > 0:
            allSources:set[str] = set()
            for node in nodes.values():
                allSources|= set(node['sources'])
            bypassMap:dict[str, str] = {}
            for nodeID, node in rankedNodes[-1].items():
                if nodeID not in allSources:
                    continue
                bypassMap[nodeID] = 'BYPASS_'+nodeID
            for oldID, bypassID in bypassMap.items():
                for nodeID in rankedNodes[-1][oldID]['targets']:
                    if nodeID not in nodes:
                        continue
                    index = nodes[nodeID]['sources'].index(oldID)
                    nodes[nodeID]['sources'][index] = bypassID
                newRank[bypassID] = {'type':'BYPASS', 'sources':[oldID], 'targets':rankedNodes[-1][oldID]['targets']}
        rankedNodes.append(newRank)
    # calc box size for each rank
    for rank in rankedNodes:
        x, y = 0, 0
        for node in rank.values():
            node['__pos'] = 0, y
            node['__box'] = _box(node, SIZE)
            x = max(x, node['__box'][0])
            y+= node['__box'][1]+V_SPACING
        rankBox.append((x, y-V_SPACING))
    # place rank boxes and edges
    edges:dict[str, Edge] = {}

    maxY = max(y for _, y in rankBox)+2*V_SPACING
    x = H_SPACING
    for box, rank in zip(rankBox, rankedNodes):
        boxX, boxY = box
        # place node in rank
        for nodeID, node in rank.items():
            _, ny = node['__pos']
            node['__pos'] = (x, (maxY-boxY)//2+ny)
            nodes[nodeID] = node
        x+= boxX+H_SPACING
        # connect to source edges
        for nodeID in rank.keys():
            connections = _connections(nodes[nodeID], SIZE)[:-1]
            for source, connect in zip(nodes[nodeID]['sources'], connections):
                if connect is None:
                    raise Exception('Should Be Imposable')
                edges[source]['outs'].append(connect)
        # place target edges for rank
        for nodeID in rank.keys():
            if len(nodes[nodeID]['targets'])==0:
                continue
            edges[nodeID] = {
                '_in':_connections(nodes[nodeID], SIZE)[-1],
                'outs':[],
                'posX':x,
            }
            x+= H_SPACING
    # make img and draw objects with appropriate size
    width, hight = x, max(y for _, y in rankBox)+2*V_SPACING
    img = Image.new('RGB', (width, hight), (255, 255, 255))
    draw = Draw(img)
    # draw nodes
    for nodeID, node in nodes.items():
        _draw(draw, node, SIZE, colorMap.get(nodeID, DEFCOLOR), 'black', 'white')

    # draw edges
    for edge in edges.values():
        lines = [edge['_in']]+edge['outs']
        posX = edge['posX']
        for line in lines:
            x, y = line
            draw.line((x, y, posX, y), fill=(0, 0, 0), width=WIDTH)
        maxY = max(y for _, y in lines)
        minY = min(y for _, y in lines)
        draw.line((posX, minY, posX, maxY), fill=(0, 0, 0), width=WIDTH)
    return img

if __name__ == '__main__':
    gen(test_data, {}).show()

