import argparse
import sys
from workflow import Workflow


def main(wf):
    parser = argparse.ArgumentParser()
    parser.add_argument('--user', dest='user', nargs='?', default=None)
    parser.add_argument('--password', dest='password', nargs='?', default=None)
    parser.add_argument('--clear', dest='clear', action='store_true')
    parser.set_defaults(clear=False)

    args = parser.parse_args(wf.args)

    if args.user:
        log.info('Saving new user: ' + args.user)
        wf.settings['user'] = args.user

    if args.password:
        username = wf.settings.get('user', None)
        if username:
            log.info('Set the password')
            wf.save_password(username, args.password, u'jira')
        else:
            log.error('User not set. The password was not stored')

    if args.clear:
        username = wf.settings.get('user')
        if username is not None:
            log.info('Clear the username and password')
            wf.settings['user'] = None
            wf.delete_password(username, u'jira')

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    log = wf.logger
    sys.exit(wf.run(main))
