import math
from Particule.EnvironmentSystem import *
from Particule.WindowEditor.CustomComponentEditor import *

@OverwriteObject()
class Vector2(InstanceEnvironmentObject):
    def __init__(self, x=0, y=0,*args, **kwargs):
        super().__init__(*args, **kwargs)
        if type(x).__name__ == "Vector3":
            self.x = x.x
            self.y = x.y
            return
        self.x = x
        self.y = y

    def get(self):
        return (self.x, self.y)
    
    def set(self, _tuple):
        self.x, self.y = _tuple
        return self
    
    def __reference__(self, *args, **kwargs):
        return self.get()
    
    def __setreference__(data):
        return NewEnv(Vector2.__name__,*data)

    def __str__(self):
        return str((self.x, self.y))

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value

    
    def __copy__(self):
        return Vector2(self.x, self.y)
    
    def __deepcopy__(self, memo):
        return Vector2(self.x, self.y)

@CustomPropertyDrawer("Vector2")
class Vector2Drawer(PropertyDrawer):
    def __init__(self,masterFrame,serializedProperty):
        super().__init__(masterFrame,serializedProperty)
        self.frame = ctk.CTkFrame(self.masterFrame)
        self.frame.pack(fill="x", expand=1, pady=2, padx=2, anchor="n")
        self.x = WithDefaultValueVar(DoubleVar,0)
        self.y = WithDefaultValueVar(DoubleVar,0)
        vector2 = self.serializedProperty.GetValue()
        self.x.set(vector2.x)
        self.y.set(vector2.y)
        self.x.trace_add("write",self.OnValueChanged)
        self.y.trace_add("write",self.OnValueChanged)
        #label grid
        self.label = ctk.CTkLabel(self.frame,text=self.serializedProperty.attributeName)
        self.label.grid(row=0,column=0,padx=2)

        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        
        self.entry1 = ctk.CTkEntry(self.frame,textvariable=self.x)
        self.entry1.grid(row=0,column=1,sticky="ew")
        self.entry2 = ctk.CTkEntry(self.frame,textvariable=self.y)
        self.entry2.grid(row=0,column=2,sticky="ew")
        self.OnValueChanged()
        self.entry1.bind("<FocusOut>",self.OnFocusOut)
        self.entry2.bind("<FocusOut>",self.OnFocusOut)

    def OnValueChanged(self,*args):
        val = self.serializedProperty.GetValue()
        val.x = self.x.get()
        val.y = self.y.get()
        self.serializedProperty.SetValue(val)

    def OnFocusOut(self,*args):
        self.x.fix()
        self.y.fix()
        self.OnValueChanged()