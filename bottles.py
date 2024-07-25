#!/usr/bin/python3

class Bottles:
    def __init__(self, colors : int, setup : list) -> None:
        self.bottles = [[] for _ in range(colors + 2)]
        if len(setup) != colors * 4:
            raise SyntaxError
        else:
            for i, b in enumerate(setup):
                self.bottles[i//4].append(b)
        self.length = len(self.bottles)

    def __repr__(self) -> str:
        layers = [[] for _ in range(4)]
        for i in range(4):
            for b in self.bottles:
                if len(b) >= i + 1:
                    layers[i].append(b[i])
                else:
                    layers[i].append(" ")
        return "\n".join(["   ".join([f"|{i}|" for i in j]) for j in layers[::-1]]) + "\n" + " ".join([f"\\_/{i:<2}" for i in range(len(self.bottles))])

    def is_valid(self, a : int, b : int) -> bool:
        if a >= len(self.bottles) or b >= len(self.bottles) or len(self.bottles[a]) == 0 or len(self.bottles[b]) == 4:
            return False
        c = self.bottles[a][-1]
        return len(self.bottles[b]) == 0 or self.bottles[b][-1] == c

    def move(self, a : int, b : int):
        if self.is_valid(a, b):
            c = self.bottles[a][-1]
            count = 0
            for i in self.bottles[a][::-1]:
                if i == c:
                    count += 1
                else:
                    break
            avail = 4 - len(self.bottles[b])
            for _ in range(count if count <= avail else avail):
                self.bottles[a].pop()
                self.bottles[b].append(c)
            return True
        return False

    def is_complete(self) -> bool:
        colors = len(self.bottles) - 2
        empties = 0
        for b in self.bottles:
            if len(b) == 0:
                empties += 1
            elif len(b) == 4 and len(set(b)) == 1:
                colors -= 1
            else:
                return False
            if colors == 0:
                return True
            if empties > 2:
                return False
        return False



if __name__ == "__main__":
    b = None
    with open("colors.setup", "r") as f:
        lines = []
        for i in f.readlines():
            lines.append(i.strip())
        num = int(lines[0])
        b = Bottles(num, lines[1].split())
    while not b.is_complete():
        print(b)
        try:
            bot1 = int(input("bottle 1: "))
            bot2 = int(input("bottle 2: "))
        except ValueError:
            print("whoopsie daisies, invalid input")
            continue
        b.move(bot1, bot2)
        print("Yay")
