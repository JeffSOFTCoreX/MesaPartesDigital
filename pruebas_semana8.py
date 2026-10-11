"""Pruebas adicionales para el avance de semana 8, con datos ficticios."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from archivo import cargar_archivo, guardar_archivo, ordenar_registros
from busqueda import buscar_documento
from registro import registrar_documento
from validacion import validar_datos


class PruebasIntegracionBasica(unittest.TestCase):
    def setUp(self):
        self.dato = {
            "codigo": "DOC-901", "tipo_documento": "Constancia",
            "estudiante": "USUARIO DE PRUEBA", "fecha": "09/10/2026",
            "estado": "Pendiente",
        }

    def test_crear_archivo_que_no_existe(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "nuevo.txt"
            self.assertEqual(cargar_archivo(ruta), [])
            self.assertTrue(ruta.exists())

    def test_guardar_y_cargar_archivo(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "documentos.txt"
            guardar_archivo([self.dato], ruta)
            self.assertEqual(cargar_archivo(ruta), [self.dato])

    def test_registro_correcto(self):
        registros = []
        with patch("builtins.input", side_effect=["DOC-901", "Constancia", "USUARIO DE PRUEBA", "09/10/2026"]):
            self.assertTrue(registrar_documento(registros))
        self.assertEqual(registros, [self.dato])

    def test_registro_duplicado(self):
        registros = [dict(self.dato)]
        with patch("builtins.input", side_effect=["doc-901"]):
            self.assertFalse(registrar_documento(registros))
        self.assertEqual(len(registros), 1)

    def test_rechaza_campo_obligatorio_vacio(self):
        dato = dict(self.dato, estudiante=" ")
        self.assertFalse(validar_datos(dato)[0])

    def test_rechaza_fecha_inexistente(self):
        dato = dict(self.dato, fecha="31/02/2026")
        self.assertEqual(validar_datos(dato), (False, "La fecha ingresada no es válida."))

    def test_rechaza_fecha_formato_incorrecto(self):
        dato = dict(self.dato, fecha="9/10/2026")
        self.assertFalse(validar_datos(dato)[0])

    def test_busqueda_independiente_de_mayusculas(self):
        self.assertIs(buscar_documento([self.dato], "doc-901"), self.dato)

    def test_busqueda_sin_resultado(self):
        self.assertIsNone(buscar_documento([self.dato], "DOC-999"))

    def test_ordenamiento_por_codigo(self):
        otros = [dict(self.dato, codigo="DOC-902"), dict(self.dato, codigo="DOC-901")]
        self.assertEqual(ordenar_registros(otros, "codigo")[0]["codigo"], "DOC-901")

    def test_ordenamiento_por_fecha(self):
        otros = [dict(self.dato, fecha="15/10/2026"), dict(self.dato, fecha="09/10/2026")]
        self.assertEqual(ordenar_registros(otros, "fecha")[0]["fecha"], "09/10/2026")

    def test_criterio_ordenamiento_invalido(self):
        self.assertIsNone(ordenar_registros([self.dato], "ciudad"))


if __name__ == "__main__":
    unittest.main()
