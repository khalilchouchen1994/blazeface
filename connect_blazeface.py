import socket, cv2, pickle,struct,imutils

#establisch sokcet connection 
client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
host_ip = '127.0.0.1' 
port = 8000
client_socket.connect((host_ip,port))
print('connected')
payload_size = struct.calcsize("Q")
while True:
	#conn,addr = client_socket.accept()
	#print('GOT CONNECTION FROM:',addr)
	if client_socket:
		cap = cv2.VideoCapture(0)	
		while(cap.isOpened()):
			ret, img = cap.read()
			#print(ret)
			#cv2.imshow('TRANSMITTING VIDEO',img)
			if ret:
                                frame = imutils.resize(img,width=320)
                                #print(frame)
                                a = pickle.dumps(frame)
                                message = struct.pack("Q",len(a))+a
                                client_socket.sendall(message)
                                print('frame sent')
                                data = b""
                                while len(data) < payload_size:
                                        data += client_socket.recv(2*4096)
                                packed_msg_size = data[:payload_size]
                                data = data[payload_size:]
                                msg_size = struct.unpack("Q", packed_msg_size)[0]
                                while len(data) < msg_size:
                                        data += client_socket.recv(4096)
                                bluured_frame_data = data[:msg_size]
                                blurred_data = data[msg_size:]
                                #deserialize frame
                                blurred_frame = pickle.loads(bluured_frame_data)
                                cv2.imshow('RECIEVED VIDEO',blurred_frame)
                                key = cv2.waitKey(1) & 0xFF
                                if key ==ord('q'):
                                        conn.close()
                                        cap.release()
                                        cv2.destroyAllWindows()
                                        break
                                        
