from pubsub import pub


class GameObject:
    def __init__(self, id, data):
        self.properties = {}

        self.position = data.get("position")
        self.id = id
        self.kind = data.get("kind")
        self.size = data.get("size", [1.0, 1.0, 1.0])
        self.texture = data.get("texture", None)
        self._identifier = data.get("identifier", None)
        self.faces = data.get("faces", {})

        self._highlight = False
        self.visible = True
        self.gravity = True
        self.x_rotation = 0
        self.y_rotation = 0
        self.z_rotation = 0

        rotation = data.get("rotation")
        if rotation is not None:
            self.x_rotation, self.y_rotation, self.z_rotation = rotation

        self.behaviors = {}
        self.collisions = []
        self._moved = False
        self.collided = False

        pub.subscribe(self.inverseGravity, "inverse_gravity")
        pub.subscribe(self.clicked, "clicked-" + str(self.id))

        if self._identifier:
            pub.subscribe(self.clicked, "clicked-" + self._identifier)

    def add_behavior(self, behavior):
        self.behaviors[behavior.__class__.__name__] = behavior
        behavior.connect(self)

    @property
    def highlight(self):
        return self._highlight

    @property
    def identifier(self):
        return self._identifier

    @identifier.setter
    def identifier(self, value):
        self._identifier = value

    @property
    def moved(self):
        return self._moved

    @property
    def kind(self):
        return self._kind

    @kind.setter
    def kind(self, value):
        self._kind = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        self._position = value

    @property
    def x_rotation(self):
        return self._x_rotation

    @x_rotation.setter
    def x_rotation(self, value):
        self._x_rotation = value

    @property
    def y_rotation(self):
        return self._y_rotation

    @y_rotation.setter
    def y_rotation(self, value):
        self._y_rotation = value

    @property
    def z_rotation(self):
        return self._z_rotation

    @z_rotation.setter
    def z_rotation(self, value):
        self._z_rotation = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def tick(self):
        from game_logic import GameLogic

        if GameLogic.get_property("paused"):
            return
        self._moved = False
        self._highlight = False
        for behavior in self.behaviors:
            self.behaviors[behavior].tick()

        self.collisions = []

    def clicked(self, game_object):
        for behavior in self.behaviors:
            self.behaviors[behavior].clicked(game_object)

    def hover(self, game_object):
        for behavior in self.behaviors:
            self.behaviors[behavior].hover(game_object)

    def get_property(self, key, default=None):
        return self.properties.get(key, default)

    def set_property(self, key, value):
        self.properties[key] = value

    def inverseGravity(self):
        self.gravity = not self.gravity

    def mark_as_collided(self):
        if not self.collided:
            self.collided = True
        else:
            raise ValueError("Object has already collided")
