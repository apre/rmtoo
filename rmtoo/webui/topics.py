#
import cherrypy

#import random
#import string
import os
#import json


from jinja2 import Environment, FileSystemLoader
#from jinja2plugin import Jinja2TemplatePlugin
from rmtoo.lib.TopicContinuumSet import TopicContinuumSet


# jinga template dir
FILES_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), u"files")
TEMPLATES_DIR = os.path.join(FILES_DIR, u"templates")
tpl = Environment(loader=FileSystemLoader(TEMPLATES_DIR))


class Topics():

    def __init__(self,topic_continuum_set_):
        self.topic_continuum_set = topic_continuum_set_

    @cherrypy.expose
    def index(self):
        tmpl = tpl.get_template('topics.html')
        cont_dict = self.topic_continuum_set.get_continuum_dict()
        topics = cont_dict.keys()
        print("Topics names:%s"%topics)
        return tmpl.render(topic_names=topics)

    @cherrypy.expose
    def req_view(self,topic_to_view,version_idx_str,req_name):
        return "view req name "
    @cherrypy.expose
    def view(self,topic_to_view,version_idx_str):
        try:
            version_idx= int(version_idx_str)
        except:
            return "error: %s MUST be a number" % version_idx_str

        cont_dict = self.topic_continuum_set.get_continuum_dict()
        print("view topic")
        if topic_to_view in cont_dict:
            print("topic to view found")
            tmpl = tpl.get_template("requirements_list.html")
            topic_continum = cont_dict[topic_to_view]
            commits_ids = topic_continum.get_vcs_commit_ids()
            print("view:%d len:%d" % (version_idx,len(commits_ids)))
            if version_idx < len(commits_ids) :
                print("len OK")
                requirements = topic_continum.get_topic_set(
                    commits_ids[version_idx].get_commit())

                requirements_ids = requirements.get_requirement_set().get_all_requirement_ids()
                view_path = "%s/%d" % (topic_to_view,version_idx)
                return tmpl.render(req_path=view_path,reqs=requirements_ids)

        return "view error %s %s" % (topic_to_view,version_idx)


    @cherrypy.expose
    def topic(self,topic_to_view):
        cont_dict = self.topic_continuum_set.get_continuum_dict()
        topic_continum = cont_dict[topic_to_view]
        commits_ids = topic_continum.get_vcs_commit_ids()

        if topic_to_view in cont_dict:
            tmpl = tpl.get_template("continuum.html")

            topic_continum = cont_dict[topic_to_view]
            commits_ids = topic_continum.get_vcs_commit_ids()

            s = topic_continum.get_topic_set(commits_ids[0].get_commit())
            for x in s.get_requirement_set().get_all_requirement_ids():
                pass
                #print("%s" %x)
            print("topic_set:%s" % s)
            #topic_set = topic_continum.get_topic_set(topic_to_view)
            versions = list(enumerate(commits_ids))
            return tmpl.render(current_topic=topic_to_view,continum_versions=versions)
            return "topics set:%s  set_ok?:%s @ %s id:%s %d "  % (
             topic_to_view ,
             self.topic_continuum_set.is_usable(),
              topic_continum,
              commits_ids[0],
              len(commits_ids)
              )




    @cherrypy.expose
    def show(self,topicset_to_view,topic_to_view):
        dbg_str =  "show topic:%s %s" % (topicset_to_view , topic_to_view)
        return dbg_str
