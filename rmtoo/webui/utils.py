
from rmtoo.lib.TopicContinuumSet import TopicContinuumSet


def get_requirement(continuum,topic_to_view,version_idx_param,req_name):
    try:
        version_idx= int(version_idx_param)
    except:
        raise "version_idx_param ->%s<- MUST be a number" % version_idx_param

    cont_dict = continuum.get_continuum_dict()
    if topic_to_view not in cont_dict:
        raise "topic_to_view ->%s<- not found" % topic_to_view


    topic_continum = cont_dict[topic_to_view]
    commits_ids = topic_continum.get_vcs_commit_ids()

    if version_idx >= len(commits_ids) :
        raise "version_idx %d must be less than  " % (version_idx,len(commits_ids))


    requirements = topic_continum.get_topic_set(
        commits_ids[version_idx].get_commit())

    requirements_ids = requirements.get_requirement_set().get_all_requirement_ids()
    print("requirements_ids:%s"%requirements_ids)

    try:
        r = requirements.get_requirement_set().get_requirement(req_name)
    except:
        raise "req_name ->%s<- not found" % req_name
    return r
