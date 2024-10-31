"""
This is the main entry of your program. Almost all things you need to implement are in this file.
The main class Sketch inherits from CanvasBase. For the parts you need to implement, they are all marked with TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun)
:version: 2021.1.1

Modified by Daniel Scrivener 07/2022


Modified by Jack Weber 10/2024
Instantiated my own character
Added an "active" list variable to keep track of currently chosen limbs in replace of the single variable previously
I removed the Interrupt scroll function because changing it to implement multi-select was too complex and technical debt
Updated the interrupt keyboard function to implement multi select
Updated the select feature to add the limb to active rather than only supporting one at a time
Updated left and right to change the color of every limb that is active
Updated up and down to rotate every active limb and then made it so if it's on the right side it's mirrored from the left side
(We know its left vs right because I named them ...1 or ...2 accordingly
Updated escape to reset the color of all active and reset the active lsit and to reset axis index
Added cycling through poses and added 5 poses

"""

import math

import numpy as np
from ModelAxes import ModelAxes
from ModelLinkage import ModelLinkage

import ColorType
from Point import Point
from CanvasBase import CanvasBase
from GLProgram import GLProgram
from Quaternion import Quaternion
import GLUtility

try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")
try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError
try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")


class Sketch(CanvasBase):
    """
    Drawing methods and interrupt methods will be implemented in this class.
    
    Variable Instruction:
        * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will print more details and do some type checking, which might be helpful in debugging

        
    Method Instruction:
        
        
    Here are the list of functions you need to override:
        * Interrupt_MouseL: Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
        * Interrupt_MouseLeftDragging: Used to deal with mouse dragging interruption.
        * Interrupt_Keyboard: Used to deal with keyboard press interruption. Use this to add new keys or new methods
        
    Here are some public variables in parent class you might need:
        
        
    """
    context = None

    debug = 1

    last_mouse_leftPosition = None
    last_mouse_middlePosition = None
    components = None

    texture = None
    shaderProg = None
    glutility = None

    lookAtPt = None
    upVector = None
    backgroundColor = None
    # use these three to control camera position, mainly used in mouse dragging
    cameraDis = None
    cameraTheta = None  # theta on horizontal sphere cut, in range [0, 2pi]
    cameraPhi = None  # in range [-pi, pi], for smooth purpose

    viewMat = None
    perspMat = None

    # Changed this to default to 0 so that we can keep conccurent axis across multi select
    select_axis_index = 0  # index of selected axis
    select_color = [ColorType.ColorType(1, 0, 0), ColorType.ColorType(0, 1, 0), ColorType.ColorType(0, 0, 1)]


    # Added this to allow to track what components are active across frames
    # Essentially select_obj index but with multiple components
    active = []

    # The number of the current pose
    pose_num = -1 
    # List of angles to set every limb to for each pose
    # Poses:
    # Waving left hand
    # Grabbing in front
    # Jumping
    # Both down
    # up down down
    poses = [
        # BODY        ARM1         BACKARM1     FOREARM1    TOPPIN1    BOTPIN1     ARM2       BACKARM2      FOREARM2    TOPPIN2     BOTPIN2      Stalk1         Eye1          Stalk2        Eye2      Fleg1       SLeg1      Tleg1       ffoot1       sfoot1      tfoot1      Fleg2        Sleg2        Tleg2        ffoot2      sfoot2         tfoot2
        [[0, 0, 0], [-30, 0, 0], [-15, 0, 0], [-15, 0, 0], [0, 0, 0], [0, 0, 0], [-30, 0, 0], [-15, 0, 0], [-15, 0, 0], [0, 0, 0],  [0, 0, 0], [30, 30, 30],   [0, 0, 0], [-30, -30, -30],[0, 0, 0], [30, 0, 0], [30, 0, 0], [30, 0, 0], [30, 0, 0],  [30, 0, 0], [30, 0, 0], [-30, 0, 0], [-30, 0, 0], [-30, 0, 0], [-30, 0 ,0], [-30, 0, 0], [-30, 0, 0]],
        [[0, 0, 0], [0, 45, 0], [0, 15, 0], [0, 15, 0], [15, 0, 0], [-15, 0, 0], [0, -45, 0], [0, -15, 0], [0, -15, 0], [-15, 0, 0],[15, 0, 0], [0, 0, 0],     [0, 0, 0], [0, 0, 0],      [0, 0, 0], [30, 0 ,0], [30, 0, 0], [30, 0, 0], [30, 0, 0],  [30, 0, 0], [30, 0, 0], [-30, 0, 0], [-30, 0, 0], [-30, 0, 0], [-30, 0, 0], [-30, 0, 0], [-30, 0, 0]],
        [[0, 0, 0], [-30, 0, 0], [-15, 0, 0], [-15, 0, 0], [0, 0, 0], [0, 0, 0], [30, 0, 0],  [15, 0, 0],  [15, 0, 0],  [0, 0, 0],  [0, 0, 0], [-30, -30, -30], [0, 0, 0], [30, 30, 30],  [0, 0, 0], [0, 0, 0],  [0, 0, 0],  [0, 0, 0],  [30, 0, 0],  [30, 0, 0], [30, 0, 0], [0, 0, 0],   [0, 0, 0],   [0, 0, 0],   [-30, 0, 0], [-30, 0, 0], [-30, 0, 0]],
        [[0, 0, 0], [30, 0, 0], [15, 0, 0], [15, 0, 0], [7, 0, 0], [-7, 0, 0], [-30, 0, 0], [-15, 0, 0], [-15, 0, 0],   [-7, 0, 0], [7, 0, 0], [30, 0, 30],     [0, 0, 0], [-30, 0, -30], [0, 0, 0], [30, 0, 0], [30, 0, 0], [30, 0, 0], [30, 0, 0],  [30, 0, 0], [30, 0, 0], [-30, 0, 0], [-30, 0, 0], [-30, 0, 0], [-30, 0, 0], [-30, 0, 0], [-30, 0, 0]],
        [[0, 0, 0], [-30, 0, 0], [15, 0, 0], [15, 0, 0], [15, 0, 0], [-15, 0, 0], [30, 0, 0], [-15, 0, 0], [-15, 0, 0], [-15, 0, 0],[15, 0, 0], [0, -30, 0],    [0, 0, 0], [0, 30, 0],    [0, 0, 0], [30, 0, 0], [30, 0, 0], [30, 0, 0], [-30, 0, 0], [-30, 0, 0],[-30, 0, 0], [-30, 0 ,0],[-30, 0 ,0], [-30, 0 ,0], [30, 0, 0], [30, 0, 0],   [30, 0, 0]],
    ]

    # If you are having trouble rotating the camera, try increasing this parameter
    # (Windows users with trackpads may need this)
    MOUSE_ROTATE_SPEED = 1
    MOUSE_SCROLL_SPEED = 2.5

    def __init__(self, parent):
        super(Sketch, self).__init__(parent)
        # prepare OpenGL context
        contextAttrib = glcanvas.GLContextAttrs()
        contextAttrib.PlatformDefaults().CoreProfile().MajorVersion(3).MinorVersion(3).EndList()
        self.context = glcanvas.GLContext(self, ctxAttrs=contextAttrib)
        # Initialize Parameters
        self.last_mouse_leftPosition = [0, 0]
        self.last_mouse_middlePosition = [0, 0]
        self.backgroundColor = ColorType.BLUEGREEN

        # add components to top level
        self.resetView()

        self.glutility = GLUtility.GLUtility()

    def resetView(self):
        self.lookAtPt = [0, 0, 0]
        self.upVector = [0, 1, 0]
        self.cameraDis = 6
        self.cameraPhi = math.pi / 6
        self.cameraTheta = math.pi / 2

        
    def InitGL(self):
        """
        Called once in order to initialize the OpenGL environemnt.
        You must set your model here (and not in __init__)
        due to the fact that the shader is only compiled once we reach this function.
        """
        self.shaderProg = GLProgram()
        self.shaderProg.compile()

        ##### TODO 3: Initialize your model
        # You should initialize your model here.
        # self.topLevelComponent should refer to your model
        # and self.components should refer to your model's components.
        # Optionally, you can create a dictionary (self.cDict) to index your model's components by name.

        model = ModelLinkage(self, Point((0, 0, 0)), self.shaderProg)

        
        axes = ModelAxes(self, Point((-1, -1, -1)), self.shaderProg)

        self.topLevelComponent.clear()
        self.topLevelComponent.addChild(model)
        self.topLevelComponent.addChild(axes)
        self.topLevelComponent.initialize()

        self.components = model.componentList
        self.cDict = model.componentDict

        gl.glClearColor(*self.backgroundColor, 1.0)
        gl.glClearDepth(1.0)
        gl.glViewport(0, 0, self.size[0], self.size[1])

        # enable depth checking
        gl.glEnable(gl.GL_DEPTH_TEST)

        # set basic viewing matrix
        self.perspMat = self.glutility.perspective(45, self.size.width, self.size.height, 0.01, 100)
        self.shaderProg.setMat4("projectionMat", self.perspMat)
        self.shaderProg.setMat4("viewMat", self.glutility.view(self.getCameraPos(), self.lookAtPt, self.upVector))
        self.shaderProg.setMat4("modelMat", np.identity(4))

    def getCameraPos(self):
        ct = math.cos(self.cameraTheta)
        st = math.sin(self.cameraTheta)
        cp = math.cos(self.cameraPhi)
        sp = math.sin(self.cameraPhi)
        result = [self.lookAtPt[0] + self.cameraDis * ct * cp,
                  self.lookAtPt[1] + self.cameraDis * sp,
                  self.lookAtPt[2] + self.cameraDis * st * cp]
        return result

    def OnResize(self, event):
        contextAttrib = glcanvas.GLContextAttrs()
        contextAttrib.PlatformDefaults().CoreProfile().MajorVersion(3).MinorVersion(3).EndList()
        self.context = glcanvas.GLContext(self, ctxAttrs=contextAttrib)
        self.size = self.GetClientSize()
        self.size[1] = max(1, self.size[1])  # avoid divided by 0
        self.SetCurrent(self.context)

        self.init = False
        self.Refresh(eraseBackground=True)
        self.Update()

    def OnPaint(self, event=None):
        """
        This will be called at every frame
        """
        self.SetCurrent(self.context)
        if not self.init:
            # Init the OpenGL environment if not initialized
            self.InitGL()
            self.init = True
        # the draw method
        self.OnDraw()

    def OnDraw(self):
        gl.glClearColor(*self.backgroundColor, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # These are per-frame updates to the shader. Update the viewing matrix
        self.viewMat = self.glutility.view(self.getCameraPos(), self.lookAtPt, self.upVector)
        self.shaderProg.setMat4("viewMat", self.viewMat)

        self.topLevelComponent.update(np.identity(4))
        self.topLevelComponent.draw(self.shaderProg)

        self.SwapBuffers()

    def OnDestroy(self, event):
        """
        Window destroy event binding

        :param event: Window destroy event
        :return: None
        """
        if self.shaderProg is not None:
            del self.shaderProg
        super(Sketch, self).OnDestroy(event)

    def Interrupt_MouseMoving(self, x, y):
        ##### TODO 6 (CS680 Required, CS480 Extra Credit): Eye movement
        # Make your creature's eyes follow the cursor.
        # The eye rotation only needs to work correctly when the creature is looking toward the viewer.
        # You do not need to account for other camera orientations.
        # Try to implement this using quaternions for additional credit!
        return


    def unprojectCanvas(self, x, y, u=0.5):
        """
        unproject a canvas point to world coordiantes. 2D -> 3D
        you need give an extra parameter u, to tell the method how far are you from znear
        u is the proportion of distance to znear / zfar-znear
        in the gluUnProject, the distribution of z is not linear when using perspective projection,
        so z=0.5 is not in the middle,
        that's why we compute out the ray and use linear interpolation and u to get the point

        :param u: u is the proportion to the znear/, in range [0, 1]
        :type u: float
        """
        result1 = self._unproject(x, y, 0.0)
        result2 = self._unproject(x, y, 1.0)
        result = Point([(1 - u) * r1 + u * r2 for r1, r2 in zip(result1, result2)])
        return result

    def _unproject(self, x, y, z):
        model_matrix = np.identity(4)
        proj_matrix = self.viewMat @ self.perspMat
        viewport = gl.glGetIntegerv(gl.GL_VIEWPORT)
        model_view_proj_matrix = proj_matrix @ model_matrix
        inv_model_view_proj_matrix = np.linalg.inv(model_view_proj_matrix)

        x_ndc = (x - viewport[0]) / viewport[2] * 2.0 - 1.0
        y_ndc = (y - viewport[1]) / viewport[3] * 2.0 - 1.0
        z_ndc = 2.0 * z - 1.0
        
        ndc_coords = np.array([x_ndc, y_ndc, z_ndc, 1.0])
        world_coords = inv_model_view_proj_matrix.T @ ndc_coords # transpose because they are row-major
        if world_coords[3] != 0:
            world_coords /= world_coords[3]
        return world_coords[:3]

    def Interrupt_MouseL(self, x, y):
        """
        When mouse click detected, store current position in last_mouse_leftPosition

        :param x: Mouse click's x coordinate
        :type x: int
        :param y: Mouse click's y coordinate
        :type y: int
        :return: None
        """
        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def Interrupt_MouseMiddleDragging(self, x, y):
        """
        When mouse drag motion with middle key detected, interrupt with new mouse position

        :param x: Mouse drag new position's x coordinate
        :type x: int
        :param y: Mouse drag new position's x coordinate
        :type y: int
        :return: None
        """

        if self.new_dragging_event:
            self.last_mouse_middlePosition[0] = x
            self.last_mouse_middlePosition[1] = y
            return
        
        dx = x - self.last_mouse_middlePosition[0]
        dy = y - self.last_mouse_middlePosition[1]

        originalMidPt = self.unprojectCanvas(*self.last_mouse_middlePosition, 0.5)

        self.last_mouse_middlePosition[0] = x
        self.last_mouse_middlePosition[1] = y

        currentMidPt = self.unprojectCanvas(x, y, 0.5)
        changes = currentMidPt - originalMidPt
        moveSpeed = 0.185 * self.cameraDis / 6
        self.lookAtPt = [self.lookAtPt[0] - changes[0] * moveSpeed,
                         self.lookAtPt[1] - changes[1] * moveSpeed,
                         self.lookAtPt[2] - changes[2] * moveSpeed]

    def Interrupt_MouseLeftDragging(self, x, y):
        """
        When mouse drag motion detected, interrupt with new mouse position

        :param x: Mouse drag new position's x coordinate
        :type x: int
        :param y: Mouse drag new position's x coordinate
        :type y: int
        :return: None
        """

        if self.new_dragging_event:
            self.last_mouse_leftPosition[0] = x
            self.last_mouse_leftPosition[1] = y
            return

        # Change viewing angle when dragging happened
        dx = x - self.last_mouse_leftPosition[0]
        dy = y - self.last_mouse_leftPosition[1]

        # restrict phi movement range, stop cameraphi changes at pole points
        self.cameraPhi = min(math.pi / 2, max(-math.pi / 2, self.cameraPhi - dy / 50))
        self.cameraTheta += dx / 100 * (self.MOUSE_ROTATE_SPEED)

        self.cameraTheta = self.cameraTheta % (2 * math.pi)

        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def update(self):
        """
        Update current canvas
        :return: None
        """
        self.topLevelComponent.update(np.identity(4))

    def Interrupt_Keyboard(self, keycode):
        """
        Keyboard interrupt bindings

        :param keycode: wxpython keyboard event's keycode
        :return: None
        """

        ##### TODO 5: Set up your poses and finish the user interface
        # Define keyboard events to make your creature act in different ways when keys are pressed.
        # Create five unique poses to demonstrate your creature's joint rotations.
        # HINT: selecting individual components is easier if you create a dictionary of components (self.cDict)
        # that can be indexed by name (e.g. self.cDict["leg1"] instead of self.components[10])

        # I ADDED THESE TO HELP MULTISELECT
        limbs = "1234567890asdfghjklzxcvbnm," 
        dict_keys = list(self.cDict.keys())

        # Code for multiselect
        # The keycodes for each limb
        if chr(keycode) in limbs:
            # Get the limb name from what keycode was pressed
            key_index = limbs.index(chr(keycode))
            limb_name = dict_keys[key_index]
            # Get the index in components from our limb name
            c_index = self.components.index(self.cDict[limb_name])
            # If it's selected and its not active, put it in active and color it, otherwise remove it and reset it
            if limb_name not in self.active:
                self.active.append(limb_name)
                self.components[c_index].setCurrentColor(self.select_color[self.select_axis_index])
            else:
                self.active.remove(limb_name)
                self.components[c_index].reset("color")
            self.update()

        if keycode in [wx.WXK_LEFT]:
            # Last rotation axis
            self.select_axis_index = (self.select_axis_index - 1) % 3

            # go through each limb and update their color
            for limb in self.active:
                c_index = self.components.index(self.cDict[limb])
                self.components[c_index].setCurrentColor(self.select_color[self.select_axis_index])

            self.update()
        if keycode in [wx.WXK_RIGHT]:
            # Next rotation axis
            self.select_axis_index = (self.select_axis_index + 1) % 3
            for limb in self.active:
                c_index = self.components.index(self.cDict[limb])
                self.components[c_index].setCurrentColor(self.select_color[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_UP]:
            # Increase rotation angle
            for limb in self.active:
                mirror = 1
                # All limbs with 2 at the end are on the right, to mirror if right then negative increse
                if limb[-1] == "2":
                    mirror = -1
                c_index = self.components.index(self.cDict[limb])
                # Got rid of wheel rotation and just added it to be mirror
                # Just got rid of intterupt scroll and put it here, needlessly compelx to change it to fit multi select
                self.components[c_index].rotate(mirror * self.MOUSE_SCROLL_SPEED,
                                                        self.components[c_index].
                                                        axisBucket[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_DOWN]:
            for limb in self.active:
                mirror = -1
                # All limbs with 2 at the end are on the right, to mirror if right then negative increse
                if limb[-1] == "2":
                    mirror = 1
                c_index = self.components.index(self.cDict[limb])
                # Got rid of wheel rotation and just added it to be mirror
                # Just got rid of intterupt scroll and put it here, needlessly compelx to change it to fit multi select
                self.components[c_index].rotate(mirror * self.MOUSE_SCROLL_SPEED,
                                                        self.components[c_index].
                                                        axisBucket[self.select_axis_index])
            self.update()
        if keycode in [wx.WXK_ESCAPE]:
            # exit component editing mode
            for limb in self.active:
                c_index = self.components.index(self.cDict[limb])
                self.components[c_index].reset("color")
            self.select_axis_index = 0
            self.active = []
            self.update()
        if chr(keycode) in "r":
            # reset viewing angle only
            self.resetView()
        if chr(keycode) in "R":
            # reset everything
            for c in self.components:
                c.reset()
            self.resetView()
            self.select_obj_index = -1
            self.select_axis_index = -1
            self.pose_num = -1
            self.update()
        # cycle through poses
        if chr(keycode) in "t":
            self.pose_num = (self.pose_num + 1) % 5
            for c_index in range(0, len(self.components)):
                c = self.components[c_index]
                c.setCurrentAngle(self.poses[self.pose_num][c_index][0], c.axisBucket[0])
                c.setCurrentAngle(self.poses[self.pose_num][c_index][1], c.axisBucket[1])
                c.setCurrentAngle(self.poses[self.pose_num][c_index][2], c.axisBucket[2])
            self.update()
            



if __name__ == "__main__":
    print("This is the main entry! ")
    app = wx.App(False)
    # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame, here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
    # Resize disabled in this one
    frame = wx.Frame(None, size=(500, 500), title="Test",
                     style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)  # Disable Resize: ^ wx.RESIZE_BORDER
    canvas = Sketch(frame)

    frame.Show()
    app.MainLoop()
