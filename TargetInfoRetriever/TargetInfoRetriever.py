import logging
import re
import requests

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class TargetInfoRetriever(object):
    __NEW_LINE = '\n'
    __CARRIAGE_RET = '\\r'
    __PADDING_BLANKS = "   "
    __REGEX_CHECK_IF_IP_IS_VALID = r'^((\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d{2}|2[0-4]\d|25[0-5])$'

    def __init__(self):
            self.__BAD_IP = None

    def retrieve_target_information(self, ip):
        global tracert, nmap, geoip, reversed_dns, http_headers

        if not ip or ip is None:
            self.__BAD_IP = requests.get('http://myexternalip.com/raw')
        else:
            self.__BAD_IP = ip

        if not re.match(self.__REGEX_CHECK_IF_IP_IS_VALID, str(self.__BAD_IP)):
            return "The passed ip: " + str(ip) + " is malformed. Currently only valid IPV4 Addresses are allowed!"

        try:
            reversed_dns = requests.get('http://api.hackertarget.com/reverseiplookup/?q=' + str(self.__BAD_IP), stream = True).text
            geoip = requests.get('http://api.hackertarget.com/geoip/?q=' + str(self.__BAD_IP), stream = True).text
            nmap = requests.get('http://api.hackertarget.com/nmap/?q=' + str(self.__BAD_IP), stream = True).text
            http_headers = requests.get('http://api.hackertarget.com/httpheaders/?q=' + str(self.__BAD_IP), stream = True).text
            tracert = requests.get('http://api.hackertarget.com/mtr/?q=' + str(self.__BAD_IP), stream = True).text
        except requests.exceptions.Timeout:
            logging.error("Maybe set up for a retry, or continue in a retry loop")
        except requests.exceptions.TooManyRedirects:
            logging.error("URL Bad? Too many redirects!")
        except requests.exceptions.RequestException as e:
            logging.error("Catastrophic ERROR - Received RequestException: " + str(e))

        return self.__get_target_info_as_dictionary()

    def __get_target_info_as_dictionary(self):
        return {"Reverse DNS":  str(reversed_dns.split(self.__NEW_LINE)),
                "GeoIP":        str(geoip.split(self.__NEW_LINE)),
                "NMAP":         str(nmap.split(self.__NEW_LINE)),
                "HTTP Headers": str(http_headers.split(self.__NEW_LINE)).replace(self.__CARRIAGE_RET, ''),
                "Trace Route":  str(tracert.split(self.__NEW_LINE)).replace(self.__PADDING_BLANKS, '')
                }
