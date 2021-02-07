from discord.ext import commands
from functions import cooldown
from collections import deque
import asyncio

from random import randint, choice

emojis = ["⬆️", "⬇️", "⬅️", "➡️"]
emojinames = ["up", "down", "left", "right"]

food_emojis = [":green_apple:", ":apple:", ":pear:", ":tangerine:", ":lemon:",
               ":banana:", ":watermelon:", ":grapes:", ":blueberries:",
               ":strawberry:", ":melon:", ":cherries:", ":peach:", ":mango:",
               ":pineapple:", ":coconut:", ":kiwi:", ":tomato:", ":eggplant:",
               ":avocado:", ":corn:", ":carrot:", ":croissant:", ":bread:",
               ":cheese:", ":bacon:", ":cut_of_meat:", ":poultry_leg:",
               ":meat_on_bone:", ":hotdog:", ":hamburger:", ":pizza:",
               ":taco:", ":fried_shrimp:", ":rice_ball:", ":icecream:",
               ":pie:", ":cupcake:", ":doughnut:", ":cookie:", ":chestnut:",
               ":peanuts:"]

class snakegame():
    
    def __init__(self):
        self.alive = True
        self.score = 0
        self.width  = 8
        self.height = 8
        self.direction = "right"
        self.food_emoji = ":apple:"  # This is immediately overwritten

        self.snake = deque()
        self.snake.appendleft((0, int(self.height/2)))
        self.snake.appendleft((1, int(self.height/2)))
        self.snake.appendleft((2, int(self.height/2)))

        self.food = self.create_food_coords()

    def board(self):
        output = f"**Score:** {self.score}\n"
        for y in range(self.height):
            output += "¦"
            for x in range(self.width):
                if (x, y) in self.snake:
                    if (x, y) == self.snake[0]:
                        if self.alive:
                            output += ":flushed:"
                        else:
                            output += ":dizzy_face:"
                    elif (x, y) == self.snake[-1]:
                        output += ":yellow_circle:"
                    else:
                        output += ":yellow_square:"
                elif (x, y) == self.food:
                    output += self.food_emoji
                else:
                    output += "<:blank:807750557032513556>"
                    
            output += "¦\n"
        return output

    def move(self):
        x, y = self.snake[0]
        direction = self.direction
        if direction == "up": y -= 1
        elif direction == "down": y += 1
        if direction == "left": x -= 1
        elif direction == "right": x += 1

        if x < 0 or x > self.width-1 or y < 0 or y > self.height-1:
            self.alive = False
            return
        
        if (x, y) in self.snake:
            self.alive = False
            return
        
        self.snake.appendleft((x, y))
        
        if (x, y) == self.food:
            self.food = self.create_food_coords()
            self.score += 1
        else:
            self.snake.pop()

    def create_food_coords(self):
        self.food_emoji = choice(food_emojis)
        x, y = randint(0, self.width-1), randint(0, self.height-1)
        while (x, y) in self.snake:
            x, y = randint(0, self.width-1), randint(0, self.height-1)
        return (x, y)
    

class snake(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.games = {}
    @commands.cooldown(1, 60, type=commands.BucketType.user)
    @commands.command(name="snake", aliases=["snek"])
    @commands.cooldown(1, 1, type=commands.BucketType.user)
    async def _Snake(self, ctx):

        user_id = ctx.author.id
        if user_id in self.games:
            await ctx.send("You are already in a game!")
            return

        game = self.games[user_id] = snakegame()
        msg = await ctx.send(game.board())

        for emoji in emojis:
            await msg.add_reaction(emoji)

        while True:
            await asyncio.sleep(0.8)
            game.move()
            await msg.edit(content=game.board())
            if not game.alive: break
        del self.games[user_id]

        fbux = game.score * 10
        self.bot.db.updatebal(ctx.author.id, fbux)
        await ctx.send("**You died, game over!**\n"
                       f"However you managed to earn **~~f~~ {fbux}**")

    @_Snake.error
    async def on_command_error(self, ctx, error):
        if type(error) is commands.CommandOnCooldown:
            wait = round(error.retry_after)
            await ctx.send(f"You must wait another {wait} seconds before playing snake again")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.id not in self.games: return
        emoji = reaction.emoji
        if emoji in emojis:
            self.games[user.id].direction = emojinames[emojis.index(emoji)]        
        await reaction.message.remove_reaction(reaction, user)
        
def setup(bot):
    bot.add_cog(snake(bot))
