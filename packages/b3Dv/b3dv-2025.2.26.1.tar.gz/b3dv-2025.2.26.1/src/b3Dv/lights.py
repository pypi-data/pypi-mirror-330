import bpy

class SunLight:
    """
    SunLight class representing the Blender sun light object.
    """

    def __init__(self, name="Sun", location=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1), strength=5.0):
        """

        :param name: Name of the sun light object.
        :param location: Location of the sun light object in the global reference frame.
        :param rotation: Rotation of the sun light object in the global reference frame in radiants.
        :param scale: Scale of the sun light object in the global reference frame.
        :param strength: Strength of the sun light object.

        """
        self.data = bpy.data.lights.new(name, 'SUN')
        self.object = bpy.data.objects.new(name, self.data)
        self.object.location = location
        self.object.rotation_euler = rotation
        self.object.scale = scale
        self.data.energy = strength

    def setLocation(self, location):
        """
        Set location of the sun light object.

        :param location: Location of the sun light object in the global reference frame.

        """
        self.object.location = location

    def setRotation(self, rotation):
        """
        Set rotation of the sun light object.

        :param rotation: Rotation of the sun light object in the global reference frame in radiants.

        """
        self.object.rotation_euler = rotation

    def setScale(self, scale):
        """
        Set scale of the sun light object.

        :param scale: Scale of the sun light object in the global reference frame.

        """
        self.object.scale = scale

    def setStrength(self, strength):
        """
        Set strength of the sun light object.

        :param strength: Strength of the sun light object.

        """
        self.data.energy = strength