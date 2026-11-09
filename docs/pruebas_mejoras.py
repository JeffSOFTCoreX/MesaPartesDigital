"""Pruebas de las mejoras de la revisión (Integrante 2)."""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from archivo import cargar_archivo, ordenar_registros
from consulta import filtrar_expedientes
from registro import registrar_documento
from validacion import LONGITUD_MAXIMA, validar_datos


def silencioso(funcion, entradas, *args):
    with patch("builtins.input", side_effect=entradas), \
         contextlib.redirect_stdout(io.StringIO()) as salida:
        resultado = funcion(*args)
    return resultado, salida.getvalue()


class PruebasMejoras(unittest.TestCase):
    def archivo(self, texto):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ruta = Path(tmp.name) / "documentos.txt"
        ruta.write_text(texto, encoding="utf-8")
        return str(ruta)

    def test_carga_tolera_espacios_alrededor_del_separador(self):
        ruta = self.archivo("EXP01 | Matrícula | Ana | 01/10/2026 | Pendiente\n")
        registro = cargar_archivo(ruta)[0]
        self.assertEqual(registro["codigo"], "EXP01")
        self.assertEqual(registro["tipo_documento"], "Matrícula")

    def test_carga_acepta_estado_en_minusculas_y_lo_normaliza(self):
        ruta = self.archivo("EXP01|Matrícula|Ana|01/10/2026|en  PROCESO\n")
        self.assertEqual(cargar_archivo(ruta)[0]["estado"], "En proceso")

    def test_carga_sigue_rechazando_estado_desconocido(self):
        ruta = self.archivo("EXP01|Matrícula|Ana|01/10/2026|Perdido\n")
        with self.assertRaises(ValueError):
            cargar_archivo(ruta)

    def test_filtro_por_tipo_ignora_tildes(self):
        registros = [{"codigo": "A", "tipo_documento": "Matrícula",
                      "estudiante": "x", "fecha": "01/01/2026", "estado": "Pendiente"}]
        self.assertEqual(len(filtrar_expedientes(registros, tipo="matricula")), 1)
        self.assertEqual(len(filtrar_expedientes(registros, tipo="MATRÍCULA")), 1)

    def test_codigo_vacio_se_rechaza_sin_pedir_mas_datos(self):
        resultado, salida = silencioso(registrar_documento, ["   "], [])
        self.assertFalse(resultado)
        self.assertIn("'codigo' es obligatorio", salida)

    def test_registro_normaliza_espacios_internos(self):
        registros = []
        silencioso(registrar_documento,
                   ["  X1 ", "  Matrícula ", "  Ana    Pérez ", "01/01/2026"], registros)
        self.assertEqual(registros[0]["estudiante"], "Ana Pérez")
        self.assertEqual(registros[0]["tipo_documento"], "Matrícula")

    def test_orden_natural_por_codigo(self):
        regs = [{"codigo": c} for c in ("EXP10", "EXP2", "exp1")]
        orden = [r["codigo"] for r in ordenar_registros(regs, "codigo")]
        self.assertEqual(orden, ["exp1", "EXP2", "EXP10"])

    def test_orden_natural_con_codigos_mixtos_no_falla(self):
        regs = [{"codigo": c} for c in ("A-10", "10", "B", "A-2", "7X")]
        self.assertEqual(len(ordenar_registros(regs, "codigo")), 5)

    def test_longitud_maxima_de_campos(self):
        datos = {"codigo": "A1", "tipo_documento": "T",
                 "estudiante": "N" * (LONGITUD_MAXIMA + 1),
                 "fecha": "01/01/2026", "estado": "Pendiente"}
        valido, mensaje = validar_datos(datos)
        self.assertFalse(valido)
        self.assertIn("supera", mensaje)
        datos["estudiante"] = "N" * LONGITUD_MAXIMA
        self.assertTrue(validar_datos(datos)[0])

    def test_ordenar_en_el_menu_muestra_la_lista(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        ruta = str(Path(tmp.name) / "documentos.txt")
        entradas = ["1", "B2", "T", "Ana", "01/01/2026",
                    "1", "A1", "T", "Luis", "02/01/2026", "7", "codigo", "9"]
        with patch.object(main, "ARCHIVO_DATOS", ruta), \
             patch("builtins.input", side_effect=entradas), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            main.main()
        texto = salida.getvalue()
        self.assertIn("Registros ordenados correctamente.", texto)
        despues = texto.split("Registros ordenados correctamente.")[1]
        self.assertLess(despues.index("A1"), despues.index("B2"))


if __name__ == "__main__":
    unittest.main()
