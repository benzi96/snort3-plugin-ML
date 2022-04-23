from MachineLearningAlgorithm.kmeans_nsl import KMeansNSL
from MachineLearningAlgorithm.svm import SVM_NSL
from MachineLearningAlgorithm.neuralnetwork import NeuralNetworkNSL
from MachineLearningAlgorithm.naivebayes import NaiveBayesNSL

from MachineLearningAlgorithm.packet import Packet
from flask import Flask, render_template
import flatbuffers
from flask import request
from flask_sockets import Sockets
import json
import time
import random
import os

total = 0
normal = 0
anomaly = 0
ddos = 0
probe = 0
r2l = 0
u2r = 0
listPackets=[]
app = Flask(__name__)
sockets = Sockets(app)
kmean = KMeansNSL()
svm = SVM_NSL()
neutralNetwork= NeuralNetworkNSL()
naiveBayes= NaiveBayesNSL()


@sockets.route('/ws')
def web_socket(ws):
    while not ws.closed:
        message = ws.receive()
        if message == "reset":
            global normal
            normal = 0
            global ddos
            ddos = 0
            global probe
            probe = 0
            global u2r
            u2r = 0
            global r2l
            r2l = 0
        
        normalResult = 0
        ddosResult = 0
        probeResult = 0
        r2lResult = 0
        u2rResult = 0
        anomalyResult = 0

        if message == "statistickmeans" or message == "statisticneuralnetwork" or message == "statisticsvm" or message == "statisticnaivebayes":
            global listPackets
            n = len(listPackets)
            if (n > 0):
                data = []
                if message == "statistickmeans":
                    data = kmean.predict(listPackets)
                # if message == "statisticneuralnetwork":
                #    data = neutralNetwork.predict(listPackets)
                # if message == "statisticsvm":
                #    data = svm.predict(listPackets)
                # if message == "statisticnaivebayes":
                #    data = naiveBayes.predict(listPackets)
                del listPackets[:n]
                
                for result in data:
                    if (result == "normal"):
                        normalResult = normalResult + 1
                    if (result == "DoS"):
                        ddosResult = ddosResult + 1
                    if (result == "Probe"):
                        probeResult = probeResult + 1
                    if (result == "R2L"):
                        r2lResult = r2lResult + 1
                    if (result == "U2R"):
                        u2rResult = u2rResult + 1
                    if (result == "anomaly"):
                        anomalyResult = anomalyResult + 1

        normal = normal + normalResult
        ddos = ddos + ddosResult
        probe = probe + probeResult
        u2r = u2r + u2rResult
        r2l = r2l + r2lResult

        if (message == "all"):
            ws.send(json.dumps({
                "all": total,
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
        "count": data.Count(),
        "srv_count": data.SrvCount(),
        "serror_rate": data.SerrorRate(),
        "srv_serror_rate": data.SrvSerrorRate(),
        "rerror_rate": data.RerrorRate(),
        "srv_rerror_rate": data.SrvRerrorRate(),
        "same_srv_rate": data.SameSrvRate(),
        "diff_srv_rate": data.DiffSrvRate(),
        "srv_diff_host_rate": data.SrvDiffHostRate(),
        "dst_host_count": data.DstHostCount(),
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
    global listPackets
    listPackets.append(packet)
    global total
    total = total + 1
    return "a"


if __name__ == '__main__':
    kmean.load_training_data('datasets/KDDTrain+.csv')
    kmean.train_clf()
    # svm.load_training_data('datasets/KDDTrain+.csv')
    # svm.train_clf()
    # neutralNetwork.load_training_data('datasets/KDDTrain+.csv')
    # neutralNetwork.train_clf()
    # naiveBayes.load_training_data('datasets/KDDTrain+.csv')
    # naiveBayes.train_clf()

    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
