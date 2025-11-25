from vidas.funcion_vidas import VIDAS


#hecemos una funcion 
def reducir_vida(VIDAS: int)-> tuple[int,bool]:
    """
    gestiona la perdida de vida disminuye el contador 

    args:
        1.(int) el numero de vidas despues de la resta 
        2.(booleano) true si es juego termino (vidas <= 0) false si continua
    
    
    """

#restamos si pierde una vida
    VIDAS -=1

#aca vamos a comprobar si se perdio las 3 vidas

    if VIDAS <= 0:
        print("GAME OVER ")

    #devolvemos el nuevo valor y true para indicar el fin del juego
        return (VIDAS, True)

    #devolvemos el numvo valor y false para indicar que el juego continua
    # es decir si vidas > 0

    else:
        return(VIDAS, False)