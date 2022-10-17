import os


class Jobs:
    def __init__(self):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                print(filename[:-3])
                #~ exec(open(filename).read())
