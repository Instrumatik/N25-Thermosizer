# Licencias y distribución (uso interno de InstruMatik)

## Cómo funciona

- Cada licencia es un texto `TWS1.<datos>.<firma>`. Los datos (titular, correo,
  edición, fecha de emisión, vencimiento opcional y huella de equipo opcional) van
  firmados con **Ed25519**.
- El programa contiene solo la **clave pública** (`licensing/__init__.py`,
  `PUBLIC_KEY_B64`) y verifica la firma sin Internet. Cambiar un solo carácter de la
  licencia invalida la firma.
- Sin licencia válida el programa funciona completo y los reportes llevan marca de agua
  «VERSIÓN DE EVALUACIÓN». Con licencia, el pie dice «Licenciado a …».
- La licencia se guarda en `%APPDATA%\InstruMatik\ThermoWellSizer\licencia.txt`.

## La clave privada

La clave privada (`thermowell_sizer_private_key.pem`) es lo único que permite emitir
licencias. **Nunca** se sube al repositorio (`.gitignore` excluye `*.pem` y
`licencia*.txt`) ni se distribuye con el programa. Guárdela en un lugar seguro con copia
de respaldo: si se pierde, no se pueden emitir más licencias para las versiones ya
instaladas; si se filtra, cualquiera puede emitirlas. En ambos casos hay que generar un
par nuevo, copiar la clave pública nueva en `PUBLIC_KEY_B64` y publicar una versión
nueva (las licencias anteriores dejan de valer en esa versión).

## Emitir una licencia

```bash
pip install -e ".[licensing]"
# Licencia para cualquier equipo, sin vencimiento:
python tools/keygen.py emitir --clave thermowell_sizer_private_key.pem \
    --titular "Empresa S.A." --correo compras@empresa.com --edicion professional
# Atada a un equipo (el cliente copia la huella desde Ayuda › Licencia) y con vencimiento:
python tools/keygen.py emitir --clave thermowell_sizer_private_key.pem \
    --titular "Empresa S.A." --vence 2027-12-31 --equipo 1A2B3C4D5E6F7A8B
```

El comando imprime el código; envíelo al cliente para que lo pegue en **Ayuda ›
Licencia…**. Ediciones disponibles: `professional` y `enterprise` (hoy ambas habilitan
lo mismo; quedan para diferenciar precios en el futuro).

## Generar el instalador

El flujo **Release Windows** (`.github/workflows/release.yml`) corre en GitHub Actions al
crear una etiqueta `v*` o a mano (*Actions › Release Windows › Run workflow*; si se completa
«etiqueta», p. ej. `v1.5.0`, crea esa versión y publica los archivos en ella):

1. Instala dependencias y corre las pruebas.
2. Genera el ejecutable con PyInstaller (`packaging/thermowell_sizer.spec`).
3. Lo ejecuta en modo de prueba (`TWS_SMOKE_TEST=1`: calcula un tag y genera un PDF).
4. Arma el instalador con Inno Setup (`packaging/installer.iss`).
5. Genera `GeneradorLicencias.exe` (este emisor, como ejecutable de consola) y arma
   `ThermoWellSizer-<versión>-paquete.zip` con el instalador, el generador, el LEEME y la
   documentación. El paquete **no** lleva la clave privada ni licencias.
6. Publica el instalador y el paquete como artefacto y, si es una etiqueta, en la página
   de la versión.

Para hacerlo en un equipo Windows propio: `pip install ".[gui,reports]" pyinstaller`,
`pyinstaller packaging/thermowell_sizer.spec --noconfirm` y luego
`iscc /DAppVersion=1.5.0 packaging\installer.iss`.

## Antes de vender a terceros

- Pase el repositorio a privado.
- Considere compilar con **Nuitka** en lugar de PyInstaller para dificultar la
  ingeniería inversa (el instalador de Inno Setup sirve igual).
- Firme el ejecutable con un certificado de firma de código para evitar el aviso de
  Windows SmartScreen.
- Revise la licencia de uso de la norma y la de los datos de materiales (ver
  `arquitectura.md`, riesgos).
