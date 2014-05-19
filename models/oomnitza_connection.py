import ConfigParser
import sys
import json
import requests


class OomnitzaConnection:

    # connection settings
    oomnitza_system_url = None
    oomnitza_username = None
    oomnitza_password = None
    oomnitza_session = None
    oomnitza_access_token = None

    def __init__(self, config_file):
        """
        Initializes Oomnitza server communication wrapper with provided config file.
        Performs authorization with server to retrieve API access token as well.
        """
        config = ConfigParser.ConfigParser()
        config.read(config_file)
        try:
            self.oomnitza_system_url = config.get('oomnitza', 'system_url')
            self.oomnitza_username = config.get('oomnitza', 'username')
            self.oomnitza_password = config.get('oomnitza', 'password')
        except ConfigParser.NoOptionError as e:
            print "[x] Error: Config file is not complete! Section '%s' must contain option '%s'. " \
                  "Check config examples at https://github.com/Oomnitza.\nExiting." % (e.section, e.option)
            sys.exit(2)
        self.oomnitza_session = requests.Session()
        self.oomnitza_access_token = self.perform_authorization()

    def perform_authorization(self):
        """
        Performs authorization with Oomnitza and returns API access token

        Reference: https://wiki.oomnitza.com/wiki/REST_API#Logging_In
        """
        headers = {'content-type': 'application/json'}
        auth_url = self.oomnitza_system_url + "/api/request_token?login=%s&password=%s" \
                                              % (self.oomnitza_username, self.oomnitza_password)
        response = self.oomnitza_session.get(auth_url, headers=headers)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print "[x] Error: Error occurred during Oomnitza authorization: '%s'. Check the 'username', " \
                  "'password' and 'system_url' options in the config file in the '[oomnitza]' section.\nExiting. " \
                  % e.message
            sys.exit(2)
        return response.json()["token"]

    def sync_assets(self, generator):
        """
        This method is used to synchronize assets to the oomnitza server
        """
        headers = {'content-type': 'application/json'}
        for _casper_data in generator:
            print '[x] Syncing computer with Oomnitza (%s)' % _casper_data['general']['udid']
            upload_url = self.oomnitza_system_url + "/casper/uploadAudit?access_token=" + self.oomnitza_access_token
            response = self.oomnitza_session.post(upload_url, data=json.dumps(_casper_data), headers=headers)
            try:
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                print "[x] Error: %s - Error occurred during computer record upload to Oomnitza: '%s'. Check the " \
                      "'assets_mapping' option in the config file in the '[oomnitza]' section.\nExiting. " % \
                      (response.text, e.message)
                sys.exit(2)