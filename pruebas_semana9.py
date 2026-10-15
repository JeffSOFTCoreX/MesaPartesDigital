"""Pruebas del guardado automático incorporado en la semana 9."""

import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from archivo import cargar_archivo, guardar_archivo


class PruebasGuardadoAutomatico(unittest.TestCase):
    def setUp(self):
        self.directorio = tempfile.TemporaryDirectory()
        self.addCleanup(self.directorio.cleanup)
        self.ruta = str(Path(self.directorio.name) / 'documentos.txt')
        parche_ruta = patch.object(main, 'ARCHIVO_DATOS', self.ruta)
        parche_ruta.start()
        self.addCleanup(parche_ruta.stop)

    def ejecutar_hasta_interrupcion(self, entradas):
        """Simula cierre repentino del programa sin seleccionar 'Salir'."""
        with patch('builtins.input', side_effect=[*entradas, KeyboardInterrupt]):
            with contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(KeyboardInterrupt):
                    main.main()

    def test_guarda_al_registrar_sin_pulsar_guardar_ni_salir(self):
        self.ejecutar_hasta_interrupcion(
            ['1', 'DOC-901', 'Constancia', 'Ana Ruiz', '14/10/2026']
        )
        registros = cargar_archivo(self.ruta)
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0]['codigo'], 'DOC-901')
        self.assertEqual(registros[0]['estado'], 'Pendiente')

    def test_guarda_al_actualizar_sin_pulsar_guardar_ni_salir(self):
        guardar_archivo([
            {'codigo': 'DOC-901', 'tipo_documento': 'Constancia',
             'estudiante': 'Ana Ruiz', 'fecha': '14/10/2026', 'estado': 'Pendiente'}
        ], self.ruta)
        self.ejecutar_hasta_interrupcion(['4', 'DOC-901', '2'])
        registros = cargar_archivo(self.ruta)
        self.assertEqual(registros[0]['estado'], 'En proceso')

    def test_no_guarda_despues_de_registro_invalido(self):
        self.ejecutar_hasta_interrupcion(
            ['1', 'DOC-902', 'Constancia', 'Ana Ruiz', '31/02/2026']
        )
        self.assertEqual(cargar_archivo(self.ruta), [])

    def test_no_guarda_despues_de_actualizacion_invalida(self):
        guardar_archivo([
            {'codigo': 'DOC-901', 'tipo_documento': 'Constancia',
             'estudiante': 'Ana Ruiz', 'fecha': '14/10/2026', 'estado': 'Pendiente'}
        ], self.ruta)
        original=Path(self.ruta).read_bytes()
        self.ejecutar_hasta_interrupcion(['4', 'DOC-901', '8'])
        self.assertEqual(Path(self.ruta).read_bytes(),original)

    def test_error_de_guardado_se_informa_sin_cerrar_el_programa(self):
        with patch.object(main, 'guardar_archivo', side_effect=OSError('ruta no disponible')):
            with contextlib.redirect_stdout(io.StringIO()) as salida:
                resultado = main.guardar_automaticamente([])
        self.assertFalse(resultado)
        self.assertIn('No se pudieron guardar', salida.getvalue())


if __name__ == '__main__':
    unittest.main()
