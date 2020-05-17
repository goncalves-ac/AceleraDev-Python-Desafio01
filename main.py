from datetime import datetime
import math

records = [
    {'source': '48-996355555', 'destination': '48-666666666', 'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097', 'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097', 'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788', 'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788', 'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099', 'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697', 'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099', 'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697', 'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097', 'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564627800, 'start': 1564626000}
]


def classify_by_phone_number(records):
    lista_completa = []

    visited = set()
    for r in records:
        if r["source"] not in visited:
            visited.add(r["source"])
            lista_completa.append({"source": r["source"], "total": 0})

    for record in records:
        custoChamada = 0

        timestampInicio = record['start']
        timestampFinal = record['end']

        periodo_diurno_inicio = datetime.fromtimestamp(timestampInicio)
        periodo_diurno_inicio = periodo_diurno_inicio.replace(hour=6, minute=00, second=00)
        periodo_diurno_inicio = periodo_diurno_inicio.timestamp()

        periodo_noturno_inicio = datetime.fromtimestamp(timestampInicio)
        periodo_noturno_inicio = periodo_noturno_inicio.replace(hour=22, minute=00, second=00)
        periodo_noturno_inicio = periodo_noturno_inicio.timestamp()

        vinte_tres_horas = datetime.fromtimestamp(timestampInicio)
        vinte_tres_horas = vinte_tres_horas.replace(hour=23, minute=59, second=59)
        vinte_tres_horas = vinte_tres_horas.timestamp()

        zero_horas = datetime.fromtimestamp(timestampInicio)
        zero_horas = zero_horas.replace(hour=00, minute=00, second=00)
        zero_horas = zero_horas.timestamp()

        if periodo_noturno_inicio > timestampInicio >= periodo_diurno_inicio:
            if timestampFinal < periodo_noturno_inicio:
                time = math.floor((timestampFinal - timestampInicio) / 60)
                custoChamada = round(((time * 0.09) + 0.36), 2)
            else:
                time = math.floor((periodo_noturno_inicio - timestampInicio) / 60)
                custoChamada = round(((time * 0.09) + 0.36), 2)

        elif vinte_tres_horas > timestampInicio >= periodo_noturno_inicio or periodo_diurno_inicio > timestampInicio \
                >= zero_horas:
            if vinte_tres_horas > timestampFinal >= periodo_noturno_inicio or periodo_diurno_inicio > timestampFinal \
                    >= zero_horas:
                custoChamada = 0.36
            else:
                time = math.floor((timestampFinal - periodo_diurno_inicio) / 60)
                custoChamada = round(((time * 0.09) + 0.36), 2)

        for d in lista_completa:
            if d["source"] == record['source']:
                d["total"] += custoChamada
                d["total"] = round(d["total"], 2)
                break

    lista_completa_final = sorted(lista_completa, key=lambda item: item['total'], reverse=True)

    return lista_completa_final