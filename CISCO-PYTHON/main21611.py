hora = int(input("Hora de inicio (horas): "))
min = int(input("Minuto de inicio (minutos): "))
dura = int(input("Duración del evento (minutos): "))

x = (hora * 60)+min+dura
y = ((min + dura) -60)
print(str(int(x//60)), str(y), sep=":")
# coloca tu código aqui