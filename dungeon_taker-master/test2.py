import pygame
import character
import enemy
import roomLib
from os import path



def main():
    # Image and Sound directories
    img_dir = path.join(path.dirname(__file__), "images")
    snd_dir = path.join(path.dirname(__file__), "sounds")

    # Initialize pygame
    pygame.init()
    pygame.mixer.init()
    ######################################################################
    #SETTINGS
    screenWidth = 800
    screenHeight = 600
    FPS = 30
    # timeDelay = 50 DEPRECATED





    #Creates window, and clock, sets Icon
    screen = pygame.display.set_mode((screenWidth, screenHeight ))
    pygame.display.set_caption("Dungeon Taker: OTA")
    icon = pygame.image.load('images/oubliette.png')
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()

    ######################################################################

    # Loading game sounds
    bug_splat_sound = pygame.mixer.Sound(path.join(snd_dir, "bug_splat.wav"))
    swoosh_sounds = []
    for snd in ["swoosh_one.wav", "swoosh_two.wav"]:
        swoosh_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

    pygame.mixer.music.load(path.join(snd_dir, "python_project_level.wav"))
    pygame.mixer.music.set_volume(0.8)

    player = character.Character()

    running = True

    def drawHandling():
        #this function handles the drawing in layers
        #RGB VALUES
        screen.fill((0,0,0))
        # pDraw()
        floor_sprites.draw(screen)
        all_sprites.draw(screen)
        wall_sprites.draw(screen)
        collision_sprites.draw(screen)
        attack_sprites.draw(screen)


    # def spawn_handling():
    #     if player.attack == True:
    #         print("spawn thing now")
    #         attack = character.Player_Attack(player.direction, player, 10)
    #         all_sprites.add(attack)
    #         player.attack = False
    #         return(attack)

    # sprite groups! <3 
    floor_sprites = pygame.sprite.Group()
    wall_sprites = pygame.sprite.Group()
    attack_sprites = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    collision_sprites = pygame.sprite.Group()
    enemy_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    #get a list of sprites with built in location information
    flyTest = enemy.Fly()
    enemy_sprites.add(flyTest)
    flyList = [flyTest]
    all_sprites.add(flyTest)
    roomLib.procRoomX()
    dungeonTiles = roomLib.drawTestRoom()
    for tile in dungeonTiles:
        if tile.tile_type == 1:
            floor_sprites.add(tile)
        if tile.tile_type == 0:

            wall_sprites.add(tile)

    coll_boxes = player.coll_list
    for box in coll_boxes:
        collision_sprites.add(box)
    colls = flyTest.coll_boxes
    for box in colls:
        collision_sprites.add(box)

    # testing fly collision

    # Loading area for rooms


    # A state machine for managing the main game loop

    # First level background music to be later menu music
    pygame.mixer.music.play(loops=-1)

    while running:

        clock.tick(FPS)
        # pygame.time.delay(timeDelay) DEPRECATED

        #Update
        
        all_sprites.update()
        # attack = spawn_handling()
        if player.attack == True:
            # print("spawn thing now")
            attack = character.Player_Attack(player.direction, player, 10)
            attack_sprites.add(attack)
            # all_sprites.add(attack)
            player.attack = False
        attack_sprites.update()
        collision_sprites.update()
        wall_sprites.update()
        running = player.game_running
        

        hits = pygame.sprite.groupcollide(collision_sprites, wall_sprites, False, False)
        if player.top_box in hits:
            player.collide_up = True
        else: 
            player.collide_up = False
        if player.bottom_box in hits:
            player.collide_down = True
        else:
            player.collide_down = False
        if player.left_box in hits:
            player.collide_left = True
        else:
            player.collide_left = False
        if player.right_box in hits:
            player.collide_right = True
        else:
            player.collide_right = False

        # and now, for the fly object
        if flyTest.top_box in hits:
            flyTest.go_up = False
        if flyTest.bottom_box in hits:
            flyTest.go_up = True
        if flyTest.left_box in hits:
            flyTest.go_left = False
        if flyTest.right_box in hits:
            flyTest.go_left = True


        ticks = pygame.sprite.groupcollide(enemy_sprites, attack_sprites, True, False)
        if flyTest in ticks:
            bug_splat_sound.play()
            print("YEEEEETT")
        if player in ticks:
            print("scored a hit")
        if ticks:
            print("the fly is hit!")
        # Draw / render
        drawHandling()

        pygame.display.flip()
    
    return ("INTRO")