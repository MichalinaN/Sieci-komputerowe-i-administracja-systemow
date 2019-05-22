import json


def writeToJSONFile(path, fileName, data):
    filePathNameWExt = './' + path + '/' + fileName + '.json'
    with open(filePathNameWExt, 'a') as fp:
        json.dump(data, fp)
        fp.write('\n')


count = 0
broad = []
net = []


def warunki(ip, mask, count):
    if len(ip) == 4 and len(mask) == 4:
        for elem in ip:
            try:
                elem, mask[count] = int(elem), int(mask[count])
            except ValueError, TypeError:
                print "IP musi byc liczba!"
                exit()
            if 0 <= elem <= 255 and 0 <= mask[count] <= 255:
                net.append(int(elem) & int(mask[count]))
                broad.append(int(elem) | (int(mask[count]) ^ 0xff))
                count += 1
            else:
                print "Wartosc oktetu oraz maska musza byc w przedziale 0-255"
                exit()
    else:
        print "Zly adres IP. Musi posiadac 4 oktety"
        exit()

def obliczanie(net, broad):
    print str(net) + '\t\t\tadres sieci'
    writeToJSONFile('./', 'plikJSON',net)
    print str(broad) + '\t\t\tadres broadcast'
    writeToJSONFile('./', 'plikJSON', broad)
    print '.'.join([bin(int(x) + 256)[3:] for x in broad]) + '\t\t\t adres broadcast binarnie'
    broadbin = "".join([bin(int(x) + 256)[3:] for x in broad]) + '    adres broadcast dziesietnie i binarnie'
    writeToJSONFile('./', 'plikJSON', broadbin)
    net[3] += 1;
    broad[3] -= 1
    print str(net) + '\t\t\tpierwszy adres hosta'
    writeToJSONFile('./', 'plikJSON', net)
    print '.'.join([bin(int(x) + 256)[3:] for x in net]) + '\t\t\t pierwszy adres hosta binarnie'
    pierhost = "".join([bin(int(x) + 256)[3:] for x in net]) + '   pierwszy adres hosta dziesietnie i binarnie'
    writeToJSONFile('./', 'plikJSON', pierhost)
    print str(broad) + '\t\t\tostatni adres hosta'
    writeToJSONFile('./', 'plikJSON', broad)
    print '.'.join([bin(int(x) + 256)[3:] for x in broad]) + '\t\t\t ostatni adres hosta binarnie'
    osthost = "".join([bin(int(x) + 256)[3:] for x in broad]) + '   ostatni adres hosta dziesietnie binarnie'
    writeToJSONFile('./', 'plikJSON', osthost)
    print str(net) + ' -',
    print str(broad) + '\t\t\tmaksymalny zasieg hostow'
    print '.'.join([bin(int(x) + 256)[3:] for x in net]) + ' -',
    print '.'.join([bin(int(x) + 256)[3:] for x in broad]) + '\t\t\tmaksymalny zasieg hostow binarnie'
    rangenet = "".join([bin(int(x) + 256)[3:] for x in net]) + '-'
    rangebroad = "".join([bin(int(x) + 256)[3:] for x in broad]) + ' maksymalny zasieg hostow binarnie'
    range = rangenet + rangebroad
    writeToJSONFile('./', 'plikJSON', range)
    znak = '-'
    writeToJSONFile('./', 'plikJSON', net)
    writeToJSONFile('./', 'plikJSON', znak)
    writeToJSONFile('./', 'plikJSON', broad)

def klasa(ip):
    klas = "".join([bin(int(x) + 256)[3:] for x in ip])
    if klas[0]=="0":
        print ("Klasa A")
        writeToJSONFile('./', 'plikJSON', 'Klasa A')
    else:
        if klas[1]=="0":
            print("Klasa B")
            writeToJSONFile('./', 'plikJSON', 'Klasa B')
        else:
            if klas[2]=="0":
                print("Klasa C")
                writeToJSONFile('./', 'plikJSON', 'Klasa C')
            else:
                if klas[3]=="0":
                    print("Klasa D")
                    writeToJSONFile('./', 'plikJSON', 'Klasa D')
    return ""


ip=raw_input("Podaj IP:\t\t")
if ip is "":
    import socket
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip.connect(("8.8.8.8", 80))
    print(ip.getsockname()[0])
    ip.close()
else:
    mask = raw_input("Podaj maske:\t\t")
    ip = ip.split('.')
    mask = mask.split('.')
    warunki(ip, mask, count)
    obliczanie(net, broad)
    klasa(ip)
    writeToJSONFile('./', 'plikJSON', mask)
    print '.'.join([bin(int(x) + 256)[3:] for x in mask]) + '\t\t\tmaska w formacie binarnym'
    maskbin = "".join([bin(int(x) + 256)[3:] for x in mask]) + '   maska dziesietnie i binarnie'
    writeToJSONFile('./', 'plikJSON', maskbin)