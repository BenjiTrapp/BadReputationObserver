from flask import Flask, jsonify

from ressources.IPFromListExtractor import IPExtractor
from ressources.TargetInfoRetriever import TargetInfoRetriever

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'my#super#duper#awesome#secret-key'


class BadReputationObserver(object):
    @app.route('/api/', methods = ['GET'])
    def api():
        return "Usage:\n To refresh the BRO-IP-List: curl -X POST URL:5000/api/bro/refresh\n" \
               "To check the reputation of an IP: curl -X GET URL:5000/api/bro/<ip>"

    @app.route('/api/reputation/', methods = ['GET'])
    def bro():
        return "(B)ad (R)eputation (O)bserver Service!"

    @app.route('/api/reputation/refresh', methods = ['POST'])
    def start_bro():
        return IPExtractor().run_ip_extractor()

    @app.route('/api/reputation/<ip>', methods = ['GET'])
    def check_reputation_of_ip(ip):
        return jsonify(IPExtractor().check_reputation_of_ip(ip))

    @app.route('/api/target_info/<ip>', methods = ['GET'])
    def check_target_info_of_ip(ip):
        return jsonify(TargetInfoRetriever().retrieve_target_information(ip))


if __name__ == '__main__':
    app.run(debug = False, host = '0.0.0.0', threaded = True)
