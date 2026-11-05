"""Implementación de ASME PTC 19.3 TW-2016 (se completa en la Fase 2).

Un módulo por subsección de la norma, todas funciones puras en SI:

=====================  ==========================================================
Módulo                 Contenido (subsección de la norma)
=====================  ==========================================================
``flow``               velocidad, Reynolds sobre el diámetro de punta (7-3, 7-5)
``strouhal``           número de Strouhal y coeficientes de arrastre/sustentación (6-4)
``natural_frequency``  fn ideal, Hf, Ha,f, Ha,s, perfil escalonado (6-5)
``compliance``         factor de flexibilidad del soporte Hc (6-6)
``frequency_limits``   Scruton, resonancia en línea y transversal, paso por resonancia (6-8)
``magnification``      factores de magnificación FM y F'M (6-9)
``stresses``           esfuerzos estáticos y dinámicos en raíz y escalón, Kt (6-10, 6-11)
``fatigue``            límites de fatiga clase A/B, factor ambiental (6-12)
``pressure``           presión externa admisible de punta, vástago y brida (6-13)
``verify``             orquestador: corre todo, registra la traza y arma los semáforos
=====================  ==========================================================
"""
