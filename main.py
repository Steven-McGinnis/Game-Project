from game_logic import GameLogic
from player_view import PlayerView
from localize import Localize
from sounds import Sounds
from movies import Movies
from end_screen import EndScreen
from start_screen import StartScreen 


class Main:
    def go(self):
        GameLogic.load_world("level1.json")

        while True:
            GameLogic.tick()
            Sounds.tick()
            Movies.tick()

            for instance in self.instances:
                instance.tick()

            if GameLogic.get_property("quit"):
                break

        end_screen = EndScreen()  # create an EndScreen instance after the main game loop
        end_screen.display()  # display the end screen

    def __init__(self):
        self.instances = []

        Localize.load()

        # create instances
        self.instances.append(GameLogic)
        self.instances.append(PlayerView())


if __name__ == "__main__":

    start_screen = StartScreen()
    start_screen.display()
    main = Main()
    
    main.go()

    Localize.save()
