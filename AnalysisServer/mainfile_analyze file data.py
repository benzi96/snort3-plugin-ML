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
import os

total = 0
normal = 0
anomaly = 0
ddos = 0
probe = 0
r2l = 0
u2r = 0
fileName = 0
myFileName = "0.csv"
app = Flask(__name__)
sockets = Sockets(app)
kmean = KMeansNSL()
svm = SVM_NSL()
neutralNetwork= NeuralNetworkNSL()


@sockets.route('/ws')
def web_socket(ws):
    while not ws.closed:
        message = ws.receive()
        if message == "statistickmeans" or message == "statisticneutralnetwork" or message == "statisticsvm":
	        global fileName
            current = fileName
            fileName = fileName + 1
            global myFileName
            myFileName = str(fileName) + ".csv"
            
            currentFileName = str(current) + ".csv"
	        if os.path.isfile(currentFileName):
                data = []
                if message == "statistickmeans":
                    kmean.load_test_data(currentFileName)
                    data, acc = kmean.test_clf()
                if message == "statisticneutralnetwork":
                    neutralNetwork.load_test_data(currentFileName)
                    data, acc = neutralNetwork.test_clf()
                if message == "statisticsvm":
                    svm.load_test_data(currentFileName)
                    data, acc = svm.test_clf()
                os.remove(currentFileName)
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
    
    global myFileName
    f=open(myFileName, "a+")
    f.write(str(data.Duration()) + "," + str(data.ProtocolType()) + "," + str(data.Service()) + "," + str(data.Flag()) + "," + str(data.SrcBytes()) + "," + str(data.DstBytes()) + "," + str(data.Land()) + "," + str(data.WrongFragment()) + "," + str(data.Urgent()) + "," + str(data.Hot()) + "," + str(data.NumFailedLogins()) + "," + str(data.LoggedIn()) + "," + str(data.NumCompromised()) + "," + str(data.RootShell()) + "," + str(data.SuAttempted()) + "," + str(data.NumRoot()) + "," + str(data.NumFileCreations()) + "," + str(data.NumShells()) + "," + str(data.NumAccessFiles()) + "," + str(data.NumOutboundCmds()) + "," + str(data.IsHostLogin()) + "," + str(data.IsGuestLogin()) + "," + str(data.Count()) + "," + str(data.SrvCount()) + "," + str(data.SerrorRate()) + "," + str(data.SrvSerrorRate()) + "," + str(data.RerrorRate()) + "," + str(data.SrvRerrorRate()) + "," + str(data.SameSrvRate()) + "," + str(data.DiffSrvRate()) + "," + str(data.SrvDiffHostRate()) + "," + str(data.DstHostSrvCount()) + "," + str(data.DstHostSrvCount()) + "," + str(data.DstHostSameSrvRate()) + "," + str(data.DstHostDiffSrvRate()) + "," + str(data.DstHostSameSrcPortRate()) + "," + str(data.DstHostSrvDiffHostRate()) + "," + str(data.DstHostSerrorRate()) + "," + str(data.DstHostSrvSerrorRate()) + "," + str(data.DstHostRerrorRate()) + "," + str(data.DstHostSrvRerrorRate()) + "\n")
    f.close()   
    global total
    total = total + 1
    return "a"


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
