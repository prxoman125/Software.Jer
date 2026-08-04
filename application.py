import pandas as pd
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Super Calculadora Multifuncional",
    page_icon="🧮",
    layout="wide",
)

# Estilo principal
st.title("🧮 Suite Interactiva de Calculadoras Especializadas")
st.markdown(
    "Selecciona un sector, una herramienta y tu moneda preferida en la barra"
    " lateral para comenzar."
)

# ==========================================
# CONFIGURACIÓN DE MONEDA EN LA BARRA LATERAL
# ==========================================
st.sidebar.header("⚙️ Configuración General")
moneda_seleccionada = st.sidebar.selectbox(
    "Selecciona la Moneda:",
    ["Dólares ($ USD)", "Pesos Mexicanos ($ MXN)"],
)

# Definir símbolo y tasas de conversión base aproximadas
if "USD" in moneda_seleccionada:
  simbolo = "$"
  tasa_cambio = 1.0
else:
  simbolo = "$"
  tasa_cambio = 18.0  # Tasa base de referencia USD a MXN

st.sidebar.markdown(f"**Moneda activa:** {moneda_seleccionada}")

# Menú de navegación ampliado en la barra lateral
st.sidebar.header("Menú de Navegación")
sector = st.sidebar.selectbox(
    "Elige un Sector:",
    [
        "📊 Finanzas y Emprendimiento",
        "🏢 Productividad y Gestión",
        "🏋️ Salud, Fitness y Nutrición",
        "📱 Creadores y Marketing",
        "🏡 Inmuebles y Bienes Raíces",
        "🎓 Educación y Cursos Online",
    ],
)

# ==========================================
# SECTOR 1: FINANZAS Y EMPRENDIMIENTO
# ==========================================
if sector == "📊 Finanzas y Emprendimiento":
  st.header("📊 Finanzas y Emprendimiento")
  herramienta_fin = st.selectbox(
      "Selecciona la herramienta:",
      [
          "Calculador de tarifas para Freelancers",
          "Calculador de rentabilidad para E-commerce",
          "Calculador de Libertad Financiera (FIRE)",
      ],
  )

  if herramienta_fin == "Calculador de tarifas para Freelancers":
    st.subheader("💼 Calculador de Tarifas para Freelancers")
    col1, col2 = st.columns(2)
    with col1:
      gastos_mes_base = st.number_input(
          f"Gastos fijos mensuales ({simbolo})",
          min_value=0.0,
          value=800.0 * tasa_cambio,
          step=50.0,
      )
      impuestos_pct = (
          st.number_input(
              "Estimación de impuestos (%)", min_value=0.0, value=20.0, step=1.0
          )
          / 100
      )
    with col2:
      horas_semana = st.number_input(
          "Horas de trabajo a la semana", min_value=1, value=30, step=1
      )
      margen_ganancia = (
          st.number_input(
              "Margen de ganancia deseado (%)",
              min_value=0.0,
              value=25.0,
              step=5.0,
          )
          / 100
      )

    if st.button("Calcular Tarifa"):
      semanas_mes = 4.33
      horas_mes = horas_semana * semanas_mes
      costo_con_margen = gastos_mes_base * (1 + margen_ganancia)
      ingreso_necesario = costo_con_margen / (1 - impuestos_pct)
      tarifa_hora = ingreso_necesario / horas_mes if horas_mes > 0 else 0

      st.success(
          f"### Tarifa recomendada por hora: {simbolo}{tarifa_hora:.2f}"
      )
      st.info(
          f"Necesitas ingresar un total de {simbolo}{ingreso_necesario:.2f} al"
          " mes para cubrir tus metas, impuestos y gastos."
      )

  elif herramienta_fin == "Calculador de rentabilidad para E-commerce":
    st.subheader("🛒 Rentabilidad para E-commerce")
    col1, col2 = st.columns(2)
    with col1:
      costo_prod = st.number_input(
          f"Costo de adquisición del producto ({simbolo})",
          min_value=0.0,
          value=10.0 * tasa_cambio,
      )
      precio_venta = st.number_input(
          f"Precio de venta al público ({simbolo})",
          min_value=0.0,
          value=35.0 * tasa_cambio,
      )
      envio = st.number_input(
          f"Costo de envío/logística ({simbolo})",
          min_value=0.0,
          value=5.0 * tasa_cambio,
      )
    with col2:
      cac = st.number_input(
          f"Costo por Adquisición (CAC / Publicidad por unidad) ({simbolo})",
          min_value=0.0,
          value=8.0 * tasa_cambio,
      )
      comision_pasarela_pct = (
          st.number_input("Comisión de pasarela de pago (%)", value=3.5) / 100
      )

    if st.button("Calcular Rentabilidad"):
      comision_monto = precio_venta * comision_pasarela_pct
      costos_totales = costo_prod + envio + cac + comision_monto
      margen_neto = precio_venta - costos_totales
      roi_pct = (margen_neto / costos_totales) * 100 if costos_totales > 0 else 0

      st.success(
          f"### Margen Neto Real por Unidad: {simbolo}{margen_neto:.2f}"
      )
      st.metric(label="ROI de la venta", value=f"{roi_pct:.2f}%")

  elif herramienta_fin == "Calculador de Libertad Financiera (FIRE)":
    st.subheader("🔥 Calculador de Libertad Financiera (Movimiento FIRE)")
    col1, col2 = st.columns(2)
    with col1:
      gasto_anual = st.number_input(
          f"Gastos anuales estimados en el retiro ({simbolo})",
          min_value=0.0,
          value=24000.0 * tasa_cambio,
      )
      tasa_retiro = (
          st.number_input(
              "Tasa de retiro seguro (%) - Regla del 4%", value=4.0
          )
          / 100
      )
    with col2:
      inversion_actual = st.number_input(
          f"Patrimonio invertido actual ({simbolo})",
          min_value=0.0,
          value=5000.0 * tasa_cambio,
      )
      rendimiento_anual = (
          st.number_input(
              "Rendimiento anual estimado de inversión (%)", value=7.0
          )
          / 100
      )

    if st.button("Calcular Meta FIRE"):
      meta_fire = gasto_anual / tasa_retiro if tasa_retiro > 0 else 0
      faltante = max(0.0, meta_fire - inversion_actual)
      st.success(
          f"### Tu número FIRE (Capital total necesario):"
          f" {simbolo}{meta_fire:,.2f}"
      )
      st.write(
          f"Te faltan **{simbolo}{faltante:,.2f}** para alcanzar tu"
          " independencia."
      )

# ==========================================
# SECTOR 2: PRODUCTIVIDAD Y GESTIÓN
# ==========================================
elif sector == "🏢 Productividad y Gestión":
  st.header("🏢 Productividad y Gestión")
  herramienta_prod = st.selectbox(
      "Selecciona la herramienta:",
      [
          "Calculador de costos de proyectos",
          "Calculador de ROI de herramientas de software",
      ],
  )

  if herramienta_prod == "Calculador de costos de proyectos":
    st.subheader("📋 Estimación de Costos de Proyectos")
    col1, col2 = st.columns(2)
    with col1:
      horas_est = st.number_input(
          "Horas estimadas de trabajo", min_value=1.0, value=50.0
      )
      tarifa_hora_recurso = st.number_input(
          f"Costo promedio por hora del equipo ({simbolo})",
          min_value=0.0,
          value=25.0 * tasa_cambio,
      )
    with col2:
      otros_costos = st.number_input(
          f"Costos adicionales (recursos/licencias puntuales) ({simbolo})",
          min_value=0.0,
          value=100.0 * tasa_cambio,
      )
      margen_desviacion = (
          st.number_input(
              "Margen de contingencia por imprevistos (%)", value=15.0
          )
          / 100
      )

    if st.button("Calcular Proyecto"):
      costo_base = (horas_est * tarifa_hora_recurso) + otros_costos
      costo_con_contingencia = costo_base * (1 + margen_desviacion)
      st.success(
          f"### Costo Total Estimado del Proyecto:"
          f" {simbolo}{costo_con_contingencia:.2f}"
      )
      st.write(
          "Incluye un buffer de contingencia de"
          f" {simbolo}{costo_base * margen_desviacion:.2f}."
      )

  elif herramienta_prod == "Calculador de ROI de herramientas de software":
    st.subheader("💻 ROI de Herramientas de Software")
    col1, col2 = st.columns(2)
    with col1:
      costo_software = st.number_input(
          f"Costo mensual de la suscripción del software ({simbolo})",
          min_value=0.0,
          value=50.0 * tasa_cambio,
      )
      horas_ahorradas = st.number_input(
          "Horas ahorradas al mes en total", min_value=0.0, value=12.0
      )
    with col2:
      valor_hora_empleado = st.number_input(
          f"Costo por hora del empleado que ahorra tiempo ({simbolo})",
          min_value=0.0,
          value=20.0 * tasa_cambio,
      )

    if st.button("Calcular ROI de Software"):
      ahorro_monetario = horas_ahorradas * valor_hora_empleado
      beneficio_neto = ahorro_monetario - costo_software
      roi = (
          (beneficio_neto / costo_software) * 100
          if costo_software > 0
          else 0
      )

      st.success(
          f"### Beneficio Neto Mensual: {simbolo}{beneficio_neto:.2f}"
      )
      st.metric(label="Retorno de Inversión (ROI)", value=f"{roi:.2f}%")

# ==========================================
# SECTOR 3: SALUD, FITNESS Y NUTRICIÓN
# ==========================================
elif sector == "🏋️ Salud, Fitness y Nutrición":
  st.header("🏋️ Salud, Fitness y Nutrición")
  herramienta_salud = st.selectbox(
      "Selecciona la herramienta:",
      [
          "Calculador de Macronutrientes y Calorías Avanzado",
          "Calculador de progresión de cargas (Gimnasio)",
      ],
  )

  if herramienta_salud == (
      "Calculador de Macronutrientes y Calorías Avanzado"
  ):
    st.subheader("🥗 Macros y Calorías con Planificador Semanal")
    col1, col2 = st.columns(2)
    with col1:
      peso = st.number_input("Peso actual (kg)", min_value=30.0, value=70.0)
      altura = st.number_input("Altura (cm)", min_value=100.0, value=175.0)
      edad = st.number_input("Edad (años)", min_value=10, value=25)
    with col2:
      genero = st.selectbox("Género", ["Hombre", "Mujer"])
      objetivo = st.selectbox(
          "Objetivo",
          ["Déficit (Definición)", "Mantenimiento", "Superávit (Volumen)"],
      )
      actividad = st.selectbox(
          "Nivel de Actividad",
          ["Sedentario", "Moderado (3-4 días/sem)", "Muy activo (5+ días/sem)"],
      )

    if st.button("Generar Plan Nutricional"):
      if genero == "Hombre":
        tmb = 88.36 + (13.4 * peso) + (4.8 * altura) - (5.7 * edad)
      else:
        tmb = 447.6 + (9.2 * peso) + (3.1 * altura) - (4.3 * edad)

      factores = {
          "Sedentario": 1.2,
          "Moderado (3-4 días/sem)": 1.55,
          "Muy activo (5+ días/sem)": 1.725,
      }
      tdee = tmb * factores[actividad]

      if "Déficit" in objetivo:
        calorias = tdee - 500
      elif "Superávit" in objetivo:
        calorias = tdee + 300
      else:
        calorias = tdee

      proteinas = peso * 2.0
      grasas = (calorias * 0.25) / 9
      carbohidratos = (calorias - (proteinas * 4 + grasas * 9)) / 4

      st.success(f"### Calorías diarias objetivo: {int(calorias)} kcal")
      st.markdown(
          f"- **Proteínas:** {int(proteinas)}g\n- **Grasas:**"
          f" {int(grasas)}g\n- **Carbohidratos:** {int(carbohidratos)}g"
      )

      st.write("---")
      st.subheader("📅 Distribución Semanal Sugerida (Macros)")
      dias = [
          "Lunes",
          "Martes",
          "Miércoles",
          "Jueves",
          "Viernes",
          "Sábado",
          "Domingo",
      ]
      tabla_nutri = pd.DataFrame({
          "Día": dias,
          "Calorías": [int(calorias)] * 7,
          "Proteína (g)": [int(proteinas)] * 7,
          "Grasas (g)": [int(grasas)] * 7,
          "Carbs (g)": [int(carbohidratos)] * 7,
      })
      st.dataframe(tabla_nutri, use_container_width=True)

  elif herramienta_salud == "Calculador de progresión de cargas (Gimnasio)":
    st.subheader("🏋️‍♂️ Calculador de 1RM y Porcentajes de Fuerza")
    peso_levantado = st.number_input(
        "Peso levantado en el ejercicio (kg)", min_value=0.0, value=80.0
    )
    repeticiones = st.number_input(
        "Repeticiones realizadas con ese peso", min_value=1, max_value=15, value=5
    )

    if st.button("Calcular Porcentajes de Carga"):
      one_rm = peso_levantado * (1 + (repeticiones / 30.0))
      st.success(f"### Tu 1RM Estimado: {one_rm:.1f} kg")

      st.write("### Tabla de Porcentajes de Entrenamiento:")
      porcentajes = [90, 85, 80, 75, 70, 65, 60]
      datos_cargas = []
      for p in porcentajes:
        carga = one_rm * (p / 100)
        datos_cargas.append(
            {"Porcentaje": f"{p}%", "Peso Sugerido": f"{carga:.1f} kg"}
        )

      st.table(pd.DataFrame(datos_cargas))

# ==========================================
# SECTOR 4: CREADORES DE CONTENIDO Y MARKETING
# ==========================================
elif sector == "📱 Creadores y Marketing":
  st.header("📱 Creadores de Contenido y Marketing")
  herramienta_mk = st.selectbox(
      "Selecciona la herramienta:",
      [
          "Calculador de Presupuesto para Campañas de Anuncios",
          "Calculador de precios de Patrocinios",
      ],
  )

  if herramienta_mk == "Calculador de Presupuesto para Campañas de Anuncios":
    st.subheader("📢 Estimación de Campañas de Anuncios (Media Buying)")
    col1, col2 = st.columns(2)
    with col1:
      presupuesto_total = st.number_input(
          f"Presupuesto Total de Campaña ({simbolo})",
          min_value=0.0,
          value=500.0 * tasa_cambio,
      )
      cpc_estimado = st.number_input(
          f"Costo por Clic (CPC) estimado ({simbolo})",
          min_value=0.01,
          value=0.50 * tasa_cambio,
      )
    with col2:
      tasa_conv = (
          st.number_input("Tasa de Conversión esperada (%)", value=2.0) / 100
      )

    if st.button("Calcular Proyección"):
      clics = presupuesto_total / cpc_estimado if cpc_estimado > 0 else 0
      conversiones = clics * tasa_conv
      cpa = presupuesto_total / conversiones if conversiones > 0 else 0

      st.success(f"### Clics estimados: {int(clics):,}")
      col_a, col_b = st.columns(2)
      col_a.metric(
          label="Conversiones Estimadas", value=f"{int(conversiones):,}"
      )
      col_b.metric(
          label="Costo por Adquisición (CPA)", value=f"{simbolo}{cpa:.2f}"
      )

  elif herramienta_mk == "Calculador de precios de Patrocinios":
    st.subheader("🤝 Calculador de Precios para Patrocinios (Influencers)")
    col1, col2 = st.columns(2)
    with col1:
      vistas_promedio = st.number_input(
          "Visualizaciones promedio por video/post", min_value=0, value=10000
      )
      engagement_rate = st.number_input(
          "Tasa de Engagement (%)", min_value=0.0, value=4.5
      )
    with col2:
      nicho = st.selectbox(
          "Nicho de mercado",
          [
              "Finanzas / Tech (Alto valor)",
              "Lifestyle / Moda",
              "Gaming / Entretenimiento",
          ],
      )

    if st.button("Calcular Tarifa Sugerida"):
      multiplicador = {
          "Finanzas / Tech (Alto valor)": 0.05 * tasa_cambio,
          "Lifestyle / Moda": 0.03 * tasa_cambio,
          "Gaming / Entretenimiento": 0.02 * tasa_cambio,
      }[nicho]

      tarifa_base = vistas_promedio * multiplicador
      ajuste_engagement = 1 + (engagement_rate / 10)
      tarifa_final = tarifa_base * ajuste_engagement

      st.success(
          f"### Tarifa recomendada por mención/post:"
          f" {simbolo}{tarifa_final:,.2f}"
      )
      st.info(
          "Este valor pondera tu audiencia base y el valor del sector comercial"
          " al que te diriges."
      )

# ==========================================
# SECTOR 5: INMUEBLES Y BIENES RAÍCES (NUEVO)
# ==========================================
elif sector == "🏡 Inmuebles y Bienes Raíces":
  st.header("🏡 Inmuebles y Bienes Raíces")
  herramienta_inmo = st.selectbox(
      "Selecciona la herramienta:",
      [
          "Calculador de Rentabilidad de Inversión Inmobiliaria (ROI / Cap Rate)",
          "Calculador de Capacidad de Crédito Hipotecario",
      ],
  )

  if (
      herramienta_inmo
      == "Calculador de Rentabilidad de Inversión Inmobiliaria (ROI / Cap Rate)"
  ):
    st.subheader("🏢 Rentabilidad Inmobiliaria (Cap Rate & Cash-on-Cash)")
    col1, col2 = st.columns(2)
    with col1:
      precio_propiedad = st.number_input(
          f"Precio de compra del inmueble ({simbolo})",
          min_value=0.0,
          value=150000.0 * tasa_cambio,
      )
      renta_mensual = st.number_input(
          f"Ingreso por renta mensual esperada ({simbolo})",
          min_value=0.0,
          value=1200.0 * tasa_cambio,
      )
    with col2:
      gastos_anuales_mantenimiento = st.number_input(
          f"Gastos anuales (predial, mantenimiento, seguro) ({simbolo})",
          min_value=0.0,
          value=2000.0 * tasa_cambio,
      )
      porcentaje_vacancia = (
          st.number_input(
              "Estimación de vacancia / meses sin alquilar (%)", value=5.0
          )
          / 100
      )

    if st.button("Calcular Rentabilidad Inmobiliaria"):
      ingreso_bruto_anual = renta_mensual * 12
      ingreso_efectivo_anual = ingreso_bruto_anual * (
          1 - porcentaje_vacancia
      )
      ingreso_neto_operativo = ingreso_efectivo_anual - gastos_anuales_mantenimiento
      cap_rate = (
          (ingreso_neto_operativo / precio_propiedad) * 100
          if precio_propiedad > 0
          else 0
      )

      st.success(
          f"### Ingreso Neto Operativo Anual (NOI):"
          f" {simbolo}{ingreso_neto_operativo:,.2f}"
      )
      st.metric(label="Tasa de Capitalización (Cap Rate)", value=f"{cap_rate:.2f}%")

  elif herramienta_inmo == "Calculador de Capacidad de Crédito Hipotecario":
    st.subheader("🏦 Simulación de Crédito Hipotecario")
    col1, col2 = st.columns(2)
    with col1:
      ingreso_mensual_hogar = st.number_input(
          f"Ingreso neto mensual del hogar ({simbolo})",
          min_value=0.0,
          value=3000.0 * tasa_cambio,
      )
      tasa_interes_anual = (
          st.number_input("Tasa de interés anual del crédito (%)", value=10.5)
          / 100
      )
    with col2:
      plazo_anios = st.selectbox(
          "Plazo del crédito (Años)", [10, 15, 20, 25, 30], index=2
      )
      capacidad_pago_pct = (
          st.number_input(
              "Porcentaje máximo de ingresos destinado a la mensualidad (%)",
              value=30.0,
          )
          / 100
      )

    if st.button("Calcular Crédito Máximo"):
      pago_mensual_max = ingreso_mensual_hogar * capacidad_pago_pct
      n_meses = plazo_anios * 12
      i_mes = tasa_interes_anual / 12

      # Fórmula de valor presente para calcular el monto del préstamo
      if i_mes > 0:
        monto_prestamo = pago_mensual_max * (
            (1 - (1 + i_mes) ** -n_meses) / i_mes
        )
      else:
        monto_prestamo = pago_mensual_max * n_meses

      st.success(
          f"### Monto máximo de crédito estimado:"
          f" {simbolo}{monto_prestamo:,.2f}"
      )
      st.info(
          f"Tu mensualidad estimada sería de {simbolo}{pago_mensual_max:,.2f}"
          f" durante {plazo_anios} años."
      )

# ==========================================
# SECTOR 6: EDUCACIÓN Y CURSOS ONLINE (NUEVO)
# ==========================================
elif sector == "🎓 Educación y Cursos Online":
  st.header("🎓 Educación y Cursos Online")
  herramienta_edu = st.selectbox(
      "Selecciona la herramienta:",
      [
          "Calculador de Rentabilidad para Lanzamientos de Cursos",
          "Calculador de Tiempo de Estudio y Retención de Alumnos",
      ],
  )

  if herramienta_edu == "Calculador de Rentabilidad para Lanzamientos de Cursos":
    st.subheader("🚀 Proyección Financiera de Lanzamiento de Info-productos")
    col1, col2 = st.columns(2)
    with col1:
      tamano_audiencia = st.number_input(
          "Tamaño de tu lista de correo / seguidores interesados",
          min_value=0,
          value=5000,
      )
      tasa_conversion_venta = (
          st.number_input(
              "Tasa de conversión de venta estimada (%)", value=1.5
          )
          / 100
      )
    with col2:
      precio_curso = st.number_input(
          f"Precio de venta del curso ({simbolo})",
          min_value=0.0,
          value=197.0 * tasa_cambio,
      )
      inversion_ads_lanzamiento = st.number_input(
          f"Inversión en publicidad para el lanzamiento ({simbolo})",
          min_value=0.0,
          value=1000.0 * tasa_cambio,
      )

    if st.button("Calcular Proyección de Lanzamiento"):
      ventas_estimadas = int(tamano_audiencia * tasa_conversion_venta)
      ingresos_totales = ventas_estimadas * precio_curso
      beneficio_neto = ingresos_totales - inversion_ads_lanzamiento
      roas = (
          ingresos_totales / inversion_ads_lanzamiento
          if inversion_ads_lanzamiento > 0
          else 0
      )

      st.success(f"### Ventas estimadas: {ventas_estimadas} alumnos")
      col_a, col_b = st.columns(2)
      col_a.metric(
          label="Ingresos Totales", value=f"{simbolo}{ingresos_totales:,.2f}"
      )
      col_b.metric(label="ROAS (Retorno de Anuncios)", value=f"{roas:.2f}x")

  elif herramienta_edu == "Calculador de Tiempo de Estudio y Retención de Alumnos":
    st.subheader("📚 Planificador de Contenido y Tiempos de Estudio")
    col1, col2 = st.columns(2)
    with col1:
      duracion_video_total_horas = st.number_input(
          "Duración total del contenido en video (horas)",
          min_value=0.1,
          value=10.0,
      )
      factor_practica = st.number_input(
          "Multiplicador de práctica/ejercicios (ej. 2x el tiempo de video)",
          min_value=1.0,
          value=2.0,
      )
    with col2:
      semanas_programa = st.number_input(
          "Duración del programa en semanas", min_value=1, value=6
      )

    if st.button("Calcular Carga Semanal"):
      horas_totales_estimadas = duracion_video_total_horas * factor_practica
      horas_por_semana = horas_totales_estimadas / semanas_programa

      st.success(
          f"### Dedicación semanal requerida: {horas_por_semana:.1f} horas/semana"
      )
      st.info(
          "Esto equivale a aproximadamente"
          f" **{horas_por_semana / 5:.1f} horas al día** si el alumno estudia"
          " de lunes a viernes."
      )
