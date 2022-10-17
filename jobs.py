import os


if __name__ == "__main__":
    for filename in os.listdir("./jobs"):
        if filename.endswith(".py"):
            print(filename[:-3])
            exec(open(f"./jobs/{filename}").read())
