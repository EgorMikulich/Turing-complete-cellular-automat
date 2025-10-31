import pygame as pg
import pickle
pg.init()
screen = pg.display.set_mode((pg.display.Info().current_w, pg.display.Info().current_h))

CELL_SIZE = 26
MAP_WIDTH = 300
MAP_HEIGHT = 300
Map_StartX = 1 # Start draw map from this cord
Map_StartY = 1 # Start draw map from this cord
Map_ScaleX = pg.display.Info().current_w // CELL_SIZE + 1 # End draw map when this cord
Map_ScaleY = pg.display.Info().current_h // CELL_SIZE + 1 # End draw map when this cord
Copy_Cords = [0,0,1,1]
Move = 1

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
#n - NOR element
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
def DrawMap():
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
                        case 'd':
                            angle = 90
                        case 'u':
                            angle = 270
                        case 'r':
                            angle = 180
                        case 'l':
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
clock = pg.time.Clock()
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
                        Mainmap[x][y], Condmap[x][y], Rotationmap[x][y] = 'e', '0', 'n'
                    case pg.K_1:
                        Mainmap[x][y], Condmap[x][y], Rotationmap[x][y] = 'l', '0', 'n'
                    case pg.K_2:
                        Mainmap[x][y], Condmap[x][y], Rotationmap[x][y] = 'w', '0', 'l'   
                    case pg.K_3:
                        Mainmap[x][y], Condmap[x][y], Rotationmap[x][y] = 'n', '1', 'n'
                    case pg.K_4:
                        Mainmap[x][y], Condmap[x][y], Rotationmap[x][y] = 'p', '0', 'l'
                    case pg.K_a:
                        if Mainmap[x][y] in ('w','p'):
                            Rotationmap[x][y] = 'l'
                    case pg.K_d:
                        if Mainmap[x][y] in ('w','p'):
                            Rotationmap[x][y] = 'r'
                    case pg.K_s:
                        if Mainmap[x][y] in ('w','p'):
                            Rotationmap[x][y] = 'd'
                    case pg.K_w:
                        if Mainmap[x][y] in ('w','p'):
                            Rotationmap[x][y] = 'u'
                    case pg.K_RIGHT:
                        if Map_ScaleX + Move <= MAP_WIDTH - 1:
                            Map_ScaleX, Map_StartX = Map_ScaleX + Move, Map_StartX + Move
                    case pg.K_LEFT:
                        if Map_StartX - Move >= 1:
                            Map_StartX, Map_ScaleX = Map_StartX - Move, Map_ScaleX - Move
                    case pg.K_UP:
                        if Map_StartY - Move >= 1:
                            Map_ScaleY, Map_StartY = Map_ScaleY - Move, Map_StartY - Move
                    case pg.K_DOWN:
                        if Map_ScaleY + Move <= MAP_HEIGHT - 1:
                            Map_ScaleY, Map_StartY = Map_ScaleY + Move, Map_StartY + Move
                    case pg.K_SPACE:
                        Solution = True
                    case pg.K_ESCAPE:
                        Game = False
                    case pg.K_j:
                        Copy_Cords[0] = x
                        Copy_Cords[1] = y
                    case pg.K_k:
                        Copy_Cords[2] = x
                        Copy_Cords[3] = y
                    case pg.K_l:
                        Counter_X = 0
                        for i in range(Copy_Cords[0],Copy_Cords[2] + 1):
                            Counter_Y = 0
                            for j in range(Copy_Cords[1],Copy_Cords[3] + 1):
                                Mainmap[x + Counter_X][y + Counter_Y] = Mainmap[i][j]
                                Condmap[x + Counter_X][y + Counter_Y] = Condmap[i][j]
                                Rotationmap[x + Counter_X][y + Counter_Y] = Rotationmap[i][j]
                                Counter_Y += 1
                            Counter_X += 1
                    case pg.K_n:
                        if Move > 1:
                            Move -= 1
                    case pg.K_m:
                        if Move < 30:
                            Move += 1
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
                if Mainmap[x][y] != 'e':
                    Check = 2 if Mainmap[x][y] == 'p' else 1
                        

                    signals = {"r": '1' if Condmap[x + Check][y] == '1' and ((Mainmap[x + Check][y] in ('l','n')) or (Rotationmap[x + Check][y] != 'l')) else '0',
                               "u": '1' if Condmap[x][y - Check] == '1' and ((Mainmap[x][y - Check] in ('l','n')) or (Rotationmap[x][y - Check] != 'd')) else '0',
                               "l": '1' if Condmap[x - Check][y] == '1' and ((Mainmap[x - Check][y] in ('l','n')) or (Rotationmap[x - Check][y] != 'r')) else '0',
                               "d": '1' if Condmap[x][y + Check] == '1' and ((Mainmap[x][y + Check] in ('l','n')) or (Rotationmap[x][y + Check] != 'u')) else '0'
                               }

                    if Mainmap[x][y] in ('w','p'):
                        UpdateCondmap[x][y] = signals[Rotationmap[x][y]]

                    elif Mainmap[x][y] == 'n':
                        UpdateCondmap[x][y] = '0' if '1' in signals.values() else '1'

        for y in range(1,MAP_HEIGHT - 1):
            for x in range(1,MAP_WIDTH - 1):
                Condmap[x][y] = UpdateCondmap[x][y]
    DrawMap()
    clock.tick(10)
