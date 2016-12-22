import os
import urllib.request
import shutil
import re
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class TorListExtractor:
    __TOR_EXIT_NODES_FILE_NAME = 'Tor_Exit_Nodes.dat'
    __TOR_ALL_NODES_FILE_NAME = 'Tor_All_Nodes.dat'
    __TOR_EXIT_NODES_LIST_URL = 'https://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv'
    __TOR_ALL_NODES_LIST_URL = 'https://torstatus.blutmagie.de/ip_list_all.php/Tor_ip_list_ALL.csv'
    __REGEX_CHECK_IF_IP_VALID = r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$'

    def __init__(self, refresh_lists = False):
        if refresh_lists:
            logging.info("Downloading fresh TOR-Lists.")
            self.__download_all_tor_nodes()
            self.__download_tor_exit_nodes()
            logging.info("Done. All TOR-Lists refreshed")

    def check_if_ip_is_exit_node(self, ip):
        return self.__is_ip_in_tor_list(ip, self.__TOR_EXIT_NODES_FILE_NAME)

    def check_if_ip_is_tor_node(self, ip):
        return self.__is_ip_in_tor_list(ip, self.__TOR_ALL_NODES_FILE_NAME)

    def __download_tor_exit_nodes(self):
        if not self.save_list_from_url(self.__TOR_EXIT_NODES_LIST_URL, self.__TOR_EXIT_NODES_FILE_NAME):
            logging.error("Download of TOR Exit Nodes list was NOT successful")
            raise Exception("File " + self.__TOR_EXIT_NODES_LIST_URL + " is not existing as assumed!")

    def __download_all_tor_nodes(self):
        if not self.save_list_from_url(self.__TOR_ALL_NODES_LIST_URL, self.__TOR_ALL_NODES_FILE_NAME):
            logging.error("Download of TOR Nodes list was NOT successful")
            raise Exception("File " + self.__TOR_ALL_NODES_LIST_URL + " is not existing as assumed!")

    def __is_ip_in_tor_list(self, ip, filename):
        if not re.match(self.__REGEX_CHECK_IF_IP_VALID, str(ip)):
            return "The passed ip: " + str(ip) + " is malformed. Currently only valid IPV4 Addresses are allowed!"

        if filename is self.__TOR_EXIT_NODES_FILE_NAME:
            result = "TOR-Exit-Node: "
        elif filename is self.__TOR_ALL_NODES_FILE_NAME:
            result = "TOR-Node: "
        else:
            logging.error("Filename: " + filename + " is not supported!")
            raise FileNotFoundError("The given filename wasn't recognized")

        with open(filename) as f:
            for line in f:
                if ip in line:
                    return result + "Yes"
        return result + "No"

    @staticmethod
    def save_list_from_url(url = None, filename = None):
        assert url is not None
        assert ("http://" in url) or ("https://" in url)
        assert filename is not None
        assert isinstance(filename, str)

        if os.path.exists(filename):
            os.remove(filename)

        with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        return os.path.exists(filename)

if __name__ == '__main__':
    TorListExtractor(refresh_lists = True)