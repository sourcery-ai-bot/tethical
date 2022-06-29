from Config import *
from panda3d.core import TransparencyAttrib, Texture
import Sprite

class Matrix(object):

    def __init__(self, battleGraphics, mp):
        self.battleGraphics = battleGraphics
        self.mp = mp
        self.container = render.attachNewNode( "matrixContainer" )

        self.tiles = [
            [[None for _ in range(self.mp['z'])] for _ in range(self.mp['y'])]
            for _ in range(self.mp['x'])
        ]


        for x,xs in enumerate(self.mp['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if self.mp['tiles'][x][y][z] is not None:
                        slope = self.mp['tiles'][x][y][z]['slope']
                        scale = self.mp['tiles'][x][y][z]['scale']
                        depth = self.mp['tiles'][x][y][z]['depth']

                        self.tiles[x][y][z] = loader.loadModel(f"{GAME}/models/slopes/{slope}")
                        self.tiles[x][y][z].reparentTo( self.container )
                        self.tiles[x][y][z].setPos(self.battleGraphics.logic2terrain( (x, y, z+depth+0.05) ))
                        self.tiles[x][y][z].setScale(3.7, 3.7, 6.0/7.0*3.7*scale)
                        self.tiles[x][y][z].setTransparency(TransparencyAttrib.MAlpha)
                        self.tiles[x][y][z].setColor( 0, 0, 0, 0 )

        self.wtex = loader.loadTexture(f'{GAME}/textures/walkable.png')
        self.wtex.setMagfilter(Texture.FTNearest)
        self.wtex.setMinfilter(Texture.FTNearest)

        self.atex = loader.loadTexture(f'{GAME}/textures/attackable.png')
        self.atex.setMagfilter(Texture.FTNearest)
        self.atex.setMinfilter(Texture.FTNearest)

    def placeChars(self, chars):
        self.chars = chars
        self.sprites = {}

        for x,xs in enumerate(self.mp['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if self.mp['tiles'][x][y][z] is not None:
                        slope = self.mp['tiles'][x][y][z]['slope']
                        scale = self.mp['tiles'][x][y][z]['scale']
                        depth = self.mp['tiles'][x][y][z]['depth']

                        if self.mp['tiles'][x][y][z].has_key('char'):
                            charid = self.mp['tiles'][x][y][z]['char']
                            char = self.chars[charid]
                            sprite = Sprite.Sprite(
                                f'{GAME}/textures/sprites/'
                                + char['sprite']
                                + '.png',
                                int(char['direction']),
                            )

                            sprite.animation = 'stand'
                            sprite.node.setPos(self.battleGraphics.logic2terrain((x,y,z)))
                            sprite.node.reparentTo( render )
                            self.sprites[charid] = sprite

    # Draw blue tile zone
    def setupPassiveWalkableZone(self, walkables):
        for x,y,z in walkables:
            self.tiles[x][y][z].setColor(1, 1, 1, 1)
            self.tiles[x][y][z].setTexture(self.wtex)

    # Tag a zone as walkable or active-walkable
    def setupWalkableZone(self, charid, walkables):
        for x,y,z in walkables:
            self.tiles[x][y][z].setColor(1, 1, 1, 1)
            self.tiles[x][y][z].setTexture(self.wtex)
            self.mp['tiles'][x][y][z]['walkablezone'] = charid

    # Draw and tag the red tile zone
    def setupAttackableZone(self, charid, attackables):
        for x,y,z in attackables:
            self.tiles[x][y][z].setColor(1, 1, 1, 1)
            self.tiles[x][y][z].setTexture(self.atex)
            self.mp['tiles'][x][y][z]['attackablezone'] = charid

    # Clear any tile zone
    def clearZone(self):
        for x,xs in enumerate(self.mp['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if self.mp['tiles'][x][y][z] is not None:
                        self.tiles[x][y][z].setColor(0, 0, 0, 0)
                        if self.mp['tiles'][x][y][z].has_key('walkablezone'):
                            del self.mp['tiles'][x][y][z]['walkablezone']
                        if self.mp['tiles'][x][y][z].has_key('attackablezone'):
                            del self.mp['tiles'][x][y][z]['attackablezone']

    # Returns the logic coordinates of a character
    def getCharacterCoords(self, charid):
        for x,xs in enumerate(self.mp['tiles']):
            for y,ys in enumerate(xs):
                for z,zs in enumerate(ys):
                    if (
                        self.mp['tiles'][x][y][z] is not None
                        and self.mp['tiles'][x][y][z].has_key('char')
                        and self.mp['tiles'][x][y][z]['char'] != 0
                        and charid == self.mp['tiles'][x][y][z]['char']
                    ):
                        return (x, y, z)
