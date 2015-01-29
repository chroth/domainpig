import sys
import logging
from topleveldomains import TopLevelDomain

def search(context):
    search_domain = context['arguments'][1]
    print 'Searching availablity for ' + search_domain

    labels = search_domain.split('.')

    if len(labels) > 1:
        tld = TopLevelDomain.load(labels[-1])
        tld.display_availablity_feedback(labels[-2])
    else:
        for tld in TopLevelDomain.all():
            tld.display_availablity_feedback(search_domain)

    return 0, ""

def show_help(context):
    context["logger"].debug("Display API help")
    msg = "BPM Commands:\n"
    keys = sorted(context['api'].keys())
    for k in keys:
        msg += "    {:17s} {:s}\n".format(k, context['api'][k][1])
    return 0, msg.strip()


if __name__ == "__main__":
    #default command
    command = "help"
    try:
        command = sys.argv[1]
    except IndexError as e:
        pass

    # setup logger
    FORMAT = "%(asctime)s %(levelname)s %(funcName)s:%(lineno)s ~ %(message)s"
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    #available commands
    api = {
        'search': (search, "Searches for domain name availablity"),
        'help': (show_help, "Show available commands"),
    }

    #context for all commands
    context = {
        'logger': logger,
        'command': command,
        'arguments': sys.argv[1:],
        'api': api
    }

    #excecute, returns code (!= 0 if failed) and a message
    if not command in api:
        command = 'help'

    code, msg = api[command][0](context)
    print msg
    sys.exit(code)
