import csv
import os
from datetime import datetime, timedelta
import shutil
# - quiz
# - zapis daty każdego pytania do logów 
# - mozliwa powtórka z błędów

class Dane():
    nazwa_uzytkownika = None

def logowanieCzyRejestracja():
    wybor = input("Czy chcesz się zalogować czy zarejestrować? (l/r): ")
    if(wybor == "l"):
        if logowanie():
            print("Zacznij naukę")
            wyborPliku()
        else:
            print("Błedne hasło lub nazwa użytkownika") 
            logowanieCzyRejestracja()     
    elif(wybor == "r"):
        if rejestracja():
            print("Konto zostało utworzone.")
            print("Zacznij naukę")
            wyborPliku()
        else:
            logowanieCzyRejestracja() 
    else:
        print("Możesz wpisać tylko l lub r")
        logowanieCzyRejestracja()     

def logowanie():
    nazwa_uzytkownika = input("Wpisz nazwę użytkownika: ")
    haslo = input("Wpisz hasło: ")  
    with open('uzytkownicy.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")
        for wiersz in reader:
            if wiersz == [nazwa_uzytkownika, haslo]:
                dane.nazwa_uzytkownika = nazwa_uzytkownika
                return True
    return False

def rejestracja():
    nazwa_uzytkownika = input("Wpisz nazwę użytkownika: ")
    haslo = input("Wpisz hasło: ")
    haslo2 = input("Powtórz hasło: ")
    if haslo == haslo2:
        with open('uzytkownicy.csv', 'r', newline='') as plik1:
            reader = csv.reader(plik1, delimiter=",")
            for wiersz in reader:
                if wiersz[0] == nazwa_uzytkownika:
                    print("Użytkownik z taką nazwą już istnieje")
                    return False
            create_user_data(nazwa_uzytkownika)
            with open('uzytkownicy.csv', 'a', newline='') as plik2:
                dopisanie = csv.writer(plik2)
                dopisanie.writerow([nazwa_uzytkownika, haslo])
                dane.nazwa_uzytkownika = nazwa_uzytkownika
                return True
    else:
        print("Hasła nie są identyczne")
        return False

def wyborPliku():
    print("1. Kolory")
    print("2. Zwierzęta")
    print("3. Jedzenie")
    wybor = input("Co chcesz się uczyć? Wpisz numer od 1 do 3 : ")
    plik = None
    if(wybor == "1"):
        plik = dane.nazwa_uzytkownika+"_kolory.csv"
    elif(wybor == "2"):
        plik = dane.nazwa_uzytkownika+"_zwierzeta.csv"
    elif(wybor == "3"):
        plik = dane.nazwa_uzytkownika+"_jedzenie.csv"
    else:
        print("Możesz wybrać tylko numer od 1 do 3")
        wyborPliku()
    quiz(plik,0)

def quiz(nazwa_pliku,flaga):
    ilosc_false = 0
    with open(nazwa_pliku, 'r', encoding='utf-8') as quizcsv:
        odczyt = csv.reader(quizcsv, delimiter=",")
        for index, wiersz in enumerate(odczyt):
            if index == 0 and flaga == 0:
                data_z_pliku = wiersz[0]
                data_z_pliku = datetime.strptime(data_z_pliku, "%Y-%m-%d %H:%M:%S.%f")
                if data_z_pliku < datetime.now():
                    with open(nazwa_pliku, 'r') as f:
                        reader = csv.reader(f)
                        data = [row for row in reader]

                    with open(nazwa_pliku, 'w', newline='') as f:
                        writer = csv.writer(f)
                        for row in data:
                            if len(row) > 2:
                                row[2] = False
                            writer.writerow(row)
                    quiz(nazwa_pliku,1)
                else:
                    continue
            elif index == 0:
                data_z_pliku = wiersz[0]
                data_z_pliku = datetime.strptime(data_z_pliku, "%Y-%m-%d %H:%M:%S.%f")
                continue
            if wiersz[2] == "False":
                ilosc_false = ilosc_false + 1
                text = "Przetłumacz "+str(wiersz[0])+": " 
                odpowiedz = input(text)
                if odpowiedz == wiersz[1]:
                    with open(nazwa_pliku, 'r') as f_in:
                        reader = csv.reader(f_in)
                        rows = [row for row in reader]
                        if data_z_pliku < datetime.now():
                            rows[0][0] = datetime.now() + timedelta(days=7)
                        rows[index][-1] = True
                    with open(nazwa_pliku, 'w', newline='') as f_out:
                        writer = csv.writer(f_out)
                        for row in rows:
                            writer.writerow(row)
                    print("Dobrze !")
                else:
                    print("Źle :c Prawidłowa odpowiedź to: ", wiersz[1])
    if ilosc_false == 0:
        print("Brak słówek do powtórzenia. Widzimy się",data_z_pliku)
    else:
        print("Koniec lekcji")
    wyborPliku()

def create_user_data(username):
    file_names = ['kolory.csv', 'zwierzeta.csv', 'jedzenie.csv']
    current_time = str(datetime.now() )
    
    for file_name in file_names:
        src_file = file_name
        dst_file = username + '_' + file_name
        shutil.copy(src_file, dst_file)
        with open(dst_file, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(current_time + '\n' + content)
dane = Dane()
logowanieCzyRejestracja()

