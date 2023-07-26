from pubsub import pub

class GameObject:
    def __init__(self, kind, id, position, size, texture=None, rotation= None, identifier=None):
        self.properties = {}
        self.position = position
        self.id = id
        self.kind = kind
        self.size = size
        self.texture = texture
        self.identifier = identifier
        self.visible = True
        self.gravity = True
        self.x_rotation = 0
        self.y_rotation = 0
        self.z_rotation = 0

        if rotation is not None:
            self.x_rotation, self.y_rotation, self.z_rotation = rotation


        self.behaviors = []
        self.collisions = []
        self._moved = False
        self.collided = False

        pub.subscribe(self.inverseGravity, "inverse_gravity")

    def add_behavior(self, behavior):
        self.behaviors.append(behavior)
        behavior.connect(self)

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
        self._moved = False
        for behavior in self.behaviors:
            behavior.tick()

        self.collisions = []

    def clicked(self):
        for behavior in self.behaviors:
            behavior.clicked()

    def get_property(self, key, default=None):
        if key in self.properties:
            return self.properties[key]

        return default

    def set_property(self, key, value):
        self.properties[key] = value

    def inverseGravity(self):
        self.gravity = not self.gravity
