"""Integración de la consulta unificada por código con el menú."""
import contextlib
import io
import unittest
from unittest.mock import patch

import main
from pruebas_filtros import datos_ficticios


class PruebasConsultaUnificada(unittest.TestCase):
    def ejecutar(self, codigo):
        with patch.object(main, "cargar_archivo", return_value=datos_ficticios()), \
             patch.object(main, "guardar_archivo") as guardar, \
             patch("builtins.input", side_effect=["2", codigo, "9"]), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            main.main()
        guardar.assert_not_called()
        return salida.getvalue()

    def test_consulta_por_codigo_muestra_documento_completo(self):
        salida = self.ejecutar(" exp-101 ")
        for dato in ["Código: EXP-101", "Tipo de documento: Matrícula",
                     "Estudiante/usuario: Usuario ficticio 101", "Fecha: 20/10/2026",
                     "Estado: Pendiente", "Programa finalizado."]:
            self.assertIn(dato, salida)
        self.assertNotIn("Código: EXP-102", salida)

    def test_codigo_inexistente_informa_y_regresa_al_menu(self):
        salida = self.ejecutar("EXP-999")
        self.assertIn("No se encontró ningún documento con el código 'EXP-999'.", salida)
        self.assertNotIn("--- INFORMACIÓN DEL DOCUMENTO ---", salida)
        self.assertIn("Programa finalizado.", salida)


if __name__ == "__main__":
    unittest.main()
