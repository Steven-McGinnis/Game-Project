from behavior import Behavior
from game_logic import GameLogic
import numpy as np
from pubsub import pub


class Goto(Behavior):
    def __init__(self, destination, speed, distance, event=None):
        super(Goto, self).__init__()

        self.destination = destination
        self.speed = speed
        self.distance = distance
        self.event = event
        self.event_sent = False

    def get_destination(self):
        result = None

        if type(self.destination) == list:
            result = self.destination

        if type(self.destination) == str:
            obj = GameLogic.get_object(self.destination)

            if obj:
                result = obj.position

        return result

    def tick(self):
        destination = self.get_destination()

        if not destination:
            return

        destination = np.array(destination)
        current = np.array(self.game_object.position)  # type: ignore
        distance = np.linalg.norm(destination - current)

        if distance <= self.distance:
            if self.event and not self.event_sent:
                pub.sendMessage(self.event, game_object=self.game_object)
                self.event_sent = True
            return

        self.event_sent = False
        direction_vector = (destination - current) / distance
        self.game_object.position = (current + self.speed * direction_vector).tolist()  # type: ignore
        self.game_object._moved = True  # type: ignore
