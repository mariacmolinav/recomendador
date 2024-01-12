import json
import os


class Colores:
    NEGRITA = "\033[1m"
    RED = "\033[31m"  # Rojo
    GREEN = "\033[32m"  # Verde
    YELLOW = "\033[33m"  # Amarillo
    BLUE = "\033[34m"  # Azul
    MAGENTA = "\033[35m"  # Magenta
    CYAN = "\033[36m"  # Cian
    RESET = "\033[0m"


CLIMAS_EMOJI = {
    "Seco": '☀️',
    "Templado": '☁️',
    "Continental": '🌲',
    "Tropical": '🌴',
    "Polar": '⛄',
}

TURISMO_EMOJI = {
    "Recreativo": '🎉',
    "Familiar": '👨🏻‍👩‍👧‍👦‍',
    "Romantico": '💘',
    "Dark": '💀',
    "Gastronómico": "🍴",
    "Cultural": "🎨",
    "Educativo": "📚"
}


def print_title():
    os.system('cls')
    text = "Veamos que destino te depara!"
    print("─" * len(text))
    print(" ".join([c for c in "BORONDOTROPICO".upper()]))
    print(text)
    print("─" * len(text))


def print_dialog(text: str):
    print("─" * len(text))
    print(text)
    print("─" * len(text))


def print_question(question: str, expected_type: type, is_required: bool = False):
    result = input(f"{question}: ")
    if not result and is_required:
        print("[ERROR] Debes introducir una respuesta\n")
        return print_question(question, expected_type, is_required)
    elif not result and not is_required:
        return None
    if expected_type in [int, float]:
        try:
            result = float(result)
            if expected_type is int:
                result = int(result)
        except:
            print("[ERROR] Debes introducir un número entero\n")
            return print_question(question, expected_type, is_required)

    return result


def select_options(question: str, options: list[str]):
    print(f"\n{question}")
    print("\n → ".join(["Seleciona una de las siguientes opciones disponibles: "] + options))
    respuesta = input("Esperando tu selección ☺: ")
    if respuesta in options:
        return respuesta
    print("[ERROR] Debes introducir una selección válida")
    return select_options(question, options)


def filtrar_destinos(presupuesto: float, clima: str | None, turismo: str):
    with open("database.json", "r", encoding='utf-8') as archivo:
        data = archivo.read()
        data = json.loads(data)
    print(f"Cargados {len(data)} destinos")
    data = [i for i in data if i["presupuesto"] <= presupuesto]
    print(f"{len(data)} para el presupuesto")

    if clima:
        data = [i for i in data if i["clima"] == clima]
        print(f"{len(data)} para el clima")
    if turismo:
        data = [i for i in data if turismo in i["turismo"]]
        print(f"{len(data)} para el turismo")
    return data


def tarjeta_destinos(destino: dict, personas: int, dias: int):
    X = f"{Colores.CYAN}꞉{Colores.RESET}"
    print(f"{Colores.CYAN}͠{Colores.RESET}" * 70)
    print(f"{X} {Colores.NEGRITA}" + " ".join([c for c in destino['nombre'].upper()]).center(68) + f"{Colores.RESET}꞉")
    print(X + f"{destino['ciudad']}, {destino['pais']}".center(69) + X)
    print(X.ljust(79, " ") + X)
    print(f"{X} " + "".join([TURISMO_EMOJI[c] for c in destino["turismo"]]).ljust(
        10) + f'{CLIMAS_EMOJI[destino["clima"]]} {destino["clima"]}'.rjust(53, " ") + f'  {X}')
    print(f"{X} " + f"{Colores.CYAN}·{Colores.RESET}" * 67 + f" {X}")
    for c in destino['actividades']:
        print(f"{X}  - " + c.ljust(65, " ") + X)
    costo = personas * dias * destino["presupuesto"]
    print(f"{X}         " + "\033[1mTOTAL $ {:,.2f}\033[0m ".format(costo).rjust(68) + X)
    print(f"{X}{Colores.YELLOW}" + "d/p $ {:,.2f}".format(destino['presupuesto']).rjust(68) + f' {Colores.RESET}{X}')
    print(f"{Colores.CYAN}͜{Colores.RESET}" * 70)


if __name__ == '__main__':

    print_title()
    # calcular presupuesto
    personas = print_question("¿Cuántas personas iran de viaje?", int, True)
    dias = print_question("¿Cuántos días irán de viaje?", int, True)
    presupuesto_total = print_question("¿Cuánto dinero piensas gastar?", float, True)
    presupuesto = presupuesto_total / personas / dias
    # print_dialog(f"entiendo que tu presupuesto te alcanzaría para un gasto de {presupuesto} por persona al día")
    # obtencion del clima
    print_title()
    clima = select_options("¿Tienes algún clima en mente?", options=["si", "no"])
    if clima == "si":
        os.system('cls')
        clima = select_options(
            "¿Qué tipo de clima prefiere?",
            list(CLIMAS_EMOJI.keys())
        )
    else:
        clima = None

    print_title()
    # obtencion del tipo de turismo
    turismo = select_options("¿Prefieres algún tipo de turismo?", options=["si", "no"])
    if turismo == "si":
        print_title()
        turismo = select_options(
            "¿Qué tipo de turismo desea hacer?",
            list(TURISMO_EMOJI.keys())
        )
    else:
        turismo = None

    print_title()
    print_dialog(
        "De maravilla, BORONDO se encargará de buscar destinos que hagan posible tus ansias del\n"
        f"turismo {turismo} {f'en el clima {clima}' if clima else ''} que deseas."
    )
    input(f"PRESIONE ENTER PARA LA SIGUIENTE RECOMENDARCION DE BORONTROPICO")


    # filtrar los destinos
    destinos = filtrar_destinos(presupuesto, clima, turismo)

    if not destinos:
        print_dialog("Lo sentimos, BORONDOTROPICO no ha podido encontrar ningún destino que ciña a sus deseos.")

    else:
        plural = "s" if len(destinos) > 1 else ""
        print_dialog(f"BORONDOTROPICO ha encontrado {len(destinos)} destino{plural} posible{plural}")
    for i in destinos:
        print_title()
        tarjeta_destinos(i, personas, dias)
        input(f"PRESIONE ENTER PARA LA SIGUIENTE RECOMENDARCION DE BORONTROPICO")
    print(f"{Colores.NEGRITA}{Colores.GREEN}HA LLEGADO AL  FINAL DE SUS POSIBLES DESTINOS{Colores.RESET}".center(70))
    print(f"{Colores.NEGRITA}{Colores.GREEN}Hasta la proxima, gracias por usar BORONDOTROPICO{Colores.RESET}".center(70))
