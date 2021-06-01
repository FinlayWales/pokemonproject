import pygame
from pygame.locals import *
import sys
import json
import math
from imports.functions import *

pokedex = json.loads(open("PokedexData/pokedex.json", encoding="utf8").read())
natures = json.loads(open("PokedexData/natures.json", encoding="utf8").read())
moves = json.loads(open("PokedexData/moves.json", encoding="utf8").read())
movelist = json.loads(open("PokedexData/movelist.json", encoding="utf8").read())
learnset = json.loads(open("PokedexData/learnset.json", encoding="utf8").read())
typeeff = json.loads(open("PokedexData/typeeff.json", encoding="utf8").read())

BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

pygame.init()
pygame.font.init()
thefont = pygame.font.SysFont('Arial', 20)

DISPLAYSURF = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Pokemon ???")

FPS = pygame.time.Clock()

class pokemon(pygame.sprite.Sprite):
    
    def __init__(self, pkmnID, level, iv, ev, moves, nature, shiny, imageExt=""):
        super().__init__()
        self.name = pokedex[pkmnID - 1]["name"]["english"]
        self.id = pkmnID
        self.level = level
        
        naturespread = natures[0][nature]
        baseStats = pokedex[pkmnID - 1]["base"]
        HP = math.floor(((2 * baseStats["HP"] + iv[0] + (ev[0]/4)) * level) / 100) + level + 10
        ATK = math.floor((math.floor(((2 * baseStats["Attack"] + iv[1] + (ev[1]/4)) * level) / 100) + 5) * naturespread[0])
        DEF = math.floor((math.floor(((2 * baseStats["Defense"] + iv[2] + (ev[2]/4)) * level) / 100) + 5) * naturespread[1])
        SPATK = math.floor((math.floor(((2 * baseStats["Sp. Attack"] + iv[3] + (ev[3]/4)) * level) / 100) + 5) * naturespread[2])
        SPDEF = math.floor((math.floor(((2 * baseStats["Sp. Defense"] + iv[4] + (ev[4]/4)) * level) / 100) + 5) * naturespread[3])
        SPD = math.floor((math.floor(((2 * baseStats["Speed"] + iv[5] + (ev[5]/4)) * level) / 100) + 5) * naturespread[4])
        
        self.stats = [HP, ATK, DEF, SPATK, SPDEF, SPD]
        self.maxhealth = self.stats[0]

        self.moveset = moves

        self.statchanges = [0, 0, 0, 0, 0, 0]

        self.pkmnimage = pygame.image.load("Sprites/Pokemon/" + str(pkmnID).rjust(3, "0") + imageExt + ".png").convert()
        self.pkmnimage.set_colorkey(self.pkmnimage.get_at((0, 0)))
        
        self.frontimage = pygame.Surface((64, 64), pygame.SRCALPHA)
        if shiny == True:
            self.frontimage.blit(self.pkmnimage, (-64, 0))
        else:
            self.frontimage.blit(self.pkmnimage, (0, 0))

        self.backimage = pygame.Surface((64, 64), pygame.SRCALPHA)
        if shiny == True:
            self.backimage.blit(self.pkmnimage, (-192, 0))
        else:
            self.backimage.blit(self.pkmnimage, (-128, 0))

        #Icons don't exist for all Pokemon yet, uncomment this once they do
        #self.iconimage = pygame.image.load("Sprites/Icons/" + str(pkmnID).rjust(3, "0") + ".png").convert()
        #self.iconimage.set_colorkey(self.iconimage.get_at((0, 0)))
        #self.iconsurf = pygame.Surface((32, 32), pygame.SRCALPHA)
        #self.iconsurf.blit(self.iconimage, (0, 0))

    def validatemoves(self):
        pokemonlearnset = learnset["".join(filter(str.isalnum, self.name.lower()))]
        for move in self.moveset:
            alnummove = "".join(filter(str.isalnum, move.lower()))
            if move not in movelist:
                print("Warning: The move \"" + move + "\" does not exist.")
            elif alnummove not in list(flatten(pokemonlearnset["level"].values())) + \
                    pokemonlearnset["tm"] + pokemonlearnset["egg"] + pokemonlearnset["tutor"] + \
                    pokemonlearnset["dreamWorld"] + pokemonlearnset["event"]:
                print("Warning: The pokemon \"" + self.name + "\" cannot learn the move \"" + move + "\"")
            elif alnummove not in list(flatten({k: v for k, v in pokemonlearnset["level"].items() if int(k) <= self.level}.values())) + \
                    pokemonlearnset["tm"] + pokemonlearnset["egg"] + pokemonlearnset["tutor"] + \
                    pokemonlearnset["dreamWorld"] + pokemonlearnset["event"]:
                print("Warning: The pokemon \"" + self.name + "\" is not high enough level to learn the move \"" + move + "\"")

    def losehealth(self, health):
        self.maxhealth -= health

    def usemove(self, moveindex, target):
        globalmoveindex = movelist.index(self.moveset[moveindex])
        movedata = moves[globalmoveindex]
        universalatk = 0

        stab = 1.5 if movedata["type"] in pokedex[self.id - 1]["type"] else 1

        typeeffect = 1
        attackingtype = typeeff[movedata["type"]]
        for pkmntype in pokedex[target.id - 1]["type"]:
            typeeffect *= attackingtype[pkmntype]
        
        modifier = stab * typeeffect
        
        attackused = movedata["category"]
        
        if attackused == "Physical":
            universalatk = self.stats[1]
        elif attackused == "Special":
            universalatk = self.stats[3]
        elif attackused == "Status":
            return False
        else:
            print("Welp, I fucked something up now didn't I?")
        
        damage = (modifier * math.floor((math.floor(2 * self.level) // 5) + 2) * movedata["power"] * universalatk) // (modifier * 50)

        target.recievedamage(damage, attackused)

    def recievedamage(self, damage, deftype):
        universaldef = 0
        
        if deftype == "Physical":
            universaldef = self.stats[2]
        elif deftype == "Special":
            universaldef = self.stats[4]
        else:
            print("Welp, I fucked something up now didn't I?")
        
        damagetaken = math.floor(damage * (1 / universaldef))
        if damagetaken == 0:
            damagetaken = 1
        
        self.losehealth(damagetaken)

    def drawfront(self, surface, xpos, ypos):
        surface.blit(pygame.transform.scale(self.frontimage, (512, 512)), (xpos, ypos))
        
    def drawback(self, surface, xpos, ypos):
        surface.blit(pygame.transform.scale(self.backimage, (512, 512)), (xpos, ypos))

    def drawicon(self, surface, xpos, ypos):
        surface.blit(pygame.transform.scale(self.iconsurf, (64, 64)), (xpos, ypos))

pkmntest = pokemon(
    448,
    100,
    [31, 31, 31, 31, 31, 31],
    [84, 84, 84, 84, 84, 84],
    ["Aura Sphere", "Swords Dance", "Flash Cannon", "Dark Pulse"],
    "Jolly",
    False
)
DISPLAYSURF.blit(pygame.transform.scale(pygame.image.load("Sprites/backgroundtest.png"), DISPLAYSURF.get_size()), (0, 0))
pkmntest.drawfront(DISPLAYSURF, DISPLAYSURF.get_width() - 650, 0)
pkmntest.drawback(DISPLAYSURF, 0, DISPLAYSURF.get_height() - 512)

#Tests move validation
pkmntest.validatemoves()

#Tests moves
print(pkmntest.maxhealth)
pkmntest.usemove(1, pkmntest)
print(pkmntest.maxhealth)

while True:
    
    pygame.display.update()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            
    FPS.tick(60)
