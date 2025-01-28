
from PIL import Image
from PIL.ImageDraw import ImageDraw, Draw

import json
from typing import TypedDict, TypeAlias

# costume types

rgb:TypeAlias = tuple[int, int, int]|str

class Node(TypedDict):
    type:str
    sources:list[str]
    targets:list[str]
    __box:tuple[int, int]
    __pos:tuple[int, int]

class Edge(TypedDict):
    _in:tuple[int, int]
    outs:list[tuple[int, int]]
    posX:int

# test datagateNode

test_data = '''{
  "truthtable" : "11111000",
  "gate_truthtables" : {
    "NOT_2" : "01010101",
    "NOR2_3" : "10001000",
    "OUTPUT_OR2_4" : "11111000",
    "c" : "10101010",
    "NOT_1" : "00110011",
    "a" : "11110000",
    "b" : "11001100"
  },
  "graph" : {"creator":"JGraphT JSON Exporter","version":"1","nodes":[{"id":"NOT_1","type":"NOT"},{"id":"b","type":"INPUT"},{"id":"NOT_2","type":"NOT"},{"id":"c","type":"INPUT"},{"id":"NOR2_3","type":"NOR2"},{"id":"OUTPUT_OR2_4","type":"OUTPUT_OR2"},{"id":"a","type":"INPUT"}],"edges":[{"id":"1","source":"b","target":"NOT_1","variable":"x"},{"id":"2","source":"c","target":"NOT_2","variable":"x"},{"id":"3","source":"NOT_1","target":"NOR2_3","variable":"x"},{"id":"4","source":"NOT_2","target":"NOR2_3","variable":"y"},{"id":"5","source":"NOR2_3","target":"OUTPUT_OR2_4","variable":"x"},{"id":"6","source":"a","target":"OUTPUT_OR2_4","variable":"y"}]}
}'''

# utilities for drawing

def _not_inputs(pos:tuple[float, float], size:int)->list[tuple[int, int]]:
    '''
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
        
    return:
        a list of input points of the circuit element
    '''
    return [(pos[0], pos[1]+4*size)]
def _nor_inputs(pos:tuple[float, float], size:int)->list[tuple[int, int]]:
    '''
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
        
    return:
        a list of input points of the circuit element
    '''
    from math import pi, sin, cos
    x = 4*size*cos(pi/6)
    y = 8*size*sin(pi/6)
    return [(pos[0]+x, pos[1]+8*size-y), (pos[0]+x, pos[1]+8*size+y)]
def _in_inputs(pos:tuple[float, float], size:int)->list[tuple[int, int]]:
    '''
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
        
    return:
        a list of input points of the circuit element
    '''
    return []
def _out_inputs(pos:tuple[float, float], size:int)->list[tuple[int, int]]:
    '''
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
        
    return:
        a list of input points of the circuit element
    '''
    return [(pos[0], pos[1]+4*size)]
def _inputs(node:Node, size:int)->list[tuple[int, int]]:
    '''
    node:
        the node that
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
        
    return:
        a list of input points of the circuit element
    '''
    funs = {'INP':_in_inputs,'NOT':_not_inputs, 'NOR':_nor_inputs, 'OUT':_out_inputs, 'BYP':lambda pos, size:[pos]}
    return funs[node['type'][:3]](node['__pos'], size)

def _not_outputs(pos:tuple[float, float], size:int)->tuple[int, int]|None:
    '''
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
        
    return:
        the output point of the circuit element
    '''
    return (pos[0]+10*size, pos[1]+4*size)
def _nor_outputs(pos:tuple[float, float], size:int)->tuple[int, int]|None:
    '''
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
        
    return:
        the output point of the circuit element
    '''
    return (pos[0]+18*size, pos[1]+8*size)
def _in_outputs(pos:tuple[float, float], size:int)->tuple[int, int]|None:
    '''
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
        
    return:
        the output point of the circuit element
    '''
    return (pos[0]+16*size, pos[1]+4*size)
def _out_outputs(pos:tuple[float, float], size:int)->tuple[int, int]|None:
    '''
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
        
    return:
        the output point of the circuit element
    '''
    return None
def _outputs(node:Node, size:int)->tuple[int, int]|None:
    '''
    node:
        the node that
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
        
    return:
        the output point of the circuit element
    '''
    funs = {'INP':_in_outputs,'NOT':_not_outputs, 'NOR':_nor_outputs, 'OUT':_out_outputs, 'BYP':lambda pos, size:pos}
    return funs[node['type'][:3]](node['__pos'], size)

def _not_box(size:int)->tuple[int, int]:
    '''
    size: 
        A scaling factor
        
    return:
        A tuple of the size of the box enclosing the circuit element (x axis, y axis)
    '''
    return 10*size, 8*size
def _nor_box(size:int)->tuple[int, int]:
    '''
    size: 
        A scaling factor
        
    return:
        A tuple of the size of the box enclosing the circuit element (x axis, y axis)
    '''
    return 18*size, 16*size
def _in_box(size:int)->tuple[int, int]:
    '''
    size: 
        A scaling factor
        
    return:
        A tuple of the size of the box enclosing the circuit element (x axis, y axis)
    '''
    return 16*size, 8*size
def _out_box(size:int)->tuple[int, int]:
    '''
    size: 
        A scaling factor
        
    return:
        A tuple of the size of the box enclosing the circuit element (x axis, y axis)
    '''
    return 16*size, 8*size
def _box(node:Node, size:int)->tuple[int, int]:
    '''
    size: 
        A scaling factor
        
    return:
        A tuple of the size of the box enclosing the circuit element (x axis, y axis)
    '''
    funs = {'INP':_in_box,'NOT':_not_box, 'NOR':_nor_box, 'OUT':_out_box, 'BYP':lambda size:(0, 0)}
    return funs[node['type'][:3]](size)

def _not_draw(draw:ImageDraw, pos:tuple[float, float], size:int, fill:rgb, outline:rgb, background:rgb)->None:
    '''
    draw:
        the interface of the Image objet that is drawn on.
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
    fill:
        fill color
    
    draws the circuit element to the Image.
    '''
    draw.polygon((pos, (pos[0]+8*size, pos[1]+4*size), (pos[0], pos[1]+8*size), pos), outline=outline, fill=fill, width=WIDTH)
    draw.ellipse((pos[0]+8*size, pos[1]+3*size, pos[0]+10*size, pos[1]+5*size), outline=outline, fill=fill, width=WIDTH)
def _nor_draw(draw:ImageDraw, pos:tuple[float, float], size:int, fill:rgb, outline:rgb, background:rgb)->None:
    '''
    draw:
        the interface of the Image objet that is drawn on.
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
    fill:
        fill color
    
    draws the circuit element to the Image.
    '''
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
def _in_draw(draw:ImageDraw, pos:tuple[float, float], size:int, fill:rgb, outline:rgb, background:rgb)->None:
    '''
    draw:
        the interface of the Image objet that is drawn on.
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
    fill:
        fill color
    
    draws the circuit element to the Image.
    '''
    draw.polygon((pos, (pos[0]+12*size, pos[1]), (pos[0]+16*size, pos[1]+4*size), (pos[0]+12*size, pos[1]+8*size), (pos[0], pos[1]+8*size), pos), outline=outline, fill=fill, width=WIDTH)
def _out_draw(draw:ImageDraw, pos:tuple[float, float], size:int, fill:rgb, outline:rgb, background:rgb)->None:
    '''
    draw:
        the interface of the Image objet that is drawn on.
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
    fill:
        fill color
    
    draws the circuit element to the Image.
    '''
    draw.polygon(((pos[0], pos[1]+4*size), (pos[0]+4*size, pos[1]), (pos[0]+16*size, pos[1]), (pos[0]+16*size, pos[1]+8*size), (pos[0]+4*size, pos[1]+8*size), (pos[0], pos[1]+4*size)), outline=outline, fill=fill, width=WIDTH)
def _draw(draw:ImageDraw, node:Node, size:int, fill:rgb, outline:rgb, background:rgb)->None:
    '''
    draw:
        the interface of the Image objet that is drawn on.
    pos:
        the position of the top left point of the box in witch the element is drawn in.
    size: 
        A scaling factor
    fill:
        fill color
    
    draws the circuit element to the Image.
    '''
    funs = {'INP':_in_draw,'NOT':_not_draw, 'NOR':_nor_draw, 'OUT':_out_draw, 'BYP':lambda draw, pos, size, fill, ol, bg:None}
    funs[node['type'][:3]](draw, node['__pos'], size, fill, outline, background)

V_SPACING = 20
H_SPACING = 10
SIZE = 5
DEFCOLOR = 'white'
WIDTH = 3

# generator functions

def gen(data:str, colorMap:dict[str, rgb])->Image.Image:
    '''
    data:
        the data of an json file describing a logic circuit
    color:
        a mapping for node ID's to rbg (0-255) int tuple or a PIL color name as strings
    
    return:
        a diagram of the logic circuit described in the data argument as PLI Image object 
    '''
    
    graph = json.loads(data)['graph']
    if graph['version'] == "1":
        # restructure nodes
        nodes:dict[str,  Node] = getNodes(graph)
        
        # rank nodes by edge dependency
        rankedNodes:list[list[str]] = getRankNodes(nodes)
        
        # calc box size for each rank
        rankBoxes:list[tuple[int, int]] = getRankBoxes(nodes, rankedNodes)
        
        # place rank boxes and edges
        edges:dict[str, Edge] = getEdges(nodes, rankedNodes, rankBoxes)
        
        
        width, hight = getImageSize(nodes, rankedNodes, rankBoxes)
        
        
        # make img and draw objects with appropriate size
        return drawImage((width, hight), nodes, edges, colorMap)

    raise Exception(f"unknown graph version '{graph['version']}'")

def getNodes(graph:list[dict[str, str]])->dict[str, Node]:
    '''
    graph:
        a graph element of the json logic circuit
    
    return:
        a dictionary with node id's as keys and Nodes as values.
    '''
    nodes:dict[str,  Node] = {node['id']:{'type':node['type'], 'sources':[], 'targets':[]} for node in graph['nodes']}
    
    # add edges to node
    for edge in graph['edges']:
        nodes[edge['target']]['sources'].append(edge['source'])
        nodes[edge['source']]['targets'].append(edge['target'])
    
    #TODO: ask AG if that is correct like that
    # replace OUTPUT_OR2 nodes
    for nodeID, node in list(nodes.items()):
        if not node['type'].startswith('OUTPUT_OR2'):
            continue
        gateNode = node.copy()
        gateNode['sources'] = [nodeID+'_NOT']
        nodes[nodeID+'_OUTPUT'] = gateNode
        notNode = node.copy()
        notNode['sources'] = [nodeID]
        notNode['targets'] = [nodeID+'_OUTPUT']
        notNode['type'] = 'NOT'
        nodes[nodeID+'_NOT'] = notNode
        node['type'] = 'NOR2'
        node['targets'] = [nodeID+'_NOT']
    
    return nodes

def getRankNodes(nodes:dict[str,  Node])->list[list[str]]:
    '''
    nodes:
        dictionary of id's and nodes
    
    ranks every node by there dependency of other nodes,
    and add nodes so that all nodes are only dependent
    on the rank before and is depended on by the next rank
    
    return:
        a list of list of node id's
        the first index has the input nodes
        the last index has the output nodes
    '''
    unranked = list(nodes.keys())
    
    rankedNodes:list[list[str]] = []
    while len(unranked)>0:
        newRankIds = []
        for nodeID in unranked:
            node = nodes[nodeID]
            if all(node not in unranked for node in node['sources']):
                newRankIds.append(nodeID)
        for id in newRankIds:
            unranked.remove(id)
        # insert bypass nodes for connection with prior nodes
        if len(rankedNodes) > 0:
            allSources:set[str] = set()
            for node in map(nodes.get, unranked):
                allSources|= set(node['sources'])
            bypassMap:dict[str, str] = {}
            for nodeID in rankedNodes[-1]:
                node = nodes[nodeID]
                if nodeID not in allSources:
                    continue
                bypassMap[nodeID] = 'BYPASS_'+nodeID
            for oldID, bypassID in bypassMap.items():
                for nodeID in nodes[oldID]['targets']:
                    if nodeID not in nodes:
                        continue
                    index = nodes[nodeID]['sources'].index(oldID)
                    nodes[nodeID]['sources'][index] = bypassID
                nodes[bypassID] = {'type':'BYPASS', 'sources':[oldID], 'targets':nodes[oldID]['targets']}
                newRankIds.append(bypassID)
        rankedNodes.append(newRankIds)
    return rankedNodes

def getRankBoxes(nodes:dict[str,  Node], rankedNodes:list[list[str]])->list[tuple[int, int]]:
    '''
    nodes:
        dictionary of id's and nodes
    rankedNodes:
        a list of list of node id's
    
    adds a __pos and __box element to each node
    __pos is the position in the box
    __box is the box containing the node
    
    return:
        list of sizes for each rank containing all there nodes
    '''
    rankBoxes:list[tuple[int, int]] = []
    
    # calc box size for each rank
    for rank in rankedNodes:
        x, y = 0, 0
        for node in map(nodes.get, rank):
            node['__pos'] = 0, y
            node['__box'] = _box(node, SIZE)
            x = max(x, node['__box'][0])
            y+= node['__box'][1]+V_SPACING
        rankBoxes.append((x, y-V_SPACING))
    return rankBoxes

def getEdges(nodes:dict[str,  Node], rankedNodes:list[list[str]], rankBoxes:list[tuple[int, int]])->dict[str, Edge]:
    '''
    nodes:
        dictionary of id's and nodes
    rankedNodes:
        a list of list of node id's
    rankBoxes:
        list of sizes for each rank containing all there nodes
    
    changes the __pos for all nodes
    __pos is changed to absolute position in the final image
    
    return:
        a dictionary if node id's as keys and edges as values
        the id is from the node that the edge starts from
    '''
    edges:dict[str, Edge] = {}

    maxY = max(y for _, y in rankBoxes)+2*V_SPACING
    x = H_SPACING
    for box, rank in zip(rankBoxes, rankedNodes):
        boxX, boxY = box
        # place node in rank
        for nodeID, node in zip(rank, map(nodes.get, rank)):
            _, ny = node['__pos']
            node['__pos'] = (x, (maxY-boxY)//2+ny)
            nodes[nodeID] = node
        x+= boxX+H_SPACING
        # connect to source edges
        for nodeID in rank:
            connections = _inputs(nodes[nodeID], SIZE)
            for source, connect in zip(nodes[nodeID]['sources'], connections):
                if connect is None:
                    raise Exception('Should Be Imposable')
                edges[source]['outs'].append(connect)
        x+=H_SPACING*len(rank)
        # place target edges for rank
        for nodeID in rank:
            x-= H_SPACING
            if len(nodes[nodeID]['targets'])==0:
                continue
            edges[nodeID] = {
                '_in':_outputs(nodes[nodeID], SIZE),
                'outs':[],
                'posX':x,
            }
        x+=H_SPACING*len(rank)
    return edges

def getImageSize(nodes:dict[str,  Node], rankedNodes:list[list[str]], rankBoxes:list[tuple[int, int]])->tuple[int, int]:
    '''
    nodes:
        dictionary of id's and nodes
    rankedNodes:
        a list of list of node id's
    rankBoxes:
        list of sizes for each rank containing all there nodes
    
    return:
        width and hight if the image
    '''
    x = H_SPACING
    for box, rank in zip(rankBoxes, rankedNodes):
        boxX, _ = box
        x+= boxX+H_SPACING
        # place target edges for rank
        for nodeID in rank:
            if len(nodes[nodeID]['targets'])==0:
                continue
            x+= H_SPACING
    return x, max(y for _, y in rankBoxes)+2*V_SPACING

def drawImage(imgSize:tuple[int,int], nodes:list[Node], edges:dict[str,Edge], colorMap:dict[str, rgb]):
    '''
    imgSize:
        width and hight if the image
    nodes:
        dictionary of id's and nodes
    edges:
        a dictionary if node id's as keys and edges as values
    colorMap:
        list of sizes for each rank containing all there nodes
    
    return:
        the image as pli image object
    '''
    img = Image.new('RGB', imgSize, (255, 255, 255))
    draw = Draw(img)
    # draw nodes
    for nodeID, node in nodes.items():
        _draw(draw, node, SIZE, colorMap.get(nodeID, DEFCOLOR) , 'black', 'white')

    # draw edges
    for edge in edges.values():
        lines = [edge['_in']]+edge['outs']
        posX = edge['posX']
        for line in lines:
            x, y = line
            draw.line([(x, y), (posX, y)], fill='black', width=WIDTH)
        maxY = max(y for _, y in lines)
        minY = min(y for _, y in lines)
        draw.line([(posX, minY), (posX, maxY)], fill='black', width=WIDTH)
    return img

# run test

if __name__ == '__main__':
    gen(test_data, {}).show()
