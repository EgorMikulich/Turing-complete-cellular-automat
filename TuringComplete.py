import pygame as pg
import pickle
pg.init()
screen = pg.display.set_mode((pg.display.Info().current_w, pg.display.Info().current_h))

CELL_SIZE = 32 size of cells (default - 32)
MAP_WIDTH = 300
MAP_HEIGHT = 300
Map_StartX = 1 # Start draw map from this cord
Map_StartY = 1 # Start draw map from this cord
Map_ScaleX = pg.display.Info().current_w // CELL_SIZE + 1 # End draw map when this cord
Map_ScaleY = pg.display.Info().current_h // CELL_SIZE + 1 # End draw map when this cord

#import and tune sprites
Sprites = [0,1,2,3,4,5,6,7,8]
Sprites[0] = pg.image.load("TuringData\\Textures\\Empty.png").convert()
Sprites[1] = pg.image.load("TuringData\\Textures\\LeverOFF.png").convert()
Sprites[2] = pg.image.load("TuringData\\Textures\\LeverON.png").convert()
Sprites[3] = pg.image.load("TuringData\\Textures\\NOOFF.png").convert()
Sprites[4] = pg.image.load("TuringData\\Textures\\NOON.png").convert()
Sprites[5] = pg.image.load("TuringData\\Textures\\WireOFF.png").convert()
Sprites[6] = pg.image.load("TuringData\\Textures\\WireON.png").convert()
Sprites[7] = pg.image.load("TuringData\\Textures\\WireplusOFF.png").convert()
Sprites[8] = pg.image.load("TuringData\\Textures\\WireplusON.png").convert()
for i in range(9):
    Sprites[i] = pg.transform.scale(Sprites[i],(CELL_SIZE,CELL_SIZE))

#e - empty
#l - lever
#w - wire
#n - NO element
#p - wire plus
Mainmap = [['e' for i in range(MAP_HEIGHT)] for j in range(MAP_WIDTH)]
#n - no rotation
#u - up
#d - down
#l - left
#r - right
Rotationmap = [['n' for i in range(MAP_HEIGHT)] for j in range(MAP_WIDTH)]
#0 - off
#1 - onn
Condmap = [['0' for i in range(MAP_HEIGHT)] for j in range(MAP_WIDTH)]
UpdateCondmap = [['0' for i in range(MAP_HEIGHT)] for j in range(MAP_WIDTH)]

# output function
def DrawMap(Mainmap,Rotationmap,Condmap):
    x,y = 0,0
    for i in range(Map_StartY,Map_ScaleY):
        for j in range(Map_StartX,Map_ScaleX):              
            if Condmap[j][i] == '0':
                numbers = [1,3,5,7]
            else:
                numbers = [2,4,6,8]
                
            match Mainmap[j][i]:
                case 'e':
                    screen.blit(Sprites[0],(x * CELL_SIZE,y * CELL_SIZE))
                case 'l':
                    screen.blit(Sprites[numbers[0]],(x  * CELL_SIZE,y  * CELL_SIZE))
                case 'n':
                    screen.blit(Sprites[numbers[1]],(x * CELL_SIZE,y * CELL_SIZE))

                case _:
                    match Rotationmap[j][i]:
                        case 'u':
                            angle = 90
                        case 'd':
                            angle = 270
                        case 'l':
                            angle = 180
                        case _:
                            angle = 0

                    if Mainmap[j][i] == 'w':
                        screen.blit(pg.transform.rotate(Sprites[numbers[2]],angle),(x  * CELL_SIZE, y  * CELL_SIZE))
                    else:
                        screen.blit(pg.transform.rotate(Sprites[numbers[3]],angle),(x  * CELL_SIZE, y  * CELL_SIZE))
            x += 1
        x = 0
        y += 1
    pg.display.flip()

Game = True
Solution = False
# main cycle
while Game:
    # modificate map     
    if not Solution:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                x, y = pg.mouse.get_pos()
                x = x // CELL_SIZE + 1 * Map_StartX
                y = y // CELL_SIZE + 1 * Map_StartY
                match event.key:
                    case pg.K_q:
                        if Mainmap[x][y] != 'e':
                            if Condmap[x][y] == '0':
                                Condmap[x][y] = '1'
                            else:
                                Condmap[x][y] = '0'
                    case pg.K_e:
                        Mainmap[x][y] = 'e'
                        Condmap[x][y] = '0'   
                        Rotationmap[x][y] = 'n'
                    case pg.K_1:
                        Mainmap[x][y] = 'l'
                        Condmap[x][y] = '0'   
                        Rotationmap[x][y] = 'n'
                    case pg.K_2:
                        Mainmap[x][y] = 'w'                        
                        Condmap[x][y] = '0'
                        Rotationmap[x][y] = 'r'   
                    case pg.K_3:
                        Mainmap[x][y] = 'n'                      
                        Condmap[x][y] = '1'
                        Rotationmap[x][y] = 'n'
                    case pg.K_4:
                        Mainmap[x][y] = 'p'                        
                        Condmap[x][y] = '0'
                        Rotationmap[x][y] = 'r'
                    case pg.K_a:
                        Rotationmap[x][y] = 'r'
                    case pg.K_d:
                        Rotationmap[x][y] = 'l'
                    case pg.K_s:
                        Rotationmap[x][y] = 'u'
                    case pg.K_w:
                        Rotationmap[x][y] = 'd'
                    case pg.K_RIGHT:
                        if Map_ScaleX < MAP_WIDTH - 1:
                            Map_ScaleX += 1
                            Map_StartX += 1
                    case pg.K_LEFT:
                        if Map_StartX > 1:
                            Map_StartX -= 1
                            Map_ScaleX -= 1
                    case pg.K_UP:
                        if Map_StartY > 1:
                            Map_ScaleY -= 1
                            Map_StartY -= 1
                    case pg.K_DOWN:
                        if Map_ScaleY < MAP_HEIGHT - 1:
                            Map_ScaleY += 1
                            Map_StartY += 1
                    case pg.K_SPACE:
                        Solution = True
                    case pg.K_ESCAPE:
                        Game = False
                    case pg.K_0:
                        with open(r"C:\\Users\\mikul\\Projects\\TuringData\\Saves\\Save_1\\main.pkl","wb") as m:
                            pickle.dump(Mainmap,m)
                        with open(r"C:\\Users\\mikul\\Projects\\TuringData\\Saves\\Save_1\\rot.pkl","wb") as r:
                            pickle.dump(Rotationmap,r)
                        with open(r"C:\\Users\\mikul\\Projects\\TuringData\\Saves\\Save_1\\cond.pkl","wb") as c:
                            pickle.dump(Condmap,c)
                    case pg.K_9:
                        with open(r"C:\\Users\\mikul\\Projects\\TuringData\\Saves\\Save_1\\main.pkl","rb") as m:
                            Mainmap = pickle.load(m)
                        with open(r"C:\\Users\\mikul\\Projects\\TuringData\\Saves\\Save_1\\rot.pkl","rb") as r:
                            Rotationmap = pickle.load(r)
                        with open(r"C:\\Users\\mikul\\Projects\\TuringData\\Saves\\Save_1\\cond.pkl","rb") as c:
                            Condmap = pickle.load(c)

    #execution
    else:
        for y in range(1,MAP_HEIGHT - 1):
            for x in range(1,MAP_WIDTH - 1):
                UpdateCondmap[x][y] = Condmap[x][y]

        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                Solution = False 

        for y in range(1,MAP_HEIGHT - 1):
            for x in range(1,MAP_WIDTH - 1):
                Check = 1
                if Mainmap[x][y] == 'p':
                    Check = 2

                signalright = '0'
                signalup = '0'
                signalleft = '0'
                signaldown = '0'
                if Condmap[x + Check][y] == '1':
                    match Mainmap[x + Check][y]:
                        case 'l' | 'n':
                            signalright = '1'
                        case _: 
                            if Rotationmap[x + Check][y] != 'r':
                                signalright = '1'

                if Condmap[x][y - Check] == '1':
                    match Mainmap[x][y - Check]:
                        case 'l' | 'n':
                            signalup = '1'
                        case _:
                            if Rotationmap[x][y - Check] != 'u':
                                signalup = '1'

                if Condmap[x - Check][y] == '1':
                    match Mainmap[x - Check][y]:
                        case 'l' | 'n':
                            signalleft = '1'
                        case _:
                            if Rotationmap[x - Check][y] != 'l':
                                signalleft = '1'

                if Condmap[x][y + Check] == '1':
                    match Mainmap[x][y + Check]:
                        case 'l' | 'n':
                            signaldown = '1'
                        case _:
                            if Rotationmap[x][y + Check] != 'd':
                                signaldown = '1'


                if Mainmap[x][y] == 'w' or Mainmap[x][y] == 'p':
                    match Rotationmap[x][y]:
                        case 'r':
                            UpdateCondmap[x][y] = signalleft
                        case 'u':
                            UpdateCondmap[x][y] = signaldown
                        case 'l':
                            UpdateCondmap[x][y] = signalright
                        case 'd':
                            UpdateCondmap[x][y] = signalup

                elif Mainmap[x][y] == 'n':
                    if signalright == '1' or signalleft == '1' or signaldown == '1' or signalup == '1':
                        UpdateCondmap[x][y] = '0'
                    else:
                        UpdateCondmap[x][y] = '1'

        for y in range(1,MAP_HEIGHT - 1):
            for x in range(1,MAP_WIDTH - 1):
                Condmap[x][y] = UpdateCondmap[x][y]
    DrawMap(Mainmap,Rotationmap,Condmap)

    pg.time.wait(100)
