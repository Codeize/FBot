from discord.ext import commands
import asyncio
from random import randint

emojis = ["⬆️", "⬇️"]
emojinames = ["up", "down"]
# ^ copied from snake.py, except dodgergame only has up and down

class dodgergame():

    def __init__(self):
        self.alive = True
        self.score = 0
        self.height = 3  # aka num of lanes
        self.width = 8  # one 'cell' is two emojis wide
        self.player = 1  # Player y-coord
        self.obstacles = list()  # List of xy tuples
        self.frames_between_obstacles = 2 # 1 = 1 obstacle per frame
        self.frames_until_obstacle = 0

    def get_board(self):
        # Get board state ready to ctx.send
        msg = ""
        for y in range(self.height):
            for x in range(self.width):
                if x == 0 and y == self.player:  # Player
                    msg += ":arrow_forward:"
                elif [x, y] in self.obstacles:  # Obstacle
                    msg += ":bomb:"
                else:  # Blank
                    msg += ":black_large_square:"  
            msg += "\n"
        msg += f"Score: {self.score}"
        return msg

    def move(self, direction):
        # Move player up/down/still
        if direction == "up":
            self.player -= 1
        elif direction == "down":
            self.player += 1
            
        # If player is out of bounds, move back
        # This can easily be modified so the player "loops" around the track
        if self.player < 0:
            self.player = 0
        elif self.player >= self.height:
            self.player = self.height - 1

        self.move_obstacles()
        self.check_collisions()

        self.frames_until_obstacle -= 1
        if self.frames_until_obstacle <= 0:
            self.frames_until_obstacle = self.frames_between_obstacles
            self.create_obstacle()

    def check_collisions(self):
        # Check if any obstacle is colliding with player
        # If so, set self.alive to False
        for obstacle in self.obstacles:
            if obstacle[0] == 0:
                if obstacle[1] == self.player:
                    self.alive = False

    def move_obstacles(self):
        # Move obstacles left, and remove them if they are off-screen
        obstacles_to_remove = list()
        for index, obstacle in enumerate(self.obstacles):
            obstacle[0] -= 1

            # If obstacle is off-screen, remove it
            # This also increments score
            if obstacle[0] < 0:
                obstacles_to_remove.append(index)
                self.score += 1
                
        self.obstacles = [obstacle for index, obstacle in
                          enumerate(self.obstacles) if not index in
                          obstacles_to_remove]
        # ^ cringe code to remove off-screen obstacles
        

    def create_obstacle(self):
        obstacle = [self.width - 1, randint(0, self.height - 1)]
        self.obstacles.append(obstacle)
    

class dodger(commands.Cog):
    game = dodgergame()

    @commands.command(name="dodger")
    async def _Dodger(self, ctx):

        game = dodgergame()

        await ctx.send(game.get_board()) # can be deleted

        while game.alive:
            # edit msg with: game.get_board()
            # ^ this includes "score = "

            # get user input here
            
            game.move("up")  # or "down" or "still" to not move
            
        # code to run when ded
        # fbux = game.score * 10
        
def setup(bot):
    bot.add_cog(dodger(bot))
