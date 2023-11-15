import os
import numpy as np
import matplotlib.pyplot as plt

folder = "sym/folder"
start_line = 5

file_names = []
std_values = []

for liczba in range(10, 201, 10):
    nazwa_pliku = f"{liczba}.txt"
    sciezka_pliku = os.path.join(folder, nazwa_pliku)

    try:
        with open(sciezka_pliku, 'r') as plik:
            lines = plik.readlines()[start_line - 1:]

            combined_line = ''.join(lines)
            data = np.fromstring(combined_line, dtype=float, sep=' ')
            odchylenie_standardowe = np.std(data)
            std_values.append(odchylenie_standardowe)
            file_names.append(nazwa_pliku)

            print(f"Odchylenie standardowe od linii {start_line} w pliku {nazwa_pliku}: {odchylenie_standardowe}")

    except Exception as e:
        print(f"Wystąpił błąd podczas analizy pliku {sciezka_pliku}: {str(e)}")

# Teraz masz listę odchyleń standardowych dla danych od piątej linii w poszczególnych plikach w folderze
print("Lista odchyleń standardowych:", std_values)

# Konwersja na listę przed utworzeniem wykresu
std_values_list = list(std_values)

# Wykres
plt.plot(file_names, std_values_list, marker='o')
plt.xticks(rotation=45, ha='right')
plt.xlabel('Nazwa pliku')
plt.ylabel('Odchylenie standardowe')
plt.title('Odchylenie standardowe')
plt.grid()
plt.tight_layout()
plt.show()