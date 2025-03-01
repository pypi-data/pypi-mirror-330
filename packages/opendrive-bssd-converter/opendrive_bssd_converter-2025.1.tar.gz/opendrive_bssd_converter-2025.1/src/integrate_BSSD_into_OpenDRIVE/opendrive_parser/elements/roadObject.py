__author__ = "Benjamin Orthen, Stefan Urban"
__copyright__ = "TUM Cyber-Physical Systems Group"
__credits__ = ["Priority Program SPP 1835 Cooperative Interacting Automobiles"]
__version__ = "0.3"
__maintainer__ = "Sebastian Maierhofer"
__email__ = "commonroad@lists.lrz.de"
__status__ = "Released"


class Object:

    def __init__(self):
        self._type = None
        self._name = None
        self._width = None
        self._height = None
        self._zOffset = None
        self._id = None
        self._s = None
        self._t = None
        self._validLength = None
        self._orientation = None
        self._hdg = None
        self._pitch = None
        self._roll = None
        
        #Add attributes according to OpenDRIVE 1.7
        self._dynamic = None
        self._length = None
        self._perpToRoad = None
        self._radius = None
        self._subtype = None
        
        #Add list to store all <repeat>-elements of an object
        self.repeats = []

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        self._type = str(value)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = str(value)

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = str(value)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = str(value)

    @property
    def zOffset(self):
        return self._zOffset

    @zOffset.setter
    def zOffset(self, value):
        self._zOffset = str(value)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = int(value)

    @property
    def s(self):
        return self._s

    @s.setter
    def s(self, value):
        self._s = float(value)

    @property
    def t(self):
        return self._t

    @t.setter
    def t(self, value):
        self._t = float(value)

    @property
    def validLength(self):
        return self._validLength

    @validLength.setter
    def validLength(self, value):
        self._validLength = str(value)

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = str(value)

    @property
    def hdg(self):
        return self._hdg

    @hdg.setter
    def hdg(self, value):
        self._hdg = str(value)

    @property
    def pitch(self):
        return self._pitch

    @pitch.setter
    def pitch(self, value):
        self._pitch = str(value)

    @property
    def roll(self):
        return self._roll

    @roll.setter
    def roll(self, value):
        self._roll = str(value)
        
    # Add attributes according to OpenDRIVE 1.7
    
    @property
    def dynamic(self):
        return self._dynamic

    @dynamic.setter
    def dynamic(self, value):
        self._dynamic = str(value)
        
    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = str(value)
        
    @property
    def perpToRoad(self):
        return self._perpToRoad

    @perpToRoad.setter
    def perpToRoad(self, value):
        self._perpToRoad = str(value)
    
    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = str(value)
        
    @property
    def subtype(self):
        return self._subtype

    @subtype.setter
    def subtype(self, value):
        self._subtype = str(value)
        
    # Added attribute "repeats" for storing all <repeat>-Elements of one <object>-element in a list
    @property
    def repeats(self):
        """ """
        self._repeats.sort(key=lambda x: x.s)
        return self._repeats

    @repeats.setter
    def repeats(self, value):
        """"""
        self._repeats = value
        

# Added object "repeat" for storing a <repeat>-Element in an object
class ObjectRepeat:

    
    def __init__(self):
        self._distance = None
        self._heightEnd = None
        self._heightStart = None
        self._length = None
        self._lengthEnd = None
        self._lengthStart = None
        self._radiusEnd = None
        self._radiusStart = None
        self._s = None
        self._tEnd = None
        self._tStart = None
        self._widthEnd = None
        self._widthStart = None
        self._zOffsetEnd = None
        self._zOffsetStart = None       


    @property
    def distance(self):
        return self._distance 

    @distance.setter
    def distance(self, value):
        self._distance = value

    @property
    def heightEnd(self):
        return self._heightEnd

    @heightEnd.setter
    def heightEnd(self, value):
        self._heightEnd = value

    @property
    def heightStart(self):
        return self._heightStart

    @heightStart.setter
    def heightStart(self, value):
        self._heightStart = value
    
    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, value):
        self._length = value
    
    @property
    def lengthEnd(self):
        return self._lengthEnd

    @lengthEnd.setter
    def lengthEnd(self, value):
        self._lengthEnd = value
    
    @property
    def lengthStart(self):
        return self._lengthStart

    @lengthStart.setter
    def lengthStart(self, value):
        self._lengthStart = value
        
    @property
    def radiusEnd(self):
        return self._radiusEnd

    @radiusEnd.setter
    def radiusEnd(self, value):
        self._radiusEnd = value
        
    @property
    def radiusStart(self):
        return self._radiusStart

    @radiusStart.setter
    def radiusStart(self, value):
        self._radiusStart = value
    
    @property
    def s(self):
        return self._s

    @s.setter
    def s(self, value):
        self._s = value
    
    @property
    def tEnd(self):
        return self._tEnd

    @tEnd.setter
    def tEnd(self, value):
        self._tEnd = value
        
    @property
    def tStart(self):
        return self._tStart

    @tStart.setter
    def tStart(self, value):
        self._tStart = value
        
    @property
    def widthEnd(self):
        return self._widthEnd

    @widthEnd.setter
    def widthEnd(self, value):
        self._widthEnd = value
    
    @property
    def widthStart(self):
        return self._widthStart

    @widthStart.setter
    def widthStart(self, value):
        self._widthStart = value
    
    @property
    def zOffsetEnd(self):
        return self._zOffsetEnd

    @zOffsetEnd.setter
    def zOffsetEnd(self, value):
        self._zOffsetEnd = value
        
    @property
    def zOffsetStart(self):
        return self._zOffsetStart

    @zOffsetStart.setter
    def zOffsetStart(self, value):
        self._zOffsetStart = value
    
        
    
