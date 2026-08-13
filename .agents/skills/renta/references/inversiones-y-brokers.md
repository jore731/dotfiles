# Tratamiento fiscal de inversiones y comisiones de brokers

Cómo tributan las inversiones (acciones, ETFs, fondos, CFDs, criptomonedas) y las comisiones de brokers como eToro, DEGIRO, Interactive Brokers, etc. en la Renta española (IRPF).

## Dónde tributan las inversiones

| Tipo de rendimiento | Base | Capítulo del manual |
|---------------------|------|---------------------|
| Dividendos, intereses, cupones | Ahorro — Rendimientos capital mobiliario | Cap. 5 |
| Ganancias/pérdidas por venta de acciones, ETFs, fondos, cripto | Ahorro — Ganancias patrimoniales | Cap. 11 |
| CFDs, futuros, opciones (especulativos) | Ahorro — Ganancias patrimoniales | Cap. 11 (Art. 37.1.m) |

## Ganancias y pérdidas patrimoniales por transmisión de valores

### Cálculo (Art. 34-36 Ley IRPF)

```
Ganancia = Valor de transmisión − Valor de adquisición
```

**Valor de adquisición** = Precio de compra + gastos inherentes (comisiones, tasas, impuestos) − amortizaciones

**Valor de transmisión** = Precio de venta − gastos inherentes (comisiones, tasas, impuestos)

> **Los intereses NO forman parte** del valor de adquisición ni de transmisión.

🔗 [Reglas generales de cálculo — valor de adquisición y transmisión](https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c11-ganancias-perdidas-patrimoniales/calculo-ganancias-perdidas-patrimoniales/reglas-generales-calculo.html)

### Valores cotizados (Art. 37.1.a)

Para acciones y ETFs cotizados:
- Valor de transmisión = Mayor entre precio de venta o valor de cotización a fecha de transmisión
- Aplica criterio FIFO (Art. 37.2)

🔗 [Transmisiones onerosas de valores cotizados](https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c11-ganancias-perdidas-patrimoniales/calculo-ganancias-perdidas-patrimoniales/ganancias-perdidas-patrimoniales-derivadas-transmisiones/transmisiones-elementos-patrimoniales/transmisiones-onerosas/valores-representativos-participacion-fondos/transmision-valores-admitidos-negociacion.html)

---

## Comisiones de brokers — Tratamiento fiscal

### Comisiones de compra/venta

**Son gastos inherentes a la adquisición/transmisión** (Art. 35) → reducen la ganancia patrimonial.

- Comisiones de compra → se suman al valor de adquisición
- Comisiones de venta → se restan del valor de transmisión
- El manual menciona explícitamente *"comisiones, Fedatario público, Registro, etc."*

### Spreads (eToro, brokers sin comisión explícita)

- El spread está embebido en el precio de ejecución
- Se refleja automáticamente en los valores de compra/venta
- No requiere ajuste manual — ya está incorporado en el precio

### Comisiones de custodia / administración y depósito

- **Solo deducibles de rendimientos del capital mobiliario** (dividendos), NO de ganancias patrimoniales
- Art. 26.1.a: *"gastos de administración y depósito de valores negociables"*
- **Excluidos expresamente:** gastos de gestión discrecional e individualizada de carteras

🔗 [Gastos deducibles: de administración y depósito](https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c05-rendimientos-capital-mobiliario/rendimientos-obtenidos-participacion-fondos-propios/dividendos-participaciones-beneficios-entidad/gastos-deducibles-administracion-deposito.html)

### Comisiones overnight (eToro CFDs)

- Se restan del resultado de la operación
- Forman parte del cálculo de la ganancia/pérdida patrimonial

### Comisiones de conversión de divisa

- Son un gasto inherente a la operación → reducen la ganancia patrimonial
- Se incluyen en el valor de adquisición o transmisión según corresponda

### Comisiones NO deducibles

| Comisión | ¿Deducible? | Motivo |
|----------|-------------|--------|
| Comisión de inactividad | ❌ No | No es inherente a ninguna operación |
| Comisión de retirada | ❌ No | No es inherente a la adquisición/transmisión de valores |
| Gestión de carteras (robo-advisors) | ❌ No | Excluido expresamente por Art. 26.1.a |

---

## Datos necesarios por broker (qué pedir y dónde obtenerlo)

> ⚠️ **Regla de oro:** el resumen/extracto anual de un broker **rara vez incluye todas las comisiones**. Pide siempre el documento de detalle por operación y, para CFDs, el estado de pérdidas y ganancias dedicado. Verifica que las comisiones declaradas no salgan a `0,00 €`.

### eToro

| Documento | Qué contiene | Cómo obtenerlo |
|-----------|--------------|----------------|
| **Account Statement (`.xlsx`)** | Detalle por operación: posiciones cerradas (acciones y CFD), comisiones, **overnight fees en columna propia**, dividendos, conversión de divisa | App/web → *Settings/Configuración → Account → Account Statement* → rango de fechas (1 ene–31 dic) → exportar a Excel |
| **Informe fiscal español (modelos 100 y 714)** `.pdf` | Resumen para residentes ES; útil como contraste, **no** para el detalle | App/web → *Documentos / Informes fiscales* |

**Claves eToro:**
- **Separa acciones reales de CFDs** — van en hojas/filas distintas del xlsx y tributan igual (Cap. 11) pero conviene desglosarlos para cuadrar.
- Las **overnight fees** aparecen en **columna propia** → réstalas del resultado del CFD (gasto inherente).
- El **spread** ya está embebido en el precio de ejecución (no se ajusta a mano).
- Usa el xlsx como fuente de cálculo; el PDF de modelos solo para verificar totales.

### Revolut

| Documento | Qué contiene | Cómo obtenerlo |
|-----------|--------------|----------------|
| **Extracto de cuenta anual (`.csv`/`.pdf`)** | Resumen por cuenta (corretaje, robo-advisor, CFD, ahorro, MMF), ventas, dividendos. **El resumen CFD reporta `Comisiones y otros cargos = 0,00 €`** | App → *cuenta → Extractos / Statements* → tipo "Consolidado/Anual" |
| **Profit and Loss Statement de la cuenta CFD (`.pdf`)** ⚠️ | **Las comisiones reales del CFD**: *Trading fees* + *Overnight fees* en la sección *Other income & fees*, además del *Gross PnL* | App → *Invest/Trading → cuenta CFD → Documentos → Profit and Loss Statement* (documento **distinto** del extracto) |

> 🚨 **Gotcha crítico Revolut CFD:** el extracto de cuenta da el resultado CFD como **neto** pero con `Comisiones = 0,00 €`; esa cifra es en realidad el **Gross PnL** (sin comisiones). Las comisiones (trading + overnight) están **únicamente** en el *Profit and Loss Statement* de la cuenta CFD. Si solo usas el CSV/extracto, **te dejas las comisiones sin deducir**.
>
> **Resultado fiscal CFD correcto = Gross PnL − (Trading fees + Overnight fees + ajustes).**

**Claves Revolut:**
- **Pide siempre el P&L Statement de la cuenta CFD** además del extracto; sin él faltan las comisiones.
- El extracto CFD da el neto como `(Σ valor cierre) − (Σ valor apertura)` sobre nocionales **agregados**; el P&L Statement da el *Gross PnL* sumando el resultado **por operación** a su tipo de cambio diario → pueden diferir en **decenas/centenas de €** por redondeo de divisa (no es error).
- El extracto mezcla **dos formatos numéricos**: español con sufijo (`1.356,11€`) e inglés con prefijo (`US$1,107.86`); identifícalo por la posición del símbolo de divisa.
- Distingue las cuentas: **corretaje** (acciones reales), **robo-advisor** (gestión de carteras → comisión NO deducible) y **CFD**.

### Checklist de verificación (cualquier broker)

- [ ] ¿La comisión total declarada es > 0? Si un resumen dice `0,00 €` en comisiones, **busca el documento de detalle**.
- [ ] ¿Has separado acciones/ETF (transmisión de valores) de CFD/derivados (Art. 37.1.m)?
- [ ] ¿Has restado overnight fees y trading fees del resultado de los CFD?
- [ ] ¿Las cifras del borrador (TaxDown u otro) **aparecen** en algún documento fuente? Si no cuadran con ninguna, revisa qué fichero usó el preparador.

---

## CFDs, futuros y opciones (Art. 37.1.m)

Las operaciones en mercados de futuros y opciones (incluidos CFDs) tributan como **ganancias patrimoniales** cuando no son operaciones de cobertura vinculadas a una actividad económica.

🔗 [Operaciones en mercados de futuros y opciones](https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/irpf-2025/c11-ganancias-perdidas-patrimoniales/calculo-ganancias-perdidas-patrimoniales/ganancias-perdidas-patrimoniales-derivadas-transmisiones/transmisiones-elementos-patrimoniales/transmisiones-onerosas/operaciones-realizadas-mercados-futuros-opciones.html)

---

## Reglas clave para inversiones

### Criterio FIFO (Art. 37.2)

Al vender parcialmente valores homogéneos, se consideran transmitidos los adquiridos en primer lugar.

### Regla antiaplicación (Art. 33.5.f)

No se computan como pérdida patrimonial las derivadas de transmisiones cuando se recompran valores homogéneos:
- **2 meses** antes o después → valores cotizados
- **1 año** antes o después → valores no cotizados

### Dividendos

- Tributan como rendimientos del capital mobiliario en la base del ahorro
- No existe mínimo exento (se eliminó en 2015)
- Retención en origen (extranjera) → deducción por doble imposición internacional (Art. 80)

### Criptomonedas

- Las permutas entre criptomonedas generan ganancia/pérdida patrimonial
- Se aplican las mismas reglas de cálculo que para valores
- Aplica FIFO y regla antiaplicación
- Obligación de informar sobre monedas virtuales (Modelo 721 si en el extranjero > 50.000 €)

---

## Resumen por tipo de comisión de broker

| Tipo de comisión | Dónde se aplica | Efecto fiscal |
|------------------|----------------|---------------|
| Compra/venta | Ganancias patrimoniales | ↑ valor adquisición / ↓ valor transmisión |
| Spread | Ganancias patrimoniales | Embebido en precio (automático) |
| Custodia/depósito | Rdtos. capital mobiliario | Gasto deducible de dividendos |
| Overnight (CFDs) | Ganancias patrimoniales | Se resta del resultado |
| Conversión divisa | Ganancias patrimoniales | Gasto inherente a la operación |
| Inactividad | — | No deducible |
| Retirada | — | No deducible |
| Gestión carteras | — | No deducible (excluido Art. 26.1.a) |
