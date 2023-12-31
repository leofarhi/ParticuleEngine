from Particule.Modules.Includes import *
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.WindowEditor.SceneWindowEditor import SceneWindowEditor
from Particule.WindowEditor.HierarchyWindowEditor import HierarchyWindowEditor
from Particule.WindowEditor.InspectorWindowEditor import InspectorWindowEditor
from Particule.WindowEditor.ProjectWindowEditor import ProjectWindowEditor
from Particule.WindowEditor.ConsoleWindowEditor import ConsoleWindowEditor
from Particule.WindowEditor.BuildSettingsWindowEditor import BuildSettingsWindowEditor
from Particule.WindowEditor.PreferencesWindowEditor import PreferencesWindowEditor
from Particule.WindowEditor.ProjectSettingsWindowEditor import ProjectSettingsWindowEditor
from Particule.Modules.MyCustomTkinter.MyMenu import MyMenu

class SplitFrame(MyPanedWindow):
    def __init__(self, master, orient, **kwargs):
        super().__init__(master, orient=orient, **kwargs)
        self.orient = orient
        self.master = master

    def Split(self,*args,**kwargs):
        frame = self.SplitFrame(*args,**kwargs)
        tabview = MyTabview(frame,bg_color="transparent")
        #change sticky grid to "ns"
        tabview.pack(side=LEFT, fill=BOTH, expand=True)
        self.MainFrames[tabview] = frame
        return tabview
    

class ScreenOrganization:
    def __init__(self,_Particule):
        self.Particule = _Particule
        
        fn = self.Particule.MainFrame
        #make Header bar
        Header = ctk.CTkFrame(fn, height=50)
        Header.pack(side=TOP, fill=X)
        #make Body
        Body = ctk.CTkFrame(fn)
        Body.pack(side=TOP, fill=BOTH, expand=True)

        self.MainMenu = MyMenu(self.Particule.window)
        self.Particule.window.config(menu=self.MainMenu)
        
        SplitCenter = SplitFrame(Body, orient=VERTICAL)
        SplitCenter.pack(side=TOP, fill=BOTH, expand=True)

        Top = SplitCenter.SplitFrame(height=600)
        SplitCenter.MainFrames[Top].configure(height=600)
        BottomTabs = SplitCenter.Split()

        SplitTop = SplitFrame(Top, orient=HORIZONTAL)
        SplitTop.pack(side=TOP, fill=BOTH, expand=True)
        TopLeftTabs = SplitTop.Split(width=300)
        TopCenterTabs = SplitTop.Split(width=1100)
        SplitTop.MainFrames[TopCenterTabs].configure(width=1100)
        TopRightTabs = SplitTop.Split(width=500)

        self.windowEditors = {}

        scene = SceneWindowEditor(TopCenterTabs)
        scene.Pack()
        self.windowEditors["Scene"] = scene

        hierarchy = HierarchyWindowEditor(TopLeftTabs)
        hierarchy.Pack()
        self.windowEditors["Hierarchy"] = hierarchy

        inspector = InspectorWindowEditor(TopRightTabs)
        inspector.Pack()
        self.windowEditors["Inspector"] = inspector

        project = ProjectWindowEditor(BottomTabs)
        project.Pack()
        self.windowEditors["Project"] = project
        
        console = ConsoleWindowEditor(BottomTabs)
        console.Pack()
        self.windowEditors["Console"] = console

    def SaveInterfaceOrganization(self):
        #get children of Body
        root = None
        for i in self.Particule.MainFrame.winfo_children():
            if type(i) is SplitFrame:
                root = i
                break
        if root is None:
            return
        def RecursiveSave(node):
            for child in node.winfo_children():
                if type(child) is SplitFrame:
                    RecursiveSave(child)
                pass
        #à terminer
    def LoadInterfaceOrganization(self):
        pass


