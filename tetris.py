# TETRIS GAME
# 2021-04-21
# By Max Liu
# Game design and visuals inspired by jstris:
# https://jstris.jezevec10.com/
# Code design lightly inspired by freeCodeCamp:
# https://www.youtube.com/watch?v=zfvxp7PgQ6c
# Sound effects from the game NullPomino

import pygame, random, time

# make sure pieces.py is in same directory for this to work
from pieces import Piece

# main class for game functionality, piece manipulation, and board features
class Tetris:
    # track user lines cleared
    lines_cleared = 0
    # default piece type is none
    Piece = None
    # where the board is displayed on the screen, offset from top left
    x = 60
    y = 60
    # initialize by generating blank playfield
    def __init__(self, height, width):
        # game starts out as active, becomes deactive upon playe6 loss
        self.active = True
        # playfield stores the entire tetris board
        self.playfield = []
        self.height = height
        self.width = width
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(0)
            self.playfield.append(row)

    # generates piece at top of the screen, check Piece class in pieces.py
    def create_piece(self, piece_type):
        self.Piece = Piece(3, 0, piece_type)

    # rotate piece, check Piece class in pieces.py
    def rotate(self, direction):
        self.Piece.rotate(direction)
        # check for collision to make sure rotation is possible
        if(self.check_collision()):
            self.Piece.rotate(-direction)

    # check piece collision
    def check_collision(self):
        # range is 4 since piece shapes are stored as numbers from 1-16
        for i in range(0, 4):
            for j in range(0, 4):
                # i * 4 + j is position (j, i), check if it's in piece shape
                if(i * 4 + j in self.Piece.return_positions()):
                    # collision with outside wall
                    if(i + self.Piece.y > self.height - 1 or j + self.Piece.x > self.width - 1):
                        return True
                    # collision with another piece in the playfield
                    if(j + self.Piece.x < 0 or self.playfield[i + self.Piece.y][j + self.Piece.x] > 0):
                        return True
        # since no collisions detected, return false
        return False

    # when user presses space, hard drop to bottom of screen and lock
    def hard_drop(self):
        # go to lowest point without collision
        while(not self.check_collision()):
            self.Piece.y += 1
        self.Piece.y -= 1
        self.lock()

    # returns lowest point of piece to help draw ghost note
    def lowest_possible(self):
        # keep track of original position since the piece doesn't actually move
        original_y = self.Piece.y
        while(not self.check_collision()):
            self.Piece.y += 1
        self.Piece.y -= 1
        # return lowest position, return piece to original position
        lowest_y = self.Piece.y
        self.Piece.y = original_y
        return lowest_y

    # when user presses space or when natural gravity takes place, move one square down
    def soft_drop(self):
        self.Piece.y += 1
        # if collides, then lock piece
        if(self.check_collision()):
            self.Piece.y -= 1
            self.lock()

    # locks piece, adds to playfield, clears lines
    def lock(self):
        # add piece shape to playfield
        for i in range(0, 4):
            for j in range(0, 4):
                if(i * 4 + j in self.Piece.return_positions()):
                    self.playfield[i + self.Piece.y][j + self.Piece.x] = self.Piece.type + 1
        self.clear_lines()
        game.Piece = None
        # play drop sound effect
        sound_effect = pygame.mixer.Sound('audio/drop.wav')
        sound_effect.play()

    # when player presses left or right arrow
    def horizontal_move(self, direction):
        # attempt to move in direction
        self.Piece.x += direction
        # if collision, return to original spot
        if(self.check_collision()):
            self.Piece.x -= direction
        # play move sound effect
        else:
            sound_effect = pygame.mixer.Sound('audio/move.wav')
            sound_effect.play()

    # once all ten pieces are filled in a row, it disappears and the other rows move down
    def clear_lines(self):
        # track how many lines are cleared
        lines = 0
        for row in range(1, self.height):
            # if there are no empty spaces, clear the line
            if(self.playfield[row].count(0) == 0):
                lines += 1
                # move all rows above down by one
                for above in range(row, 1, -1):
                    for j in range(0, self.width):
                        self.playfield[above][j] = self.playfield[above - 1][j]
        # if line was cleared, play sound effect
        if(lines > 0):
            self.lines_cleared += lines
            sound_effect = pygame.mixer.Sound('audio/clear.wav')
            sound_effect.play()

# draws playfield grid
def draw_grid():
    # vertical lines
    for i in range(0, game.width + 1):
        pygame.draw.line(screen, DARK_GREY, (game.x + scale * i + 1, game.y + 1),
                                            (game.x + scale * i + 1, game.y + scale*game.height), 1)
    # horizontal lines
    for j in range(0, game.height + 1):
        pygame.draw.line(screen, DARK_GREY, (game.x + 1, game.y + scale * j + 1),
                                            (game.x + scale*game.width, game.y + scale * j + 1), 1)

# draws border around playfield
def draw_border():
    # draw playfield border
    # horizontal lines
    for offset in [0, scale * game.width]:
        pygame.draw.line(screen, LIGHT_GREY, (game.x + offset + 1, game.y + 1),
                         (game.x + offset + 1, game.y + scale*game.height), 2)
    # vertical lines
    for offset in [0, scale * game.height]:
        pygame.draw.line(screen, LIGHT_GREY, (game.x + 1, game.y + offset + 1),
                                             (game.x + scale*game.width, game.y + offset + 1), 2)
    # draw next piece border and hold piece border
    # horizontal lines
    for v_offset in [0, scale*7]:
        for offset in [0, 180]:
            pygame.draw.line(screen, LIGHT_GREY, (game.x + scale * game.width + offset + 30, game.y + v_offset + 1),
                                                 (game.x + scale * game.width + offset + 30, game.y + v_offset + scale*4 + 1), 2)
        # vertical lines
        for offset in [0, scale*4]:
            pygame.draw.line(screen, LIGHT_GREY, (game.x + scale*game.width + 30, game.y + v_offset + offset + 1),
                                                 (game.x + scale*game.width + 210, game.y + v_offset + offset + 1), 2)

# draw current piece and ghost piece onto the screen
def draw_current_piece():
    lowest_possible = game.lowest_possible()
    # draw using every rectangle of the shape
    for i in range(0, 4):
        for j in range(0, 4):
            p = i * 4 + j
            # if the position is in the shape
            if(p in game.Piece.return_positions()):
                # draw ghost piece, which is darker than the actual piece
                pygame.draw.rect(screen, (PIECE_COLOURS[game.Piece.type + 1][0]/2,
                                          PIECE_COLOURS[game.Piece.type + 1][1]/2,
                                          PIECE_COLOURS[game.Piece.type + 1][2]/2),
                                 [game.x + scale * (j + game.Piece.x) + 1,
                                  game.y + scale * (i + lowest_possible) + 1,
                                  scale, scale])
                # draw current piece
                pygame.draw.rect(screen, PIECE_COLOURS[game.Piece.type + 1],
                                 [game.x + scale * (j + game.Piece.x) + 1,
                                  game.y + scale * (i + game.Piece.y) + 1,
                                  scale, scale])
                    
# draw full playfield
def draw_playfield():
    for i in range(0, game.height):
        for j in range(0, game.width):
            # if game.playfield > 0, then there is a piece there
            if(game.playfield[i][j] > 0):
                # playfield has colour information (bound to piece type)
                pygame.draw.rect(screen, PIECE_COLOURS[game.playfield[i][j]],
                    [game.x + scale * j + 1, game.y + scale * i + 1, scale, scale])

# draw next piece preview
def draw_next_piece():
    global piece_list
    # next piece is at piece_number position, since the current piece is actually piece_number - 1
    next_piece = Piece.pieces[piece_list[piece_number]]
    # draw next piece
    for i in range(0, 4):
        for j in range(0, 4):
            p = i * 4 + j
            # next_piece[0] is the default rotation of the piece
            if(p in next_piece[0]):
                # use piece colour based on type
                pygame.draw.rect(screen, PIECE_COLOURS[piece_list[piece_number] + 1],
                    [game.x + scale * (j + 12),
                    game.y + scale * (i + 1),
                    scale, scale])

# draws hold piece, can be nothing
def draw_hold_piece():
    global piece_list, hold_piece
    if(hold_piece != None):
        # draw hold piece
        for i in range(0, 4):
            for j in range(0, 4):
                p = i * 4 + j
                # the default rotation of the piece
                if(p in Piece.pieces[hold_piece][0]):
                    # use piece colour based on type
                    pygame.draw.rect(screen, PIECE_COLOURS[hold_piece + 1],
                        [game.x + scale * (j + 12),
                        game.y + scale * (i + 8),
                        scale, scale])

# draws title, next piece, hold piece, stats
def draw_text():
    # set font
    main_font = pygame.font.SysFont('myanmartext', 25, True, False)
    # have to render first then blit in pygame
    title_text = main_font.render("Max's Tetris Game", True, WHITE)
    next_text = main_font.render("Next Piece", True, WHITE)
    hold_text = main_font.render("Hold Piece", True, WHITE)

    # draw some statistics, elapsed time is rounded to 2 significant figures
    elapsed_time = main_font.render("Time: " + str(round(time.time() - time_start, 2)), True, WHITE)
    lines_cleared = main_font.render("Lines: " + str(game.lines_cleared), True, WHITE)
    pieces_placed = main_font.render("Pieces: " + str(total_pieces), True, WHITE)
    
    # blit based on scale
    screen.blit(next_text, (game.x + scale * game.width + 56, game.y + scale*4 + 5))
    screen.blit(hold_text, (game.x + scale * game.width + 56, game.y + scale*11 + 5))
    screen.blit(title_text, (200, 20))
    screen.blit(elapsed_time, (70, game.y + scale*20 + 5))
    screen.blit(lines_cleared, (70, game.y + scale*21 + 5))
    screen.blit(pieces_placed, (70, game.y + scale*22 + 5))

# displays message at the center of the screen
def display_message(message, y, bold):
    if(bold):
        font = pygame.font.SysFont("Source Code Pro", 60)
    else:
        font = pygame.font.SysFont("myanmartext", 30)
    display_text = font.render(message, 1, WHITE)
    display_position = display_text.get_rect(center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + y))
    screen.blit(display_text, display_position)

# draws
def draw_rectangle():
    # size of rectangle
    rectangle_surface = pygame.Surface((9*SCREEN_WIDTH/10, 3*SCREEN_HEIGHT/10))
    # transparency
    rectangle_surface.set_alpha(220)
    # fill entire surface
    rectangle_surface.fill((0,0,0))
    # defined using top left coordinates
    screen.blit(rectangle_surface, (SCREEN_WIDTH/20, 3.5*SCREEN_HEIGHT/10))
    # defined using top left coordinates and height/width
    pygame.draw.rect(screen, (200,200,200), pygame.Rect(SCREEN_WIDTH/20, 3.5*SCREEN_HEIGHT/10,
                                                        9*SCREEN_WIDTH/10, 3*SCREEN_HEIGHT/10), 5)

# draws at the beginning of each game, instructions
def draw_start_text():
    display_message("Pygame Tetris!", -70, True)
    display_message("Arrow keys to move, space to drop.", -22, False)
    display_message("A/S to rotate, C to hold.", 10, False)
    display_message("Clear 40 lines to win.", 42, False)
    display_message("Press any key to begin.", 74, False)

# draws at game over (player wins or loses)
def draw_end_text():
    display_message("Game Over!", -20, True)
    display_message("Press R to restart.", 25, False)

# draws all parts of the game, piece_active is false when intializing the game
def full_redraw(piece_active):
    screen.fill((10,10,20))
    if(piece_active):
        draw_current_piece()
    draw_playfield()
    draw_grid()
    draw_border()
    draw_next_piece()
    draw_hold_piece()
    draw_text()

# waits for user to press a key before continuing
def wait_for_input(key = "any"):
    pause = True
    while(pause):
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                return "exit"
            elif(event.type == pygame.KEYDOWN):
                if(key == "any" or event.key == ord(key)):
                    return

# initialize the game engine
pygame.init()

# define colours
PIECE_COLOURS = [
    (0, 0, 0),
    (15, 155, 215),
    (33, 65, 198),
    (227, 91, 2),
    (89, 177, 1),
    (215, 15, 55),
    (175, 41, 138),
    (227, 159, 2)
]
WHITE = (255, 255, 255)
DARK_GREY = (50, 50, 50)
LIGHT_GREY = (150, 150, 150)

# fixed screen height and width
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 800

# everything gets rendered to screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
scale = 30

# sets window caption
pygame.display.set_caption("Tetris")
# sets window icon
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# loop until the user clicks the close button
user_exit = False

while(user_exit == False):
    # starts the main game, 20x10 by default. Other sizes may be buggy.
    game = Tetris(20, 10)
    # tracks game time for gravity
    counter = 0
    # tracks how long the player has held down, for soft drop
    down_counter = -1
    down_pressed = False
    # tracks piece number for bagged randomness
    piece_number = 0
    # tracks total number of pieces placed
    total_pieces = 0
    # instead of generating random pieces, all seven pieces are given in a random order
    piece_list = list(range(0, 7))
    random.shuffle(piece_list)
    # also keep track of the next bag so that next piece preview always works
    next_piece_list = list(range(0, 7))
    random.shuffle(next_piece_list)
    # track whether or not hold was used and what the hold piece was
    hold_used = False
    hold_piece = None
    
    # keep track of time
    time_start = time.time()
    # draw everything initially, the "false" is to not draw the current piece, which doesn't exist
    full_redraw(False)
    # start screen with instructions
    draw_rectangle()
    draw_start_text()
    pygame.display.update()
    # wait for any key as input to begin playing
    user_input = wait_for_input()
    if(user_input == "exit"):
        user_exit = True
    # reset timer
    time_start = time.time()

    # main game loop
    while(game.active):
        # if there is no piece, generate one
        if(game.Piece == None):
            game.create_piece(piece_list[piece_number])
            piece_number += 1
            # if the end of the scrambled bag is reached
            if(piece_number == 7):
                # replace current bag with next bag and scramble next bag
                piece_list = next_piece_list
                random.shuffle(next_piece_list)
                piece_number = 0
            # player is allowed to hold again (can hold once per piece)
            hold_used = False
            # if there is a collision, player loses, if player clears 40 lines player wins
            if(game.check_collision() or game.lines_cleared > 39):
                # need to redraw text to increase piece_number accurately
                full_redraw(False)
                game.active = False
                # play game over sound effect
                sound_effect = pygame.mixer.Sound('audio/gameover.wav')
                sound_effect.play()
                # break out of while loop since game has ended
                break
        counter += 1
        # every 180 ticks drop the piece due to gravity, or drop from down being pressed
        if(counter % 180 == 0 or (down_pressed and down_counter % 40 == 0)):
            game.soft_drop()
        # track how long user has held down
        if(down_counter != -1):
            down_counter += 1
        
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                user_exit = True
                break
            # check the user's keypresses
            elif(event.type == pygame.KEYDOWN):
                if(game.Piece != None):
                    # clockwise rotation
                    if(event.key == ord('a')):
                        game.rotate(1)
                    # counterclockwise rotation
                    elif(event.key == ord('s')):
                        game.rotate(-1)
                    # hold piece
                    elif(event.key == ord('c')):
                        # if hold hasn't been used before that turn
                        if(not hold_used):
                            hold_used = True
                            # if there is no piece held
                            if(hold_piece == None):
                                # hold piece becomes the current piece
                                hold_piece = game.Piece.type
                                # create the piece which comes after
                                game.create_piece(piece_list[piece_number])
                                piece_number += 1
                                if(piece_number == 7):
                                    random.shuffle(next_piece_list)
                                    piece_number = 0
                                    piece_list = next_piece_list
                            # if there is a piece held, simply swap the pieces
                            else:
                                hold_piece_temp = hold_piece
                                hold_piece = game.Piece.type
                                game.create_piece(hold_piece_temp)
                            # play hold sound effect
                            sound_effect = pygame.mixer.Sound('audio/hold.wav')
                            sound_effect.play()
                    # move piece left
                    elif(event.key == pygame.K_LEFT):
                        game.horizontal_move(-1)
                    # move piece right
                    elif(event.key == pygame.K_RIGHT):
                        game.horizontal_move(1)
                    # soft drop
                    elif(event.key == pygame.K_DOWN):
                        down_pressed = True
                        down_counter = 0
                    # hard drop
                    elif(event.key == pygame.K_SPACE):
                        game.hard_drop()
                # resets game
                if(event.key == ord('r')):
                    game.active = False
                    # play game over sound effect
                    sound_effect = pygame.mixer.Sound('audio/gameover.wav')
                    sound_effect.play()
            elif(event.type == pygame.KEYUP):
                # user has let go of the down key
                if(event.key == pygame.K_DOWN):
                    down_counter = -1
                    down_pressed = False
        # if user closed game
        if(user_exit):
            break
        # calls all draw function
        if(game.Piece != None):
            full_redraw(True)
            pygame.display.update()
        # if piece is None, that means it was placed, increase total_pieces
        else:
            total_pieces += 1
    # game has ended (player won/lost)
    if(game.active == False and not user_exit):
        # display game over screen
        draw_rectangle()
        draw_end_text()
        pygame.display.update()
        # wait for player to press R to restart
        user_input = wait_for_input('r')
        if(user_input == "exit"):
            user_exit = True

# if main while loop is quit, then exit the program
pygame.quit()
