from behavior import Behavior

class Jump(Behavior):
    def __init__(self, jump_speed, jump_height):
        self.jump_speed = jump_speed
        self.jump_height = jump_height
        self.is_jumping = False
        self.elapsed_time = 0 

    def tick(self):
        if self.is_jumping:
            progress = self.elapsed_time / self.jump_speed

            if progress > 1:
                self.is_jumping = False
                self.elapsed_time = 0
                self.game_object.position[1] = 0 #type: ignore
            else:
                height = 4 * self.jump_height * progress * (1 - progress)
                self.game_object.position[1] = height #type: ignore
                self.elapsed_time += 1

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.elapsed_time = 0
