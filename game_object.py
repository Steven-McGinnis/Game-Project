class GameObject:
    def __init__(self, kind, id, position):
        self.position = position
        self.id = id
        self.kind = kind
        self.x_rotation = 0
        self.y_rotation = 0
        self.z_rotation = 0
    
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

    def tick(self):
        pass

    def clicked(self):
        pass
