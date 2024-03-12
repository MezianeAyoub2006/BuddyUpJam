import xmltodict, pyperclip, math, pygame
from engine.tilemap.management.pattern import *

def list_to_matrix(list, xcount):
    matrix=[]
    for i in range(len(list)//xcount):
        matrix.append(list[i*xcount: (i+1)*xcount])
    return matrix

def tiled_to_pattern(path, scaling=1):
    pattern = []
    with open(path, "r") as file:
        data = xmltodict.parse(file.read())
        if "map" in data:
            data = data["map"]
    if isinstance(data["layer"], list):
        for layer in data["layer"]:
            modified_layer = [None if int(i) == 0 else int(i)-1 for i in layer["data"]["#text"].strip().split(",")]
            pattern.append({"data" : list_to_matrix(modified_layer, int(layer["@width"])), "meta_data" : {"name" : layer["@name"],"objects" : []}})
    else:
        modified_layer = [None if int(i) == 0 else int(i)-1 for i in data["layer"]["data"]["#text"].strip().split(",")]
        pattern.append({"data" : list_to_matrix(modified_layer, int(data["layer"]["@width"])), "meta_data" : {"name" : data["layer"]["@name"], "objects" : []}})
    if isinstance(data["objectgroup"], list):
        for group in data["objectgroup"]:
            objs = []
            for object in group["object"]:    
                if "@gid" in object:
                    objs.append({"id" : int(object["@gid"]) - 1, "pos" : (math.floor(float(object["@x"])), math.floor(float(object["@y"])))})
                elif "@width" in object:
                    print(object["@width"])
                    objs.append(pygame.Rect(math.floor(float(object["@x"]))*scaling, math.floor(float(object["@y"]))*scaling, math.ceil(float(object["@width"]))*scaling, math.ceil(float(object["@height"]))*scaling))
            pattern.append({"data" : None, "meta_data" : {"name" : group["@name"], "objects" : objs}})
    return Pattern(pattern)

def load_tiled(map_path, tileset_path, scaling=1):
    pattern = tiled_to_pattern(map_path, scaling)
    with open(map_path, "r") as file:
        file_data = xmltodict.parse(file.read())["map"]
        size = (int(file_data["@width"]), int(file_data["@height"]))
        pyperclip.copy(str(file_data))
    with open(tileset_path, "r") as file:
        tileset_data = xmltodict.parse(file.read())["tileset"]
        if not "tile" in tileset_data:
            tileset_data["tile"] = []
    return {"size" : size, "pattern" : pattern, "tileset_data" : tiled_process_tileset_data(tileset_data["tile"])}

def tiled_process_tileset_data(tileset_data):
        data = {}
        for tile in tileset_data:
            data[int(tile["@id"])] = {}
            if isinstance(tile["properties"]["property"], list):
                for property in tile["properties"]["property"]:
                    data[int(tile["@id"])][property["@name"]] = property["@value"]
            if isinstance(tile["properties"]["property"], dict):
                data[int(tile["@id"])][tile["properties"]["property"]["@name"]] = tile["properties"]["property"]["@value"]
        return data