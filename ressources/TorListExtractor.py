import os
import urllib.request
import shutil


class TorListExtractor:
    __TOR_EXIT_NODES_FILE_NAME = '../lists/Tor_Exit_Nodes.dat'
    __TOR_ALL_NODES_FILE_NAME = '../lists/Tor_All_Nodes.dat'
    __TOR_EXIT_NODES_LIST_URL = 'https://torstatus.blutmagie.de/ip_list_exit.php/Tor_ip_list_EXIT.csv'
    __TOR_ALL_NODES_LIST_URL = 'https://torstatus.blutmagie.de/ip_list_all.php/Tor_ip_list_ALL.csv'

    def __init__(self):
        pass

    def download_tor_exit_nodes(self):
        if not self.save_list_from_url(self.__TOR_EXIT_NODES_LIST_URL, self.__TOR_EXIT_NODES_FILE_NAME):
            raise Exception("File " + self.__TOR_EXIT_NODES_LIST_URL + " is not existing as assumed!")

    def download_all_tor_nodes(self):
        if not self.save_list_from_url(self.__TOR_ALL_NODES_LIST_URL, self.__TOR_ALL_NODES_FILE_NAME):
            raise Exception("File " + self.__TOR_ALL_NODES_LIST_URL + " is not existing as assumed!")

    @staticmethod
    def save_list_from_url(url = None, filename = None):
        assert url is not None
        assert filename is not None

        if os.path.exists(filename):
            os.remove(filename)

        with urllib.request.urlopen(url) as response, open(filename, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        return os.path.exists(filename)

if __name__ == '__main__':
    TorListExtractor().download_all_tor_nodes()
    TorListExtractor().download_tor_exit_nodes()