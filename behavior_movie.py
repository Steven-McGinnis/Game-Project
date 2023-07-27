from behavior import Behavior
from movies import Movies

from pubsub import pub

class Movie(Behavior):
    def __init__(self, movie, playevent, pauseevent, stopevent, loop=False):
        super(Movie, self).__init__()
    
        self.loop = loop
        self.movie = movie

        pub.subscribe(self.play, playevent)
        pub.subscribe(self.pause, pauseevent)
        pub.subscribe(self.stop, stopevent)


    def play(self, game_object):
        Movies.play_movie(self.movie, self.loop)

    def pause(self, game_object):
        Movies.pause_movie(self.movie)

    def stop(self, game_object):
        Movies.stop_movie(self.movie)
