"""Profundidad de las fichas de opciones y modos de selección."""

from __future__ import annotations

from typing import Any

_MODE_WHY = (
    "En automático TS propone valores coherentes con el proceso y los justifica; en manual "
    "respeta lo que exija una especificación de cliente. Mezclar ambos permite fijar lo que "
    "está decidido y dejar que TS resuelva el resto.",
    "In automatic TS proposes values consistent with the process and justifies them; in "
    "manual it respects what a client specification requires. Mixing both lets you fix what "
    "is decided and let TS solve the rest.")

DEEP: dict[str, dict[str, Any]] = {
    "opt.damping": {
        "essence": (
            "El amortiguamiento ζ es la fracción de energía de vibración que se pierde en cada "
            "ciclo: por fricción interna del metal (los granos se deslizan levemente), por "
            "microdeslizamientos en el apoyo y por el fluido. Un ζ de 0,0005 significa que la "
            "vibración libre tarda unos 300 ciclos en caer a la mitad.",
            "Damping ζ is the fraction of vibration energy lost each cycle: by internal metal "
            "friction (grains slip slightly), micro-slip at the support and the fluid. A ζ of "
            "0.0005 means free vibration takes about 300 cycles to halve."),
        "why": (
            "Entra en el Scruton y decide qué límite de frecuencia se aplica. Un valor "
            "optimista puede aprobar una vaina peligrosa.",
            "It enters Scruton and decides which frequency limit applies. An optimistic value "
            "can pass a dangerous well."),
        "worked": ("Con ζ = 0,0005 → N_Sc = 0,43; con ζ = 0,003 → N_Sc = 2,6 (cambia el límite).",
                   "With ζ = 0.0005 → N_Sc = 0.43; with ζ = 0.003 → N_Sc = 2.6 (changes the "
                   "limit)."),
        "mistakes": ("- Subirlo sin ensayo para que cumpla.",
                     "- Raising it without testing so it passes."),
    },
    "opt.strouhal": {
        "essence": (
            "Elige entre la correlación de la norma (N_S en función de Re) o un valor fijo de "
            "0,22, que usan algunas planillas antiguas.",
            "Chooses between the standard's correlation (N_S as a function of Re) or a fixed "
            "0.22, used by some older spreadsheets."),
        "why": ("La correlación es la de la norma; el valor fijo sirve para comparar.",
                "The correlation is the standard's; the fixed value is for comparison."),
        "worked": ("Re = 5·10⁵: correlación puede dar un N_S distinto de 0,22.",
                   "Re = 5·10⁵: the correlation may give an N_S different from 0.22."),
        "mistakes": ("- Usar el fijo para un cálculo de emisión.",
                     "- Using the fixed value for an issued calculation."),
    },
    "opt.fe": {
        "essence": (
            "Un ambiente corrosivo reduce la resistencia a la fatiga: la corrosión crea "
            "picaduras que actúan como entallas y acelera el crecimiento de fisuras. F_E "
            "descuenta ese efecto del límite de fatiga.",
            "A corrosive environment reduces fatigue strength: corrosion creates pits acting "
            "as notches and speeds crack growth. F_E discounts that effect from the fatigue "
            "limit."),
        "why": ("Sin descuento, la vaina puede fatigarse antes de lo previsto.",
                "Without the discount, the well may fatigue sooner than expected."),
        "worked": ("F_E = 0,5 en agua de mar: el límite de fatiga efectivo se reduce a la "
                   "mitad.",
                   "F_E = 0.5 in seawater: the effective fatigue limit halves."),
        "mistakes": ("- Dejar 1 en servicios ácidos.", "- Leaving 1 in acidic services."),
    },
    "opt.metal_state": {
        "essence": (
            "Una raíz soldada tiene defectos microscópicos, tensiones residuales y cambios de "
            "microestructura que reducen la resistencia a la fatiga frente a una raíz "
            "mecanizada de barra.",
            "A welded root has microscopic defects, residual stresses and microstructural "
            "changes that reduce fatigue strength compared with a machined bar-stock root."),
        "why": ("Puede cambiar el límite de fatiga a más del doble.",
                "It can change the fatigue limit by more than a factor of two."),
        "worked": ("316 mecanizado ≈ 48 MPa; soldado ≈ 21 MPa (valores típicos).",
                   "Machined 316 ≈ 48 MPa; welded ≈ 21 MPa (typical values)."),
        "mistakes": ("- Elegir «no soldado» para una vaina con brida soldada.",
                     "- Choosing «not welded» for a well with a welded flange."),
    },
    "opt.amber": {
        "essence": (
            "Define desde qué cercanía al límite el estado pasa a amarillo. Es un margen de "
            "ingeniería para no aceptar diseños al filo.",
            "It defines how close to the limit the status turns amber. It is an engineering "
            "margin to avoid accepting knife-edge designs."),
        "why": ("Los datos de proceso tienen incertidumbre; el margen la absorbe.",
                "Process data have uncertainty; the margin absorbs it."),
        "worked": ("Margen 10 %: r = 0,37 con límite 0,4 → amarillo.",
                   "10 % margin: r = 0.37 with limit 0.4 → amber."),
        "mistakes": ("- Ponerlo en 0.", "- Setting it to 0."),
    },
    "opt.flange_manual": {
        "essence": ("Presión admisible de brida cargada a mano, por ejemplo de un catálogo de "
                    "proveedor o una brida no normalizada.",
                    "Flange allowable pressure entered by hand, for example from a supplier "
                    "catalogue or a non-standard flange."),
        "why": ("Reemplaza la tabla B16.5: debe tener respaldo documental.",
                "It replaces the B16.5 table: it must be documented."),
        "worked": ("Brida especial de proveedor: 120 bar a 200 °C.",
                   "Special supplier flange: 120 bar at 200 °C."),
        "mistakes": ("- Cargar la presión de prueba como de diseño.",
                     "- Entering test pressure as design."),
    },
    "opt.inline": {
        "essence": ("Permite que la vaina opere por encima de la resonancia en línea si solo "
                    "la atraviesa en transitorios.",
                    "Allows the well to run above in-line resonance if it only crosses it in "
                    "transients."),
        "why": ("Habilita diseños más largos en gases, con verificación del paso.",
                "It enables longer designs in gases, with a passage check."),
        "worked": ("Compresor que arranca en 30 s: paso breve, aceptable.",
                   "Compressor starting in 30 s: brief passage, acceptable."),
        "mistakes": ("- Activarlo en líquidos.", "- Enabling it for liquids."),
    },
    "opt.corrosion_cases": {
        "essence": ("Evalúa también la vaina con el sobreespesor consumido (fin de vida).",
                    "Also evaluates the well with the allowance consumed (end of life)."),
        "why": ("Una vaina más delgada vibra a menos frecuencia y es más débil.",
                "A thinner well vibrates at lower frequency and is weaker."),
        "worked": ("Nueva r = 0,36; corroída r = 0,41 → manda la corroída.",
                   "New r = 0.36; corroded r = 0.41 → corroded governs."),
        "mistakes": ("- Desactivarlo con sobreespesor cargado.",
                     "- Turning it off with an allowance entered."),
    },
    "opt.supplier": {
        "essence": ("Calcula sin masa añadida del fluido, como los ratings genéricos de "
                    "proveedores.",
                    "Calculates without fluid added mass, like generic supplier ratings."),
        "why": ("Sirve para comparar con catálogos; no para el diseño final en líquidos.",
                "Useful to compare with catalogues; not for final design in liquids."),
        "worked": ("En agua, f_n sin masa añadida puede ser 3 a 5 % mayor.",
                   "In water, f_n without added mass can be 3 to 5 % higher."),
        "mistakes": ("- Emitir el cálculo con esta opción.",
                     "- Issuing the calculation with this option."),
    },
    "f.mode_material": {
        "essence": ("Decide si el material, el recubrimiento y el sobreespesor los elegís vos o "
                    "TS, a partir de la matriz de compatibilidad, la temperatura, el H₂S, los "
                    "cloruros y la erosión.",
                    "Decides whether material, coating and allowance are chosen by you or by "
                    "TS, from the compatibility matrix, temperature, H₂S, chlorides and "
                    "erosion."),
        "why": _MODE_WHY,
        "worked": ("Agua a 120 °C sin agentes: TS elige 316/316L, sin recubrimiento.",
                   "Water at 120 °C with no agents: TS picks 316/316L, no coating."),
        "mistakes": ("- Dejar automático cuando el cliente exige otro material.",
                     "- Leaving automatic when the client requires another material."),
    },
    "f.mode_connection": {
        "essence": ("Decide si tipo, tamaño, clase y cara los elegís vos o TS, a partir del "
                    "fluido, la presión y la temperatura de diseño.",
                    "Decides whether type, size, class and face are chosen by you or by TS, "
                    "from fluid, design pressure and temperature."),
        "why": _MODE_WHY,
        "worked": ("Gas a 60 bar y 300 °C: TS elige bridada clase 600 RF.",
                   "Gas at 60 bar and 300 °C: TS picks flanged class 600 RF."),
        "mistakes": ("- No revisar la clase frente a la especificación de cañería.",
                     "- Not checking the class against the piping spec."),
    },
    "f.mode_geometry": {
        "essence": ("Decide si el perfil y las cotas los elegís vos o TS, que prueba diseños "
                    "típicos y largos normalizados hasta que todos los casos cumplen.",
                    "Decides whether profile and dimensions are chosen by you or by TS, which "
                    "tries typical designs and standard lengths until all cases pass."),
        "why": _MODE_WHY,
        "worked": ("TS prueba cónico 10½\", luego 7½\", hasta encontrar uno que cumple.",
                   "TS tries tapered 10½\", then 7½\", until one passes."),
        "mistakes": ("- Fijar U a mano y dejar automático el resto esperando que cumpla.",
                     "- Fixing U by hand and leaving the rest automatic expecting a pass."),
    },
    "f.mode_sensor": {
        "essence": ("Decide si el diámetro de vaina del sensor lo elegís vos o TS según el "
                    "agujero.",
                    "Decides whether the sensor sheath diameter is chosen by you or by TS from "
                    "the bore."),
        "why": _MODE_WHY,
        "worked": ("Agujero 6,6 mm → vaina de 6,35 mm (¼\").",
                   "6.6 mm bore → 6.35 mm (¼\") sheath."),
        "mistakes": ("- Comprar el sensor antes de cerrar el agujero.",
                     "- Buying the sensor before fixing the bore."),
    },
}
