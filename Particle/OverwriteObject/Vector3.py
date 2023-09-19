import math
from Particle.EnvironmentSystem import *
from Particle.WindowEditor.CustomComponentEditor import *

@OverwriteObject()
class Vector3(InstanceEnvironmentObject):
    def __init__(self, x=0, y=0, z=0,*args, **kwargs):
        super().__init__(*args, **kwargs)
        if type(x).__name__ == "Vector2":
            self.x = x.x
            self.y = x.y
            self.z = y
            return
        self.x = x
        self.y = y
        self.z = z

    def get(self):
        return (self.x, self.y, self.z)
    
    def set(self, _tuple):
        self.x, self.y, self.z = _tuple
        return self
    
    def __reference__(self, *args, **kwargs):
        return self.get()
    
    def __setreference__(data):
        return NewEnv(Vector3.__name__,*data)
    
    def __str__(self):
        return str((self.x, self.y, self.z))
    
    
    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        
        raise IndexError("Vector3 index out of range")
    
    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        
        raise IndexError("Vector3 index out of range")
    
    def __copy__(self):
        return Vector3(self.x, self.y, self.z)
    
    def __deepcopy__(self, memo):
        return Vector3(self.x, self.y, self.z)
        
@CustomPropertyDrawer("Vector3")
class Vector3Drawer(PropertyDrawer):
    def __init__(self,masterFrame,serializedProperty):
        super().__init__(masterFrame,serializedProperty)
        self.frame = Frame(self.masterFrame)
        self.frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.x = DoubleVar()
        self.y = DoubleVar()
        self.z = DoubleVar()
        vector3 = self.serializedProperty.GetValue()
        self.x.set(vector3.x)
        self.y.set(vector3.y)
        self.z.set(vector3.z)
        self.x.trace_add("write",self.OnValueChanged)
        self.y.trace_add("write",self.OnValueChanged)
        self.z.trace_add("write",self.OnValueChanged)
        #label grid
        self.label = Label(self.frame,text=self.serializedProperty.attributeName)
        self.label.grid(row=0,column=0)
        
        self.entry1 = Entry(self.frame,textvariable=self.x)
        self.entry1.grid(row=0,column=1)
        self.entry2 = Entry(self.frame,textvariable=self.y)
        self.entry2.grid(row=0,column=2)
        self.entry3 = Entry(self.frame,textvariable=self.z)
        self.entry3.grid(row=0,column=3)
        self.OnValueChanged()
        self.entry1.bind("<FocusOut>",self.OnFocusOut)
        self.entry2.bind("<FocusOut>",self.OnFocusOut)
        self.entry3.bind("<FocusOut>",self.OnFocusOut)

    def OnValueChanged(self,*args):
        val = self.serializedProperty.GetValue()
        try:
            self.x.get()
            self.y.get()
            self.z.get()
        except:
            return
        val.x = self.x.get()
        val.y = self.y.get()
        val.z = self.z.get()
        self.serializedProperty.SetValue(val)

    def OnFocusOut(self,*args):
        try:self.x.get()
        except:self.x.set(0)
        try:self.y.get()
        except:self.y.set(0)
        try:self.z.get()
        except:self.z.set(0)
        self.OnValueChanged()