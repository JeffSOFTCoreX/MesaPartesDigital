"""Pruebas de la revisión del sistema (Integrante 2): errores corregidos."""
import contextlib
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from actualizacion import actualizar_estado
from archivo import cargar_archivo
from validacion import validar_datos


class PruebasRevision(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ruta = Path(self.tmp.name) / "documentos.txt"

    def ejecutar_main(self, entradas):
        with patch.object(main, "ARCHIVO_DATOS", str(self.ruta)), \
             patch("builtins.input", side_effect=entradas), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            main.main()
        return salida.getvalue()

    def test_ruta_de_datos_no_depende_de_la_carpeta_de_ejecucion(self):
        self.assertTrue(os.path.isabs(main.ARCHIVO_DATOS))
        self.assertEqual(Path(main.ARCHIVO_DATOS).parent, Path(main.__file__).resolve().parent)

    def test_archivo_con_bom_se_carga_y_se_encuentra_el_primer_codigo(self):
        self.ruta.write_bytes(
            b"\xef\xbb\xbfEXP01|Matr\xc3\xadcula|Ana|01/10/2026|Pendiente\n")
        registros = cargar_archivo(str(self.ruta))
        self.assertEqual(registros[0]["codigo"], "EXP01")
        salida = self.ejecutar_main(["2", "EXP01", "9"])
        self.assertIn("Código: EXP01", salida)

    def test_mismo_estado_no_cuenta_como_cambio(self):
        registros = [{"codigo": "A1", "estado": "Pendiente"}]
        with patch("builtins.input", side_effect=["A1", "1"]), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            self.assertFalse(actualizar_estado(registros))
        self.assertIn("ya está en estado 'Pendiente'", salida.getvalue())

    def test_mismo_estado_no_reescribe_ni_pisa_el_respaldo(self):
        self.ejecutar_main(["1", "A1", "Tipo", "Ana", "01/10/2026", "9"])
        self.ejecutar_main(["6", "A1", "2", "9"])      # genera .bak (Pendiente)
        bak = self.ruta.with_name("documentos.txt.bak")
        antes = bak.read_text(encoding="utf-8")
        self.ejecutar_main(["6", "A1", "2", "9"])      # mismo estado: sin guardar
        self.assertEqual(bak.read_text(encoding="utf-8"), antes)

    def test_estado_persiste_al_cerrar_y_reabrir(self):
        self.ejecutar_main(["1", "A1", "Tipo", "Ana", "01/10/2026", "9"])
        self.ejecutar_main(["6", "A1", "3", "9"])
        self.assertEqual(cargar_archivo(str(self.ruta))[0]["estado"], "Atendido")

    def test_ctrl_d_en_el_menu_sale_sin_traceback(self):
        with patch.object(main, "ARCHIVO_DATOS", str(self.ruta)), \
             patch("builtins.input", side_effect=EOFError()), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            main.ejecutar()
        self.assertIn("Programa finalizado.", salida.getvalue())

    def test_ctrl_c_a_mitad_de_registro_no_pierde_lo_guardado(self):
        self.ejecutar_main(["1", "A1", "Tipo", "Ana", "01/10/2026", "9"])
        with patch.object(main, "ARCHIVO_DATOS", str(self.ruta)), \
             patch("builtins.input", side_effect=["1", "A2", KeyboardInterrupt()]), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            main.ejecutar()
        self.assertIn("interrumpido", salida.getvalue())
        self.assertEqual(len(cargar_archivo(str(self.ruta))), 1)

    def test_fecha_con_digitos_no_ascii_sigue_rechazada(self):
        datos = {"codigo": "A1", "tipo_documento": "T", "estudiante": "E",
                 "fecha": "١٢/٠١/٢٠٢٦", "estado": "Pendiente"}
        self.assertFalse(validar_datos(datos)[0])


if __name__ == "__main__":
    unittest.main()
