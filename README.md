# Projekt-1-kryptografia

Projekt zaliczeniowy z przedmiotu **Kryptografia – ćwiczenia** (semestr jesienny 2026). Aplikacja konsolowa napisana w Pythonie umożliwia szyfrowanie i deszyfrowanie tekstu.

## Menu

```text
PROJEKT 1 - KRYPTOGRAFIA
1. Szyfruj
2. Deszyfruj
3. Pokaz informacje o szyfrach
0. Zakoncz
```

Po wybraniu szyfrowania lub deszyfrowania program prosi o numery indeksów, tekst i — zależnie od algorytmu — klucz.

## Wybór szyfru

Algorytm jest dobierany automatycznie na podstawie **reszty z dzielenia sumy numerów indeksów przez 3**:

| Suma indeksów modulo 3 | Algorytm | Klucz |
|---|---|---|
| 0 | Szyfr podstawieniowy (Cezara) | Liczba całkowita, np. `3` |
| 1 | Szyfr Vigenère'a | Słowo z co najmniej 8 liter A–Z, np. `TAJEMNICA` |
| 2 | Szyfr permutacyjny | Stała permutacja zapisana w kodzie |

Numery indeksów można rozdzielać spacjami, przecinkami lub średnikami. Program akceptuje też pojedynczy numer.

## Opis algorytmów

### Szyfr podstawieniowy (Cezara)

Każda litera alfabetu łacińskiego jest przesuwana o liczbę pozycji określoną kluczem. Deszyfrowanie wykonuje przesunięcie w przeciwną stronę.

Przykład dla klucza `3`: `ABC` → `DEF` → `ABC`.

### Szyfr Vigenère'a

Kolejne litery słowa kluczowego określają przesunięcia kolejnych liter tekstu. Klucz jest powtarzany w razie potrzeby. Do klucza zaliczają się wyłącznie litery A–Z; wymagane jest minimum 8 liter.

### Szyfr permutacyjny

Program przestawia znaki w blokach po 6 znaków zgodnie ze stałą permutacją:

```python
PERMUTACJA = (2, 5, 0, 4, 1, 3)
```

Ostatni blok jest w razie potrzeby uzupełniany znakiem `~`. Szyfrogram ma format `DLUGOSC:TEKST`, aby przy deszyfrowaniu dało się usunąć dopełnienie. W tym wariancie użytkownik nie wpisuje osobnego klucza.

## Przykład użycia

```text
Wybierz opcje: 1
Numery indeksow (oddziel spacjami lub przecinkami): 123456
Wybrany szyfr: podstawieniowy
Podaj tekst jawny: ABC
Klucz - liczba calkowita: 3

WYNIK: DEF
```

Aby odszyfrować wynik, wybierz `2`, wpisz te same numery indeksów, szyfrogram `DEF` i klucz `3`.

## Obsługa błędów

Program sprawdza m.in.:

- czy wybrano istniejącą opcję menu;
- czy numery indeksów składają się z cyfr i poprawnych separatorów;
- czy tekst nie jest pusty ani nie składa się wyłącznie z białych znaków;
- czy klucz Cezara jest liczbą całkowitą;
- czy klucz Vigenère'a zawiera co najmniej 8 liter A–Z (bez spacji i cyfr);
- czy szyfrogram permutacyjny ma poprawny nagłówek i długość.

Przy błędnych danych program wyświetla komunikat i wraca do menu.

## Uwagi

- Szyfry Cezara i Vigenère'a zmieniają wyłącznie litery `A–Z` i `a–z`, zachowując ich wielkość. Polskie znaki, cyfry, spacje i interpunkcja pozostają bez zmian.
- Szyfr permutacyjny przestawia **wszystkie znaki**, także spacje i znaki interpunkcyjne.

## Struktura projektu

```text
projekt-1-kryptografia/
├── projekt_1_kryptografia.py
└── README.md
```
