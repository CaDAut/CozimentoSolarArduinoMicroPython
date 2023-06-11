
import ephem
from datetime import datetime, timedelta

# Converter graus, minutos e segundos para radianos
def dms_to_radians(degrees, minutes, seconds):
    return (degrees + minutes/60 + seconds/3600) * ephem.degree

# Coordenadas fornecidas
latitude = dms_to_radians(-19, -48, -57)
longitude = dms_to_radians(-43, -57, -15)

# Data e hora inicial
start_time = datetime.now()

# Número de iterações (5 minutos cada)
num_iterations = 12

# Matriz para armazenar as posições
pos_latitude = []
pos_longitude = []

# Calcular a posição do sol a cada 5 minutos
for i in range(num_iterations):
    # Calcular a data e hora atual
    current_time = start_time + timedelta(minutes=5*i)

    # Criar um objeto Observer para as coordenadas fornecidas
    observer = ephem.Observer()
    observer.lat = latitude
    observer.lon = longitude
    observer.elevation = 0

    # Definir a data e hora atual para o objeto Observer
    observer.date = current_time

    # Calcular a posição atual do sol
    sun = ephem.Sun(observer)
    sun.compute(observer)

    # Armazenar as posições na matriz
    pos_latitude.append(sun.alt)
    pos_longitude.append(sun.az)

# Imprimir as posições
print("Posição Latitude:")
for lat in pos_latitude:
    print(lat)

print("Posição Longitude:")
for lon in pos_longitude:
    print(lon)
