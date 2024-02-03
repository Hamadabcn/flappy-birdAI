import pygame
import neat
import time
import os
import random
pygame.font.init()  # to start writing

WIN_WIDTH = 550
WIN_HEIGHT = 780
GEN = 0
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))), 
            pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
            pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))]
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
STAT_FONT = pygame.font.SysFont("ariel", 50)


# Bird class representing the flappy bird
class Bird:
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 20
    ANIMATION_TIME = 5
    
    # Initialize the object x, y positions
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
    
    # make the bird jump 
    def jump(self):
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y
    
    # make the bird move  
    def move(self):
        self.tick_count += 1 
        
        # for downward acceleration
        displacement = self.vel*self.tick_count + 1.5*self.tick_count**2
        
        if displacement >= 16:
            displacement = 16
            
        if displacement < 0:
            displacement -= 2
            
        self.y = self.y + displacement
        
        if displacement < 0 or self.y < self.height + 50: # to tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
                
            else: # to tilt down
                if self.tilt > -90:
                    self.tilt -= self.ROT_VEL
                    
    # draw the bird
    def draw(self, win):
        self.img_count += 1
        
        # For animation of bird, loop through three images
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0
            
        # so when bird is nose diving it isn't flapping
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
            
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center=self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
        
    # gets the mask for the current image of the bird
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
    
# represents a pipe object
class Pipe:
    GAP = 200
    VEL = 5

    def __init__(self, x): # initialize pipe object for x, y
        self.x = x
        self.height = 0 
    
        self.top = 0
        self.bottom = 0
        
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG
        
        self.passed = False
        
        self.set_height()
    
    # to set the height of the pipe, from the top of the screen
    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
        
    # move pipe based on vel
    def move(self):
        self.x -= self.VEL
        
    # draw both the top and bottom of the pipe
    def draw(self, win):
        
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        
    # returns if a point is colliding with the pipe
    def collide(self, bird, win):    
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))
        
        b_point = bird_mask.overlap(bottom_mask, bottom_offset) # if they don't collide this option will return none
        t_point = bird_mask.overlap(top_mask, top_offset)
        
        if b_point or t_point:
            return True
        return False
    
# represents the moving floor of the game
class Base:
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG
    
    def __init__(self, y): # Initialize the object
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH
        
    # move floor so it looks like its scrolling
    def move(self):
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
            
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
            
    # draw the floor, this is two images that move together
    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
        
# draws the windows for the main game loop     
def draw_window(win, birds, pipes, base, score, gen):
    win.blit(BG_IMG, (0, 0))
    
    for pipe in pipes:
        pipe.draw(win)
    
    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    
    text = STAT_FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(text, (10, 10))   
    
    base.draw(win)
    for bird in birds:
        bird.draw(win)
    pygame.display.update()
    
    
# runs the simulation of the current population of birds and sets their fitness based on the distance they reach in the game
def main(genomes, config):
    global GEN
    GEN += 1
    nets = []
    ge = []
    birds = []
    
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230,350))
        g.fitness = 0
        ge.append(g)
    
    base = Base(730)
    pipes = [Pipe(600)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    
    run = True
    while run:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                
        # determine whether to use the first or second pipe on the screen for neural network input
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break
                
        # give each bird a fitness of 0.1 for each frame it stays alive
        for x, bird in enumerate(birds):
            bird.move()
            ge[x].fitness += 0.1
            
            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[x].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            
            # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
            if output[0] > 0.5:
                bird.jump()
        
        #bird.move()
        add_pipe = False
        rem = []
        for pipe in pipes:
            for x, bird in enumerate(birds):
                if pipe.collide(bird, win):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                
                if not pipe.passed and pipe.x < bird.x: 
                    pipe.passed = True
                    add_pipe = True
                    
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)
                
            pipe.move()
            
        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5
            pipes.append(Pipe(600))
            
            
        for r in rem:
            pipes.remove(r)
        
        for x, bird in enumerate(birds):    
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)
        
        base.move()     
        draw_window(win, birds, pipes, base, score, GEN)

# runs the NEAT algorithm to train a neural network to play flappy bird
def run(config_path):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)
        
        # Create the population, which is the top-level object for a NEAT run
        p = neat.Population(config)
        
        # Add a stdout reporter to show progress in the terminal
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        
        # Run for up to 50 generations
        winner = p.run(main, 50)

# Determine path to configuration file
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.text")
    run(config_path)
    
# runs the NEAT algorithm to train a neural network to play flappy bird
def run(config_path):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)
        
        # Create the population, which is the top-level object for a NEAT run
        p = neat.Population(config)
        
        # Add a stdout reporter to show progress in the terminal
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        
        # Run for up to 50 generations
        winner = p.run(main, 50)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)
    