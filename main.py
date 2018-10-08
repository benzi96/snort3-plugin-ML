from kmeans.kmeans_nsl import KMeansNSL
from kmeans.svm import SVM_NSL
from kmeans.neuralnetwork import NeuralNetworkNSL

from kmeans.packet import Packet
from flask import Flask, render_template
import flatbuffers
from flask import request
from flask_sockets import Sockets
import json
import time
import random

normal = 0
anomaly = 0
ddos = 0
probe = 0
r2l = 0
u2r = 0

app = Flask(__name__)
sockets = Sockets(app)
kmean = KMeansNSL()
svm = SVM_NSL()
neutralNetwork= NeuralNetworkNSL()


@sockets.route('/ws')
def web_socket(ws):
    while not ws.closed:
        message = ws.receive()
        if (message == "statistic"):
            ws.send(json.dumps({
                "normal": normal,
                "anomaly": anomaly,
                "ddos": ddos,
                "probe": probe,
                "r2l": r2l,
                "u2r": u2r
            }))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict_packet():
    raw_data = request.get_data()
    data = Packet.GetRootAsPacket(raw_data, 0)
    packet = {
        "duration": data.Duration(),
        "protocol_type": data.ProtocolType(),
        "service": data.Service(),
        "flag": data.Flag(),
        "src_bytes": data.SrcBytes(),
        "dst_bytes": data.DstBytes(),
        "land": data.Land(),
        "wrong_fragment": data.WrongFragment(),
        "urgent": data.Urgent(),
        "hot": data.Hot(),
        "num_failed_logins": data.NumFailedLogins(),
        "logged_in": data.LoggedIn(),
        "num_compromised": data.NumCompromised(),
        "root_shell": data.RootShell(),
        "su_attempted": data.SuAttempted(),
        "num_root": data.NumRoot(),
        "num_file_creations": data.NumFileCreations(),
        "num_shells": data.NumShells(),
        "num_access_files": data.NumAccessFiles(),
        "num_outbound_cmds": data.NumOutboundCmds(),
        "is_host_login": data.IsHostLogin(),
        "is_guest_login": data.IsGuestLogin(),
        "count": data.Count(),
        "srv_count": data.SrvCount(),
        "serror_rate": data.SerrorRate(),
        "srv_serror_rate": data.SrvSerrorRate(),
        "rerror_rate": data.RerrorRate(),
        "srv_rerror_rate": data.SrvRerrorRate(),
        "same_srv_rate": data.SameSrvRate(),
        "diff_srv_rate": data.DiffSrvRate(),
        "srv_diff_host_rate": data.SrvDiffHostRate(),
        "dst_host_count": data.DstHostSrvCount(),
        "dst_host_srv_count": data.DstHostSrvCount(),
        "dst_host_same_srv_rate": data.DstHostSameSrvRate(),
        "dst_host_diff_srv_rate": data.DstHostDiffSrvRate(),
        "dst_host_same_src_port_rate": data.DstHostSameSrcPortRate(),
        "dst_host_srv_diff_host_rate": data.DstHostSrvDiffHostRate(),
        "dst_host_serror_rate": data.DstHostSerrorRate(),
        "dst_host_srv_serror_rate": data.DstHostSrvSerrorRate(),
        "dst_host_rerror_rate": data.DstHostRerrorRate(),
        "dst_host_srv_rerror_rate": data.DstHostSrvRerrorRate()
    }
    # result = kmean.predict(packet)
    # result = svm.predict(packet)
    # result = neutralNetwork.predict(packet)
    neutralNetwork.load_test_data('datasets/KDDTest+.csv')
    data, acc = neutralNetwork.test_clf()
    for result in data:
        if (result == "normal"):
            global normal
            normal = normal + 1
        if (result == "DoS"):
            global ddos
            ddos = ddos + 1
        if (result == "Probe"):
            global probe
            probe = probe + 1
        if (result == "R2L"):
            global r2l
            r2l = r2l + 1
        if (result == "U2R"):
            global u2r
            u2r = u2r + 1
        if (result == "anomaly"):
            global anomaly
            anomaly = anomaly + 1
    return acc


if __name__ == '__main__':
    # kmean.load_training_data('datasets/KDDTrain+.csv')
    # kmean.train_clf()
    # svm.load_training_data('datasets/KDDTrain+.csv')
    # svm.train_clf()
    neutralNetwork.load_training_data('datasets/KDDTrain+.csv')
    neutralNetwork.train_clf()

    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

