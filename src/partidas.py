from typing import NamedTuple
import csv
from datetime import datetime
from collections import defaultdict,Counter
 
Partida = NamedTuple("Partida", [
    ("pj1", str),
    ("pj2", str),
    ("puntuacion", int),
    ("tiempo", float),
    ("fecha_hora", datetime),
    ("golpes_pj1", list[str]),
    ("golpes_pj2", list[str]),
    ("movimiento_final", str),
    ("combo_finish", bool),
    ("ganador", str),
    ])

#REPASAR:
#El strptime para datetime
#Repasar los lectores de csv (Parsea lista sobretodo)

def parsea_lista(texto:str)->list[str]:
    res = []
    texto = texto.replace("[","").replace("]","") #Hay corchetes al inicio y al final de la lista y hay que quitarlos
    for trozo in texto.split(","):
        res.append(trozo.strip())
    return res

def transforma_dia(dianum:int)->str:
    dias = ["Lunes","Martes","Miércoles","Jueves","Viernes","Sábado","Domingo"]
    return dias[dianum]


def lee_partidas(ruta:str)->list[Partida]:
    """
    Recibe una cadena de texto con la ruta de un fichero csv, 
    y devuelve una lista de tuplas Partida con la información contenida en el fichero.
    """
    with open (ruta,encoding="utf-8") as f:
        res=[]
        lector = csv.reader(f)
        next(lector)
        for pj1,pj2,puntuacion,tiempo,fecha_hora,golpes1,golpes2,movimientof,combof,ganador in lector:
            puntuacion = int(puntuacion)
            tiempo = float(tiempo)
            fecha_hora = datetime.strptime(fecha_hora,"%Y-%m-%d %H:%M:%S")
            golpes1 = parsea_lista(golpes1)
            golpes2 = parsea_lista(golpes2)
            if combof=="1": 
                combof=True
            else: 
                combof=False
            res.append(Partida(pj1,pj2,puntuacion,tiempo,fecha_hora,golpes1,golpes2,movimientof,combof,ganador))
        return res
    
def victora_mas_rapida(lista:list[Partida])->tuple[str,str,float]: 
    """
    Recibe una lista de tuplas de tipo Partida y devuelve una tupla compuesta por los dos personajes 
    y el tiempo de aquella partida que haya sido la más rápida en acabar. 
    Implemente este ejercicio usando solo bucles.
    """
    min = None
    for partida in lista:
        if min == None or min.tiempo > partida.tiempo:
            min = partida
    return min.pj1,min.pj2,min.tiempo

def top_ratio_medio_personajes(partidas:list[Partida],n:int)->list[str]: 
    """
    Recibe una lista de tuplas de tipo Partida y un número entero n, y devuelve una lista con los n nombres 
    de los personajes cuyas ratios de eficacia media sean las más bajas. La ratio de eficacia 
    se calcula dividiendo la puntuación entre el tiempo de aquellas partidas que haya ganado el personaje. 
    Es decir, si Ryu ha ganado 3 combates, su ratio media se calcula con los cocientes puntuacion/tiempo de dichos combates.
    """
    ratios = defaultdict(list)
    for partida in partidas:
        ratios[partida.ganador].append(partida.puntuacion/partida.tiempo)
    
    res = defaultdict(float)
    for clave, listav in ratios.items():
        res[clave]=sum(listav)/len(listav)
    
    return [elem[0] for elem in sorted(res.items(),key= lambda x:x[1])][:n]
    #return sorted(res, key = lambda j:res.get(j))[:n]

def enemigos_mas_debiles(partidas:list[Partida],player:str)->tuple[list,int]: 
    """
    Recibe una lista de tuplas de tipo Partida y una cadena de texto personaje. 
    El objetivo de esta función es calcular los oponentes frente a los que el personaje ha ganado más veces. 
    Para ello, esta función devuelve una tupla compuesta por una lista de nombres y el número de victorias, 
    de aquellos contrincantes contra los cuales el número de victorias haya sido el mayor. 
    Es decir, si introducimos como parámetro el valor Ken y este ha ganado 2 veces contra Blanka, 
    2 contra Ryu y 1 contra Bison, la función deberá devolver (['Blanka', 'Ryu'], 2)
    """
    victorias = defaultdict(int)
    for partida in partidas:
        if player == partida.ganador:
            if player == partida.pj1:
                victorias[partida.pj2]+=1
            else:
                victorias[partida.pj1]+=1
    maximo = max(victorias.values())
    perdedores = []
    for jugador, victoria in victorias.items():
        if victoria == maximo:
            perdedores.append(jugador)
    return perdedores,maximo

def movimientos_comunes(partidas:list[Partida],player1:str,player2:str)->list[str]: 
    """
    Recibe una lista de tuplas de tipo Partida y dos cadenas de texto personaje1 y personaje2, 
    y devuelve una lista con los nombres de aquellos movimientos que se repitan entre personaje1 y personaje2.
    Tenga solo en cuenta los movimientos que aparecen listados en los campos golpes_pj1 y golpes_pj2.
    """
    mov_com = set()
    for partida in partidas:
        mov_com.update(set(partida.golpes_pj1)&set(partida.golpes_pj2))
    return mov_com

def dia_mas_combo_finish(partidas:list[Partida])->str: 
    """
    Recibe una lista de tuplas de tipo Partida, y devuelve el día de la semana en el que hayan acabado más partidas 
    con un combo finish. Use el método weekday() de datetime para obtener el día de la semana en formato numérico, 
    siendo 0 el lunes y 6 el domingo. Para hacer la traducción del número al nombre, utilice una función auxiliar.
    """
    #res = defaultdict(int)
    #for partida in partidas:
    #    if partida.combo_finish==True:
    #        res[partida.fecha_hora.weekday()]+=1
    res = Counter(partida.fecha_hora.weekday() for partida in partidas if partida.combo_finish == True)
    max = res.most_common()
    return transforma_dia(max[0][0])