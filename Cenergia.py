from flask import Blueprint, render_template, request
import random

cenergia_bp = Blueprint('cenergia', __name__)

energy_saving_tips = {
    "refrigerador": [
        "Mantén el refrigerador lejos de fuentes de calor como hornos o ventanas soleadas.",
        "Asegúrate de que las puertas del refrigerador estén bien selladas.",
        "No introduzcas alimentos calientes en el refrigerador, deja que enfríen primero."
    ],
    "aire acondicionado": [
        "Limpia o cambia los filtros regularmente.",
        "Mantén las puertas y ventanas cerradas mientras usas el aire acondicionado.",
        "Usa ventiladores para complementar el aire acondicionado y reducir su uso."
    ],
    "lavadora": [
        "Usa agua fría siempre que sea posible.",
        "Lava cargas completas en lugar de medias cargas para ahorrar energía.",
        "Limpia el filtro de la lavadora regularmente para mantenerla eficiente."
    ],
    "televisor": [
        "Apaga el televisor cuando no lo estés viendo.",
        "Usa configuraciones de brillo y contraste más bajas.",
        "Desenchufa el televisor si no lo usarás por un periodo prolongado."
    ],
    "computadora": [
        "Habilita el modo de suspensión o ahorro de energía.",
        "Apaga la computadora y el monitor cuando no estén en uso.",
        "Desconecta cargadores o periféricos innecesarios."
    ]
}

@cenergia_bp.route('/consumoE', methods=['GET', 'POST'])
def consumoE():
    if request.method == 'GET':
        return render_template('consumoE.html')
    elif request.method == 'POST':
        try:
            device_name = request.form.get('device_name', '').lower()
            wattage = float(request.form.get('wattage', 0))
            hours_per_day = float(request.form.get('hours_per_day', 0))
            days_per_month = int(request.form.get('days_per_month', 0))
            if not device_name or wattage <= 0 or hours_per_day <= 0 or days_per_month <= 0:
                return render_template('consumoE.html', error="Por favor, completa todos los campos con valores válidos.")
            monthly_consumption = (wattage * hours_per_day * days_per_month) / 1000
            tips = energy_saving_tips.get(device_name, ["Apaga los dispositivos cuando no estén en uso para ahorrar energía."])
            tip = random.choice(tips)
            return render_template(
                'result.html',
                device_name=device_name.capitalize(),
                monthly_consumption=monthly_consumption,
                tip=tip
            )
        except ValueError:
            return render_template('consumoE.html', error="Por favor, ingresa valores numéricos válidos.")
