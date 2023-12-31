from Particule.Modules.Includes import *
from Particule.OverwriteObject.Object import Object
from Particule.OverwriteObject.Component import Component
from Particule.OverwriteObject.Transform import Transform
from Particule.EnvironmentSystem import *


@OverwriteObject()
class GameObject(Object):
    def __init__(self, name="GameObject", UUID=None,*args, **kwargs):
        super().__init__(UUID,*args, **kwargs)
        self.name = name
        self.activeInHierarchy = True
        self.activeSelf = True
        self.isStatic = False
        #self.layer = Layer.Default
        #self.scene = scene
        #self.tag = Tag.Untagged
        if UUID==None:
            self.transform = Transform(self)
            self.components = [self.transform]

        self.frameOfComponents = None #la frame qui affiche les components dans l'Inspector

    def SetScene(self, scene):
        self.scene = scene
        hierarchy = self.Particule.GetEditor("Hierarchy")
        if hierarchy!= None:
            hierarchy.UpdateHierarchy(self)

    def setDict(self, dict):
        super().setDict(dict)
        if self.transform is None:
            self.transform = Transform(self)
            self.components = [self.transform]

    def Destroy(self):
        hierarchy = self.Particule.GetEditor("Hierarchy")
        if hierarchy!= None:
            hierarchy.RemoveGameObjectInHierarchy(self)
        for component in self.components:
            component.Destroy()
        self.components.clear()
        return super().Destroy()