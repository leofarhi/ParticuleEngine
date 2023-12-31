import subprocess
import platform

from Particule.OverwriteObject.Vector3 import Vector3
from Particule.OverwriteObject.Vector2 import Vector2

from Particule.Modules.Screen import GetScreenSize
from Particule.Modules.Includes import *
from Particule.Modules.LanguageSystem import LanguageSystem
from Particule.Modules.Directory import *
from Particule.WindowEditor.WindowEditor import WindowEditor
from Particule.WindowEditor.HubWindowEditor import HubWindowEditor
from Particule.WindowEditor.SceneWindowEditor import SceneWindowEditor
from Particule.ScreenOrganization import ScreenOrganization
from Particule.AssetSystem import AssetSystem
from Particule.SceneManager import SceneManager
from Particule.OverwriteObject.AssetItem import AssetItem
from Particule.OverwriteObject.Scene import Scene
from Particule.OperationsSystem import OperationsSystem

from Particule.EnvironmentSystem import NewEnv,EnvironmentSystem

ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class Particule:
    version = "2023.1b"
    def __init__(self):
        GlobalVars.Particule = self
        self.window = None
        self.config = {
            "name": "",
            "projectPath": "",
            "template": "",
            "language":"",
            "version":"",
            "lastOpened": "",
            "scene": "",#Scene actuellement ouverte (UUID)
        }
        self.ParticulePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

    def HubWindow(self):
        hub = HubWindowEditor()
        hub.Pack()

    def GetEditor(self,editorName):
        return self.screenOrganization.windowEditors.get(editorName,None)

    def SaveConfig(self,config=None):
        if config == None:
            config = self.config
        with open(os.path.join(config["projectPath"], "config.proj"), "w") as file:
            json.dump(config, file, indent=4)

    def AddCommandsMenu(self,path:str,commands:dict,addSeparator=True):
        if addSeparator:
            self.screenOrganization.MainMenu.AddSeparator(path)
        for command in commands:
            self.screenOrganization.MainMenu.AddCommand(path+"/"+command,commands[command])

    def SetActiveCommandMenu(self,fullPath:str,active:bool):
        if active:
            self.screenOrganization.MainMenu.EnableCommand(fullPath)
        else:
            self.screenOrganization.MainMenu.DisableCommand(fullPath)

    def SetSecondMainFrame(self):
        if self.SecondFrame != None:
            return None
        self.MainFrame.pack_forget()
        self.SecondFrame = ctk.CTkFrame(self.window)
        self.SecondFrame.pack(fill=BOTH, expand=True)
        return self.SecondFrame

    def SetMainFrame(self):
        if self.SecondFrame != None:
            self.SecondFrame.destroy()
            self.SecondFrame = None
        self.MainFrame.pack(fill=BOTH, expand=True)

    def Start(self):
        self.window = ctk.CTk()
        self.window.title('Particule - ' + Particule.version)
        screen_size = GetScreenSize()
        self.window.geometry(str(screen_size[0]) + "x" + str(screen_size[1]))
        WindowEditor.LoadWindowIcon(self)
        #can resize
        self.window.resizable(True, True)
        #Mettre en plein écran
        self.window.attributes('-fullscreen', False)

        pathProject = self.config.get("projectPath")
        try:
            DeleteDir(os.path.join(pathProject, "Library", "tmp"))
            DeleteDir(os.path.join(pathProject, "Build"))
        except:
            pass
        CreateDir(os.path.join(pathProject, "Assets"))
        CreateDir(os.path.join(pathProject, "Library"))
        CreateDir(os.path.join(pathProject, "Library", "tmp"))
        CreateDir(os.path.join(pathProject, "Build"))

        self.MainFrame = ctk.CTkFrame(self.window)
        self.MainFrame.pack(fill=BOTH, expand=True)
        self.SecondFrame = None

        self.environmentSystem = EnvironmentSystem(self)
        self.environmentSystem.roots.append(self.ParticulePath+"/Engine")
        self.environmentSystem.UpdateFiles()
        self.environmentSystem.Compile()

        self.sceneManager = SceneManager(self)
        self.screenOrganization = ScreenOrganization(self)
        self.assetSystem = AssetSystem(self)
        self.assetSystem.ScanAssets()
        
        CallBacksStackCall("OnCreateMenu")

        self.environmentSystem.roots.append(self.config["projectPath"]+"/Assets")
        self.environmentSystem.UpdateFiles()
        self.environmentSystem.Compile()

        self.operationsSystem = OperationsSystem(self)

        self.LoadLastScene()

        #Quitter
        self.window.protocol("WM_DELETE_WINDOW", self.Quit)
        self.window.bind("<F11>", self.ToggleFullScreen)
        self.window.mainloop()

    def ToggleFullScreen(self, event=None):
        #change geometry
        self.window.geometry("{0}x{1}+0+0".format(*GetScreenSize()))
        ScalingTracker.deactivate_automatic_dpi_awareness = not ScalingTracker.deactivate_automatic_dpi_awareness
        self.window.attributes("-fullscreen", not self.window.attributes("-fullscreen"))
    
    def Restart(self):
        self.window.destroy()
        self.Start()

    def LoadLastScene(self):
        pathProject = self.config.get("projectPath")
        #Load Scene
        scene_UUID = self.config.get("scene")
        if scene_UUID != "":
            #Check if UUID exist
            sceneAsset = AssetItem.GetAssetItemFromUUID(scene_UUID)
            if sceneAsset != None:
                #Load scene
                self.sceneManager.LoadScene(sceneAsset)
            else:
                scene_UUID = ""
        if scene_UUID == "":
            #Check if int Assets/Scenes/SampleScene.scene exist
            path_scene_sample =os.path.join(pathProject, "Assets", "Scenes", "SampleScene.scene")
            if os.path.isfile(path_scene_sample):
                #Load SampleScene
                sceneAsset = AssetItem.GetAssetItem(path_scene_sample)
                self.sceneManager.LoadScene(sceneAsset)
            else:
                #Create SampleScene
                CreateDir(os.path.join(pathProject, "Assets", "Scenes"))
                self.sceneManager.CreateScene(os.path.join(pathProject, "Assets", "Scenes", "SampleScene.scene"))

    def Quit(self):
        if messagebox.askokcancel(LanguageSystem.GetText("Quit"),
                                  LanguageSystem.GetText("Voulez-vous vraiment quitter ?")):
            self.window.destroy()

    @AddCallBackToStack("OnCreateMenu")
    def OnCreateMenu():
        GlobalVars.Particule.AddCommandsMenu("File", {
            "Quitter": GlobalVars.Particule.Quit
        }, True)
