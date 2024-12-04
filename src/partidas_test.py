from partidas import *

def test_lee_partidas(ruta):
    datos = lee_partidas(ruta)
    print(f"Se han leído {len(datos)} registros")
    print(f"Mostrando los tres primeros registro leídos: {datos[:3]}")

def test_victoria_rapida(ruta):
    datos = lee_partidas(ruta)
    vic = victora_mas_rapida(datos)
    print(f"La partida más rápida duró {vic[2]} y fue entre {vic[0]} y {vic[1]}")

def test_top_ratio(ruta,n):
    datos = lee_partidas(ruta)
    print(f"Los {n} nombres con ratio más baja son: {top_ratio_medio_personajes(datos,n)}")

def test_enemigos_mas_debiles(ruta,player):
    datos = lee_partidas(ruta)
    en = enemigos_mas_debiles(datos,player)
    print(f"Los enemigos más débiles que se han enfrentado a {player} son {en[0]}, los ha ganado {en[1]} veces")

def test_movimientos_comunes(ruta,player1,player2):
    datos = lee_partidas(ruta)
    mov = movimientos_comunes(datos,player1,player2)
    print(f"Los movimientos que tienen en común los jugadores {player1} y {player2} son: {mov}")

def test_dia_mas_combo_finish(ruta):
    datos = lee_partidas(ruta)
    dia = dia_mas_combo_finish(datos)
    print(f"El día de la semana con más combo finish es el: {dia}")

if __name__ == "__main__":
    test_lee_partidas("data/games.csv")
    test_victoria_rapida("data/games.csv")
    test_top_ratio("data/games.csv",5)
    test_enemigos_mas_debiles("data/games.csv","Ken")
    test_movimientos_comunes("data/games.csv","Ryu","Ken")
    test_dia_mas_combo_finish("data/games.csv")
