"""Implementación de ASME PTC 19.3 TW-2016.

Un módulo por subsección de la norma, todas funciones puras en SI:

=====================  ==========================================================
Módulo                 Contenido (subsección de la norma)
=====================  ==========================================================
``flow``               velocidad, Reynolds, Strouhal y presiones dinámicas (6-3, 6-4, 7-3)
``natural_frequency``  fn ideal, Hf, Ha,f, Ha,s, perfil escalonado (6-5)
``compliance``         factor de flexibilidad del soporte Hc (6-6)
``frequency_limits``   Scruton, velocidad de resonancia en línea y magnificación (6-8, 6-9)
``stresses``           esfuerzos estáticos y dinámicos en raíz y escalón, Kt (6-10, 6-11)
``fatigue``            límites de fatiga clase A/B, factor ambiental (6-12)
``pressure``           presión externa admisible de punta, vástago y brida (6-13)
``verify``             orquestador: corre todo, registra la traza y arma los semáforos
=====================  ==========================================================
"""
