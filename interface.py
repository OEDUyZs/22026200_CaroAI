import pygame

from gui.button import *
import source.utils as utils


SIZE = 540
PIECE = 32

N = utils.N

MARGIN = utils.MARGIN
GRID = utils.GRID

FPS = 60


class GameUI(object):

    def __init__(self, ai):

        self.ai = ai
        self.colorState = {}
        self.mapping = utils.create_mapping()

        pygame.init()
        self.screen = pygame.display.set_mode((SIZE, SIZE))
        pygame.display.set_caption('Caro AI 9x9')

        self.blackPiece = pygame.transform.scale(
            pygame.image.load("assets/black_piece.png").convert_alpha(),
            (PIECE, PIECE)
        )

        self.whitePiece = pygame.transform.scale(
            pygame.image.load("assets/white_piece.png").convert_alpha(),
            (PIECE, PIECE)
        )

        self.menuBoard = pygame.image.load(
            "assets/menu_board.png"
        ).convert_alpha()

        self.buttonSurf = pygame.image.load(
            "assets/button.png"
        ).convert_alpha()

        # Nút bấm size chuẩn
        self.buttonSurf = pygame.transform.scale(
            self.buttonSurf,
            (140, 60)
        )

        self.drawBoard()

    # =========================
    # DRAW BOARD
    # =========================
    def drawBoard(self):

        self.screen.fill((255, 255, 255))

        for i in range(N):
            pos = MARGIN + i * GRID

            pygame.draw.line(
                self.screen,
                (200, 200, 200),
                (MARGIN, pos),
                (SIZE - MARGIN, pos),
                2
            )

            pygame.draw.line(
                self.screen,
                (200, 200, 200),
                (pos, MARGIN),
                (pos, SIZE - MARGIN),
                2
            )

        center = N // 2
        cx = MARGIN + center * GRID
        cy = MARGIN + center * GRID

        pygame.draw.circle(
            self.screen,
            (0, 0, 0),
            (int(cx), int(cy)),
            5
        )

        pygame.display.update()

    # =========================
    # MENU
    # =========================
    def drawMenu(self):

        menu_board = pygame.transform.scale(
            self.menuBoard,
            (350, 120)
        )

        menu_board_rect = menu_board.get_rect(
            center=self.screen.get_rect().center
        )

        menu_font = pygame.font.SysFont(
            "arial",
            22
        )

        # Tiếng Anh
        menu_text = menu_font.render(
            'CHOOSE YOUR SIDE:',
            True,
            'white'
        )

        menu_board.blit(menu_text, (55, 25))

        self.screen.blit(
            menu_board,
            menu_board_rect
        )

        pygame.display.update()

    def drawButtons(self, button1, button2, surface):
        button1.draw(surface)
        button2.draw(surface)
        pygame.display.update()

    # =========================
    # PLAYER COLOR
    # =========================
    def checkColorChoice(
        self,
        button_x,
        button_o,
        pos
    ):

        if button_x.rect.collidepoint(pos):
            self.colorState[-1] = 'black'
            self.colorState[1] = 'white'
            self.ai.turn = -1  # X đi trước (Người)

        elif button_o.rect.collidepoint(pos):
            self.colorState[-1] = 'white'
            self.colorState[1] = 'black'
            self.ai.turn = 1   # O đi sau (Máy)

    # =========================
    # DRAW PIECE
    # =========================
    def drawPiece(self, state, i, j):

        x, y = self.mapping[(i, j)]
        x = x - PIECE / 2
        y = y - PIECE / 2

        if state == 'black':
            self.screen.blit(self.blackPiece, (x, y))
        elif state == 'white':
            self.screen.blit(self.whitePiece, (x, y))

        pygame.display.update()

    # =========================
    # RESULT
    # =========================
    def drawResult(self, tie=False):

        menu_board = pygame.transform.scale(
            self.menuBoard,
            (400, 190)
        )

        width, height = menu_board.get_size()
        font = pygame.font.SysFont('arial', 25, True)

        if tie:
            text = "TIE GAME!"
            render_text = font.render(text, True, 'white')
            text_size = render_text.get_size()
            (x, y) = (width // 2 - text_size[0] // 2, height // 4 - text_size[1] // 2)
            menu_board.blit(render_text, (x, y))

        else:
            text = 'THE WINNER IS:'
            render_text = font.render(text, True, 'white')
            size1 = render_text.get_size()
            (x1, y1) = (width // 2 - size1[0] // 2, 30)

            winner = self.ai.getWinner()
            render_winner = font.render(str.upper(winner), True, 'white')
            size2 = render_winner.get_size()
            (x2, y2) = (width // 2 - size2[0] // 2, 30 + size1[1])

            menu_board.blit(render_text, (x1, y1))
            menu_board.blit(render_winner, (x2, y2))

        restart_font = pygame.font.SysFont('arial', 18)
        restart_text = 'Play again?'
        render_restart = restart_font.render(restart_text, True, 'white')
        restart_size = render_restart.get_size()
        (x3, y3) = (width // 2 - restart_size[0] // 2, height // 2)

        menu_board.blit(render_restart, (x3, y3))
        self.screen.blit(menu_board, (SIZE // 2 - width // 2, MARGIN // 2))

        pygame.display.update()