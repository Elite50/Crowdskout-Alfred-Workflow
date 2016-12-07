from feedback import Feedback
import sys

PAGES = {
    'dashboard': {
        'endpoint': '/dashboard',
        'title': 'Dashboard'
    },
    'search': {
        'endpoint': '/search',
        'title': 'Search'
    },
    'new-profile': {
        'endpoint': '/search/new',
        'title': 'New Profile'
    },
    'charts': {
        'endpoint': '/analysis/charts',
        'title': 'Charts'
    },
    'new-charts': {
        'endpoint': '/analysis/charts/chart/intro',
        'title': 'New Chart'
    },
    'segments': {
        'endpoint': '/audience/segments',
        'title': 'Segments'
    },
    'new-segments': {
        'endpoint': '/audience/segments/new',
        'title': 'New Segment'
    },
    'new-segments-folder': {
        'endpoint': '/audience/segments/folder',
        'title': 'Create New Folder'
    },
    'lists': {
        'endpoint': '/audience/lists',
        'title': 'Lists'
    },
    'new-list': {
        'endpoint': '/audience/lists/new',
        'title': 'Create New List'
    },
    'data-entry-forms': {
        'endpoint': '/tools/data-entry-forms',
        'title': 'Data Entry Forms'
    },
    'new-data-entry-forms': {
        'endpoint': '/tools/data-entry-forms/new',
        'title': 'New Data Entry Form'
    },
    'web-forms': {
        'endpoint': '/tools/web-forms',
        'title': 'Web Forms'
    },
    'new-web-forms': {
        'endpoint': '/tools/web-forms/new',
        'title': 'New Web Form'
    },
    'social-media': {
        'endpoint': '/tools/social-media',
        'title': 'Social Media Forms'
    },
    'new-social-media': {
        'endpoint': '/tools/social-media/new',
        'title': 'New Social Media Form'
    },
    'email': {
        'endpoint': '/tools/email',
        'title': 'Email'
    },
    'new-email': {
        'endpoint': '/tools/email/new',
        'title': 'New Email'
    },
    'daytripper': {
        'endpoint': '/tools/daytripper',
        'title': ''
    },
    'new-daytripper': {
        'endpoint': '/tools/daytripper/new',
        'title': 'New Daytrip'
    },
    'import': {
        'endpoint': '/tools/import',
        'title': 'Import'
    },
    'exports': {
        'endpoint': '/tools/exports',
        'title': 'Export'
    },
    'new-exports': {
        'endpoint': '/tools/exports/new',
        'title': 'New Export'
    },
    'integrations': {
        'endpoint': '/settings/integrations',
        'title': 'Integrations'
    },
    'attributes': {
        'endpoint': '/settings/general/attributes',
        'title': 'Custom Attributes'
    },
    'new-attributes': {
        'endpoint': '/settings/general/attributes/new',
        'title': 'New Custom Attribute'
    },
    'user': {
        'endpoint': '/settings/user-settings/user-management',
        'title': 'User Management'
    },
    'new-user': {
        'endpoint': '/settings/user-settings/new',
        'title': 'Create New User'
    },
    'account': {
        'endpoint': '/settings/client-settings',
        'title': 'Account Settings'
    },
    'account-list': {
        'endpoint': '/settings/accounts',
        'title': 'Accounts'
    },
    'new-account': {
        'endpoint': '/settings/accounts/new',
        'title': 'Create New Account'
    },
}

APP_URL = 'https://app.crowdskout.com'


class CrowdskoutPage(Feedback):
    def __init__(self, args):
        Feedback.__init__(self)
        # Default location is dashboar
        self.cs_location = 'dashboard' if len(args) == 1 else str(args[1]).lower()

    def find_location(self):
        result = []
        for key, info in PAGES.items():
            location_url = APP_URL + info['endpoint']
            if self.cs_location in key:
                result.append((info['title'], location_url))

        # Sort the result by the length of URL
        result.sort(key=lambda x: len(x[1]))
        for title, url in result:
            self.add_item(title=title, subtitle=url, valid='YES', arg=url, icon='icon.png')


if 1 <= len(sys.argv) <= 2:
    cs_page = CrowdskoutPage(sys.argv)

    cs_page.find_location()

    print cs_page
