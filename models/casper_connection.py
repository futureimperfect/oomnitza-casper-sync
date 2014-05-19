import ConfigParser
import sys
import json
import requests


class CasperConnection:

    # connection settings
    casper_system_url = None
    casper_username = None
    casper_password = None
    casper_configuration = {}

    def __init__(self, config_file):
        """
        Initializes Casper communication wrapper with provided config file
        """
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        try:
            self.casper_system_url = config.get('casper', 'system_url')
            self.casper_username = config.get('casper', 'username')
            self.casper_password = config.get('casper', 'password')
            self.casper_configuration = dict(asset_mapping=json.loads(config.get('casper', 'asset_mapping')),
                                             sync_identifier=json.loads(config.get('casper', 'identifier')))
        except ConfigParser.NoOptionError as e:
            print "[x] Error: Config file is not complete! Section '%s' must contain option '%s'. " \
                  "Check config examples at https://github.com/Oomnitza.\nExiting." % (e.section, e.option)
            sys.exit(2)
        except ValueError:
            print "[x] Error: Options 'asset_mapping', 'software_mapping' from [casper] section and 'identifier' from" \
                  " [sync] section from config must be represented as JSON. " \
                  "Check config examples at https://github.com/Oomnitza.\nExiting."
            sys.exit(2)

    def http_get(self, url):
        """
        Performs HTTP GET and returns JSON response body
        """
        response = requests.get(url,
                                auth=(self.casper_username, self.casper_password),
                                headers={'Accept': 'application/json'})
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print "[x] Error: Error occurred during communication with Casper: '%s'. Check the '[casper]' section in " \
                  "config file.\nExiting. " \
                  % e.message
            sys.exit(2)
        return response.json()

    def get_the_list_of_computers(self):
        """
        This method is used to retrieve the data about OSX machines from Casper
        """
        return [_['id'] for _ in self.http_get('%s/JSSResource/computers' % self.casper_system_url)['computers']]

    def get_the_details_of_the_computer_full(self, _id):
        """
        This method is used to retrieve the details of computer by its Casper's ID
        """
        return self.http_get('%s/JSSResource/computers/id/%s' % (self.casper_system_url, _id))['computer']

    def get_the_details_of_all_the_computers(self):
        """
        Generator for the details of all the computers.
        """
        for _id in self.get_the_list_of_computers():
            _full_details = self.get_the_details_of_the_computer_full(_id)
            _full_details['oomnitza'] = self.casper_configuration
            yield _full_details