import os
import logging
import re
import requests

from urllib.error import HTTPError
from contextlib2 import closing
from ressources.BadReputationLists import badReputationIPLists

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class IPExtractor(object):
    __REGEX_VALIDATE_IP = r'(?:\d{1,3}\.){3}\d{1,3}'
    __REGEX_CHECK_IF_IP_VALID = r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$'

    def __init__(self, list_name = '../lists/bad_reputation_ip_list.dat'):
        self.__BAD_IP_LIST_NAME = list_name
        self.__TEMP_BAD_IP_LIST_NAME = self.__BAD_IP_LIST_NAME + ".lists"

    def run_ip_extractor(self):
        logging.info("##### Extracting IPS from .txt-List #####")
        self.__extract_ips_from_txt_list()
        logging.info("##### Remove doubled IPS #####")
        info = self.__remove_doubled_ips()
        return "Done. All Lists were refreshed! " + str(info)

    def check_reputation_of_ip(self, ip, ):
        if not re.match(self.__REGEX_CHECK_IF_IP_VALID, str(ip)):
            return "The passed ip: " + str(ip) + " is malformed. Currently only valid IPV4 Addresses are allowed!"

        result = "reputation: "

        with open(self.__BAD_IP_LIST_NAME) as f:
            for line in f:
                if ip in line:
                    return result + "BAD"
        return result + "GOOD"

    def __extract_ips_from_txt_list(self):
        global copy
        outfile = open(self.__TEMP_BAD_IP_LIST_NAME, 'w+')
        ips = []

        for url in badReputationIPLists:
            try:
                assert isinstance(url, str)
                assert ("http://" in url) or ("https://" in url)

                logging.info("Checking URL: " + url)
                copy = requests.get(url, stream = True)
            except HTTPError as error_code:
                logging.error("The requested URL: " + url + " has returned" + str(error_code))
                continue
            except AssertionError as e:
                logging.error("An AssertionError occurred: " + str(e.__cause__))
                continue

            with closing(copy):
                for line in copy.iter_lines():
                    line = line.rstrip()
                    line = line.decode('utf-8')
                    regex = re.findall(self.__REGEX_VALIDATE_IP, line)

                    if len(regex) > 0 is not None and regex not in ips:
                        ips.append(regex[0])

            for ip in ips:
                ip_address = "".join(ip)
                if not ip_address == "":
                    outfile.write(ip_address + "\n")

        outfile.close()

    def __remove_doubled_ips(self) -> str:
        count_doubled_ips = 0
        ips_seen = set()
        outfile = open(self.__BAD_IP_LIST_NAME, "w+")

        for line in open(self.__TEMP_BAD_IP_LIST_NAME, "r"):
            if line not in ips_seen:
                outfile.write(line)
                ips_seen.add(line)
            else:
                count_doubled_ips += 1
        outfile.close()
        os.remove(self.__TEMP_BAD_IP_LIST_NAME)

        return "A total of: " + str(len(ips_seen)) + " IPs has been seen with " \
               + str(count_doubled_ips) + " doubled ips"
