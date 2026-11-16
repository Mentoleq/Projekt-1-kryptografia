"""Projekt 1 – Kryptografia. Python 3, aplikacja konsolowa.

Wybor algorytmu: suma numerow indeksow modulo 3.
0 = szyfr podstawieniowy (Cezara), 1 = Vigenere, 2 = permutacyjny.
"""

# Modul re sluzy do sprawdzania poprawnosci danych za pomoca wyrazen regularnych.
import re

# Alfabet lacinski ma 26 liter; szyfry literowe dzialaja na A-Z oraz a-z.
# Polskie znaki, cyfry, spacje i interpunkcja nie sa przesuwane.
ALFABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PERMUTACJA = (2, 5, 0, 4, 1, 3)  # Hardcoded, 6 roznych pozycji od 0 do 5.


def pobierz_tekst(etykieta):
    """Pobiera tekst i odrzuca pusty napis lub same biale znaki."""
    tekst = input(etykieta)
    if not tekst.strip():
        raise ValueError("Tekst nie moze byc pusty ani skladac sie z samych spacji.")
    return tekst


def pobierz_indeksy():
    """Wczytuje numery indeksow i zwraca reszte z ich sumy modulo 3.

    Reszta 0 oznacza szyfr podstawieniowy, 1 - Vigenere, 2 - permutacyjny.
    """
    dane = input("Numery indeksow (oddziel spacjami lub przecinkami): ").strip()
    if not re.fullmatch(r"\d+(?:[\s,;]+\d+)*", dane):
        raise ValueError("Podaj co najmniej jeden poprawny numer indeksu (cyfry).")
    # Dzielimy wpisany ciag po spacjach, przecinkach lub srednikach.
    # Kazdy fragment zamieniamy na liczbe calkowita.
    indeksy = [int(x) for x in re.split(r"[\s,;]+", dane)]
    return sum(indeksy) % 3


def pobierz_klucz_liczbowy():
    """Wczytuje przesuniecie Cezara, np. 3, -2 lub 29."""
    wartosc = input("Klucz - liczba calkowita: ").strip()
    if not re.fullmatch(r"[+-]?\d+", wartosc):
        raise ValueError("Klucz musi byc liczba calkowita.")
    return int(wartosc)


def pobierz_klucz_slowo():
    """Wymaga slowa kluczowego z co najmniej osmiu liter A-Z."""
    klucz = input("Slowo kluczowe (minimum 8 liter A-Z): ").strip().upper()
    if not re.fullmatch(r"[A-Z]{8,}", klucz):
        raise ValueError("Klucz musi miec minimum 8 liter alfabetu A-Z, bez cyfr i spacji.")
    return klucz


def przesun_litere(znak, przesuniecie):
    """Przesuwa litere A-Z/a-z; inne znaki pozostawia bez zmian."""
    # ord() zwraca kod znaku, a chr() zamienia kod z powrotem na znak.
    # Odejmujemy kod A, aby litery numerowac od 0 do 25.
    # Modulo 26 sprawia, ze po Z wracamy do A.
    if 'A' <= znak <= 'Z':
        return chr((ord(znak) - ord('A') + przesuniecie) % 26 + ord('A'))
    if 'a' <= znak <= 'z':
        return chr((ord(znak) - ord('a') + przesuniecie) % 26 + ord('a'))
    return znak


def szyfr_podstawieniowy(tekst, klucz, deszyfruj=False):
    """Podstawienie monoalfabetyczne: alfabet przesuniety o podana liczbe."""
    # Przy odszyfrowywaniu odwracamy kierunek przesuniecia.
    # Przyklad: ABC + 3 = DEF, natomiast DEF - 3 = ABC.
    krok = -klucz if deszyfruj else klucz
    return ''.join(przesun_litere(znak, krok) for znak in tekst)


def szyfr_vigenere(tekst, klucz, deszyfruj=False):
    """Klucz przesuwa sie tylko dla liter A-Z/a-z."""
    # Budujemy wynik po jednym znaku. Licznik klucza rosnie tylko dla liter.
    # Dzieki temu spacje i znaki interpunkcyjne nie zuzywaja liter klucza.
    wynik = []
    numer_litery = 0
    for znak in tekst:
        if ('A' <= znak <= 'Z') or ('a' <= znak <= 'z'):
            # Kolejne litery klucza wyznaczaja rozne przesuniecia: A=0, B=1 itd.
            # Operator % powoduje powtarzanie klucza po jego zakonczeniu.
            przesuniecie = ord(klucz[numer_litery % len(klucz)]) - ord('A')
            wynik.append(przesun_litere(znak, -przesuniecie if deszyfruj else przesuniecie))
            numer_litery += 1
        else:
            wynik.append(znak)
    return ''.join(wynik)


def szyfr_permutacyjny(tekst, deszyfruj=False):
    """Permutacja blokow 6 znakow, zachowuje wszystkie znaki, takze spacje.

    Szyfrogram zawiera naglowek dlugosci, aby usunac dopelnienie po odszyfrowaniu.
    """
    # W tej wersji przestawiamy pozycje znakow w blokach szescioliterowych.
    # Permutacja jest wpisana na stale, zgodnie z wymaganiami zadania.
    n = len(PERMUTACJA)
    if not deszyfruj:
        dlugosc = len(tekst)
        # Ostatni blok uzupelniamy znakiem ~ do wielokrotnosci 6.
        # Oryginalna dlugosc pozwoli pozniej usunac tylko dodane znaki.
        dopelniony = tekst + ('~' * (-dlugosc % n))
        bloki = [dopelniony[i:i+n] for i in range(0, len(dopelniony), n)]
        # Dla kazdego bloku pobieramy znaki w kolejnosci z PERMUTACJA.
        # Np. pierwszy znak wyniku pochodzi z pozycji 2 bloku.
        zaszyfrowany = ''.join(''.join(blok[j] for j in PERMUTACJA) for blok in bloki)
        return f"{dlugosc}:{zaszyfrowany}"

    # Odszyfrowanie rozpoczynamy od odczytania naglowka DLUGOSC:TEKST.
    # partition dzieli napis tylko na pierwszym dwukropku.
    naglowek, separator, zawartosc = tekst.partition(':')
    if not separator or not naglowek.isdigit():
        raise ValueError("Niepoprawny szyfrogram: wymagany format DLUGOSC:TEKST.")
    dlugosc = int(naglowek)
    # Kontrola, czy dlugosc blokow i liczba znakow dopelnienia sa mozliwe.
    if len(zawartosc) % n != 0 or dlugosc > len(zawartosc) or len(zawartosc) - dlugosc >= n:
        raise ValueError("Niepoprawna dlugosc szyfrogramu permutacyjnego.")
    wynik = []
    for i in range(0, len(zawartosc), n):
        blok = zawartosc[i:i+n]
        # Odwracamy permutacje: kazdy znak wraca na pierwotna pozycje.
        oryginal = [''] * n
        for pozycja, indeks in enumerate(PERMUTACJA):
            oryginal[indeks] = blok[pozycja]
        wynik.extend(oryginal)
    # Odcinamy dopelnienie, korzystajac z dlugosci zapisanej w naglowku.
    return ''.join(wynik)[:dlugosc]


def menu():
    """Wyswietla menu tekstowe i zwraca wybor uzytkownika."""
    print("\n" + "=" * 48)
    print("PROJEKT 1 - KRYPTOGRAFIA")
    print("1. Szyfruj")
    print("2. Deszyfruj")
    print("3. Pokaz informacje o szyfrach")
    print("0. Zakoncz")
    return input("Wybierz opcje: ").strip()


def uruchom():
    """Glowna petla programu: menu, walidacja, wybor szyfru i wynik."""
    print("Szyfr wybierany automatycznie z sumy indeksow modulo 3.")
    # Petla dziala do wybrania zera albo przerwania programu.
    while True:
        try:
            opcja = menu()
            if opcja == '0':
                print("Koniec programu.")
                return
            if opcja == '3':
                print("0: podstawieniowy (Cezara), klucz: liczba calkowita")
                print("1: Vigenere, klucz: slowo co najmniej 8-literowe")
                print("2: permutacyjny, stala permutacja:", PERMUTACJA)
                continue
            if opcja not in ('1', '2'):
                print("Blad: wybierz 0, 1, 2 lub 3.")
                continue

            # Rodzaj szyfru wynika z numerow indeksow, a nie z recznego wyboru.
            typ = pobierz_indeksy()
            deszyfruj = opcja == '2'
            print("Wybrany szyfr:", ('podstawieniowy', 'Vigenere', 'permutacyjny')[typ])
            tekst = pobierz_tekst("Podaj szyfrogram: " if deszyfruj else "Podaj tekst jawny: ")
            # Dla kazdego algorytmu pobieramy odpowiedni rodzaj klucza.
            # Permutacja nie wymaga podawania klucza, bo jest stala w kodzie.
            if typ == 0:
                klucz = pobierz_klucz_liczbowy()
                wynik = szyfr_podstawieniowy(tekst, klucz, deszyfruj)
            elif typ == 1:
                klucz = pobierz_klucz_slowo()
                wynik = szyfr_vigenere(tekst, klucz, deszyfruj)
            else:
                wynik = szyfr_permutacyjny(tekst, deszyfruj)
            print("\nWYNIK:", wynik)
        # Nieprawidlowe dane nie koncza programu: pokazujemy komunikat
        # i wracamy do menu, aby mozna bylo sprobowac ponownie.
        except ValueError as blad:
            print("Blad:", blad)
        except (EOFError, KeyboardInterrupt):
            print("\nPrzerwano program.")
            return


# Ten warunek uruchamia aplikacje tylko po wykonaniu pliku bezposrednio.
# Przy imporcie jako modul funkcje mozna testowac bez wlaczania menu.
if __name__ == '__main__':
    uruchom()
