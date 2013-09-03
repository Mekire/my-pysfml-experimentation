from __future__ import division
import os
import sys
import sfml as sf


DIRECT_DICT = {sf.Keyboard.LEFT  : (-1, 0),
               sf.Keyboard.RIGHT : ( 1, 0),
               sf.Keyboard.UP    : ( 0,-1),
               sf.Keyboard.DOWN  : ( 0, 1)}


SCREEN_SIZE = sf.Vector2(800, 600)
CAPTION = "Move me with the Arrow Keys."


class Player(object):
    def __init__(self,position,radius,speed):
        self.speed = speed
        self.image = sf.CircleShape()
        self.image.outline_thickness = 10
        self.image.radius = radius
        self.image.origin = (radius,radius)
        self.image.position = sf.Vector2(*position)
        self.image.outline_color = sf.Color.BLACK
        self.image.fill_color = sf.Color(255, 100, 200)

    def update(self,delta):
        movement = sf.Vector2(0,0)
        for key in DIRECT_DICT:
            if sf.Keyboard.is_key_pressed(key):
                movement[0] += DIRECT_DICT[key][0]*self.speed*delta
                movement[1] += DIRECT_DICT[key][1]*self.speed*delta
        self.image.move(movement)
        self.clamp(SCREEN_SIZE)

    def clamp(self,clamp_to):
        with_rad = self.image.radius+self.image.outline_thickness
        pos = [None,None]
        for i in (0,1):
            minny = max(self.image.position[i],with_rad)
            pos[i] = min(clamp_to[i]-with_rad,minny)
        self.image.position = pos


class Control(sf.RenderWindow):
    def __init__(self):
        sf.RenderWindow.__init__(self,sf.VideoMode(*SCREEN_SIZE), CAPTION)
##        self.vertical_synchronization = True
        self.framerate_limit = 60
        self.active = True
        self.clock = sf.Clock()
        self.player = Player(SCREEN_SIZE/2,100,300)
        self.done = False

    def event_loop(self):
        for event in self.events:
            if type(event) is sf.CloseEvent:
                self.close()
                self.done = True

    def main_loop(self):
        while not self.done:
            delta = self.clock.restart().seconds
            self.event_loop()
            self.player.update(delta)
            self.clear(sf.Color(255, 255, 255))
            self.draw(self.player.image)
            self.display()


if __name__ == "__main__":
    run_it = Control()
    run_it.main_loop()
    sys.exit()
