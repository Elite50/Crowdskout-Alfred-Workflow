from feedback import Feedback
import urllib
import sys

PROJECTS = ["https://crowdskout.atlassian.net/browse/"]

DEFAULT_PROJECT = 'CROW'


class Ticket(Feedback):
    def __init__(self):
        Feedback.__init__(self)
        self.raw_ticket_number = urllib.quote(sys.argv[1])

    def ticket_number_standardization(self, project_url):
        """
        Convert raw ticket number into ticket URL
        """
        ticket_number = '{0}-{1}'.format(DEFAULT_PROJECT, self.raw_ticket_number) if self.raw_ticket_number.isdigit() else self.raw_ticket_number
        ticket_url = project_url + ticket_number
        return ticket_number, ticket_url

    def add_ticket_to_feedback(self, project_url):
        ticket_number, ticket_url = self.ticket_number_standardization(project_url)
        self.add_item(title="JIRA Ticket {0}".format(ticket_number), subtitle=ticket_url, valid='YES', arg=ticket_url, icon='icon.png')

    def get_ticket_in_project(self):
        """
        Get ticket URL for all projects
        """
        map(self.add_ticket_to_feedback, PROJECTS)


if len(sys.argv) == 2:
    ticket = Ticket()

    ticket.get_ticket_in_project()
    
    print ticket