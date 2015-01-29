from termcolor import colored
import os

class TopLevelDomain(object):
    TLD_DIRECTORY = 'tlds'

    def __init__(self):
        self.name = ''
        self.whois_server = ''
        self.available_reply = ''

    @classmethod
    def load(self, filename):
        tld_file = file(os.path.join(self.TLD_DIRECTORY, filename))
        tld = self()
        tld.name = filename
        content = tld_file.readlines()
        tld.whois_server = content[0].strip()
        tld.available_reply = content[1].strip()
        return tld

    @classmethod
    def all(self):
        return [TopLevelDomain.load(f) for f in os.listdir(self.TLD_DIRECTORY) if f[0] != '.' and os.path.isfile(os.path.join(self.TLD_DIRECTORY, f))]

    def whois(self, domainname):
        return os.popen("whois -h {:s} {:s}.{:s}".format(self.whois_server, domainname, self.name))

    def get_reply_for(self, domainname):
        reply = self.available_reply.replace('#{domain_name}', '{:s}'.format(domainname))
        return reply.replace('#{domain}', '{:s}.{:s}'.format(domainname, self.name))

    def is_available(self, domainname):
        whois_response = self.whois(domainname)

        while True:
            line = whois_response.readline()
            if line[:3] == '>>>':
              while True:
                next_line = whois_response.readline()
                if next_line[:3] == '>>>':
                    line = line.strip() + ' ' + next_line[4:]
                else:
                    break

            if not line:
                break

            if line.lower().strip() == self.get_reply_for(domainname).lower():
                return True

        return False

    def display_availablity_feedback(self, domainname):
        if self.is_available(domainname):
            print "{:s}.{:s} is {:s}".format(domainname, self.name, colored('available', 'green'))
        else:
            print "{:s}.{:s} is {:s}".format(domainname, self.name, colored('not available', 'red'))
