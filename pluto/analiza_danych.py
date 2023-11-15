import matplotlib.pyplot as plt
import numpy as np

srednia = []
wszystkie_sub = []  # Lista list, przechowująca wyniki sub dla każdego pliku

for numer_pliku in range(1, 20, 2):
    nazwa_pliku = f"sym_{numer_pliku}.txt"
    sciezka_pliku = f"10_11/pomiary_800M_f_zmienne/pomiary/{nazwa_pliku}"

    sub = []

    with open(sciezka_pliku, "r") as plik:
        numbers = [float(line.strip()) for line in plik]
        prev = numbers[1]
        for i in range(2, len(numbers) - 3):
            sub.append(abs(1 - (abs(numbers[i] - prev))))
            prev = numbers[i]

    wszystkie_sub.append(sub)  # Dodanie wyników sub dla danego pliku do listy wszystkie_sub

# Wygenerowanie wykresu
for i, sub in enumerate(wszystkie_sub):
    plt.plot(sub, label=f"sym_{2*i + 1}.txt")  # Dodanie etykiety z nazwą pliku
    plt.title("Błąd względny pomiaru zmiany o 1 stopień f=800100000 fs=10000000")
    plt.xlabel("Mierzony stopień")
    plt.ylabel("Błąd względny pomiaru")
    plt.legend()  # Dodanie legendy
    plt.grid()
    plt.show()

