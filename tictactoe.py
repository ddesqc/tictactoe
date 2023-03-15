import pygame, sys, random
from pygame import mixer
import numpy as np


pygame.init()
sys.setrecursionlimit(1500)

def setres(res):
    global WIDTH, HEIGHT, frame, STANDARD, LIGN_WIDT,WIN_LIGN_WIDTH,font,font1,font2,CIRCLE_R,CIRCLE_WIDTH,CIRCLE_WIDTH,CROSS_WIDTH,SPACE,FONT,ROWS,COLS
    WIDTH = HEIGHT = res
    ROWS = COLS = 3
    FONT = "data\kimberley bl.ttf"
    font, font1, font2 = pygame.font.Font(FONT, WIDTH//15), pygame.font.Font(FONT, WIDTH//10), pygame.font.Font(FONT, WIDTH//45)
    LIGN_WIDT = 5
    WIN_LIGN_WIDTH = WIDTH//60
    CIRCLE_R = WIDTH//9
    CIRCLE_WIDTH = WIDTH//45
    #Taille d'un cube
    STANDARD = WIDTH//ROWS
    CROSS_WIDTH = WIDTH//36
    SPACE = WIDTH//16
    frame = pygame.display.set_mode((WIDTH,HEIGHT),pygame.HWSURFACE|pygame.DOUBLEBUF)
    pygame.display.update()


setres(900)
# music
mixer.music.load("data\C418-Sweden.mp3")
mixer.music.play(-1)

click_sound = mixer.Sound("data\click.wav")

BLANC = (255,255,255)
FRAME_COLOR = (1,1,1)
MAIN_LIGN_COLOR = (169,169,169)
CIRCLE_COLOR = (147,112,219)
CROSS_COLOR = (0,128,128)
BG_SCORE_COLOR = (100,100,100)

TEXT_COLOR = (255,255,5)

#Couleur de la ligne de Victoire
CIRCLE_COLOR_WIN = (255,250,205)
CROSS_COLOR_WIN = (220,20,60)
#nom de la fênetre
pygame.display.set_caption("TIC TAC TOE")
gicon = pygame.image.load("data\icon.png")
pygame.display.set_icon(gicon)
board = np.zeros((ROWS,COLS))

def cadrage():
    #Verticales
    pygame.draw.line(frame, MAIN_LIGN_COLOR, (STANDARD,0), (STANDARD,HEIGHT),LIGN_WIDT)
    pygame.draw.line(frame, MAIN_LIGN_COLOR, (2*STANDARD,0), (2*STANDARD,HEIGHT),LIGN_WIDT)
    #Horizontales
    pygame.draw.line(frame, MAIN_LIGN_COLOR, (0,STANDARD), (WIDTH,STANDARD),LIGN_WIDT)
    pygame.draw.line(frame, MAIN_LIGN_COLOR, (0,2*STANDARD), (WIDTH,2*STANDARD),LIGN_WIDT)


def figures():
    for row  in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 1:
                pygame.draw.circle(frame, CIRCLE_COLOR, (int(col*STANDARD+STANDARD//2), int(row*STANDARD+STANDARD//2)), CIRCLE_R, CIRCLE_WIDTH)
            elif board[row][col] == 2 :
                pygame.draw.line(frame, CROSS_COLOR, (col * STANDARD + SPACE,row * STANDARD + STANDARD - SPACE), (col* STANDARD+ STANDARD-SPACE,row * STANDARD+SPACE),CROSS_WIDTH)
                pygame.draw.line(frame, CROSS_COLOR, (col * STANDARD+SPACE,row * STANDARD+SPACE), (col* STANDARD+STANDARD-SPACE,row * STANDARD +STANDARD-SPACE),CROSS_WIDTH)
                

def intent(row, col, player):
    board[row][col] = player


def free_square(row, col):
    if board[row][col] == 0:
        return True
    else:
        return False


def board_full(count):
    if count < ROWS*COLS:
        return False
    else:
        return True


def check_winner(player):
    for col in range(COLS):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            ligne_verticale(col,player)
            return True
    for row in range(ROWS):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            ligne_horizontale(row,player)
            return True
    if board[2][0] == player and board[1][1] == player and board[0][2] == player:
        diag_crois(player)
        return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        diag_decrois(player)
        return True
    return False


def check_draw():
    if check_winner(1) or check_winner(2):
        return False
    for row  in range(ROWS):
        for col in range(COLS):
            if board[row][col] == 0 or check_winner(1) == True or check_winner(2) == True:
                return False
    return True


def ligne_verticale(col, player):
    X = col * STANDARD + STANDARD//2
    if player == 1:
        couleur = CIRCLE_COLOR_WIN
    elif player == 2:
        couleur = CROSS_COLOR_WIN
    pygame.draw.line(frame, couleur, (X,15),(X,HEIGHT-15),WIN_LIGN_WIDTH)


def ligne_horizontale(row,player):
    Y = row * STANDARD + STANDARD//2
    if player == 1:
        couleur = CIRCLE_COLOR_WIN
    elif player == 2:
        couleur = CROSS_COLOR_WIN
    pygame.draw.line(frame,couleur,(15,Y),(WIDTH-15,Y),WIN_LIGN_WIDTH)


def diag_crois(player):
    if player == 1:
        couleur = CIRCLE_COLOR_WIN
    elif player == 2:
        couleur = CROSS_COLOR_WIN
    pygame.draw.line(frame,couleur,(15, HEIGHT -15),(WIDTH -15,15),WIN_LIGN_WIDTH)


def diag_decrois(player):
    if player == 1:
        couleur = CIRCLE_COLOR_WIN
    elif player == 2:
        couleur = CROSS_COLOR_WIN
    pygame.draw.line(frame,couleur,(15,15),(WIDTH-15,HEIGHT-15),WIN_LIGN_WIDTH)


def restart():
    frame.fill(FRAME_COLOR)
    cadrage()
    for row in range(ROWS):
        for col in range(COLS):
            board[row][col] = 0
    

def draw_scoreboard(draw,winj1,winj2):
    scoreboard = font2.render(f"SCOREBOARD : NULLE = {draw}, Joueur 1 = {winj1} victoires, Joueur 2 = {winj2} victoires",True,TEXT_COLOR)
    text_rect = scoreboard.get_rect(center=(WIDTH//2, WIDTH//45))
    BG_BLOCK = pygame.Surface(scoreboard.get_size())
    BG_BLOCK.fill(BG_SCORE_COLOR)
    BG_BLOCK.blit(scoreboard, (0, 0))
    frame.blit(BG_BLOCK, text_rect)


def draw_scoreboardIA1(draw,winj,winia):
    scoreboard = font2.render(f"SCOREBOARD : NULLE = {draw}, Joueur = {winj} victoires, IA = {winia} victoires",True,TEXT_COLOR)
    text_rect = scoreboard.get_rect(center=(WIDTH//2, WIDTH//45))
    BG_BLOCK = pygame.Surface(scoreboard.get_size())
    BG_BLOCK.fill(BG_SCORE_COLOR)
    BG_BLOCK.blit(scoreboard, (0, 0))
    frame.blit(BG_BLOCK, text_rect)


def info():
    info = font2.render("ESPACE pour rejouer ESCAPE pour retourner au menu", True,TEXT_COLOR)
    text_rect = info.get_rect(center=(WIDTH//2, HEIGHT-HEIGHT//45))
    BG_BLOCK = pygame.Surface(info.get_size())
    BG_BLOCK.fill(BG_SCORE_COLOR)
    BG_BLOCK.blit(info, (0, 0))
    frame.blit(BG_BLOCK, text_rect)


def draw_draw():
    draw = font.render("NULLE!", True, TEXT_COLOR)
    text_rect = draw.get_rect(center=(WIDTH//2, HEIGHT//2))
    BG_BLOCK = pygame.Surface(draw.get_size())
    BG_BLOCK.fill(BG_SCORE_COLOR)
    BG_BLOCK.blit(draw, (0, 0))
    frame.blit(BG_BLOCK, text_rect)
    info()


def draw_win_j1():
    j1 = font.render("VICTOIRE JOUEUR 1!", True, TEXT_COLOR)
    text_rect = j1.get_rect(center=(WIDTH//2, HEIGHT//2))
    BG_BLOCK = pygame.Surface(j1.get_size())
    BG_BLOCK.fill(BG_SCORE_COLOR)
    BG_BLOCK.blit(j1, (0, 0))
    frame.blit(BG_BLOCK, text_rect)
    info()

def draw_win_j():
    j1 = font.render("VICTOIRE DU JOUEUR!", True, TEXT_COLOR)
    text_rect = j1.get_rect(center=(WIDTH//2, HEIGHT//2))
    BG_BLOCK = pygame.Surface(j1.get_size())
    BG_BLOCK.fill(BG_SCORE_COLOR)
    BG_BLOCK.blit(j1, (0, 0))
    frame.blit(BG_BLOCK, text_rect)
    info()


def draw_win_ai():
    j2 = font.render("VICTOIRE DE L'IA!", True, TEXT_COLOR)
    text_rect = j2.get_rect(center=(WIDTH//2, HEIGHT//2))
    BG_BLOCK = pygame.Surface(j2.get_size())
    BG_BLOCK.fill(BG_SCORE_COLOR)
    BG_BLOCK.blit(j2, (0, 0))
    frame.blit(BG_BLOCK, text_rect)
    info()


def draw_win_j2():
    j2 = font.render("VICTOIRE JOUEUR 2!", True, TEXT_COLOR)
    text_rect = j2.get_rect(center=(WIDTH//2, HEIGHT//2))
    BG_BLOCK = pygame.Surface(j2.get_size())
    BG_BLOCK.fill(BG_SCORE_COLOR)
    BG_BLOCK.blit(j2, (0, 0))
    frame.blit(BG_BLOCK, text_rect)
    info()


pygame.display.update()

click = False
def main_menu():
    global click
    while True:
        frame.fill(FRAME_COLOR)
        titre = font1.render("TIC TAC TOE", True, TEXT_COLOR)
        text_rect = titre.get_rect()
        text_rect.center = ((WIDTH//2,WIDTH//13))
        frame.blit(titre, text_rect)

        mx, my = pygame.mouse.get_pos()
 
        button_1 = pygame.Rect(0, 0, WIDTH//2, HEIGHT//9)
        button_2 = pygame.Rect(0, 0, WIDTH//2, HEIGHT//9)
        button_3 = pygame.Rect(0, 0, WIDTH//2, HEIGHT//9)
        button_4 = pygame.Rect(0, 0, WIDTH//2, HEIGHT//9)

        button_1.center = (WIDTH//2, HEIGHT/4.5)
        button_2.center = (WIDTH//2, HEIGHT/2.25)
        button_3.center = (WIDTH//2, HEIGHT/1.5)
        button_4.center = (WIDTH//2, HEIGHT/1.125)

        pygame.draw.rect(frame,CIRCLE_COLOR, button_1)#,WIDTH//18
        pygame.draw.rect(frame,CIRCLE_COLOR, button_2)
        pygame.draw.rect(frame,CIRCLE_COLOR, button_3)
        pygame.draw.rect(frame,CIRCLE_COLOR, button_4)

        jvj = font2.render("JOUEUR VS JOUEUR", True, CIRCLE_COLOR_WIN)
        jvj_rect = jvj.get_rect(center=(button_1.center))
        frame.blit(jvj, jvj_rect)

        jvai = font2.render("IA DÉBUTANT", True, CIRCLE_COLOR_WIN)
        jvai_rect = jvai.get_rect(center=(button_2.center))
        frame.blit(jvai, jvai_rect)

        jvai2 = font2.render("IA EXPERTE", True, CIRCLE_COLOR_WIN)
        jvai2_rect = jvai2.get_rect(center=(button_3.center))
        frame.blit(jvai2, jvai2_rect)

        opt = font2.render("OPTIONS", True, CIRCLE_COLOR_WIN)
        opt_rect = opt.get_rect(center=(button_4.center))
        frame.blit(opt, opt_rect)

        if button_1.collidepoint((mx, my)):
            if click:
                click_sound.play()
                game()
        if button_2.collidepoint((mx, my)):
            if click:
                click_sound.play()
                ai1()
        if button_3.collidepoint((mx, my)):
            if click:
                click_sound.play()
                ai2()
        if button_4.collidepoint((mx, my)):
            if click:
                click_sound.play()
                option()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()


def option():
    frame.fill(FRAME_COLOR)
    running = True
    while running:
        mx2, my2 = pygame.mouse.get_pos()

        options = font1.render("OPTIONS", True, TEXT_COLOR)
        options_rect = options.get_rect()
        options_rect.center = ((WIDTH//2,WIDTH//13))
        frame.blit(options, options_rect)

        res = font.render("Résolution", True, TEXT_COLOR)
        res_rect = res.get_rect()
        res_rect.center = ((WIDTH//2,WIDTH//4))
        frame.blit(res, res_rect)

        mus = font.render("Musique", True, TEXT_COLOR)
        mus_rect = mus.get_rect()
        mus_rect.center = ((WIDTH//2,WIDTH/1.8))
        frame.blit(mus, mus_rect)

        button_6 = pygame.Rect(0, 0, WIDTH//6, HEIGHT//9)
        button_9 = pygame.Rect(0, 0, WIDTH//6, HEIGHT//9)
        button_12 = pygame.Rect(0, 0, WIDTH//6, HEIGHT//9)
        button_MON = pygame.Rect(0, 0, WIDTH//4, HEIGHT//9)
        button_MOFF = pygame.Rect(0, 0, WIDTH//4, HEIGHT//9)

        button_6.center = (WIDTH/6, HEIGHT/2.5)
        button_9.center = (WIDTH/2, HEIGHT/2.5)
        button_12.center = (WIDTH/1.2, HEIGHT/2.5)
        button_MON.center = (WIDTH/3, HEIGHT/1.3)
        button_MOFF.center = (WIDTH/1.5, HEIGHT/1.3)

        pygame.draw.rect(frame,CIRCLE_COLOR, button_6)
        pygame.draw.rect(frame,CIRCLE_COLOR, button_9)
        pygame.draw.rect(frame,CIRCLE_COLOR, button_12)
        pygame.draw.rect(frame,CIRCLE_COLOR, button_MON)
        pygame.draw.rect(frame,CIRCLE_COLOR, button_MOFF)

        res1 = font2.render("600x600", True, CIRCLE_COLOR_WIN)
        res1_rect = res1.get_rect(center=(button_6.center))
        frame.blit(res1, res1_rect)

        res2 = font2.render("900x900", True, CIRCLE_COLOR_WIN)
        res2_rect = res2.get_rect(center=(button_9.center))
        frame.blit(res2, res2_rect)

        res3 = font2.render("1200x1200", True, CIRCLE_COLOR_WIN)
        res3_rect = res3.get_rect(center=(button_12.center))
        frame.blit(res3, res3_rect)

        musiqueON = font2.render("ON", True, CIRCLE_COLOR_WIN)
        musiqueON_rect = musiqueON.get_rect(center=(button_MON.center))
        frame.blit(musiqueON, musiqueON_rect)

        musiqueOFF = font2.render("OFF", True, CIRCLE_COLOR_WIN)
        musiqueOFF_rect = musiqueOFF.get_rect(center=(button_MOFF.center))
        frame.blit(musiqueOFF, musiqueOFF_rect)

        if button_6.collidepoint((mx2, my2)):
            if click:
                click_sound.play()
                setres(600)
        if button_9.collidepoint((mx2, my2)):
            if click:
                click_sound.play()
                setres(900)
        if button_12.collidepoint((mx2, my2)):
            if click:
                click_sound.play()
                setres(1200)
        if button_MOFF.collidepoint((mx2, my2)):
            if click:
                click_sound.play()
                pygame.mixer.music.pause()
        if button_MON.collidepoint((mx2, my2)):
            if click:
                click_sound.play()
                pygame.mixer.music.unpause()
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.update()
        

def game():
    frame.fill(FRAME_COLOR)
    cadrage()
    player = 1
    turn = 2
    flag = False
    DRAW, WIN_J1, WIN_J2, COUNT = 0, 0, 0, 0
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN and not flag:
                #coordonnées clique souris
                dX = e.pos[0]
                dY = e.pos[1]
                c_row = int(dY // STANDARD)
                c_col = int(dX // STANDARD)
                if free_square(c_row, c_col):
                    if player == intent(c_row,c_col,player):
                        intent(c_row,c_col,player)
                    figures()
                    COUNT +=1
                    if COUNT == 9 and not check_winner(player):
                        flag = True
                        DRAW += 1
                        draw_draw()
                        draw_scoreboard(DRAW,WIN_J1,WIN_J2)
                    if check_winner(player):
                        if player == 1:
                            WIN_J1 += 1
                            draw_win_j1()
                            draw_scoreboard(DRAW,WIN_J1,WIN_J2)
                        elif player == 2:
                            WIN_J2 += 1
                            draw_win_j2()
                            draw_scoreboard(DRAW,WIN_J1,WIN_J2)
                        flag = True
                    player = player % 2 + 1
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    player = turn
                    turn = turn % 2 + 1
                    flag = False
                    COUNT = 0
                    restart() 
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    restart()
                    running = False
        pygame.display.update()


def ai1():
    frame.fill(FRAME_COLOR)
    cadrage()
    player = 1
    turn = 2
    flag = False
    DRAW, WIN_J, WIN_IA, COUNT = 0, 0, 0, 0 #WIN_J et WIN_AI

    running = True
    while running:
        for e in pygame.event.get():
            if player == 1:
                if e.type == pygame.MOUSEBUTTONDOWN and not flag:
                    #coordonnées clique souris
                    dX = e.pos[0]
                    dY = e.pos[1]
                    c_row = int(dY // STANDARD)
                    c_col = int(dX // STANDARD)

                    if free_square(c_row, c_col):
                        if player == intent(c_row,c_col,player):
                            intent(c_row,c_col,player)
                        figures()
                        COUNT +=1
                        #if COUNT == 9 and not check_winner(player):
                        if check_draw():
                            flag = True
                            DRAW += 1
                            draw_draw()
                            draw_scoreboardIA1(DRAW,WIN_J,WIN_IA)
                        if check_winner(player):
                            WIN_J += 1
                            draw_win_j1()
                            draw_scoreboardIA1(DRAW,WIN_J,WIN_IA)
                            flag = True
                        player = player % 2 + 1
            elif not flag and player == 2:
                run = True
                while run:
                    x = random.randint(0,2)
                    y = random.randint(0,2)
                    if free_square(x,y):
                        run = False
                intent(x,y,player)
                figures()
                COUNT +=1
                if COUNT == 9 and not check_winner(player):
                    flag = True
                    DRAW += 1
                    draw_draw()
                    draw_scoreboardIA1(DRAW,WIN_J,WIN_IA)
                if check_winner(player):
                    WIN_IA += 1
                    draw_win_ai()
                    draw_scoreboardIA1(DRAW,WIN_J,WIN_IA)
                    flag = True
                player = player % 2 + 1
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    player = turn
                    turn = turn % 2 + 1
                    flag = False
                    COUNT = 0
                    restart() 
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    restart()
                    running = False
        pygame.display.update()


board2 = {'0,0': ' ', '0,1': ' ', '0,2': ' ',
         '1,0': ' ', '1,1': ' ', '1,2': ' ',
         '2,0': ' ', '2,1': ' ', '2,2': ' '}

def checkWhichMarkWon(mark):
    if board2['0,0'] == board2['0,1'] and board2['0,0'] == board2['0,2'] and board2['0,0'] == mark:
        return True
    elif (board2['1,0'] == board2['1,1'] and board2['1,0'] == board2['1,2'] and board2['1,0'] == mark):
        return True
    elif (board2['2,0'] == board2['2,1'] and board2['2,0'] == board2['2,2'] and board2['2,0'] == mark):
        return True
    elif (board2['0,0'] == board2['1,0'] and board2['0,0'] == board2['2,0'] and board2['0,0'] == mark):
        return True
    elif (board2['0,1'] == board2['1,1'] and board2['0,1'] == board2['2,1'] and board2['0,1'] == mark):
        return True
    elif (board2['0,2'] == board2['1,2'] and board2['0,2'] == board2['2,2'] and board2['0,2'] == mark):
        return True
    elif (board2['0,0'] == board2['1,1'] and board2['0,0'] == board2['2,2'] and board2['0,0'] == mark):
        return True
    elif (board2['2,0'] == board2['1,1'] and board2['2,0'] == board2['0,2'] and board2['2,0'] == mark):
        return True
    else:
        return False


def checkDraw():
    for key in board2.keys():
        if (board2[key] == ' '):
            return False
    return True


def spaceIsFree(position):
    if board2[position] == ' ':
        return True
    else:
        return False


def move():
    bestScore = -10
    bestMove = '0'
    for key in board2.keys():
        if (board2[key] == ' '):
            board2[key] = 2
            score = minimax(board2, False)
            board2[key] = ' '
            if (score > bestScore):
                bestScore = score
                bestMove = key
    row = int(float(bestMove[0]))
    col = int(float(bestMove[2]))
    if spaceIsFree(bestMove):
        intent(row,col,2)
        board2[bestMove] = 2


def minimax(board2, isMaximizing):
    if (checkWhichMarkWon(2)):
        return 1
    elif (checkWhichMarkWon(1)):
        return -1
    elif (checkDraw()):
        return 0

    if (isMaximizing):
        bestScore = -10
        for key in board2.keys():
            if (board2[key] == ' '):
                board2[key] = 2
                score = minimax(board2, False)
                board2[key] = ' '
                if (score > bestScore):
                    bestScore = score
        return bestScore
    else:
        bestScore = 10
        for key in board2.keys():
            if (board2[key] == ' '):
                board2[key] = 1
                score = minimax(board2, True)
                board2[key] = ' '
                if (score < bestScore):
                    bestScore = score
        return bestScore


def ai2():
    global board2
    frame.fill(FRAME_COLOR)
    cadrage()
    player = 1
    turn = 2
    flag = False
    DRAW, WIN_J, WIN_IA, COUNT = 0, 0, 0, 0

    running = True
    while running:
        for e in pygame.event.get():
            j = 0
            if player == 1:
                if e.type == pygame.MOUSEBUTTONDOWN and not flag:
                    #coordonnées clique souris
                    dX = e.pos[0]
                    dY = e.pos[1]
                    c_row = int(dY // STANDARD)
                    c_col = int(dX // STANDARD)
                    if free_square(c_row, c_col):
                        if player == intent(c_row,c_col,player):
                            intent(c_row,c_col,player)
                        j = str(c_row)+","+str(c_col)
                        board2[j] = player
                        figures()
                        COUNT +=1
                        if COUNT == 9 and not check_winner(player):
                            flag = True
                            DRAW += 1
                            draw_draw()
                            draw_scoreboardIA1(DRAW,WIN_J,WIN_IA)
                        if check_winner(player):
                            WIN_J += 1
                            draw_win_j1()
                            draw_scoreboardIA1(DRAW,WIN_J,WIN_IA)
                            flag = True
                        player = player % 2 + 1
            elif not flag and player == 2:
                move()
                figures()
                COUNT +=1
                if COUNT == 9 and not check_winner(player):
                    flag = True
                    DRAW += 1
                    draw_draw()
                    draw_scoreboardIA1(DRAW,WIN_J,WIN_IA)
                if check_winner(player):
                    WIN_IA += 1
                    draw_win_ai()
                    draw_scoreboardIA1(DRAW,WIN_J,WIN_IA)
                    flag = True
                player = player % 2 + 1
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    player = turn
                    turn = turn % 2 + 1
                    flag = False
                    COUNT = 0
                    board2 = dict.fromkeys(board2, ' ')
                    restart() 
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_ESCAPE:
                    board2 = dict.fromkeys(board2, ' ')
                    restart()
                    running = False
        pygame.display.update()
main_menu()
