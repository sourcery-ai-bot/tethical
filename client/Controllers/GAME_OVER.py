from Config import GAME
import GUI

def execute(client, iterator):
    if client.charbars:
        client.charbars.hide()
    if client.charcard:
        client.charcard.hide()
    for charid in client.matrix.sprites:
        if client.matrix.sprites[charid].animation == 'walk':
            client.updateSpriteAnimation(charid, 'stand')
    client.music.stop()
    client.music = base.loader.loadSfx(f'{GAME}/music/33.ogg')
    client.music.play()
    GUI.GameOver(client.end)