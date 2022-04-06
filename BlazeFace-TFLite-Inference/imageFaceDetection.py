import cv2
import socket,cv2, pickle,struct
from BlazeFaceDetection.blazeFaceDetector import blazeFaceDetector

scoreThreshold = 0.7
iouThreshold = 0.3
modelType = "front"

# Initialize face detector
faceDetector = blazeFaceDetector(modelType, scoreThreshold, iouThreshold)

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#host_name  = socket.gethostname()
#host_ip = socket.gethostbyname(host_name)
host_ip='0.0.0.0'
print('HOST IP:',host_ip)
port = 8000
socket_address = (host_ip,port)
data = b""
payload_size=struct.calcsize("Q")

# Socket Bind
server_socket.bind(socket_address)

# Socket Listen
server_socket.listen(5)
print("LISTENING AT:",socket_address)

conn, addr = server_socket.accept()
print('Connected with ' + addr[0] + ':' + str(addr[1]))

while True:
        print('waiting for next frame')
        while len(data) < payload_size:
                data += conn.recv(2*4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("Q", packed_msg_size)[0]
        while len(data) < msg_size:
                data += conn.recv(2*4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        #deserialize frame
        frame = pickle.loads(frame_data)
        print('frame recieved')
        # Detect faces
        detectionResults = faceDetector.detectFaces(frame)
        # Draw detections
        img_plot = faceDetector.drawDetections(frame, detectionResults)
        #cv2.imshow("detections", img_plot)
        print('frame blurred')
        blured_serilized = pickle.dumps(img_plot)
        blurred_message = struct.pack("Q",len(blured_serilized))+blured_serilized
        conn.sendall(blurred_message)
        print('frame sent')
        key = cv2.waitKey(1) & 0xFF
        if key  == ord('q'):
                break
client_socket.close()
#cv2.waitKey(0)
