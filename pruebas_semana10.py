"""Pruebas de integridad de registros y errores de archivos (semana 10)."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from archivo import cargar_archivo


class PruebasIntegridadArchivos(unittest.TestCase):
    def setUp(self):
        self.carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(self.carpeta.cleanup)
        self.ruta = Path(self.carpeta.name) / "documentos.txt"

    def escribir(self, *lineas):
        self.ruta.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    def test_detecta_lineas_con_cantidad_incorrecta_de_campos(self):
        self.escribir("COD-001|Constancia|Ana Ruiz|15/10/2026|Pendiente", "LINEA|INCOMPLETA")
        original = self.ruta.read_bytes()
        with self.assertRaisesRegex(ValueError, "1 registro"):
            cargar_archivo(self.ruta)
        self.assertEqual(self.ruta.read_bytes(), original)

    def test_detecta_fecha_invalida_y_campos_vacios(self):
        self.escribir("COD-001|Constancia|Ana Ruiz|31/02/2026|Pendiente",
                      "COD-002|Constancia| |15/10/2026|Pendiente",
                      "COD-003|Constancia|Ana Ruiz|15/10/2026|Pendiente")
        with self.assertRaisesRegex(ValueError, "2 registro"):
            cargar_archivo(self.ruta)

    def test_detecta_codigos_duplicados_sin_distinguir_mayusculas(self):
        self.escribir("COD-001|Constancia|Ana Ruiz|15/10/2026|Pendiente",
                      "cod-001|Matrícula|Juan Paz|16/10/2026|En proceso")
        with self.assertRaisesRegex(ValueError, "1 registro"):
            cargar_archivo(self.ruta)

    def test_error_de_lectura_impide_abrir_menu(self):
        with patch.object(main, "cargar_archivo", side_effect=PermissionError("sin permisos")), \
             patch("builtins.input", side_effect=AssertionError("No debería mostrar menú")), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            main.main()
        self.assertIn("No se pudieron cargar", salida.getvalue())

    def test_guardado_manual_informa_error_sin_finalizar(self):
        with patch.object(main, "ARCHIVO_DATOS", str(self.ruta)), \
             patch.object(main, "guardar_archivo", side_effect=[OSError("sin espacio"), None]) as mock_guardado, \
             patch("builtins.input", side_effect=["6", "8"]), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            main.main()
        self.assertEqual(mock_guardado.call_count, 2)
        self.assertIn("No se pudieron guardar", salida.getvalue())
        self.assertIn("Programa finalizado", salida.getvalue())

    def test_error_al_salir_permite_reintentar(self):
        with patch.object(main, "ARCHIVO_DATOS", str(self.ruta)), \
             patch.object(main, "guardar_archivo", side_effect=[OSError("sin permisos"), None]) as mock_guardado, \
             patch("builtins.input", side_effect=["8", "8"]), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            main.main()
        self.assertEqual(mock_guardado.call_count, 2)
        self.assertIn("seguirá abierto", salida.getvalue())
        self.assertIn("Programa finalizado", salida.getvalue())


if __name__ == "__main__":
    unittest.main()
