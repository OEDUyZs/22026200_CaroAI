from gui.interface import *
from source.AI import *
from gui.button import Button

import source.utils as utils
import source.gomoku as gomoku

import pygame
import sys
import os

# =========================
# LAUNCHER MENU
# =========================
def console_menu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("="*50)
    print("       CARO AI - CONFIGURATION LAUNCHER       ")
    print("="*50)
    print("Chọn độ khó (Giới hạn độ sâu tìm kiếm):")
    print("  1. Easy   (Depth 1)")
    print("  2. Medium (Depth 2)")
    print("  3. Hard   (Depth 3)")
    
    while True:
        try:
            depth = int(input("=> Nhập lựa chọn (1-3): "))
            if depth in [1, 2, 3]: break
            print("Vui lòng chỉ nhập 1, 2 hoặc 3!")
        except:
            print("Lỗi! Vui lòng nhập số.")

    print("\nChọn thuật toán AI:")
    print("  1. Minimax thuần (Không cắt nhánh)")
    print("  2. Alpha-Beta Pruning (Tối ưu)")
    
    while True:
        try:
            algo = int(input("=> Nhập lựa chọn (1-2): "))
            if algo in [1, 2]: break
            print("Vui lòng chỉ nhập 1 hoặc 2!")
        except:
            print("Lỗi! Vui lòng nhập số.")
            
    print("\nĐANG KHỞI ĐỘNG GIAO DIỆN GAME...")
    return depth, algo

# =========================
# START GAME
# =========================
def startGame():
    
    depth, algo = console_menu()
    pygame.init()

    ai = GomokuAI(depth=depth)
    ai.algo = algo

    game = GameUI(ai)

    # Đổi sang Tiếng Anh
    button_x = Button(
        game.buttonSurf,
        180,
        290,
        "X (FIRST)",
        16
    )

    button_o = Button(
        game.buttonSurf,
        360,
        290,
        "O (SECOND)",
        16
    )

    game.drawMenu()
    game.drawButtons(button_x, button_o, game.screen)

    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                mouse_pos = pygame.mouse.get_pos()

                if button_x.checkMousePos(mouse_pos) or button_o.checkMousePos(mouse_pos):
                    
                    game.checkColorChoice(button_x, button_o, mouse_pos)
                    game.drawBoard()

                    # AI first move
                    if game.ai.turn == 1:
                        game.ai.firstMove()
                        game.drawPiece('black', game.ai.currentI, game.ai.currentJ)
                        game.ai.turn *= -1

                    main(game)

                    # END GAME CHECK
                    if game.ai.checkResult() is not None:
                        game.drawResult()
                        yes_button = Button(game.buttonSurf, 200, 155, "YES", 18)
                        no_button = Button(game.buttonSurf, 350, 155, "NO", 18)
                        game.drawButtons(yes_button, no_button, game.screen)

                        waiting = True
                        while waiting:
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    pygame.quit()
                                    sys.exit()
                                if e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                                    pos = pygame.mouse.get_pos()
                                    if yes_button.checkMousePos(pos):
                                        startGame() 
                                        return
                                    elif no_button.checkMousePos(pos):
                                        pygame.quit()
                                        sys.exit()

# =========================
# MAIN LOOP
# =========================
def main(game):

    end = False
    result = game.ai.checkResult()

    while not end:

        turn = game.ai.turn
        color = game.colorState[turn]

        # AI TURN
        if turn == 1:
            move_i, move_j = gomoku.ai_move(game.ai)

            game.ai.setState(move_i, move_j, turn)
            game.ai.rollingHash ^= game.ai.zobristTable[move_i][move_j][0]
            game.ai.emptyCells -= 1
            game.drawPiece(color, move_i, move_j)
            
            result = game.ai.checkResult()
            game.ai.turn *= -1
            
            pygame.event.clear()

        # HUMAN TURN
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if turn == -1:
                if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()

                    human_move = utils.pos_pixel2map(mouse_pos[0], mouse_pos[1])
                    move_i = human_move[0]
                    move_j = human_move[1]

                    if game.ai.isValid(move_i, move_j):
                        game.ai.boardValue = game.ai.evaluate(move_i, move_j, game.ai.boardValue, -1, game.ai.nextBound)
                        game.ai.updateBound(move_i, move_j, game.ai.nextBound)
                        game.ai.currentI = move_i
                        game.ai.currentJ = move_j
                        
                        game.ai.setState(move_i, move_j, turn)
                        game.ai.rollingHash ^= game.ai.zobristTable[move_i][move_j][1]
                        game.ai.emptyCells -= 1
                        
                        game.drawPiece(color, move_i, move_j)
                        result = game.ai.checkResult()
                        game.ai.turn *= -1

        if result is not None:
            end = True

        pygame.display.update()

# =========================
# RUN
# =========================
if __name__ == '__main__':
    startGame()