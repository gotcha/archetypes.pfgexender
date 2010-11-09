from Products.Five import zcml

from collective.testcaselayer import ptc as tcl_ptc

from archetypes import pfgextender


class Layer(tcl_ptc.BasePTCLayer):

    def afterSetUp(self):
        zcml.load_config('testing.zcml', package=pfgextender)
        self.addProfile('archetypes.pfgextender:testing')


layer = Layer(bases=[tcl_ptc.ptc_layer])
