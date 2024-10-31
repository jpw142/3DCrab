"""
Model our creature and wrap it in one class.
First version on 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

----------------------------------

Modified by Daniel Scrivener 09/2023

Modified by Jack Weber 10/2024
Imported Sphere and created red sphere
Color picked colors from my reference image
Imported Cone 
Created the crab
Limited all of the angles of movement for the limbs
created component list and dictionary of all limbs
"""

from Component import Component
from Point import Point
import ColorType as Ct
from Shapes import Cube
from Shapes import Cylinder
from Shapes import Sphere
from Shapes import Cone


import numpy as np


class ModelLinkage(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature. 
    #
    # In order to simplify the process of constructing your model, the rotational origin of each Shape has been offset by -1/2 * dz,
    # where dz is the total length of the shape along its z-axis. In other words, the rotational origin lies along the smallest 
    # local z-value rather than being at the translational origin, or the object's true center. 
    # 
    # This allows Shapes to rotate "at the joint" when chained together, much like segments of a limb. 
    #
    # In general, you should construct each component such that it is longest in its local z-direction: 
    # otherwise, rotations may not behave as expected.
    #
    # Please see Blackboard for an illustration of how this behavior works.



    ##### TODO 4: Define creature's joint behavior
    # Requirements:
    #   1. Set a reasonable rotation range for each joint,
    #      so that creature won't intersect itself or bend in unnatural ways
    #   2. Orientation of joint rotations for the left and right parts should mirror each other.
    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, display_obj=None):
        super().__init__(position, display_obj)
        self.contextParent = parent
        
        # COLORS
        body_color = Ct.ColorType(172/255, 160/255, 113/255)
        leg_color = Ct.ColorType(185/255, 154/255, 74/255)
        pincer_color = Ct.ColorType(221/255, 210/255, 226/255)
        stalk_color = Ct.ColorType(182/255, 170/255, 123/255)

        body = Sphere(Point((0, 0, 0)), shaderProg, [1, 1, 2], body_color, limb=False)

        # 1 indicates left 2 indicates right

        # LEFT ARM
        arm1 = Cylinder(Point((0, 0, 1.90)), shaderProg, [0.1, 0.1, 0.2], body_color)
        arm1.setRotateExtent(self.uAxis, -30, 30) # Red Axis
        arm1.setRotateExtent(self.vAxis, 0, 45) # Green Axis
        arm1.setRotateExtent(self.wAxis, -15, 15)
        
        backarm1 = Cylinder(Point((0, 0, 0.4)), shaderProg, [0.2, 0.2, 0.3], leg_color)
        backarm1.setRotateExtent(self.uAxis, -15, 15)
        backarm1.setRotateExtent(self.vAxis, 0, 15)
        backarm1.setRotateExtent(self.wAxis, -15, 15)

        forearm1 = Cylinder(Point((0, 0, 0.5)), shaderProg, [0.3, 0.3, 0.4], leg_color)
        forearm1.setRotateExtent(self.uAxis, -15, 15)
        forearm1.setRotateExtent(self.vAxis, 0, 15)
        forearm1.setRotateExtent(self.wAxis, -15, 15)

        top_pincer1 = Cone(Point((0, 0.15, 0.7)), shaderProg, [0.3, 0.1, 0.3], pincer_color)
        top_pincer1.setRotateExtent(self.uAxis, 0, 15)
        top_pincer1.setRotateExtent(self.vAxis, 0, 0)
        top_pincer1.setRotateExtent(self.wAxis, 0, 0)

        bot_pincer1 = Cone(Point((0, -0.15, 0.7)), shaderProg, [0.3, 0.1, 0.3], pincer_color)
        bot_pincer1.setRotateExtent(self.uAxis, -15, 0)
        bot_pincer1.setRotateExtent(self.vAxis, 0, 0)
        bot_pincer1.setRotateExtent(self.wAxis, 0, 0)

        self.addChild(body)
        body.addChild(arm1)
        arm1.addChild(backarm1)
        backarm1.addChild(forearm1)
        forearm1.addChild(top_pincer1)
        forearm1.addChild(bot_pincer1)
        
        # RIGHT ARM
        arm2 = Cylinder(Point((0, 0, -1.80)), shaderProg, [-0.1, -0.1, -0.2], body_color)
        arm2.setRotateExtent(self.uAxis, -30, 30) # Red Axis
        arm2.setRotateExtent(self.vAxis, -45, 0) # Green Axis
        arm2.setRotateExtent(self.wAxis, -15, 15)

        backarm2 = Cylinder(Point((0, 0, -0.4)), shaderProg, [-0.2, -0.2, -0.3], leg_color)
        backarm2.setRotateExtent(self.uAxis, -15, 15)
        backarm2.setRotateExtent(self.vAxis, -15, 0)
        backarm2.setRotateExtent(self.wAxis, -15, 15)

        forearm2 = Cylinder(Point((0, 0, -0.5)), shaderProg, [-0.3, -0.3, -0.4], leg_color)
        forearm2.setRotateExtent(self.uAxis, -15, 15)
        forearm2.setRotateExtent(self.vAxis, -15, 0)
        forearm2.setRotateExtent(self.wAxis, -15, 15)

        top_pincer2 = Cone(Point((0, 0.15, -0.7)), shaderProg, [-0.3, -0.1, -0.3], pincer_color)
        top_pincer2.setRotateExtent(self.uAxis, -15, 0)
        top_pincer2.setRotateExtent(self.vAxis, 0, 0)
        top_pincer2.setRotateExtent(self.wAxis, 0, 0)

        bot_pincer2 = Cone(Point((0, -0.15, -0.7)), shaderProg, [-0.3, -0.1, -0.3], pincer_color)
        bot_pincer2.setRotateExtent(self.uAxis, 0, 15)
        bot_pincer2.setRotateExtent(self.vAxis, 0, 0)
        bot_pincer2.setRotateExtent(self.wAxis, 0, 0)

        body.addChild(arm2)
        arm2.addChild(backarm2)
        backarm2.addChild(forearm2)
        forearm2.addChild(top_pincer2)
        forearm2.addChild(bot_pincer2)

        # LEFT EYE STALK
        stalk1 = Cylinder(Point((0, 0.9, 0.75)), shaderProg, [0.1, 0.3, 0.1], stalk_color)
        stalk1.setRotateExtent(self.uAxis, -30, 30)
        stalk1.setRotateExtent(self.vAxis, -30, 30)
        stalk1.setRotateExtent(self.wAxis, -30, 30)

        eye1 = Sphere(Point((0., 0.3, 0.)), shaderProg, [0.2, 0.2, 0.2], Ct.BLACK, limb=False)

        body.addChild(stalk1)
        stalk1.addChild(eye1)


        # RIGHT EYE STALK
        stalk2 = Cylinder(Point((0, 0.9, -0.75)), shaderProg, [-0.1, -0.3, -0.1], stalk_color)
        stalk2.setRotateExtent(self.uAxis, -30, 30)
        stalk2.setRotateExtent(self.vAxis, -30, 30)
        stalk2.setRotateExtent(self.wAxis, -30, 30)
        eye2 = Sphere(Point((0., 0.3, 0.)), shaderProg, [0.2, 0.2, 0.2], Ct.BLACK, limb=False)

        body.addChild(stalk2)
        stalk2.addChild(eye2)

        # Left Legs
        fleg1 = Cylinder(Point((0.4, -0.6, 1.3)), shaderProg, [0.1, 0.1, 0.4], leg_color)
        fleg1.setRotateExtent(self.uAxis, 0, 30)
        fleg1.setRotateExtent(self.vAxis, -15, 15)
        fleg1.setRotateExtent(self.wAxis, -15, 15)
        sleg1 = Cylinder(Point((0, -0.6, 1.4)), shaderProg, [0.1, 0.1, 0.4], leg_color)
        sleg1.setRotateExtent(self.uAxis, 0, 30)
        sleg1.setRotateExtent(self.vAxis, -15, 15)
        sleg1.setRotateExtent(self.wAxis, -15, 15)
        tleg1 = Cylinder(Point((-0.4, -0.6, 1.3)), shaderProg, [0.1, 0.1, 0.4], leg_color)
        tleg1.setRotateExtent(self.uAxis, 0, 30)
        tleg1.setRotateExtent(self.vAxis, -15, 15)
        tleg1.setRotateExtent(self.wAxis, -15, 15)

        ffoot1 = Cone(Point((0., 0., 0.7)), shaderProg, [0.1, 0.1, 0.3], leg_color)
        ffoot1.setRotateExtent(self.uAxis, -30, 30)
        ffoot1.setRotateExtent(self.vAxis, -15, 15)
        ffoot1.setRotateExtent(self.wAxis, -15, 15)
        sfoot1 = Cone(Point((0., 0., 0.7)), shaderProg, [0.1, 0.1, 0.3], leg_color)
        sfoot1.setRotateExtent(self.uAxis, -30, 30)
        sfoot1.setRotateExtent(self.vAxis, -15, 15)
        sfoot1.setRotateExtent(self.wAxis, -15, 15)
        tfoot1 = Cone(Point((0., 0., 0.7)), shaderProg, [0.1, 0.1, 0.3], leg_color)
        tfoot1.setRotateExtent(self.uAxis, -30, 30)
        tfoot1.setRotateExtent(self.vAxis, -15, 15)
        tfoot1.setRotateExtent(self.wAxis, -15, 15)

        body.addChild(fleg1)
        body.addChild(sleg1)
        body.addChild(tleg1)
        fleg1.addChild(ffoot1)
        sleg1.addChild(sfoot1)
        tleg1.addChild(tfoot1)

        # Right Legs
        fleg2 = Cylinder(Point((0.4, -0.6, -1.3)), shaderProg, [-0.1, -0.1, -0.4], leg_color)
        fleg2.setRotateExtent(self.uAxis, -30, 0)
        fleg2.setRotateExtent(self.vAxis, -15, 15)
        fleg2.setRotateExtent(self.wAxis, -15, 15)
        sleg2 = Cylinder(Point((0, -0.6, -1.4)), shaderProg, [-0.1, -0.1, -0.4], leg_color)
        sleg2.setRotateExtent(self.uAxis, -30, 0)
        sleg2.setRotateExtent(self.vAxis, -15, 15)
        sleg2.setRotateExtent(self.wAxis, -15, 15)
        tleg2 = Cylinder(Point((-0.4, -0.6, -1.3)), shaderProg, [-0.1, -0.1, -0.4], leg_color)
        tleg2.setRotateExtent(self.uAxis, -30, 0)
        tleg2.setRotateExtent(self.vAxis, -15, 15)
        tleg2.setRotateExtent(self.wAxis, -15, 15)

        ffoot2 = Cone(Point((0., 0., -0.7)), shaderProg, [-0.1, -0.1, -0.3], leg_color)
        ffoot2.setRotateExtent(self.uAxis, -30, 30)
        ffoot2.setRotateExtent(self.vAxis, -15, 15)
        ffoot2.setRotateExtent(self.wAxis, -15, 15)
        sfoot2 = Cone(Point((0., 0., -0.7)), shaderProg, [-0.1, -0.1, -0.3], leg_color)
        sfoot2.setRotateExtent(self.uAxis, -30, 30)
        sfoot2.setRotateExtent(self.vAxis, -15, 15)
        sfoot2.setRotateExtent(self.wAxis, -15, 15)
        tfoot2 = Cone(Point((0., 0., -0.7)), shaderProg, [-0.1, -0.1, -0.3], leg_color)
        tfoot2.setRotateExtent(self.uAxis, -30, 30)
        tfoot2.setRotateExtent(self.vAxis, -15, 15)
        tfoot2.setRotateExtent(self.wAxis, -15, 15)

        body.addChild(fleg2)
        body.addChild(sleg2)
        body.addChild(tleg2)
        fleg2.addChild(ffoot2)
        sleg2.addChild(sfoot2)
        tleg2.addChild(tfoot2)

        

        self.componentList = [body,arm1, backarm1, forearm1, top_pincer1, bot_pincer1, 
                              arm2, backarm2, forearm2, top_pincer2, bot_pincer2, 
                              stalk1, eye1, stalk2, eye2, 
                              fleg1, sleg1, tleg1, ffoot1, sfoot1, tfoot1,
                              fleg2, sleg2, tleg2, ffoot2, sfoot2, tfoot2
                              ]
        self.componentDict = {
                "body": body,
                "arm1": arm1,
                "backarm1": backarm1,
                "forearm1": forearm1,
                "top_pincer1": top_pincer1,
                "bot_pincer1": bot_pincer1,
                "arm2": arm2,
                "backarm2": backarm2,
                "forearm2": forearm2,
                "top_pincer2": top_pincer2,
                "bot_pincer2": bot_pincer2,
                "stalk1": stalk1,
                "eye1": eye1,
                "stalk2": stalk2,
                "eye2": eye2,
                "fleg1": fleg1,
                "sleg1": sleg1,
                "tleg1": tleg1,
                "ffoot1": ffoot1,
                "sfoot1": sfoot1,
                "tfoot1": tfoot1,
                "fleg2": fleg2,
                "sleg2": sleg2,
                "tleg2": tleg2,
                "ffoot2": ffoot2,
                "sfoot2": sfoot2,
                "tfoot2": tfoot2,
        }


