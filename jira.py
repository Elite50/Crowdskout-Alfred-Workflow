import base64
import json
import sys
import time
import urllib
import urllib2

from workflow import Workflow

BASE_JIRA_URL = "https://crowdskout.atlassian.net"

DEFAULT_PROJECT = 'CROW'

BOARD_ID = 10
DATA_BOARD_ID = 13

options = [
    ('open', {
        'order': 0,
        'subtitle': 'Input Ticket Number...',
        'default': True
    }),
    ('search', {
        'order': 0,
        'subtitle': 'Input Keyword...',
        'default': True
    }),
    ('current_sprint', {
        'order': 0,
        'url': '/secure/RapidBoard.jspa?projectKey={0}&rapidView={1}'.format(DEFAULT_PROJECT, BOARD_ID),
        'default': True
    }),
    ('backlog', {
        'order': 0,
        'url': '/secure/RapidBoard.jspa?projectKey={0}&rapidView={1}&view=planning'.format(DEFAULT_PROJECT, BOARD_ID),
        'default': True
    }),
    ('data_import', {
        'order': 0,
        'url': '/secure/RapidBoard.jspa?rapidView={0}'.format(DATA_BOARD_ID),
        'default': False
    }),
    ('create', {
        'order': 0,
        'url': '/secure/CreateIssue!default.jspa',
        'default': True
    }),
    ('my_open_issue', {
        'order': 0,
        'url': '/issues/?filter=-1',
        'default': False
    }),
    ('report_by_me', {
        'order': 0,
        'url': '/issues/?filter=-2',
        'default': False
    }),
    ('components', {
        'order': 0,
        'url': '/projects/{0}?selectedItem=com.atlassian.jira.jira-projects-plugin:components-page'.format(DEFAULT_PROJECT),
        'default': False
    }),
    ('reports', {
        'order': 0,
        'url': '/projects/{0}?selectedItem=com.atlassian.jira.jira-projects-plugin:components-page'.format(DEFAULT_PROJECT),
        'default': False
    })
]


class TicketWorkflow(Workflow):
    def __init__(self):
        Workflow.__init__(self)

    def match_option(self, arg_1):
        arg_option = next(iter(arg_1), '')  # fetch the first item

        # Sort the items
        for option, option_info in options:
            if option.startswith(arg_option):
                option_info['order'] = 2
            elif arg_option in option:
                option_info['order'] = 1

        sorted_options = sorted([(k, v) for k, v in options], key=lambda x: -x[1]['order'])

        # Add the items by the order
        for option, option_info in sorted_options:

            # If the arg is empty, only desplay the default options
            if not arg_option and not option_info['default']:
                continue

            # Generate title from option name
            title = option.replace('_', ' ').capitalize()

            autocomplete = option

            is_actionable = bool(option_info.get('url'))

            # The subtitle is URL if it jumps to a webapage, otherwise fetch the subtitle from option info
            if is_actionable:
                subtitle = arg = BASE_JIRA_URL + option_info['url']
            else:
                arg = None
                subtitle = option_info.get('subtitle')
                autocomplete += ' '  # Add an extra space to continue typing next arg

            self.add_item(title=title,
                          subtitle=subtitle,
                          valid=True if is_actionable else False,
                          arg=arg,
                          icon=u'icon.png',
                          autocomplete=autocomplete)
            
    def open(self, args):
        query = next(iter(args), '')  # fetch the first item
        ticket_number = '{0}-{1}'.format(DEFAULT_PROJECT, query) if query.isdigit() else query
        ticket_url = self.ticket_url(ticket_number)

        self.add_item(title=u"Open Ticket {0}".format(ticket_number),
                      subtitle=ticket_url,
                      valid=True,
                      arg=ticket_url,
                      icon=u'icon.png')
        time.sleep(0.8)

        jql = urllib.quote('key="{0}"'.format(ticket_number))

        for ticket_number, ticket_title in self.search_from_api(jql=jql, fields='id,key,summary', max=1):
            ticket_url = self.ticket_url(ticket_number)
            self.add_item(title=ticket_title,
                          subtitle=ticket_url,
                          valid=True,
                          arg=ticket_url,
                          icon=u'icon.png')

    def search(self, args):
        args = ' '.join(args)
        jql = urllib.quote('text ~ "{0}"'.format(args))
        self.add_item(title=u'Search for "{0}"'.format(args),
                      subtitle=u'Search for "{0}" in JIRA'.format(args),
                      valid=True,
                      arg=u"{0}/issues/?jql={1}".format(BASE_JIRA_URL, jql),
                      icon=u'icon.png')

        time.sleep(0.8)
        for ticket_number, ticket_title in self.search_from_api(jql=jql, fields='id,key,summary', max=8):
            ticket_url = self.ticket_url(ticket_number)
            self.add_item(title=ticket_number,
                          subtitle=ticket_title,
                          valid=True,
                          arg=ticket_url,
                          icon=u'icon.png')

    @staticmethod
    def search_from_api(jql, fields, max):
        """
        Given keywords, search it through JIRA API, return the ticket number and title of results
        :param jql: keyword for searching
        :param max: maximum number of search result
        :return: iter((ticket_number, ticket_title), )
        """
        # https://developer.atlassian.com/jiradev/jira-apis/jira-rest-apis/jira-rest-api-tutorials/jira-rest-api-example-query-issues
        api_url = "{0}/rest/api/2/search?jql={1}&maxResults={2}&fields={3}".format(BASE_JIRA_URL, jql, max, fields)
        request = urllib2.Request(api_url)
        # TODO: user/pass input config
        api_base64string = base64.b64encode('{0}:{1}'.format('user', 'pwd'))
        request.add_header("Authorization", "Basic %s" % api_base64string)
        try:
            request_result = urllib2.urlopen(request).read()
            result = json.loads(request_result)
        except:
            result = {}

        for search_result in result.get('issues', []):
            ticket_number = search_result.get('key', '')
            ticket_title = search_result.get('fields', {}).get('summary')
            yield (ticket_number, ticket_title)

    @staticmethod
    def ticket_url(ticket_number):
        return "{0}/browse/{1}".format(BASE_JIRA_URL, ticket_number)

    def run_command(self, arg_1, arg_2):
        if arg_1[0] == 'search':
            self.search(args=arg_2)
        elif arg_1[0] == 'open':
            self.open(args=arg_2)


def main(wf):
    arg_1 = sys.argv[1:2]  # The first arg is option
    arg_2 = sys.argv[2:]  # All other args from second one are query
    if arg_2:
        wf.run_command(arg_1=arg_1, arg_2=arg_2)
    else:
        wf.match_option(arg_1=arg_1)

    wf.send_feedback()


if __name__ == '__main__':
    wf = TicketWorkflow()
    log = wf.logger
    sys.exit(wf.run(main))
