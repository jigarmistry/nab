# !/usr/bin/env python3.5
# -*- coding:utf-8 -*-

import time
import json
import socket
import threading

neat_host = ''
neat_port = 8888
http_host = ''
http_port = 8080

acc_id_str  = ''
ret_dat_str = ''

# Clear screen
print("\033c")
print(" ")
print("          THE PYTHON NAB SERVER IS RUNNING.")
print("          =================================")
print(" ")

###############################################################################
##  Start of neat_srv                                                        ##
###############################################################################
def neat_srv(name, HOST, PORT):
    global acc_id_str
    global ret_dat_str
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, int(PORT)))
    listen_socket.listen(1)

    print('     The ' + name + ' server is listening on port %s' % PORT)
    print('')
    i = 0

    while True:
        i += 1
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024).decode("utf-8")
        print('================================================================================')
        GETorPOST = request.split( )[0]

        if GETorPOST=='GET':
            ###################################################################
            ##  GETs the following from NEAT.                                ##
            ###################################################################
            id_get_dict = json.loads('{"'+request.split( )[1].split('?')[1].replace('&','", "').replace('=','":"')+'"}')
            print('==> GET  ' + str(i) + ' from player '+id_get_dict["Player"]+' on server '+id_get_dict["Server"]+' city number '+id_get_dict["City"]+' time stamp '+id_get_dict["Time"])
            ###################################################################
            ##  Got account info from NEAT, respond with a command.          ##
            ###################################################################
            if i % 3 == 0:
                ## print("yes")
                http_response = 'echo "Python NAB server says Hi!"' + str(i)
##                http_response = 'json_encode(city.troop)'
            else:
                ## print("no")
                http_response = 'json_encode(city.troop)'
##                http_response = 'echo "Python NAB server says Hi!"' + str(i)
            ##  http_response = 'troop w:1000,s:1000'
            ##  http_response = 'resetgoals'
            ##  http_response = 'echo json_encode(city.goals)'
            ###################################################################
            
        elif GETorPOST=='POST':
            ###################################################################
            ##  POSTed from NEAT.                                            ##
            ##  N.B. This might be Return/Account or Account/Return order.   ##
            ###################################################################   
            ret_dat = request.split('Return=')[1].split('Account=')
            ret_dat_str = '{"Return":' + str(ret_dat[0]).replace('&','')+'}'
            ## print(request)
            acc_id = request.split('Account=')[1].split('Return=')
            acc_id_str = str(acc_id[0]).replace('&','')
            ###################################################################
            ##  Massage 'Return' into a dictionary.                          ##
            ###################################################################
            ret_dat_str = ret_dat_str.replace('%5C%22','').replace('%20',' ').replace('%2E','.')
            ret_dat_str = ret_dat_str.replace('%22','"').replace('%2C',',').replace('%3A',':').replace('%7B','{').replace('%7D','}').replace('%5B','[').replace('%5D',']')
            ret_dat_str = ret_dat_str.replace('"{','{"').replace('}"','"}').replace(':','":"').replace(',','","').replace('""','"').replace('"{"','{"')
            
            try:
                ret_dat_dict = json.loads(ret_dat_str)
##                print (ret_dat_dict)
            except:
                print(ret_dat_str)
                
            ###################################################################
            ##  Massage 'Account' into a dictionary.                         ##
            ###################################################################
            acc_id_str = acc_id_str.replace('%7B%22','{"').replace('%22%7D','"}').replace('%22%3A%22','":"').replace('%22%2C%22','","')
            acc_id_str = acc_id_str.replace('%22%3A','":"').replace('%2C%22','","').replace('%7D','"}')
            
            try:
                id_post_dict = json.loads(acc_id_str)
                print('==> POST ' + str(i) + ' from player '+id_post_dict["Player"]+' on server '+id_post_dict["Server"]+' city number '+id_post_dict["City"]+' time stamp '+id_post_dict["Time"])
            except:
                print(acc_id_str)
                
            http_response = '"OKAY"'

        else:
            http_response = '"ERROR"'

        client_connection.sendall(bytes(http_response.encode('utf-8')))
        client_connection.close()

###############################################################################
##  End of neat_srv                                                          ##
###############################################################################

###############################################################################
##  Start of http_srv                                                        ##
###############################################################################

def http_srv(name, HOST, PORT):
    global acc_id_str
    global ret_dat_str
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, int(PORT)))
    listen_socket.listen(1)

    print('     The ' + name + ' server is listening on port %s' % PORT)
    print('')
    i = 0

    while True:
        i += 1
        client_connection, client_address = listen_socket.accept()
        request = client_connection.recv(1024).decode("utf-8")

        ##  print (request)

        http_response = '''
            <!DOCTYPE html>
            <html>
            <head>
              <title>Status of Bots.</title>
              <body>
                <canvas id="myCanvas" width="200" height="100" style="border:1px solid #000000;">
                Your browser does not support the HTML5 canvas tag.
                </canvas>
                <meta charset="utf-8">
              <script type="text/javascript" src="script.js"></script>
              <meta http-equiv="refresh" content="4" >
              <script>
                var c = document.getElementById("myCanvas");
                var ctx = c.getContext("2d");
                // Create gradient
                var grd = ctx.createLinearGradient(0,0,200,0);
                grd.addColorStop(0,"green");
                grd.addColorStop(1,"white");
                // Fill with gradient
                ctx.fillStyle = grd;
                ctx.fillRect(10,10,150,80);
                ctx.font = "30px Arial";
                ctx.fillText("NAB",10,50);
              </script>
              </body>
            </head>
            ''' + '<h2><p style="color:red">Hello from the Python NAB server, index No. - ' + str(i) + '</h2><p>' + acc_id_str + '<p>' + ret_dat_str


        client_connection.sendall(bytes(http_response.encode('utf-8')))
        client_connection.close()
        
###############################################################################
##  End of http_srv                                                          ##
###############################################################################


def Main():

    neat_server = threading.Thread(target = neat_srv, args = ('neat_srv', neat_host, str(neat_port)))
    http_server = threading.Thread(target = http_srv, args = ('http_srv', http_host, str(http_port)))
    
    neat_server.start()
    http_server.start()


if __name__ == '__main__':
    Main()



