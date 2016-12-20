# BadReputationObserver
BRO - Bad Reputation Observer

### WTF is BRO? ###
* BRO is a small service to crawl several IP-Blacklists 
* A tiny service to check the Reputation of a given IP-Address
* This service also uses the API from hacktarget.com to check the IP with the following tools:
    * Reverse DNS"
    * GeoIP
    * NMAP
    * Trace Route
    * HTTP Headers
    
### Current TODO List ###
1. Implement Flask-Security / OAuth
2. Some clean-up and refactorings to be on a "more Pythonic" Style
3. Add Nikto Scan?!
4. Add TOR Nodes from blutmagie.de Lists 
5. Add VPN-IP Lists
6. Implement a safe MongoDB Connection to store the IP-Mess 


### Why did you create this Service? ###
This Service was implemented to learn python and creating a webservice with flask 
