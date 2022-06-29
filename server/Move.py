import math
import Character

def getadjacentwalkables( party, charid, tiles ):

    walkables = []

    for x1, y1, z1 in tiles:
        for x2, y2 in ( (x1-1, y1), (x1+1, y1), (x1, y1-1), (x1, y1+1) ):
            try:
                t2 = party['map']['tiles'][x2][y2]
                if t2 and x2 >= 0 and y2 >= 0:
                    walkables.extend(
                        (x2, y2, z2)
                        for z2, t3 in enumerate(t2)
                        if t3
                        and (
                            not t3.has_key('char')
                            or party['chars'][t3['char']]['team']
                            == party['chars'][charid]['team']
                            or party['chars'][t3['char']]['hp'] == 0
                        )
                        and t3['walkable']
                        and t3['selectable']
                        and math.fabs(z2 - z1)
                        <= party['chars'][charid]['jump']
                    )

            except:
                pass

    return walkables

def GetWalkables( party, charid ):

    # get the current tile
    tile = Character.Coords( party, charid )
    # recursively add walkables tiles to the list
    walkables = [ tile ]
    for _ in range(1, party['chars'][charid]['move']+1):
        walkables.extend( getadjacentwalkables( party, charid, walkables ) )

    # remove current tile from the list
    filtered_walkables = [walkable for walkable in walkables if walkable != tile]
    walkables = filtered_walkables

    # remove tiles containing characters from the list
    filtered_walkables = []
    for walkable in walkables:
        x, y, z = walkable
        if not party['map']['tiles'][x][y][z].has_key('char'):
            filtered_walkables.append( walkable )
    walkables = filtered_walkables

    return walkables

def IsWalkable( party, charid, x, y, z ):

    return (x, y, z) in GetWalkables( party, charid )

def GetNewDirection( x1, y1, x2, y2 ):

    dx = x2 - x1
    dy = y2 - y1

    if math.fabs(dy) > math.fabs(dx):
        return 1 if dy > 0 else 0
    else:
        return 2 if dx > 0 else 3

def GetPath( party, charid, x1, y1, z1, x2, y2, z2 ):

    tree = { '-'.join(map(str,(x1,y1,z1))) : {} }
    buildtree( party, charid, tree, party['chars'][charid]['move']-1, '-'.join(map(str,(x2,y2,z2))) )

    paths = []
    findpathes( tree, [], paths )

    return [tuple(map(int,tile.split('-'))) for tile in paths[0]]

def buildtree ( party, charid, tree, moves, dest ):

    for k1 in tree.keys():

        for adj in getadjacentwalkables( party, charid, [ tuple(map(int,k1.split('-'))) ] ):
            k2 = '-'.join( map( str, adj ) )

            if k2 == dest:
                tree[k1][k2] = 'X'
                return
            else:
                tree[k1][k2] = {}

        if moves > 0:
            buildtree( party, charid, tree[k1], moves-1, dest )

def findpathes ( tree, p, paths ):

    for k in tree.keys():
        if tree[k] == 'X':
            paths.append( p + [k] )
        else:
            findpathes( tree[k], p + [k], paths )

