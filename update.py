import os
import sys

from workflow import Workflow, ICON_INFO


GITHUB_SLUG = 'Elite50/Crowdskout-Alfred-Workflow'
VERSION = open(os.path.join(os.path.dirname(__file__),
                            'version')).read().strip()

log = None


def main(wf):
    query = None
    if len(wf.args):
        query = wf.args[0]

    wf.add_item(u'Current version : {}'.format(VERSION),
                u'Version currently installed',
                icon=ICON_INFO)

    wf.send_feedback()


if __name__ == '__main__':
    update_settings = {'github_slug': GITHUB_SLUG, 'version': VERSION}
    wf = Workflow(update_settings=update_settings)
    log = wf.logger

    if wf.update_available:
        # Add a notification to top of Script Filter results
        wf.add_item(u'New version available',
                    u'Action this item to install the update',
                    autocomplete=u'workflow:update',
                    icon=ICON_INFO)

    sys.exit(wf.run(main))
