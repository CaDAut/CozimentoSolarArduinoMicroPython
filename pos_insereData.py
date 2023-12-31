#Esse script python calcula a posição do sol em relação a cidade de Belo Horizonte - MG 
#(latitude = (-19, -48, -57) - longitude = (-43, -57, -15)) em um determidado momento.
#Esse arquivo solcita ao usuário que ele entre com a data para o cálculo da posição sol.
#Haverá uma versão em MicroPython deste mesmo código.

import ephem

# Converter graus, minutos e segundos para radianos
def dms_to_radians(degrees, minutes, seconds):
    return (degrees + minutes/60 + seconds/3600) * ephem.degree

# Coordenadas fornecidas
latitude = dms_to_radians(-19, -48, -57)
longitude = dms_to_radians(-43, -57, -15)

# Data e hora específica
#(date = '2023/06/11 12:00:00'  # Exemplo: Ano/Mês/Dia Hora:Minuto:Segundo)
print("Informe a data com o seguinte formato: Ano/Mês/Dia Hora:Minuto:Segundo")
date = input()#'2023/06/11 12:00:00')

# Criar um objeto Observer para as coordenadas fornecidas
observer = ephem.Observer()
observer.lat = latitude
observer.lon = longitude
observer.elevation = 0

# Definir a data e hora para o objeto Observer
observer.date = date

# Calcular a posição do sol
sun = ephem.Sun(observer)
sun.compute(observer)

# Obter a posição do sol nas coordenadas fornecidas
pos_latitude = sun.alt
pos_longitude = sun.az

# Imprimir as posições
print("Posição Latitude:", pos_latitude)
print("Posição Longitude:", pos_longitude)
