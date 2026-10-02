"""
Datos de ejemplo de Claudia Spa, para ver la página completa mientras llegan los reales.

Los carga `python manage.py cargar_ejemplos`. Precios, duraciones y textos son de ejemplo: los pasos de la limpieza
facial son los reales de la dueña; los cuidados y los casos de "avísanos antes si…" son orientaciones generales que
ella debe revisar y ajustar, sobre todo los del plasma y la depilación láser.
"""

# Textos que comparten varios servicios
LIMPIEZA_PASOS = """Limpieza de la piel con jabón facial
Exfoliación
Mascarilla para comedones
Vapor
Extracción manual y con hidrafacial
Mascarilla según tu tipo de piel
Aparatología para desinflamar la piel
Hidratación con velo
Máscara LED
Masaje manual y bloqueador para terminar"""

PLASMA_DESPUES = """Es normal un poco de enrojecimiento o inflamación durante unas horas
No te maquilles ni te laves el rostro durante 12 horas
Usa bloqueador solar y evita el sol directo durante varios días
No hagas ejercicio intenso, sauna ni piscina durante 24 horas
No te apliques ácidos ni exfoliantes durante 5 días"""

PLASMA_CONSULTAR = """Estás en embarazo o lactancia
Tienes problemas de coagulación o tomas anticoagulantes
Tienes anemia, cáncer o alguna enfermedad de la sangre
Tienes fiebre, una infección o herpes en el rostro
Estás en tratamiento médico o tomas medicamentos"""

LASER_IDEAL = """Vellos encarnados o irritación por la cuchilla
Quienes quieren dejar la cera o la cuchilla
Axilas, bozo, piernas, bikini y otras zonas"""

LASER_ANTES = """Rasura la zona con cuchilla 24 horas antes (sin cera ni pinzas)
Deja de usar cera y pinzas desde un mes antes
No te asolees ni uses autobronceador las 2 semanas anteriores
Ven con la piel limpia, sin cremas, desodorante ni maquillaje en la zona"""

LASER_DESPUES = """Es normal un poco de enrojecimiento durante unas horas
Usa bloqueador solar en la zona y evita el sol durante una semana
Entre sesiones no uses cera ni pinzas; si lo necesitas, usa cuchilla
Evita sauna, piscina y ejercicio intenso durante 24 horas"""

LASER_CONSULTAR = """Estás en embarazo o lactancia
Tu piel está bronceada o te asoleaste hace poco
Tomas medicamentos que dan sensibilidad al sol, como algunos antibióticos o la isotretinoína
Tienes tatuajes, lunares o heridas en la zona
Tienes tendencia a queloides o algún problema hormonal"""

SERVICIOS = [
    {
        "nombre": "Limpieza facial profunda",
        "slug": "limpieza-facial-profunda",
        "categoria": "facial",
        "destacado": True,
        "descripcion_breve": "Limpieza completa con extracción, hidrafacial y máscara LED.",
        "descripcion": """Es nuestro tratamiento más pedido. Retira impurezas, células muertas, puntos negros y exceso de grasa para que tu piel respire y se vea limpia, fresca y luminosa.

Combina la extracción manual con el hidrafacial, que limpia e hidrata sin agredir la piel, y termina con aparatología y máscara LED para calmar y desinflamar. Antes de empezar revisamos tu tipo de piel para elegir las mascarillas y los productos adecuados.""",
        "ideal_para": """Piel con puntos negros o comedones
Piel grasa o mixta
Piel opaca o cansada
Cualquier persona que quiera mantener su piel sana""",
        "que_incluye": LIMPIEZA_PASOS,
        "recomendaciones": "Para mantener los resultados, repítela cada 4 a 6 semanas. Si quieres renovar tu piel aún más, "
        "pregunta por el combo con plasma rico en plaquetas.",
        "cuidados_antes": """Ven sin maquillaje, si te es posible
No exfolies tu rostro los 2 días anteriores
No te depiles el rostro con cera los 3 días anteriores
Si usas retinol o ácidos, suspéndelos 3 días antes""",
        "cuidados_despues": """Usa bloqueador solar todos los días
Evita el sol directo y el maquillaje durante 24 horas
No toques ni manipules las zonas tratadas
No uses exfoliantes ni productos con ácidos durante 3 días""",
        "consultar_antes": """Estás en embarazo o lactancia
Tienes alergia a algún producto o cosmético
Usas medicamentos para el acné, como la isotretinoína
Tienes heridas, herpes o una infección en el rostro
Te hiciste otro procedimiento facial hace poco""",
        "duracion_min": 75,
        "duracion_max": 90,
        "precio": 90000,
    },
    {
        "nombre": "Plasma rico en plaquetas",
        "slug": "plasma-rico-en-plaquetas",
        "categoria": "facial",
        "destacado": True,
        "descripcion_breve": "Tratamiento regenerativo que usa tu propio plasma para renovar la piel del rostro.",
        "descripcion": """Se toma una pequeña muestra de tu sangre y se procesa para separar el plasma, que es rico en plaquetas y factores de crecimiento. Después se aplica en el rostro para estimular el colágeno y la regeneración natural de la piel.

Ayuda a mejorar la textura, la firmeza y la luminosidad, y a suavizar líneas finas y marcas. Como es tu propio plasma, el riesgo de alergia es muy bajo. Los resultados aparecen poco a poco durante las semanas siguientes.""",
        "ideal_para": """Piel sin brillo o cansada
Líneas finas y primeros signos de la edad
Marcas leves de acné
Piel que perdió firmeza""",
        "que_incluye": """Valoración de tu piel
Limpieza del rostro
Toma de una pequeña muestra de sangre
Separación del plasma
Aplicación del plasma en el rostro
Mascarilla calmante y bloqueador""",
        "recomendaciones": "Para mejores resultados se recomiendan 3 sesiones, con un mes entre cada una, y después un "
        "mantenimiento cada 6 meses.",
        "cuidados_antes": """Ven sin maquillaje
Toma bastante agua el día anterior y el mismo día
Come algo liviano antes de venir; no vengas en ayunas
Evita el alcohol las 24 horas anteriores
No tomes aspirina ni antiinflamatorios los 3 días anteriores, salvo que te los haya ordenado tu médico""",
        "cuidados_despues": PLASMA_DESPUES,
        "consultar_antes": PLASMA_CONSULTAR,
        "duracion_min": 45,
        "duracion_max": 60,
        "precio": 180000,
    },
    {
        "nombre": "Hidratación facial con máscara LED",
        "slug": "hidratacion-facial-con-mascara-led",
        "categoria": "facial",
        "descripcion_breve": "Hidratación profunda con luz LED para una piel suave y luminosa.",
        "descripcion": """Un tratamiento suave para devolverle a tu piel el agua y la luminosidad que pierde con el sol, el clima o el estrés. Limpiamos el rostro, aplicamos activos hidratantes y terminamos con máscara LED, una luz que calma, desinflama y ayuda a regenerar la piel.

Es relajante, no duele y puedes seguir con tu día normalmente.""",
        "ideal_para": """Piel seca o deshidratada
Piel sensible o enrojecida
Piel opaca
Antes de un evento especial""",
        "que_incluye": """Limpieza de la piel
Exfoliación suave
Sérum hidratante
Mascarilla hidratante
Máscara LED
Crema hidratante y bloqueador""",
        "recomendaciones": "Puedes hacerla cada 15 días o una vez al mes. Es un buen complemento entre una limpieza "
        "facial y otra.",
        "cuidados_antes": """Ven sin maquillaje, si te es posible
No exfolies tu rostro el día anterior""",
        "cuidados_despues": """Usa bloqueador solar todos los días
Toma bastante agua para mantener la hidratación
Puedes maquillarte desde el día siguiente""",
        "consultar_antes": """Estás en embarazo
Tienes epilepsia o sensibilidad a la luz
Tomas medicamentos que dan sensibilidad a la luz
Tienes alergia a algún cosmético""",
        "duracion_min": 40,
        "duracion_max": 50,
        "precio": 70000,
    },
    {
        "nombre": "Limpieza facial + plasma rico en plaquetas",
        "slug": "limpieza-facial-plasma-rico-en-plaquetas",
        "categoria": "facial",
        "es_combo": True,
        "descripcion_breve": "La limpieza profunda y el plasma en una sola cita, a mejor precio.",
        "descripcion": """Los dos tratamientos faciales más pedidos en una sola cita. Primero hacemos la limpieza facial profunda, que deja tu piel lista; después aplicamos el plasma rico en plaquetas, que la regenera y le da firmeza y luminosidad.

Con la piel limpia, el plasma se aprovecha mejor. Y al tomarlos juntos pagas menos que por separado.""",
        "ideal_para": """Piel opaca, con puntos negros y primeros signos de la edad
Quienes quieren renovar su piel por completo
Prepararte para una fecha especial (con una semana de margen)""",
        "que_incluye": """Limpieza facial profunda completa
Toma de una pequeña muestra de sangre
Aplicación del plasma rico en plaquetas
Mascarilla calmante y bloqueador""",
        "recomendaciones": "Puedes repetir el combo cada 1 o 2 meses. Entre un combo y otro, la limpieza facial sola "
        "ayuda a mantener los resultados.",
        "cuidados_antes": """Ven sin maquillaje
No exfolies tu rostro los 2 días anteriores
Toma bastante agua y come algo liviano antes de venir
Evita el alcohol las 24 horas anteriores
No tomes aspirina ni antiinflamatorios los 3 días anteriores, salvo que te los haya ordenado tu médico""",
        "cuidados_despues": PLASMA_DESPUES,
        "consultar_antes": PLASMA_CONSULTAR,
        "duracion_min": 120,
        "duracion_max": 150,
        "precio": 240000,
        "precio_anterior": 270000,
    },
    {
        "nombre": "Masaje relajante",
        "slug": "masaje-relajante",
        "categoria": "corporal",
        "destacado": True,
        "descripcion_breve": "Libera tensiones y descansa cuerpo y mente.",
        "descripcion": """Un masaje de cuerpo completo con movimientos suaves y firmes que sueltan la tensión de los músculos, mejoran la circulación y bajan el estrés.

Usamos aceites o cremas, música suave y un ambiente tranquilo para que te desconectes un rato. La presión se ajusta a lo que te guste.""",
        "ideal_para": """Estrés o cansancio
Tensión en el cuello, la espalda y los hombros
Dificultad para descansar
Un regalo para alguien especial""",
        "que_incluye": """Una charla corta sobre tus zonas de tensión y la presión que prefieres
Masaje de espalda, cuello y hombros
Masaje de brazos y manos
Masaje de piernas y pies
Cierre con movimientos suaves""",
        "recomendaciones": "Para mantener el cuerpo libre de tensión, recomendamos un masaje cada 2 a 4 semanas.",
        "cuidados_antes": """Ven con ropa cómoda
Evita comer pesado la hora anterior
Llega 10 minutos antes para empezar con calma""",
        "cuidados_despues": """Toma bastante agua
Descansa y evita el ejercicio intenso ese día
Evita bañarte con agua muy caliente justo después""",
        "consultar_antes": """Estás en embarazo
Tienes várices, flebitis u otro problema de circulación
Tienes una lesión, una fractura o una cirugía reciente
Tienes fiebre, gripa o una infección en la piel
Tienes la presión alta sin control""",
        "duracion_min": 50,
        "duracion_max": 60,
        "precio": 70000,
    },
    {
        "nombre": "Levantamiento de glúteos",
        "slug": "levantamiento-de-gluteos",
        "categoria": "corporal",
        "destacado": True,
        "descripcion_breve": "Tonifica, reafirma y levanta con aparatología, sin cirugía.",
        "descripcion": """Un tratamiento sin cirugía que combina aparatología y técnicas manuales para tonificar, dar firmeza y mejorar la forma de los glúteos.

Los equipos estimulan el músculo y la circulación de la zona y mejoran la apariencia de la piel. Los resultados son progresivos: se notan más con varias sesiones, acompañadas de ejercicio y buena alimentación. En la valoración armamos el plan según tu caso.""",
        "ideal_para": """Glúteos con poca firmeza
Mejorar la forma sin cirugía
Piel de naranja leve en la zona
Complementar el ejercicio""",
        "que_incluye": """Valoración de la zona
Exfoliación
Aparatología para tonificar y reafirmar
Masaje reafirmante
Gel o crema reafirmante""",
        "recomendaciones": "Se recomienda un plan de 8 a 10 sesiones, 2 veces por semana. En la valoración te decimos "
        "cuántas necesitas.",
        "cuidados_antes": """Ven con ropa cómoda
Toma bastante agua el día anterior
Evita comer pesado la hora anterior
No te apliques cremas en la zona ese día""",
        "cuidados_despues": """Toma bastante agua
Haz ejercicio de piernas y glúteos para potenciar los resultados
Mantén una alimentación balanceada
Es normal sentir la zona un poco sensible o caliente durante unas horas""",
        "consultar_antes": """Estás en embarazo o lactancia
Tienes marcapasos o implantes metálicos
Tienes várices u otro problema de circulación
Te hiciste una cirugía en la zona
Tienes alguna enfermedad del corazón""",
        "duracion_min": 45,
        "duracion_max": 60,
        "duracion_por_sesion": True,
        "precio": 80000,
        "tipo_precio": "desde",
        "sufijo_precio": "por sesión",
    },
    {
        "nombre": "Depilación láser",
        "slug": "depilacion-laser",
        "categoria": "corporal",
        "descripcion_breve": "Piel suave por más tiempo. La duración y el precio dependen de la zona.",
        "descripcion": """El láser actúa sobre la raíz del vello y lo debilita sesión tras sesión, hasta que crece mucho menos, más delgado y más claro. Dura más que la cera o la cuchilla y ayuda a evitar los vellos encarnados y la irritación.

Se puede hacer en axilas, bozo, piernas, zona de bikini y otras zonas. La duración y el precio dependen del tamaño de la zona.""",
        "ideal_para": LASER_IDEAL,
        "que_incluye": """Valoración de la piel y del vello
Limpieza de la zona
Aplicación del láser
Gel calmante y bloqueador""",
        "recomendaciones": "Como el vello crece por etapas, se necesitan varias sesiones: normalmente de 6 a 8, con 4 a "
        "6 semanas entre una y otra. Con el paquete de 5 sesiones pagas menos.",
        "cuidados_antes": LASER_ANTES,
        "cuidados_despues": LASER_DESPUES,
        "consultar_antes": LASER_CONSULTAR,
        "duracion_min": 15,
        "duracion_max": 45,
        "precio": 50000,
        "tipo_precio": "desde",
    },
    {
        "nombre": "Paquete de depilación láser (5 sesiones)",
        "slug": "paquete-depilacion-laser-5-sesiones",
        "categoria": "corporal",
        "es_combo": True,
        "descripcion_breve": "5 sesiones en una misma zona, a mejor precio que pagándolas por separado.",
        "descripcion": """La depilación láser necesita varias sesiones, así que el paquete te deja las 5 primeras en una misma zona a mejor precio que pagándolas una por una.

Las sesiones se programan con 4 a 6 semanas entre una y otra, que es el tiempo que el vello tarda en volver a crecer. El precio depende de la zona.""",
        "ideal_para": LASER_IDEAL,
        "que_incluye": """5 sesiones de depilación láser en una misma zona
Valoración de la piel y del vello en la primera sesión
Gel calmante y bloqueador en cada sesión""",
        "recomendaciones": "Para mejores resultados, no dejes pasar más de 6 semanas entre sesiones. Algunas zonas "
        "necesitan sesiones de mantenimiento después del paquete.",
        "cuidados_antes": LASER_ANTES,
        "cuidados_despues": LASER_DESPUES,
        "consultar_antes": LASER_CONSULTAR,
        "duracion_min": 15,
        "duracion_max": 45,
        "duracion_por_sesion": True,
        "precio": 220000,
        "tipo_precio": "desde",
        "sufijo_precio": "las 5 sesiones",
    },
]

# El combo del slider se muestra solo durante el mes actual (las fechas las pone el comando).
DIAPOSITIVAS = [
    {
        "antetitulo": "Facial · el más pedido",
        "titulo": "Tu piel, renovada desde la primera sesión",
        "texto": "Limpieza facial profunda con extracción, hidrafacial y máscara LED.",
        "texto_boton": "Ver el servicio",
        "destino": "servicio",
        "servicio": "limpieza-facial-profunda",
    },
    {
        "antetitulo": "Promoción del mes",
        "titulo": "Limpieza facial + plasma rico en plaquetas",
        "texto": "Los dos en una sola cita y a mejor precio.",
        "texto_boton": "Quiero este combo",
        "destino": "servicio",
        "servicio": "limpieza-facial-plasma-rico-en-plaquetas",
        "este_mes": True,
    },
    {
        "antetitulo": "Tecnología",
        "titulo": "Hidrafacial, máscara LED y aparatología",
        "texto": "Equipos modernos para resultados que se notan.",
        "texto_boton": "Conocer la tecnología",
        "destino": "tecnologia",
    },
    {
        "antetitulo": "Día de la madre",
        "titulo": "Consiéntela con un momento para ella",
        "texto": "Un masaje relajante o una limpieza facial: el regalo perfecto.",
        "texto_boton": "Pide tu cita",
        "destino": "whatsapp",
        "activa": False,
    },
]

TECNOLOGIA = [
    ("Hidrafacial", "Limpia, extrae e hidrata en profundidad, sin agredir la piel."),
    ("Máscara LED", "Luz que calma, desinflama y ayuda a regenerar la piel."),
    ("Aparatología", "Equipos para tonificar, reafirmar y desinflamar el rostro y el cuerpo."),
]

PREGUNTAS = [
    (
        "¿Cuánto dura cada servicio?",
        "Cada servicio muestra su duración aproximada. Los tiempos pueden variar según cada persona.",
    ),
    (
        "¿Cómo pido una cita?",
        "Por WhatsApp o por teléfono, con un día de anticipación. Te pedimos llegar 10 minutos antes.",
    ),
    ("¿Qué medios de pago reciben?", "Efectivo, Nequi y transferencia bancaria."),
    ("¿Hay que dar un abono?", "En algunos servicios se pide un abono por transferencia para apartar tu cita."),
    ("¿Atienden a domicilio?", "En algunos casos, sí. Escríbenos por WhatsApp y lo acordamos."),
]

# Lunes a sábado: mañana y tarde
HORARIO = [(dia, abre, cierra) for dia in range(1, 7) for abre, cierra in (("09:00", "13:00"), ("14:00", "19:00"))]

NOSOTROS_TITULO = "Manos expertas que cuidan de ti"
NOSOTROS_ANIOS = 15
NOSOTROS_TEXTO = """En Claudia Spa cada tratamiento se adapta a tu piel y a tu cuerpo. Te atiende siempre la misma persona: una cosmetóloga con más de 15 años de experiencia y formación en cosmiatría y en enfermería.

Un espacio tranquilo, limpio y pensado para que te tomes un tiempo para ti."""

FOTOS_LOCAL = ["Recepción del spa", "Cabina de tratamientos", "Equipos de aparatología"]
