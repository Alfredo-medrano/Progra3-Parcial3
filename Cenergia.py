from flask import Blueprint, render_template, request
import random

cenergia_bp = Blueprint('cenergia', __name__)

energy_saving_tips = {
    "refrigerador": [
        "Mantén el refrigerador lejos de fuentes de calor como hornos o ventanas soleadas.",
        "Asegúrate de que las puertas del refrigerador estén bien selladas.",
        "No introduzcas alimentos calientes en el refrigerador, deja que enfríen primero.",
        "Evita abrir la puerta del refrigerador innecesariamente."
    ],
    "aire acondicionado": [
        "Limpia o cambia los filtros regularmente.",
        "Mantén las puertas y ventanas cerradas mientras usas el aire acondicionado.",
        "Usa ventiladores para complementar el aire acondicionado y reducir su uso.",
        "Ajusta la temperatura a 24°C para mantener un buen equilibrio entre confort y ahorro de energía."
    ],
    "lavadora": [
        "Usa agua fría siempre que sea posible.",
        "Lava cargas completas en lugar de medias cargas para ahorrar energía.",
        "Limpia el filtro de la lavadora regularmente para mantenerla eficiente.",
        "Utiliza ciclos cortos para pequeñas cargas."
    ],
    "televisor": [
        "Apaga el televisor cuando no lo estés viendo.",
        "Usa configuraciones de brillo y contraste más bajas.",
        "Desenchufa el televisor si no lo usarás por un periodo prolongado.",
        "Usa un regulador de energía para evitar el consumo en espera."
    ],
    "computadora": [
        "Habilita el modo de suspensión o ahorro de energía.",
        "Apaga la computadora y el monitor cuando no estén en uso.",
        "Desconecta cargadores o periféricos innecesarios.",
        "Reduce el brillo de la pantalla."
    ],
    "microondas": [
        "Usa el microondas para calentar solo lo necesario.",
        "Desconecta el microondas cuando no lo estés usando para evitar el consumo de energía en espera.",
        "Usa recipientes aptos para microondas y cubre los alimentos para evitar pérdidas de calor."
    ],
    "secadora": [
        "Usa la secadora solo cuando sea necesario, y para cargas completas.",
        "Limpia el filtro de pelusa después de cada uso para mantener la eficiencia.",
        "Seca la ropa en el exterior cuando las condiciones lo permitan.",
        "Usa el ciclo de baja temperatura para evitar un consumo excesivo."
    ],
    "ventilador": [
        "Apaga el ventilador cuando salgas de la habitación.",
        "Usa ventiladores de techo para distribuir el aire de manera más eficiente.",
        "Aprovecha las corrientes naturales de aire abriendo ventanas en lugares estratégicos."
    ],
    "impresora": [
        "Apaga la impresora cuando no la estés usando.",
        "Imprime solo cuando sea necesario y usa ambos lados del papel para ahorrar recursos.",
        "Configura la impresora para que se apague automáticamente después de un tiempo sin uso."
    ],
    "cafetera": [
        "Desenchufa la cafetera cuando no la estés usando para evitar el consumo en espera.",
        "Prepara solo la cantidad de café que vas a consumir.",
        "Usa una cafetera con apagado automático para evitar que se quede encendida."
    ],
    "aspiradora": [
        "Usa la aspiradora solo cuando sea necesario y para áreas que realmente lo necesiten.",
        "Limpia los filtros regularmente para asegurar que la aspiradora funcione eficientemente.",
        "Opta por modelos de aspiradora de bajo consumo energético."
    ],
    "lavavajillas": [
        "Usa el lavavajillas solo cuando esté lleno para maximizar su eficiencia.",
        "Usa ciclos de lavado corto o eco cuando sea posible.",
        "Desenchufa el lavavajillas cuando no lo estés usando para evitar el consumo en espera."
    ],
    "hervidor de agua": [
        "Hervir solo la cantidad de agua que necesites.",
        "Desenchufa el hervidor después de usarlo para evitar el consumo en espera.",
        "Mantén limpio el hervidor para evitar que se acumule cal y afecte su rendimiento."
    ],
    "hornos eléctricos": [
        "Evita abrir la puerta del horno durante la cocción para que no se pierda calor.",
        "Aprovecha el calor residual del horno para terminar de cocinar.",
        "Usa utensilios de cocina de metal o vidrio para maximizar la eficiencia energética."
    ]
}


@cenergia_bp.route('/consumoE', methods=['GET', 'POST'])
def consumoE():
    if request.method == 'GET':
        return render_template('consumoE.html')
    elif request.method == 'POST':
        try:
            device_name = request.form.get('device_name', '').lower()  # Dispositivo seleccionado
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