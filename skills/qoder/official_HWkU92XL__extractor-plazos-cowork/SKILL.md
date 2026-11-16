---
name: extractor-plazos-cowork
description: "Extrae plazos de resoluciones judiciales, calcula fechas límite con días hábiles y genera alertas de vencimiento. Usar cuando se reciba cualquier resolución judicial, notificación, diligencia con plazo, o cuando el usuario diga 'calcula el plazo', 'cuándo vence', 'fecha límite', 'plazo para recurrir', 'plazo de contestación', 'nos han notificado', 'controla este plazo', o cualquier referencia a plazos procesales, fechas de vencimiento, o cómputo de días hábiles."
---

# Extractor de Plazos Procesales — ALY Abogados

## Contexto

Un plazo perdido es un caso perdido. Esta skill extrae plazos de resoluciones judiciales, calcula fechas límite considerando días hábiles, festivos y especialidades jurisdiccionales, y genera alertas priorizadas por urgencia. Es la skill con mayor impacto en la práctica diaria: se ejecuta con cada notificación judicial.

## Reglas de cómputo

### Días hábiles vs naturales

**Días hábiles (regla general en civil, contencioso, mercantil):**
- Se excluyen sábados, domingos y festivos
- Agosto es inhábil (art. 183 LOPJ) salvo excepciones

**Días naturales:**
- Plazos sustantivos (prescripción, caducidad)
- Plazos de jurisdicción penal
- Plazos de jurisdicción laboral (agosto es hábil)
- Plazos administrativos (Ley 39/2015): días hábiles, pero sábados son inhábiles

### Especialidades

**Agosto inhábil:** Civil, mercantil, contencioso-administrativo (jurisdicción).
**Agosto hábil:** Penal, laboral, procedimientos urgentes (medidas cautelares, violencia de género, internamiento), procedimientos de protección de derechos fundamentales.

**Inicio del cómputo:** Día siguiente a la notificación (art. 133 LEC).
**Vencimiento en sábado/festivo:** Se traslada al siguiente día hábil.

### Festivos aplicables (Las Palmas de Gran Canaria)

**Nacionales:** 1 y 6 enero, Viernes Santo, 1 mayo, 15 agosto, 12 octubre, 1 noviembre, 6 y 25 diciembre.
**Canarias:** 30 mayo (Día de Canarias), 2 febrero (Candelaria).
**Las Palmas de GC:** 24 junio (San Juan), 8 septiembre (Virgen del Pino). [Verificar calendario judicial anual vigente]

## Flujo de trabajo

### Paso 1 — Identificar la resolución

Del documento procesal, extraer:
- Tipo: auto, providencia, sentencia, decreto, diligencia de ordenación
- Órgano: Tribunal de Instancia, Audiencia Provincial, TS, TSJ
- Jurisdicción: civil, penal, laboral, contencioso-administrativo, mercantil
- Número de procedimiento
- Fecha de la resolución
- Fecha de notificación (si consta; si no, marcar [●])

### Paso 2 — Extraer plazos del texto

Identificar todos los plazos mencionados en la resolución:

**Plazos de recurso:**
- Reposición: 5 días hábiles (art. 452 LEC) / 5 días hábiles (art. 79 LJCA)
- Apelación: 20 días hábiles (art. 458 LEC)
- Casación: 20 días hábiles (art. 479 LEC) / 30 días hábiles (art. 89 LJCA)
- Queja: 10 días hábiles (art. 495 LEC)
- Suplicación (laboral): 5 días hábiles para anuncio

**Plazos de actuación:**
- Contestación a la demanda: 20 días hábiles (art. 404 LEC)
- Personación: 10 días hábiles (art. 16 LEC, publicación edictos)
- Subsanación: plazo fijado en la resolución (generalmente 10 días)
- Oposición a ejecución: 10 días hábiles (art. 556 LEC)
- Oposición a monitorio: 20 días hábiles (art. 815 LEC)

**Plazos sustantivos (días naturales):**
- Prescripción de acciones
- Caducidad de instancia
- Plazos contractuales

### Paso 3 — Calcular fecha límite

Para cada plazo detectado:

1. Determinar fecha de inicio: día siguiente a la notificación
2. Determinar tipo de días: hábiles o naturales según jurisdicción y tipo de plazo
3. Aplicar exclusiones: sábados y domingos (si hábiles), festivos, agosto (si inhábil)
4. Calcular fecha de vencimiento
5. Si vence en sábado/domingo/festivo: trasladar al siguiente hábil

**⚠️ NIVELES DE URGENCIA:**
- 🔴 **CRÍTICO:** Menos de 3 días hábiles desde hoy
- 🟡 **URGENTE:** Entre 3 y 10 días hábiles desde hoy
- 🟢 **NORMAL:** Más de 10 días hábiles desde hoy

### Paso 4 — Generar alerta

```
# ⚠️ ALERTA DE PLAZO PROCESAL

**Nivel:** 🔴 CRÍTICO / 🟡 URGENTE / 🟢 NORMAL

**Procedimiento:** [tipo] nº [número]
**Órgano:** [tribunal]
**Resolución:** [tipo] de fecha [fecha]
**Notificación:** [fecha] (si no consta: [●] — CALCULAR DESDE NOTIFICACIÓN EFECTIVA)

## Plazos detectados (ordenados por urgencia)

### Plazo 1: [tipo de plazo]
- **Días:** [X] días [hábiles/naturales]
- **Inicio cómputo:** [fecha]
- **Fecha límite:** **[fecha]**
- **Acción requerida:** [qué hay que hacer]
- **Jurisdicción:** [civil/penal/laboral/contencioso]
- **Agosto inhábil:** [Sí/No]

### Plazo 2: [si hay más plazos]
[...]

## Notas de cómputo
- [Cualquier especialidad aplicada: agosto, festivos locales, etc.]
- [Si la fecha de notificación no consta, indicar que el cálculo es provisional]
```

## Conexión con otras skills

- Si el plazo es para alegaciones EPI → encadenar con **alegaciones-epi-cowork** (Skill 4)
- Si requiere informe al cliente → encadenar con **informe-situacion-cliente-cowork** (Skill 2)
- Si el plazo es de recurso → verificar recurribilidad antes de actuar

## Reglas irrenunciables

- Si no consta fecha de notificación, marcar [●] e indicar que el cálculo es provisional.
- Siempre verificar si agosto es hábil o inhábil según jurisdicción.
- "Tribunal de Instancia" siempre, nunca "Juzgado".
- Ante duda sobre tipo de días (hábiles vs naturales), aplicar el cómputo más conservador (menos días).
- El calendario de festivos locales puede variar cada año: marcar [VERIFICAR CALENDARIO JUDICIAL VIGENTE] si hay duda.
