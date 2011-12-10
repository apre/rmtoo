'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
  Sometimes there are so called 'Requirements Hotspots'.  These are
  requirements which have too many links.
   
 (c) 2010-2011 by flonatel GmhH & Co. KG

 For licensing details see COPYING
'''

from rmtoo.lib.analytics.Result import Result
from rmtoo.lib.analytics.Base import Base

class HotSpot(Base):

    max_incoming = 7
    max_outgoing = 4

    def __init__(self, config):
        Base.__init__(self)

    def requirement(self, req):
        success = True
        if len(req.incoming) > HotSpot.max_incoming:
            self.add_result(
                Result("HotSpot", req.get_id(), -10,
                    ["Number of incoming links is too high: %d" %
                       len(req.incoming)]))
            self.set_failed()

        if len(req.outgoing) > HotSpot.max_outgoing:
            self.add_result(
                Result("HotSpot", req.get_id(), -10,
                 ["Number of outgoing links is too high: %d" %
                    len(req.outgoing)]))
            self.set_failed()

