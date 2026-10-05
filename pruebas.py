import unittest
from unittest.mock import patch

from actualizacion import ESTADOS, actualizar_estado, cambiar_estado


class PruebasActualizacionEstado(unittest.TestCase):

    def setUp(self):
        self.registros = [{"codigo": "DOC-001", "estado": "Pendiente"}]

    def test_estados_definidos(self):
        self.assertEqual(
            list(ESTADOS.values()), ["Pendiente", "En proceso", "Atendido"]
        )

    def test_cambio_pendiente_a_en_proceso(self):
        with patch("builtins.input", side_effect=["DOC-001", "2"]):
            resultado = actualizar_estado(self.registros)
        self.assertTrue(resultado)
        self.assertEqual(self.registros[0]["estado"], "En proceso")

    def test_seleccion_invalida_no_cambia_estado(self):
        with patch("builtins.input", side_effect=["DOC-001", "9"]):
            resultado = actualizar_estado(self.registros)
        self.assertFalse(resultado)
        self.assertEqual(self.registros[0]["estado"], "Pendiente")

    def test_codigo_inexistente(self):
        with patch("builtins.input", side_effect=["DOC-999"]):
            resultado = actualizar_estado(self.registros)
        self.assertFalse(resultado)

    def test_cambiar_estado_directo(self):
        self.assertTrue(cambiar_estado(self.registros[0], "3"))
        self.assertEqual(self.registros[0]["estado"], "Atendido")
        self.assertFalse(cambiar_estado(self.registros[0], "abc"))


if __name__ == "__main__":
    unittest.main()
