"""Pruebas de reemplazo completo, respaldo y fallos de guardado."""
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import archivo
from pruebas_filtros import datos_ficticios


class PruebasGuardadoSeguro(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = Path(carpeta.name) / "documentos.txt"
        self.respaldo = self.ruta.with_name("documentos.txt.bak")
        self.datos = datos_ficticios()
        archivo.guardar_archivo(self.datos, self.ruta)
        self.original = self.ruta.read_bytes()

    def comprobar_original(self):
        self.assertEqual(self.ruta.read_bytes(), self.original)
        self.assertEqual(list(self.ruta.parent.glob("*.tmp")), [])

    def test_guardado_y_respaldo_exacto(self):
        archivo.guardar_archivo(self.datos[:1], self.ruta)
        self.assertEqual(archivo.cargar_archivo(self.ruta), self.datos[:1])
        self.assertEqual(self.respaldo.read_bytes(), self.original)

    def test_primera_escritura_no_crea_respaldo_inexistente(self):
        self.assertFalse(self.respaldo.exists())
        self.assertEqual(archivo.cargar_archivo(self.ruta), self.datos)

    def test_fallo_de_escritura_parcial_conserva_original(self):
        crear = tempfile.NamedTemporaryFile

        def crear_con_fallo(*args, **kwargs):
            temporal = crear(*args, **kwargs)
            escribir = temporal.write

            def escribir_parcial(contenido):
                escribir(contenido[:8])
                raise OSError("Disco lleno durante escritura")

            temporal.write = escribir_parcial
            return temporal

        with patch.object(archivo.tempfile, "NamedTemporaryFile", side_effect=crear_con_fallo):
            with self.assertRaises(OSError):
                archivo.guardar_archivo(self.datos[:1], self.ruta)
        self.comprobar_original()

    def test_fallo_de_sincronizacion_conserva_original(self):
        with patch.object(archivo.os, "fsync", side_effect=OSError("Fallo de disco")):
            with self.assertRaises(OSError):
                archivo.guardar_archivo([], self.ruta)
        self.comprobar_original()

    def test_fallo_al_crear_temporal_conserva_original(self):
        with patch.object(archivo.tempfile, "NamedTemporaryFile", side_effect=PermissionError("Sin permisos")):
            with self.assertRaises(OSError):
                archivo.guardar_archivo([], self.ruta)
        self.comprobar_original()

    def test_fallo_al_reemplazar_respaldo_conserva_ambos(self):
        self.respaldo.write_bytes(b"respaldo anterior")
        with patch.object(archivo.os, "replace", side_effect=PermissionError("Respaldo bloqueado")):
            with self.assertRaises(OSError):
                archivo.guardar_archivo([], self.ruta)
        self.comprobar_original()
        self.assertEqual(self.respaldo.read_bytes(), b"respaldo anterior")

    def test_fallo_al_reemplazar_principal_conserva_original(self):
        reemplazar = os.replace

        def reemplazar_con_fallo(origen, destino):
            if Path(destino) == self.ruta:
                raise PermissionError("Archivo principal bloqueado")
            reemplazar(origen, destino)

        with patch.object(archivo.os, "replace", side_effect=reemplazar_con_fallo):
            with self.assertRaises(OSError):
                archivo.guardar_archivo([], self.ruta)
        self.comprobar_original()
        self.assertEqual(self.respaldo.read_bytes(), self.original)

    def test_respaldo_se_actualiza_a_version_inmediatamente_anterior(self):
        archivo.guardar_archivo(self.datos[:2], self.ruta)
        intermedio = self.ruta.read_bytes()
        archivo.guardar_archivo(self.datos[:1], self.ruta)
        self.assertEqual(self.respaldo.read_bytes(), intermedio)

    def test_lista_vacia_guarda_y_respalda(self):
        archivo.guardar_archivo([], self.ruta)
        self.assertEqual(self.ruta.read_bytes(), b"")
        self.assertEqual(self.respaldo.read_bytes(), self.original)

    def test_fallo_inicial_no_publica_archivo_incompleto(self):
        nueva = self.ruta.parent / "nuevo.txt"
        with patch.object(archivo.os, "fsync", side_effect=OSError("Sin espacio")):
            with self.assertRaises(OSError):
                archivo.guardar_archivo(self.datos, nueva)
        self.assertFalse(nueva.exists())
        self.assertEqual(list(self.ruta.parent.glob("*.tmp")), [])


if __name__ == "__main__":
    unittest.main()
