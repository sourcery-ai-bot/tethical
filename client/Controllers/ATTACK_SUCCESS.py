from direct.interval.IntervalGlobal import Sequence, Func
import SequenceBuilder

def execute(client, iterator):
    charid = iterator.getString()
    targetid = iterator.getString()
    damages = iterator.getUint8()

    charid = iterator.getString()
    target = client.party['chars'][targetid]
    target['hp'] = target['hp'] - damages
    target['hp'] = max(target['hp'], 0)
    seq = Sequence()
    seq.append( SequenceBuilder.characterAttackSequence(client, charid, targetid) )
    seq.append( Func(client.send.UPDATE_PARTY) )
    seq.start()