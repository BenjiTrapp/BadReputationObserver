import os
import urllib.request
import shutil
import re
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class TorListExtractor:
    __TOR_EXIT_NODES_FILE_NAME = 'lists/Tor_Exit_Nodes.dat'
    __TOR_ALL_NODES_FILE_NAME = 'lists/Tor_All_Nodes.dat'
    __TOR_EXIT_NODES_LIST_URL = 'https://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv'
    __TOR_ALL_NODES_LIST_URL = 'https://torstatus.blutmagie.de/ip_list_all.php/Tor_ip_list_ALL.csv'
    __REGEX_CHECK_IF_IP_VALID = r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$'

    def __init__(self, refresh_lists = False):
        if refresh_lists:
            logging.info("Downloading fresh TOR-Lists.")
            self.__download_all_tor_nodes()
            self.__download_tor_exit_nodes()
            logging.info("Done. All TOR-Lists refreshed")

    def check_tor_node(self, ip):
        return [{"TOR-Exit-Node": self.__is_ip_in_tor_list(ip, self.__TOR_EXIT_NODES_FILE_NAME)},
                {"TOR-Node:": self.__is_ip_in_tor_list(ip, self.__TOR_ALL_NODES_FILE_NAME)}]

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

        assert filename is self.__TOR_ALL_NODES_FILE_NAME or filename is self.__TOR_EXIT_NODES_FILE_NAME

        with open(filename) as f:
            for line in f:
                if ip in line:
                    return "Yes"
        return "No"

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