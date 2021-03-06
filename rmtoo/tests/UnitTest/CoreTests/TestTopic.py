'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
  Unit test for Topic

 (c) 2010,2012 by flonatel GmbH & Co. KG

 For licensing details see COPYING
'''

from rmtoo.lib.Topic import Topic
from rmtoo.lib.digraph.Digraph import Digraph
from rmtoo.lib.RMTException import RMTException
from rmtoo.tests.lib.TestConfig import TestConfig
from rmtoo.tests.lib.TestVCS import TestVCS

class TestTopic:

    def test_neg_01(self):
        "Topic: (internal) check if Name tag exists"
        dg = Digraph()

        tconfig = TestConfig()
        tconfig.set_value("topic_root_node", "/nothing/compare")
        tvcs = TestVCS(tconfig)
        tfileinfo = TestVCS.FileInfo(1)

        try:
            topic = Topic(dg, tconfig, tvcs, None, tfileinfo, None)
            assert(False)
        except RMTException, rmte:
            assert(rmte.id() == 62)

