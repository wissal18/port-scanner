import socket
import sys
import re # regular-expression library

from services import services


MAX_PORTS = 65353



def help():
    print(f"[HELP]  usage: python {sys.argv[0]} <target-address> <starting-port> <ending-port>")



def isAddressValid(address):

    isValid = re.search("^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", address)
    if isValid:
        return True
    return False

def portIsInteger(portString):
    try:
        port = int(portString)
    except ValueError:
        return False
    return True

def portIsValid(port):
    return 0 < int(port) < MAX_PORTS

def checkArgs():
    if len(sys.argv) <4 :
        print("[ERROR] Please specify the address , the starting-port and the ending-port ")
        help()
        exit(1)
    if not isAddressValid(sys.argv[1]):
        print(f"[ERROR] This is an invalid IP address!")
        help()
        exit(2)
    if not portIsInteger(sys.argv[2]) or not portIsInteger(sys.argv[3]):
        print(f"[ERROR] The port should be an integer number")
        help()
        exit(3)
    if not portIsValid(sys.argv[2]) or not portIsValid(sys.argv[3]):
        print(f"[ERROR] Port should be between 0 and {MAX_PORTS}")
        help()
        exit(4)
    if int(sys.argv[2]) > int(sys.argv[3]):
        print(f"[ERROR]: Ending port should be greater than the starting port")
        help()
        exit(5)

def addFile(port):
    f = open("open_ports.txt", "a")
    f.write(str(port))
    f.close()

def scannerPort(port):
    host = str(sys.argv[1])
    host_port = (host, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex(host_port):
        print(f"[-]  Port {port} is closed")
    else:
        service = services.get(port)
        if service:
            print(f"[+]  Port {port} is open. {service} is found")
        else:
            print(f"[+]  Port {port} is open")
        addFile(port)
    sock.close()


def main():
    checkArgs()

    startingPort = int(sys.argv[2])
    endingPort = int(sys.argv[3])
    for port in range(startingPort,endingPort+1):
        scannerPort(port)



if __name__ == "__main__":
    main()
