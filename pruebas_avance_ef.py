"""Pruebas nuevas para el avance EF: integridad, salida y resumen.

Los datos son ficticios y todos los archivos se crean en directorios temporales.
"""

import contextlib
import io
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from archivo import cargar_archivo, guardar_archivo, ordenar_registros
from busqueda import buscar_documento
from consulta import resumen_por_estado
from registro import registrar_documento
from validacion import validar_datos


def dato(codigo="DOC-1", estado="Pendiente"):
    return {
        "codigo": codigo,
        "tipo_documento": "Constancia",
        "estudiante": "Estudiante ficticio",
        "fecha": "31/10/2026",
        "estado": estado,
    }


class PruebasAvanceEF(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = Path(carpeta.name) / "documentos.txt"
        ruta_patch = patch.object(main, "ARCHIVO_DATOS", str(self.ruta))
        ruta_patch.start()
        self.addCleanup(ruta_patch.stop)

    def ejecutar_menu(self, entradas, guardado_simulado=None):
        import archivo
        guardar_real = archivo.guardar_archivo
        contador = [0]

        def guardar_con_fallo(*args, **kwargs):
            contador[0] += 1
            if contador[0] <= (guardado_simulado or 0):
                raise OSError("Fallo simulado")
            return guardar_real(*args, **kwargs)

        with patch("builtins.input", side_effect=entradas), \
                patch.object(main, "guardar_archivo", side_effect=guardar_con_fallo), \
                contextlib.redirect_stdout(io.StringIO()) as salida:
            main.main()
        return salida.getvalue(), contador[0]

    def test_rechaza_separador_en_campo(self):
        registro = dato()
        registro["tipo_documento"] = "Solicitud | Constancia"
        self.assertFalse(validar_datos(registro)[0])
        self.assertIn("carácter no permitido", validar_datos(registro)[1])

    def test_rechaza_saltos_y_tab_independientemente_del_campo(self):
        for invalido in ("Nombre\nAlterado", "Nombre\rAlterado", "Nombre\tAlterado"):
            with self.subTest(valor=repr(invalido)):
                registro = dato()
                registro["estudiante"] = invalido
                self.assertFalse(validar_datos(registro)[0])

    def test_al_registrar_valor_con_barra_no_incorpora_registro(self):
        registros = []
        with patch("builtins.input", side_effect=["DOC-1", "Oficio | Consulta", "Persona X", "31/10/2026"]), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(registrar_documento(registros))
        self.assertEqual(registros, [])

    def test_guardado_invalido_no_modifica_archivo_principal(self):
        guardar_archivo([dato()], self.ruta)
        anterior = self.ruta.read_bytes()
        invalido = dato("DOC-2")
        invalido["estudiante"] = "Original | Distinto"
        with self.assertRaises(ValueError):
            guardar_archivo([dato(), invalido], self.ruta)
        self.assertEqual(self.ruta.read_bytes(), anterior)

    def test_guardado_rechaza_codigos_duplicados_normalizados(self):
        guardar_archivo([dato("DOC-1")], self.ruta)
        with self.assertRaisesRegex(ValueError, "Código duplicado"):
            guardar_archivo([dato("DOC-1"), dato(" doc-1 ")], self.ruta)
        self.assertEqual(len(cargar_archivo(self.ruta)), 1)

    def test_carga_detecta_duplicado_con_espacio_en_codigo(self):
        linea = "DOC-1|Constancia|Ficticio|31/10/2026|Pendiente\n"
        linea_espacios = " doc-1 |Constancia|Ficticio|31/10/2026|Pendiente\n"
        self.ruta.write_text(linea + linea_espacios, encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicado"):
            cargar_archivo(self.ruta)

    def test_carga_normaliza_codigo_con_espacios_sin_perder_busqueda(self):
        self.ruta.write_text(" DOC-1 |Constancia|Ficticio|31/10/2026|Pendiente\n", encoding="utf-8")
        registros = cargar_archivo(self.ruta)
        self.assertEqual(registros[0]["codigo"], "DOC-1")
        self.assertIs(buscar_documento(registros, "doc-1"), registros[0])

    def test_fallo_guardado_no_permite_salir_sin_aviso_y_reintento_manual(self):
        entradas = ["1", "DOC-1", "Constancia", "Persona ficticia", "31/10/2026", "9", "n", "8", "9"]
        salida, intentos = self.ejecutar_menu(entradas, guardado_simulado=1)
        self.assertEqual(intentos, 2)
        self.assertIn("ADVERTENCIA: hay cambios sin guardar", salida)
        self.assertIn("seguirá abierto", salida)
        self.assertIn("Información guardada correctamente", salida)
        self.assertEqual(len(cargar_archivo(self.ruta)), 1)

    def test_reintento_automatico_al_salir_tras_fallo(self):
        entradas = ["1", "DOC-1", "Constancia", "Persona ficticia", "31/10/2026", "9", "s"]
        salida, intentos = self.ejecutar_menu(entradas, guardado_simulado=1)
        self.assertEqual(intentos, 2)
        self.assertIn("Programa finalizado", salida)
        self.assertEqual(len(cargar_archivo(self.ruta)), 1)

    def test_reintento_fallido_mantiene_menu_abierto(self):
        entradas = ["1", "DOC-1", "Constancia", "Persona ficticia", "31/10/2026", "9", "s", "8", "9"]
        salida, intentos = self.ejecutar_menu(entradas, guardado_simulado=2)
        self.assertEqual(intentos, 3)
        self.assertIn("seguir\u00e1 abierto para intentar guardar", salida)
        self.assertIn("Programa finalizado", salida)
        self.assertEqual(len(cargar_archivo(self.ruta)), 1)

    def test_ordenar_cambia_y_guarda_antes_de_salir(self):
        guardar_archivo([dato("DOC-9"), dato("DOC-1")], self.ruta)
        self.ejecutar_menu(["7", "codigo", "9"])
        self.assertEqual([r["codigo"] for r in cargar_archivo(self.ruta)], ["DOC-1", "DOC-9"])

    def test_ordenar_ya_ordenado_no_guarda_sin_cambios(self):
        guardar_archivo([dato("DOC-1"), dato("DOC-9")], self.ruta)
        _, intentos = self.ejecutar_menu(["7", "codigo", "9"])
        self.assertEqual(intentos, 0)

    def test_resumen_por_estado(self):
        registros = [dato("A", "Pendiente"), dato("B", "Pendiente"),
                     dato("C", "En proceso"), dato("D", "Atendido")]
        self.assertEqual(resumen_por_estado(registros), {
            "Pendiente": 2, "En proceso": 1, "Atendido": 1,
        })
        self.assertEqual(len(registros), 4)

    def test_recuperacion_documentada_desde_respaldo(self):
        guardar_archivo([dato("DOC-1")], self.ruta)
        guardar_archivo([dato("DOC-1"), dato("DOC-2")], self.ruta)
        self.ruta.write_text("registro dañado | incompleto", encoding="utf-8")
        with self.assertRaises(ValueError):
            cargar_archivo(self.ruta)
        respaldo = self.ruta.with_name(self.ruta.name + ".bak")
        shutil.copyfile(respaldo, self.ruta)
        recuperados = cargar_archivo(self.ruta)
        self.assertEqual([r["codigo"] for r in recuperados], ["DOC-1"])


if __name__ == "__main__":
    unittest.main()
