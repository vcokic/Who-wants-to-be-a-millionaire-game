import json
import random


class Pitanja(object):
    """
    klasa sa svim pitanjima iz json datoteke te izdvojenih 15 pitanja za igru
    """

    __sva_pitanja = []
    pitanja_15 = []

    def __init__(self):
        with open("svaPitanja.json") as sp:
            self.sva_pitanja = json.load(sp)
            sp.close()

    def dohvati_random_pitanja(self):
        """
        Dohvaca 15 random pitanja koja ce se postaviti igracu

        :return: Nothing
        """

        # indeksi pitanja u json datoteci
        indexi = []

        # treba nam 15 razlicitih brojeva
        while len(indexi) < 15:
            i = random.randint(0, len(self.sva_pitanja) - 1)
            if i not in indexi:
                indexi.append(i)

        # sortiramo indekse kako bi pitanja bila poredana od najlakseg prema tezima
        indexi.sort()

        # brisemo sve iz liste kako bi bili sigurni da je prazna
        self.pitanja_15 = []

        # dodajemo pitanja u listu koristeci random izabrane indekse
        for i in indexi:
            self.pitanja_15.append(self.sva_pitanja[i])

    def __repr__(self):
        return self.__class__.__name__ + "()"


class Pitanje(object):
    """
    klasa za svako pojedinacno pitanje
    """

    jockerov_odgovor = []

    def __init__(self, pitanje, a, b, c, d, tocan):
        self.__pitanje = pitanje
        self.__oznake = ["A", "B", "C", "D"]
        self.__odgovori = [a, b, c, d]
        self.__tocan_odgovor = tocan

    @property
    def pitanje(self):
        return self.__pitanje

    @property
    def oznake(self):
        return self.__oznake

    @oznake.setter
    def oznake(self, oznake):
        self.__oznake = oznake

    @property
    def odgovori(self):
        return self.__odgovori

    @odgovori.setter
    def odgovori(self, odgovori):
        self.__odgovori = odgovori

    @property
    def tocan_odgovor(self):
        return self.__tocan_odgovor

    def je_tocan(self, ponudeni):
        """
        Provjerava je li odgovor koji je igrač ponudio točan

        :param ponudeni: igracev ponudeni odgovor
        :return: True / False
        """

        return ponudeni == self.tocan_odgovor

    def izbrisi_odgovor(self):
        """
        odgovore koje je jocker pola-pola vratio postavlja u odgovore

        :return: Nothing
        """

        # preostale oznake s pripadajucim odgovorima
        preostale_oznake = []
        preostali_odgovori = []

        # provjeravamo koje oznake je jocker vratio te ih dodajemo u listu
        for o in self.jockerov_odgovor:
            if o == "A":
                preostale_oznake.append(self.oznake[0])
                preostali_odgovori.append(self.odgovori[0])
            elif o == "B":
                preostale_oznake.append(self.oznake[1])
                preostali_odgovori.append(self.odgovori[1])
            elif o == "C":
                preostale_oznake.append(self.oznake[2])
                preostali_odgovori.append(self.odgovori[2])
            else:
                preostale_oznake.append(self.oznake[3])
                preostali_odgovori.append(self.odgovori[3])

        # u oznake i odgovore spremamo listu onih koje je jocker vratio
        self.oznake = preostale_oznake
        self.odgovori = preostali_odgovori

    def __repr__(self):
        return self.__class__.__name__ + '(%r, %r, %r, %r, %r, %r)' % \
               (self.pitanje, self.odgovori[0], self.odgovori[1],
                self.odgovori[2], self.odgovori[3], self.tocan_odgovor)

    def __str__(self):
        return self.pitanje + '\nA: ' + self.odgovori[0] + '\nB: ' + self.odgovori[1] + '\nC: ' + \
               self.odgovori[2] + '\nD: ' + self.odgovori[3] + '\ntocan odgovor: ' + self.tocan_odgovor


class Jocker(object):
    """
    klasa jockera koje igrac ima na raspolaganju
    """

    __svi_jockeri = ["pitaj_publiku", "zovi", "pola_pola"]
    __jocker = ""

    def __init__(self, jocker=""):
        if jocker in self.svi_jockeri:
            self.__jocker = jocker
            self.svi_jockeri.remove(jocker)

    @property
    def svi_jockeri(self):
        return self.__svi_jockeri

    @svi_jockeri.setter
    def svi_jockeri(self, jockeri):
        self.__svi_jockeri = jockeri

    @property
    def jocker(self):
        return self.__jocker

    @jocker.setter
    def jocker(self, jocker):
        self.__jocker = jocker

    @staticmethod
    def pitaj_publiku(lista_oznaka):
        """
        za svaki odgovor postavlja postotke koje je publika odabrala

        :param lista_oznaka: lista oznaka ["A" - "D"] za trenutno pitanje
        :return: lista svih oznaka s pripadajucim postotcima
        """

        # suma svih postotaka
        suma_vjerojatnosti = 100

        # lista u kojoj ce se nalaziti oznake s pripadajucim postotcima
        # rezultat = [[oznaka, postotak],...]
        rezultat = []

        # kopirana lista oznaka
        zamjena = lista_oznaka[:]

        # random izaberemo 1 ili 3 odgovora te postotak te ubacimo u rezultat
        for i in range(len(zamjena) - 1):
            izabrani_odgovor = random.choice(zamjena)
            zamjena.remove(izabrani_odgovor)
            postotak = random.randint(0, suma_vjerojatnosti)
            suma_vjerojatnosti -= postotak
            rezultat.append([izabrani_odgovor, postotak])

        # zadnju oznaku i postotak ubacimo u rezultat
        rezultat.append([zamjena[0], suma_vjerojatnosti])

        # sortira rezultat tako da oznake budu ["A", "B", "C", "D"]
        rezultat.sort(key=lambda x: x[0])

        return rezultat

    @staticmethod
    def zovi(lista_odgovora):
        """
        vraca odgovor kojeg predlaze jocker zovi

        :param lista_odgovora: lista odgovora za trenutno pitanje
        :return: indeks na kojem se nalazi predlozeni odgovor
        """

        return random.randint(0, len(lista_odgovora) - 1)

    @staticmethod
    def pola_pola(tocan):
        """
        vraca dva odgovora od kojih je jedan tocan

        :param tocan: oznaka tocnog odgovora za trenutno pitanje
        :return: lista s tocnim i jednim random odgovorom
        """

        # lista svih oznaka
        odgovori = ["A", "B", "C", "D"]

        # u rezultat odmah ubacujemo tocan
        rezultat = [tocan]
        odgovori.remove(tocan)

        # u rezultat dodajemo jednu od preostale tri oznake
        rezultat.append(random.choice(odgovori))
        rezultat.sort()

        return rezultat

    def __str__(self):
        return self.jocker.title()

    def __repr__(self):
        return self.__class__.__name__ + "(%s)" % self.jocker


class Igrac(object):
    """
    klasa u kojoj se nalaze podatci o igracu
    """

    __iznosi = [0, 100, 200, 300, 500, 1000, 2000, 4000, 8000, 16000, 32000, 64000, 125000, 250000, 500000, 1000000]

    def __init__(self, ime):
        self.__ime = ime
        self.__iznos_ukupno = 0
        self.__prijedeni_prag = 0

    @property
    def ime(self):
        return self.__ime

    @property
    def iznos_ukupno(self):
        return self.__iznos_ukupno

    @iznos_ukupno.setter
    def iznos_ukupno(self, iznos):
        self.__iznos_ukupno = iznos

    @property
    def prijedeni_prag(self):
        return self.__prijedeni_prag

    @prijedeni_prag.setter
    def prijedeni_prag(self, prag):
        self.__prijedeni_prag = prag

    @property
    def iznosi(self):
        return self.__iznosi

    def __str__(self):
        return self.ime.title() + ', ukupan iznos: ' + str(self.iznos_ukupno) + \
               ', prijeđeni prag: ' + str(self.prijedeni_prag)

    def __repr__(self):
        return self.__class__.__name__ + '(%r)' % self.__ime


class PrikazIgre(object):
    """
    view klasa
    """

    @staticmethod
    def odvoji_redak():
        """
        ispisuje red sa 50 zvjezdica

        :return: Nothing
        """

        print("*" * 50)

    def prikazi_pocetak_igre(self):
        """
        ispisuje naslov igre

        :return: Nothing
        """

        self.odvoji_redak()
        print("*" * 12 + "TKO ŽELI BITI MILIJUNAŠ " + "*" * 13)
        self.odvoji_redak()

    @staticmethod
    def prikazi_unos_imena():
        """
        igrac upisuje ime

        :return: ime igraca
        """

        return input("Unesi ime: ")

    @staticmethod
    def prikazi_pitanje(pitanje_objekt, broj_pitanja, iznos):
        """
        prikazuje pitanje

        :param pitanje_objekt: trenutno pitanje
        :param broj_pitanja: redni broj pitanja
        :param iznos: iznos za trenutno pitanje
        :return: Nothing
        """

        # redni broj pitanja i iznos
        print(str(broj_pitanja) + ". Pitanje (" + str(iznos) + " kn): ")

        # pitanje
        print(pitanje_objekt.pitanje)

        # provjeravamo koje su oznake preostale
        # ako je iskoristen jocker pola-pola imamo samo dvije oznake
        for i in range(len(pitanje_objekt.odgovori)):
            if pitanje_objekt.oznake[i] == "A":
                print(">>A: " + pitanje_objekt.odgovori[i])
            elif pitanje_objekt.oznake[i] == "B":
                print(">>B: " + pitanje_objekt.odgovori[i])
            elif pitanje_objekt.oznake[i] == "C":
                print(">>C: " + pitanje_objekt.odgovori[i])
            else:
                print(">>D: " + pitanje_objekt.odgovori[i])

    @staticmethod
    def prikazi_mogucnosti_za_nastavak():
        """
        igrač unosi zeli li odustati, koristiti jockera ili odgovoriti

        :return: 1 ako odustaje / 2 ako koristi jockera / 3 ako odgovara
        """

        # najprije mu ponudimo opcije koje ima
        print("Upišite 1 ako želite odustati.\n"
              "Upišite 2 ako želite koristiti jockera.\n"
              "Upišite 3 ako želite odgovoriti.")

        return input("Vaša odluka: ")

    @staticmethod
    def ispisi_osvojeni_iznos(iznos):
        """
        ispisuje iznos koji je igrač osvojio

        :param iznos: iznos koji je igrac osvojio
        :return: Nothing
        """

        osvojeni_iznos = " Osvojili ste: " + str(iznos) + " kn "

        # duljina ispisa je 50 kako bi uredno izgledalo
        duljina = 50 - len(osvojeni_iznos)
        print("*" * (duljina // 2) + osvojeni_iznos + "*" * (duljina - duljina // 2))

    @staticmethod
    def igrac_odgovara():
        """
        igrač upisuje odgovor

        :return: A, B, C ili D
        """

        return input(">>Vaš konačan odgovor je: ")

    @staticmethod
    def ispis_poruke_o_odgovoru(odgovor, tocan_odgovor=""):
        """
        ispisuje je li odgovor kojeg je igrač ponudio točan ili ne

        :param odgovor: True / False
        :param tocan_odgovor: oznaka tocnog odgovora
        :return: Nothing
        """

        # ako je odgovor tocan
        if odgovor:
            print("Točan odgovor!")

        # ako nije tocan ispisujemo oznaku tocnog odgovora
        else:
            print("Pogrešan odgovor!")
            print("Točan odgovor je: " + tocan_odgovor)

    @staticmethod
    def prikazi_prag(prag):
        """
        prikazuje prag kojeg je igrac presao

        :param prag: 1000 ili 32000
        :return: Nothing
        """

        if prag == 1000:
            print("*" * 9 + " Prešli ste prvi prag (1000 kn) " + "*" * 9)
        else:
            print("*" * 8 + " Prešli ste drugi prag (32000 kn) " + "*" * 8)

    @staticmethod
    def prikazi_jockere(lista_jockera):
        """
        prikazuje jockere koje igrač ima na raspolaganju

        :param lista_jockera: lista svih jockera
        :return jocker: jocker kojeg je izabrao ili None ako nema jockera
        """

        # ako je lista prazna (igrac iskoristio sve jockere)
        if not lista_jockera:
            print("Svi jockeri su iskorišteni.")
            return

        # ako lista nije prazna ispisujemo preostale jockere
        else:
            print("Preostali jockeri na izboru: ")
            for i in range(len(lista_jockera)):
                if lista_jockera[i] == "pitaj_publiku":
                    print("{}) >>Pitaj publiku".format(i + 1))
                elif lista_jockera[i] == "zovi":
                    print("{}) >>Zovi!".format(i + 1))
                else:
                    print("{}) >>Pola - pola".format(i + 1))

            return input("Unesite broj jockera kojeg želite koristiti: ")

    def prikazi_jockerov_odgovor(self, jocker, pitanje_objekt, broj_pitanja, iznos):
        """
        prikazuje pitanje s odgovorima koje je jocker ponudio

        :param jocker: trenutni jocker koji se koristi
        :param pitanje_objekt: trenutno pitanje
        :param broj_pitanja: redni broj pitanja
        :param iznos: iznos za trenutno pitanje
        :return: Nothing
        """

        # ako je jocker pitaj publiku uz odgovore ispisujemo i odgovarajuce postotke
        if jocker == "pitaj_publiku":
            print(str(broj_pitanja) + ". Pitanje (" + str(iznos) + " kn): ")
            print(pitanje_objekt.pitanje)
            for i in range(len(pitanje_objekt.odgovori)):
                if pitanje_objekt.oznake[i] == "A":
                    print(">>A: " + pitanje_objekt.odgovori[i] + " - " +
                          str(pitanje_objekt.jockerov_odgovor[i][1]) + "%")
                elif pitanje_objekt.oznake[i] == "B":
                    print(">>B: " + pitanje_objekt.odgovori[i] + " - " +
                          str(pitanje_objekt.jockerov_odgovor[i][1]) + "%")
                elif pitanje_objekt.oznake[i] == "C":
                    print(">>C: " + pitanje_objekt.odgovori[i] + " - " +
                          str(pitanje_objekt.jockerov_odgovor[i][1]) + "%")
                else:
                    print(">>D: " + pitanje_objekt.odgovori[i] + " - " +
                          str(pitanje_objekt.jockerov_odgovor[i][1]) + "%")

        # ako je jocker zovi ili pola - pola za ispis pitanja koristimo prije definiranu metodu
        else:
            self.prikazi_pitanje(pitanje_objekt, broj_pitanja, iznos)

            # ako je jocker zovi nakon pitanja ispisujemo odgovor kojeg je jocker predlozio
            if jocker == "zovi":
                print(">>>Jocker zovi predlaže odgovor " + pitanje_objekt.oznake[pitanje_objekt.jockerov_odgovor] +
                      ": " + pitanje_objekt.odgovori[pitanje_objekt.jockerov_odgovor])

    @staticmethod
    def prikazi_odluku_o_nastavku():
        """
        igrac unosi zeli li ponovno igrati ili ne

        :return: da / ne
        """

        return input("Želite li ponovno igrati (da/ne)? ")


class Igra(object):
    """
    controler klasa
    """

    def __init__(self, prikaz):
        self.__prikaz = prikaz
        self.__pitanja = Pitanja()  # 3
        self.__broj_pitanja = 1
        self.__jocker = Jocker()  # 4
        self.__igrac = None

    @property
    def prikaz(self):
        return self.__prikaz

    @property
    def pitanja(self):
        return self.__pitanja

    @pitanja.setter
    def pitanja(self, pitanja):
        self.__pitanja = pitanja

    @property
    def broj_pitanja(self):
        return self.__broj_pitanja

    @property
    def jocker(self):
        return self.__jocker

    @jocker.setter
    def jocker(self, jocker):
        self.__jocker = jocker

    @property
    def igrac(self):
        return self.__igrac

    @igrac.setter
    def igrac(self, igrac):
        self.__igrac = igrac

    def igranje_milijunasa(self):  # 1
        """
        glavna metoda igre

        :return: Nothing
        """

        self.prikaz.prikazi_pocetak_igre()  # 2
        self.unos_igraca()  # 3
        self.pitanja.dohvati_random_pitanja()  # 4

        # za svako pitanje
        for p in self.pitanja.pitanja_15:
            trenutno_pitanje = self.postavljanje_pitanja(p)  # 5
            # odgovor je False dok igrac ne odgovori tocno
            odgovor = False
            while True:
                odluka = self.odluka_o_nastavku()  # 6
                # igrac je odustao
                if odluka == "1":
                    print("*" * 15 + " Točan odgovor je " + trenutno_pitanje.tocan_odgovor + " " + "*" * 15)
                    self.prikaz.odvoji_redak()  # 7
                    self.izracun_osvojenog_iznosa()  # 8
                    break
                # igrac koristi jockera
                elif odluka == "2":
                    self.koristenje_jockera(trenutno_pitanje)  # 9
                # igrac odgovara
                elif odluka == "3":
                    odgovor = self.odgovaranje_na_pitanje(trenutno_pitanje)  # 10
                    break

            # ako je igrac odustao ili krivo odgovorio
            if odluka == "1" or (odluka == "3" and not odgovor):
                break

            self.__broj_pitanja += 1

        # igrac je odgovorio na sva pitanja tocno
        if self.__broj_pitanja == 16:
            self.izracun_osvojenog_iznosa()  # 11

        ponovno_pokreni = self.ponovno_pokretanje_igre()  # 12
        # ako igrac zeli ponovno igrat
        if ponovno_pokreni:
            main()  # 13

    def unos_igraca(self):  # 1
        """
        provjerava je li igrac unio ime

        :return: Nothing
        """

        # ponavljamo unos sve dok igrac unosi ime bez znakova
        while True:
            ime = self.prikaz.prikazi_unos_imena()  # 2  # 3

            # ako je unos dobar, stvaramo instancu klase Igrac()
            if ime.strip():
                self.prikaz.odvoji_redak()  # 4
                self.igrac = Igrac(ime)  # 5
                break

    def postavljanje_pitanja(self, pitanje_objekt):  # 1
        """
        instancira objekt klase Pitanje()

        :param pitanje_objekt: trenutno pitanje
        :return: pitanje
        """

        # stvaramo instancu klase Pitanje() te prikazemo to pitanje igracu
        p = Pitanje(pitanje_objekt['question'], pitanje_objekt['A'], pitanje_objekt['B'],
                    pitanje_objekt['C'], pitanje_objekt['D'], pitanje_objekt['answer'])  # 2
        self.prikaz.prikazi_pitanje(p, self.broj_pitanja, self.igrac.iznosi[self.broj_pitanja])  # 3
        self.prikaz.odvoji_redak()  # 4
        return p  # 5

    def odluka_o_nastavku(self):  # 1
        """
        provjerava zeli li igrac odustat, koristit jockera ili odgovorit

        :return: 1 / 2 / 3
        """

        # ponavljamo unos dok igrac ne unese 1, 2 ili 3
        while True:
            odgovor = self.prikaz.prikazi_mogucnosti_za_nastavak()  # 2  # 3
            self.prikaz.odvoji_redak()  # 4
            if odgovor == "1" or odgovor == "2" or odgovor == "3":
                return odgovor  # 5

    def koristenje_jockera(self, pitanje_objekt):  # 1
        """
        provjerava kojeg jockera je igrač odabrao

        :return: Nothing
        """

        # ponavljamo unos dok igrac nije unio ispravan broj (1, 2, 3)
        while True:
            odluka = self.prikaz.prikazi_jockere(self.jocker.svi_jockeri)  # 2  # 3
            self.prikaz.odvoji_redak()  # 4

            # ako igrac nema jockera na raspolaganju
            if odluka is None:
                print("odluka je none")
                self.jocker = Jocker()  # 5
                break

            # ako ima jockera i unios je tocan
            elif "0" < odluka <= str(len(self.jocker.svi_jockeri)):
                self.jocker = Jocker(self.jocker.svi_jockeri[int(odluka) - 1])  # 6
                break

        # temeljem unosa pozivamo odgvarajucu metodu
        if self.jocker.jocker == "pitaj_publiku":
            pitanje_objekt.jockerov_odgovor = self.jocker.pitaj_publiku(pitanje_objekt.oznake)  # 7
        elif self.jocker.jocker == "zovi":
            pitanje_objekt.jockerov_odgovor = self.jocker.zovi(pitanje_objekt.odgovori)  # 8
        elif self.jocker.jocker == "pola_pola":
            pitanje_objekt.jockerov_odgovor = self.jocker.pola_pola(pitanje_objekt.tocan_odgovor)  # 9
            # ostavljamo samo one oznake i odgovore koje je jocker vratio
            pitanje_objekt.izbrisi_odgovor()  # 10
        self.prikaz.prikazi_jockerov_odgovor(self.jocker.jocker, pitanje_objekt,
                                             self.broj_pitanja, self.igrac.iznosi[self.broj_pitanja])  # 11
        self.prikaz.odvoji_redak()  # 12

    def odgovaranje_na_pitanje(self, pitanje_objekt):  # 1
        """
        provjera je li igrač točno odgovorio

        :param pitanje_objekt: trenutno pitanje
        :return: True / False
        """

        # ponavljamo unos dok igrac nije unio jednu od ponudeih oznaka
        while True:
            odgovor = self.prikaz.igrac_odgovara()  # 2  # 3

            # ako se odgovor nalazi u ponudenim oznakama
            if odgovor.upper() in pitanje_objekt.oznake:

                # provjeravamo je li odgovor tocan
                tocan = pitanje_objekt.je_tocan(odgovor.upper())  # 4

                # ako je igrac tocno odgovorio
                if tocan:
                    self.prikaz.odvoji_redak()  # 5
                    self.prikaz.ispis_poruke_o_odgovoru(True)  # 6
                    self.prikaz.odvoji_redak()  # 7
                    # povecamo mu ukupan osvojeni iznos
                    self.igrac.iznos_ukupno = self.igrac.iznosi[self.broj_pitanja]  # 8

                    # ako je presao prag prikazemo poruku o tome
                    if self.igrac.iznos_ukupno == 1000 or self.igrac.iznos_ukupno == 32000:
                        self.igrac.prijedeni_prag = self.igrac.iznos_ukupno  # 9
                        self.prikaz.prikazi_prag(self.igrac.prijedeni_prag)  # 10
                        self.prikaz.odvoji_redak()  # 11
                    return True  # 12

                # igrac je krivo odgovorio
                else:
                    # ispisemo mu tocan odgovor te osvojeni iznos
                    self.prikaz.odvoji_redak()  # 13
                    self.prikaz.ispis_poruke_o_odgovoru(False, pitanje_objekt.tocan_odgovor)  # 14
                    self.prikaz.odvoji_redak()  # 15
                    self.prikaz.ispisi_osvojeni_iznos(self.igrac.prijedeni_prag)  # 16
                    self.prikaz.odvoji_redak()  # 17
                    return False  # 18

    def izracun_osvojenog_iznosa(self):  # 1
        """
        ispis iznosa kojeg je igrač osvojio

        :return: Nothing
        """

        self.prikaz.ispisi_osvojeni_iznos(self.igrac.iznos_ukupno)  # 2
        self.prikaz.odvoji_redak()  # 3

    def ponovno_pokretanje_igre(self):  # 1
        """
        provjera zeli li igrac ponovno igrat

        :return: True / False
        """

        # ponavljamo unos dok igrac ne unese da ili ne
        while True:
            odluka = self.prikaz.prikazi_odluku_o_nastavku()  # 2  # 3
            if odluka.upper() == "NE":
                return False  # 4
            elif odluka.upper() == "DA":
                # resetiramo jockere
                Jocker.svi_jockeri = ["pitaj_publiku", "zovi", "pola_pola"]  # 5
                self.jocker = Jocker()  # 6
                return True  # 7


def main():
    # stvaramo instancu klase PrikazIgre() i Igra() te pozivamo glavnu metodu
    prikaz = PrikazIgre()  # 1
    igra = Igra(prikaz)  # 2
    igra.igranje_milijunasa()  # 5


if __name__ == "__main__":
    main()
