import pygame
from pygame.locals import *
from pygame.color import *
import pymunk as pm
from pymunk import Vec2d
import sys
import random
import math
import datetime

def to_pygame(p):
    """Small hack to convert pymunk to pygame coordinates"""
    return int(p[0]), int(-p[1]+600)

class Ball:
    """
    Provides a ball for the player to fire from the trebuchet
    """

    def __init__(self, space, x, y):
        """
        Sets up pygame and pymunk properties for the Ball
        """
        #mass = 3
        mass = 5
        radius = 20
        inertia = pm.moment_for_circle(mass, 0, radius, (0,0))
        body = pm.Body(mass, inertia)
        body.position = (x,y)
        shape = pm.Circle(body, radius, (0,0))
        shape.friction = 15.0
        shape.elasticity = 0.9
        space.add(body, shape)
        self.ball = shape
        self.colour = THECOLORS["red"]

    def draw(self):
        """
        Draws the ball to the screen
        """
        global screen

        ball = self.ball
        r = ball.radius
        p = to_pygame(ball.body.position)
        pygame.draw.circle(screen, self.colour, p, int(r), 20)

    def random_colour(self):
        """
        Picks the balls colour at random
        """

        rand = random.randint(0,3)

        if rand == 0:
            self.colour = THECOLORS["blue"]
        elif rand == 1:
            self.colour = THECOLORS["green"]
        elif rand == 2:
            self.colour = THECOLORS["orange"]
        elif rand == 3:
            self.colour = THECOLORS["brown"]

    def fire(self, force):
        """
        Applys an impulse to the ball object
        """
        pm.Body.apply_impulse(self.ball.body, (force,0))

    def get_position(self):
        """
        Returns the Ball's coordinates
        """
        return self.ball.body.position

    def reposition(self, x, y):
        """
        Allows user to move the ball to a specified location
        """
        self.ball.body.position = (x,y)

    def delete(self, space):
        """
        Removes occurences of the Crate object from pymunk's space
        """
        space.remove(self.ball)
        space.remove(self.ball.body)


class Crate:
    """
    Provides a crate object for building structure in the game_complete
    Can be a small crate or larger TNT crate by supplying an optional
    paramter to the contructor
    """

    def __init__(self, space, starting_position, is_tnt=False, mass=6.0):
        """
        Sets up pygame and pymunk properties for the Ball
        Decides whether a normal or TNT crate was requested
        """
        self.is_tnt = is_tnt
        if is_tnt:
            points = [(-46, -46), (-46, 46), (46,46), (46, -46)]
            self.crate_img = pygame.image.load("tnt_crate.png")
        else:
            points = [(-23, -23), (-23, 23), (23,23), (23, -23)]
            self.crate_img = pygame.image.load("crate.png")

        moment = pm.moment_for_poly(int(mass), points, (0,0))
        body = pm.Body(mass, moment)
        body.position = starting_position
        shape = pm.Poly(body, points, (0,0))
        shape.friction = 1
        space.add(body,shape)
        self.crate = shape
        self.run_count = 0

    def brake_crate(self):
        """
        Changes the crates image to a 'broken' style crate,
        Only for use with smaller crates
        """        
        self.run_count += 1
        if self.run_count == 1:
            num = random.randint(1,2)

            if not self.is_tnt:
                self.crate_img = \
                        pygame.image.load("broken_crate{0}.png".format(num))

    def draw(self):
        """
        Draws the crate to the screen, depending on it's type
        """
        global screen

        crate = self.crate
        if self.is_tnt:
            crate_img = pygame.transform.rotozoom(self.crate_img, \
                                            math.degrees(crate.body.angle), 1)
            box_x = crate.body.position[0] - crate_img.get_size()[1] + 46
            box_y = crate.body.position[1] + crate_img.get_size()[1] - 46
        else:            
            crate_img = pygame.transform.rotozoom(self.crate_img, \
                                            math.degrees(crate.body.angle), 1)
            box_x = crate.body.position[0] - 23
            box_y = crate.body.position[1] + 23

        crate_rect = crate_img.get_rect()
        crate_rect = crate_rect.move(to_pygame((box_x, box_y)))
        screen.blit(crate_img,crate_rect)

    def delete(self, space):
        """
        Removes occurences of the Crate object from pymunk's space
        """
        space.remove(self.crate)
        space.remove(self.crate.body)

class Snake:
    """
    Provides a Snake character as the player's enemy
    """

    snakes_alive = 0 # Static
    already_killed_snake = False
    
    def __init__(self, space, starting_position, mass=1.0):
        """
        Sets up pygame and pymunk properties for the Snake
        """
        points = [(-40, -40), (-40, 40), (40,40), (40, -40)]
        moment = pm.moment_for_poly(int(mass), points, (0,0))
        body = pm.Body(mass, moment)
        body.position = starting_position
        shape = pm.Poly(body, points, (0,0))
        shape.friction = 1
        space.add(body,shape)
        self.snake = shape
        self.snake_img = pygame.image.load("snake.png")
        Snake.snakes_alive += 1        

    def draw(self):
        """
        Draws the Snake to the screen
        """

        global screen
        
        snake_img = pygame.transform.rotozoom(self.snake_img, \
                                math.degrees(self.snake.body.angle), 1)
        snake_x = self.snake.body.position[0] - 36
        snake_y = self.snake.body.position[1] + 36

        snake_rect = snake_img.get_rect()
        snake_rect = snake_rect.move(to_pygame((snake_x, snake_y)))
        screen.blit(snake_img,snake_rect)

    def is_dead(self):
        """
        Returns whether the snake is dead, by checking if it is near
        the toxic puddle
        """
        return self.snake.body.position[1] < 110 + self.snake_img.get_size()[0]

    def kill_snake(self):
        """
        Changes Snakes image to a dead one
        """
        if not self.already_killed_snake:
            Snake.snakes_alive -= 1
            self.snake_img = pygame.image.load("dead_snake.png")
            self.already_killed_snake = True

    def delete(self, space):
        """
        Removes occurences of the Snake object from pymunk's space
        """
        space.remove(self.snake)
        space.remove(self.snake.body)

    # Static
    def all_snakes_dead():
        """
        Static Class method,
        Returns whether all snakes are dead or not
        """
        return Snake.snakes_alive == 0

class Image:
    """
    Simplifies the creation and displaying of static images
    """
    
    def __init__(self, filename, starting_position=None):
        """
        Initialise the Image
        """
        self.img = pygame.image.load(filename)
        self.rect = self.img.get_rect()
        if starting_position:
            self.move(starting_position)

    def move(self, position):
        """
        Reposition the image
        """
        self.rect = self.rect.move(position)

    def display(self):
        """
        Draws the image to the screen
        """
        global screen
        screen.blit(self.img, self.rect)

    def get_size(self):
        """
        Returns the images dimesions
        """
        return self.img.get_size()

class Message:
    """
    Abstracts pygame's font object, for easier use.
    Intended to be used annonymously
    """
    
    def __init__(self, message, position, size=50, colour=(255,255,255)):
        """
        Initialise the Message
        """
        self.font = pygame.font.Font('cartwheel.otf', size)
        self.text = self.font.render(message, 1, colour)
        self.position = position
        self.message = message
        self.size = size

    def display(self):
        """
        Prints the Message to the screen
        """
        global screen
        screen.blit(self.text,self.position)

    def display_shadow(self):
        """
        Prints the Message to the screen with a shadow effect
        """
        global screen
        shadow_font = pygame.font.Font('cartwheel.otf', self.size)
        shadow_text = shadow_font.render(self.message, 1, (10,10,10))
        screen.blit(shadow_text, (self.position[0] + 3, self.position[1] + 3))
        screen.blit(self.text,self.position)

def main():
    
    # Setup Level common variables -------------------------------- ##

    force    = 2300 # Force upon the ball when it is fired
    rampsize = 100  # end coordinate of the ball's ramp

    pygame.init()    
    pygame.display.set_caption("Angry Clones")
    clock = pygame.time.Clock()    

    # Set up static images, these never move
    greyed_out = Image("greyed_out.jpg")
    background = Image("machinarium_floor.jpg")
    trebuchet  = Image("trebuchet.png", (20,450))

    global screen
    screen = pygame.display.set_mode(background.get_size())
    
    space = pm.Space()
    space.gravity = (0.0, -300.0)
    body = pm.Body()

    # ground
    ground = pm.Segment(body, (0,100), (1050, 100), .0)
    ground.friction = 6.0
    space.add(ground)

     #left wall
    left_wall = pm.Segment(body, to_pygame((0,0)), to_pygame((0, 2000)), .0)
    left_wall.friction = 6.0
    space.add(left_wall)

    # ball area
    ball_area = pm.Segment(body, (0,110), (60,110), .0)
    space.add(ball_area)

    
    # Title Screen ------------------------------------------------- ##

    count = 0
    while count < 70:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                # Space bar skips the title screen
                if event.key == 32:
                    count = 71

        greyed_out.display()
        
        Message("Angry Clones!", (220,250), 95).display_shadow()

        pygame.display.flip()
        count += 1

    # End Title Screen ---------------------------------------------- ##

    # Main Game loop ------------------------------------------------ ##

    game_complete = False
    level = 0
    while not game_complete:

        # Record time now, to see how fast you complete the game
        start_game_timer = datetime.datetime.now()

        trying_again = True
        while trying_again:

            # Level setup ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

            if level == 0:
                balls = []    
                x,y = (2,110)
                balls.append(Ball(space, x, y))

                # Add crates
                crates = []
                crates += [Crate(space, (500,85+(23+i*51))) for i in range(3)]
                crates += [Crate(space, (600,85+(23+i*51))) for i in range(3)]
                crates += [Crate(space, (505+46,278), True)]

                # Add one snake
                snakes = []
                snakes.append(Snake(space, to_pygame((551,232))))

                level_complete = False
                level_failed = False
                count = 0

            if level == 1:
                
                # Remove all old crates etc from the playing area
                for crate in crates:
                    crate.delete(space)
                for ball in balls:
                    ball.delete(space)
                for snake in snakes:
                    snake.delete(space)

                balls = []    
                x,y = (2,110)
                balls.append(Ball(space, x, y))

                # Map of intended level     -   Key
                #------------------------------------------------
                #                #T#            S = Snake
                #             S  ###  S       
                #            #T# #T# #T#      #T# = TNT crate
                #            ### ### ###      ###
                #           #   #   #   #
                #           #   #   #   #
                #           #   #   #   #
                #           A B C D E F G


                # Add crates
                crates = []
                crates += [Crate(space, (500,85+(23+i*51))) for i in range(3)]#A
                crates += [Crate(space, (600,85+(23+i*51))) for i in range(3)]#C
                crates += [Crate(space, (700,85+(23+i*51))) for i in range(3)]#E
                crates += [Crate(space, (800,85+(23+i*51))) for i in range(3)]#G
                crates += [Crate(space, (505+46,278), True)] #B
                crates += [Crate(space, (605+46,278), True)] #D
                crates += [Crate(space, (705+46,278), True)] #F
                crates += [Crate(space, (605+46,378), True)] #D higher

                # Add snakes
                Snake.snakes_alive = 0
                snakes = []
                snakes.append(Snake(space, (551,350)))
                snakes.append(Snake(space, (751,350)))

                level_complete = False
                level_failed = False
                count = 0
                start_timer = datetime.datetime.now()

            if level == 2:
                
                # Remove all old crates etc from the playing area
                for crate in crates:
                    crate.delete(space)
                for ball in balls:
                    ball.delete(space)
                for snake in snakes:
                    snake.delete(space)

                balls = []    
                x,y = (2,110)
                balls.append(Ball(space, x, y))

                # Map of intended level     - Key
                #------------------------------------------------
                #              S          S = Snake
                #             #T#       
                #          S  ###       #T# = TNT crate
                #         #T# #T#       ###
                #      S  ### ### 
                #     #T# #T# #T#    
                #     ### ### ###
                #      A   B   C     

                # Add crates
                crates = []
                crates += [Crate(space, (305+46,170), True)] #A
                crates += [Crate(space, (505+46,170), True)] #B
                crates += [Crate(space, (505+46,270), True)] #
                crates += [Crate(space, (705+46,170), True)] #C
                crates += [Crate(space, (705+46,270), True)] #
                crates += [Crate(space, (705+46,370), True)] #

                # Add snakes
                Snake.snakes_alive = 0
                snakes = []
                snakes.append(Snake(space, (351,310)))
                snakes.append(Snake(space, (551,410)))
                snakes.append(Snake(space, (751,510)))

                level_complete = False
                level_failed = False
                count = 0
                start_timer = datetime.datetime.now()

            # End Level Setup ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

            # Game-play loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##
            
            while not level_complete and not level_failed:

                space.step(1/30.0)
                clock.tick(30)
                    
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit(0)
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit(0)
                        # Spacebar is pressed
                        if event.key == 32: # Reset the ball if lost
                            balls[0].delete(space)
                            balls = []    
                            x,y = (2,110)
                            balls.append(Ball(space, x, y))
                            balls[0].random_colour()

                #Get ramp slope from mouse 'y'
                rampsize = to_pygame(pygame.mouse.get_pos())[1]
                slope = pm.Segment(body, (60,110), (250,rampsize), .0)
                space.add(slope)

                background.display()
                trebuchet.display()  
                balls[0].draw()          

                if pygame.mouse.get_pressed()[0]:
                    balls[0].fire(force/3)

                for crate in crates:
                    crate.draw()

                # Add variety to crate's looks
                if level == 0:
                    crates[1].brake_crate()
                    crates[5].brake_crate()
                    crates[0].brake_crate()

                if level == 1:                    
                    crates[3].brake_crate()
                    crates[8].brake_crate()
                    crates[1].brake_crate()
                    crates[5].brake_crate()

                for snake in snakes:
                    snake.draw()
                    if snake.is_dead():
                        snake.kill_snake() #This doesn't make sense!
                        Message("The Snake is Dead!", \
                                                (600,600)).display_shadow()
                    
                    #If you kill all the snakes you win the level
                    if Snake.all_snakes_dead():
                        level_complete = True
                        level_failed = False
                        pass

                #Draw Ramp
                pygame.draw.aaline(screen, THECOLORS['red'], \
                                to_pygame((60,110)), to_pygame((250,rampsize)))
                #Draw Ball Area
                pygame.draw.aaline(screen, THECOLORS['red'],\
                                to_pygame((0,110)), to_pygame((60,110)))

                #If mouse goes of screen to the right, bring it back
                if to_pygame(balls[0].get_position())[0] > 1024:
                    balls[0].reposition(1,110)

                #Display number of snakes left
                Message("{0}".format("Snakes Left: {0}"\
                        .format(Snake.snakes_alive)),(0,0), 30).display_shadow()

                #Time attack for levels 2 and 3
                if level > 0:
                    #Work out time remaining
                    delta = datetime.datetime.now() - start_timer
                    Message("{0}".format("Time Left: {0}"\
                                    .format(30 - delta.seconds)),(830,0),30)\
                                                            .display_shadow()

                    #If time has passed, you fail the level
                    if 30 - delta.seconds <= 0:
                        level_failed = True

                pygame.display.flip()
                count += 1
                #del slope

            # End Game-play Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ##

            # You have either completed the level or failed it

            # FAILED: Ask if you would like to try again --------------- ##
            
            if level_failed:
                count = 0
                while count < 70:
                    space.step(1/30.0)
                    clock.tick(30)

                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit(0)
                        elif event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                pygame.quit()
                                sys.exit(0)
                            # Spacebar is pressed
                            if event.key == 32:
                                trying_again = True
                                # End the loop and start next level
                                count = 71

                    greyed_out.display()
                    
                    if count < 30:
                        Message("Good Try!", (320,250), 95).display_shadow()

                    if count > 30:
                        Message("Press SPACE to try again", (80,250), 80)\
                                                            .display_shadow()
                        Message("Press ESC to quit", (300,400), 60)\
                                                            .display_shadow()

                    pygame.display.flip()
                    count += 1

                    # Trick to halt the game on message
                    if count == 32:
                        count = 31

            # End Try again screen ------------------------------------ ##

            # You didn't fail, show next level screen ----------------- ##

            if level_complete:
                count = 0
                while count < 70:

                    for event in pygame.event.get():
                        if event.type == QUIT:
                            pygame.quit()
                            sys.exit(0)
                        elif event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                pygame.quit()
                                sys.exit(0)
                            if event.key == 32:
                                want_to_try_again = True
                                count = 71

                    greyed_out.display()
                    
                    # No need if you are on the last level,
                    # Just go to final conratulations screen
                    if level < 2:
                        # Display this message first
                        if count < 30:
                            Message("Well Done", (320,250), 95).display_shadow()

                        # Then this
                        if count > 30:
                            next_lvl = level + 2
                            Message("Level {0}".format(next_lvl),\
                                                 (350,250), 95).display_shadow()
                    else:
                        count = 71

                    pygame.display.flip()
                    count += 1
                if level == 2:
                    game_complete = True
                    trying_again = False
                else:
                    level += 1

        # End next level screen -------------------------------------- ##
       
        # Completed the game 
        # (can only try again or quit so must have won to get here)

        end_time = datetime.datetime.now()
        time_taken =  end_time - start_game_timer

        count = 0
        while count < 70:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit(0)
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)
                    if event.key == 32:
                        want_to_try_again = True
                        count = 71

            greyed_out.display()
            
            # Display this message first
            if count < 30:
                Message("Game Completed!", (130,250), 95).display_shadow()

            # Then this
            if count > 30:
                Message("You completed the game", (190,250), 65)\
                                                            .display_shadow()
                Message("In: {0} seconds".format(time_taken.seconds),\
                                                (230,350), 95).display_shadow()

            pygame.display.flip()
            count += 1

if __name__ == '__main__':
    main()
