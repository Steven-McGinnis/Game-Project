from behavior import Behavior
import math

import time

class PowerUpBob(Behavior):
    def __init__(self, bob_distance, bob_speed):
        self.bob_distance = bob_distance
        self.bob_speed = bob_speed
        self.initial_position = None
        self.start_time = time.time()  # Time when the behavior started

    def connect(self, game_object):
        super().connect(game_object)
        self.initial_position = list(self.game_object.position) # type: ignore

    def tick(self):
        if self.initial_position is None:
            return

        # Calculate time since behavior started
        elapsed_time = time.time() - self.start_time

        # Calculate bobbing position based on a sine wave
        bob_position = math.sin(elapsed_time * self.bob_speed) * self.bob_distance

        # Apply bobbing position
        self.game_object.position[1] = self.initial_position[1] + bob_position # type: ignore
