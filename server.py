import socket
import time
import json
from threading import Thread, Lock

global HOST, PORT, CONNECTION_LIST, RECV_BUFFER
HOST = 'localhost' #adres IP lokalnego komputera
PORT = 6666
CONNECTION_LIST = [] #lista podpietych klientow
RECV_BUFFER = 2048 #jaka wielkosc moze miec otrzymana wiadomosc z polaczonego gniazda

def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'w') as fp:
        json.dump(data, fp)
        fp.write('\n')

class Client(): #polaczenie z klientem, potrzebna dla stworzenia obiektow
    def __init__(self, conn, name):  #metoda init to konstruktor, kiedy wywolam metode, python tworzy obiekt i przekazuje go jako 1 element
        self.conn = conn    #tworzenie obiektu, dla polaczenia
        self.name = name    #tworzenie obiektu - unikatowe ID(name) dla klienta
    def send(self, message):
        self.conn.send(message)     #wyslanie wiadomosci
    def recv(self):
        return self.conn.recv(RECV_BUFFER)  #bierze pod uwage wielkosc
    def close(self):
        self.conn.close()

def get_client(name):
    for client in CONNECTION_LIST: #dla kazdego klienta w liscie
        if client.name == name:     #jesli klient istnieje i ma jakas nazwe zwraca klienta
            return client
    return None         #nic nie zwraca

def broadcast_data(data, lock):
    lock.acquire()          #uzyskujemy blokade
    for cl in CONNECTION_LIST:  #pobieramy dane
        cl.send(data)
    lock.release()      #zwalniamy blokade

def handle_client(client, lock):
    while True:
        data = client.recv()        #naszymi danymi sa pobrane z klienta
        if not data:                #jesli nie ma danych to break
            break
        if data == "q" or data == "Q":      #jesli nacisniemy q to konczy nasz czat i daje odpowiedz
            response = "Uzytkownik " + client.name + " opuscil grupe!"
        else:
            response = "Wiadomosc uzytkownika " + client.name + " : " + data + " " + time.strftime("%H:%M") #jesli napis bedzie inny daje wtedy odpowiedz jaka byla wiadomosc  klienta
            dic = {'Wiadomosc uzytkownika': client.name + ' ' + data + ' ' + time.strftime("%H:%M")}
            tab.append(dic)
        broadcast_data(response, lock)      #idzie do tej funkcji i daje odpowiedz do kazdego z listy polaczonych, wykorzystuje blokade
        if data == "q" or data == "Q":  #czynnosc sie powtarza
            break
        writeToJSONFile('./', 'plikJSON', tab)
    lock.acquire()      #konczy petle while, daje blokade
    CONNECTION_LIST.remove(client)  #by moc usunac klienta ktory opuscil czat
    client.close()          #zamyka klienta
    print "   Uzytkownik " + client.name + " opuscil czat!"
    lock.release()          #zwalnia blokade


def handle_server(server_socket, lock):
    while True:
        conn, addr = server_socket.accept()         #akceptacja polaczenia
        print "Nawiazano nowe polaczenie z adresu " + str(addr)
        name = conn.recv(RECV_BUFFER)       #name to otrzymane z polaczenia dane (recv)
        print "   Uzytkownik to " + name    #uztkowanik ma nazwe name
        client = get_client(name)           #tworzymy i otrzymujemy klienta o podanej nazwie
        if client:
            conn.send('0')          #if false, jesli blad
            conn.close()
            print "   Wystapil blad, polaczenie z adresu " + str(addr) + " zostanie zakonczone!"    #niepowodzenie
        else:
            conn.send('1')
            client = Client(conn, name)         #tworzy nowego klienta ( u nas uzytkownik czatu)
            CONNECTION_LIST.append(client)      #dopisuje na koncu listy noego klienta
            print "   Nawiazano polaczenie!"        #polaczenie zostalo nawiazane
            response = "Uzytkownik %s dolaczyl do czatu!" % name    #odtrzymujemy odpowiedz
            length = str(len(CONNECTION_LIST))      #pobieramy dlugosc naszej listy
            response += "\nObecnie mamy %s uzytkownikow w chat room'ie!" % length  #dodajemy kolejnych ale tak zeby nie wykroczylo poza zakres
            broadcast_data(response, lock)      #wracamy do funkcji z otrzymaniem odpowiedzi
            Thread(target=handle_client, args=(client, lock)).start()  #target to obiekt do wywolania  metodzie, args to nasze argumenty, start zaczyna aktownosc thread

def start_server():
    global HOST, PORT
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #tworzenie socketu
    while True:
        try:
            server_socket.bind((HOST, PORT))  #zawiazanie gniazd z hostem i portem, nie moze byc juz powiazane z noczym innym
        except socket.error: #sprawdzenie warunku
            PORT += 1
            if PORT > 9999:
                print 'Nie mozna uruchomic serwera, przepraszamy!'
                return
        else:
            break

    server_socket.listen(10)  #serwer zostaje wlaczony do nawiazania polaczenia, 10 to liczba maksymalnych nieudanych polaczen
    print "Czat nasluchuje portu " + str(PORT)
    lock = Lock()  #blokada, czeka
    handle_server(server_socket, lock)

if __name__ == '__main__':
    tab = []
    start_server()
