from pathlib import Path
import shutil
import fitz  #NECESITA PyMuPDF

carpeta_actual = Path(__file__).parent

archivo_entrada = carpeta_actual / "test.pdf"#NOMBRE DEL ARCHIVO PDF A CORTAR
carpeta_salida = carpeta_actual / "secciones"#NOMBRE DE CARPETA EN LA QUE SE GUARDAN LOS TROZOS

# Borra la carpeta anterior para evitar abrir archivos viejos
if carpeta_salida.exists():
    shutil.rmtree(carpeta_salida)

carpeta_salida.mkdir()

if not archivo_entrada.exists():
    print("No se encontró el archivo:")
    print(archivo_entrada)
    exit()

rangos = [       #LOS RANGOS DE PAGINAS VAN A VARIAR DEPENDIENDO, MARCAR LAS REQUERIDAS
    (18, 32),
    (32, 71),
    (71, 89),
    (89, 115),
    (115, 179)
]

pdf_original = fitz.open(archivo_entrada)

print(f"PDF original: {pdf_original.page_count} páginas")

for numero_seccion, (inicio, fin) in enumerate(rangos, start=1):
    nuevo_pdf = fitz.open()  # IMPORTANTE: debe estar dentro del for

    nuevo_pdf.insert_pdf(
        pdf_original,
        from_page=inicio - 1,
        to_page=fin - 1
    )

    archivo_salida = carpeta_salida / f"seccion_{numero_seccion}_paginas_{inicio}-{fin}.pdf"

    nuevo_pdf.save(
        archivo_salida,
        garbage=4,
        deflate=True
    )

    print(
        f"Creado: {archivo_salida.name} | "
        f"Páginas esperadas: {fin - inicio + 1} | "
        f"Páginas reales: {nuevo_pdf.page_count}"
    )

    nuevo_pdf.close()

pdf_original.close()

print("\nListo. Revisa la carpeta 'secciones'.")