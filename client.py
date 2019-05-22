from optparse import OptionParser   #bibliotelka do analizowania wiersza polecan
import socket, sys
import time
from threading import Thread, Lock

global PORT, HOST, RECV_BUFFER, killall
HOST = 'localhost'
PORT = 6666
RECV_BUFFER = 2048
killall = False #zamyka procesy


def send_data(client, lock):
    global killall
    while True:
        if killall:     #jesli zamknie wszystkie procesy to break bo nie ma zadnych procesow
            break
        data = str(raw_input())     #przyjmujemy dane
        client.send(data)           #do funkcji client wysyla dane ktore wpiszemy
        if send_data == "q" or send_data == "Q":
            lock.acquire()
            killall = True      #zamkniete wszystkie procesy klienta
            client.close()
            lock.release()
            break


def recv_data(client, lock):
    global killall
    while True:
        if killall:
            break
        try:
            data = client.recv(RECV_BUFFER)
        except:
            lock.acquire()
            killall = True
            print "Serwer zakonczyl polaczenie, wychodze..."
            lock.release()
            break
        if not data:
            lock.acquire()
            killall = True
            print "Serwer zakonczyl polaczenie, wyjscie..."
            lock.release()
            break
        response = '\n' + data + '\n'  #odpowiada, ze to jest ta wiadomosc
        sys.stdout.write(response)     #wyswietla ale w serwerze


def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print 'Polaczyles sie z serwerem!'
    name = str(raw_input("Wpisz imie: "))
    client_socket.send(name)            #wysyla dane do funkcji klient
    response = client_socket.recv(RECV_BUFFER)      #odpowiedz wysyla do serwera otrzymane dane
    if response == "0":
        print'Nazwa %s jest zajeta! Polaczenie zostanie przerwane!' % name
        return
    if response == "1":
        print 'Uzytkownik podlaczony!'
        print 'Witaj ' + name + ' w naszym czacie! Nacisnij "q" aby wyjsc!'
        lock = Lock()
        Thread(target=send_data, args=(client_socket, lock)).start() #zaczyna watki od wyslanych i od otrzymanych danych
        Thread(target=recv_data, args=(client_socket, lock)).start()


if __name__ == '__main__':
    start_client()