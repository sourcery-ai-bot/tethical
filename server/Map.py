from panda3d.core import loadPrcFile
loadPrcFile("config.prc")
from pandac.PandaModules import *
import json

GAME = ConfigVariableString('game', 'fft').getValue()

def load(name):
    with open(f'{GAME}/maps/{name}.json', 'r') as f:
        m = json.loads(f.read())
    tiles = [
        [[None for _ in range(m['z'])] for _ in range(m['y'])]
        for _ in range(m['x'])
    ]

    for t in m['tiles']:
        tiles[int(t['x'])][int(t['y'])][int(t['z'])] = t

    m['tiles'] = tiles

    return m
