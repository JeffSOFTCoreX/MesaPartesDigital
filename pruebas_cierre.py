"""Pruebas del cierre del programa cuando falla el guardado (Integrante 1).

Cubre Ctrl+C y fin de entrada con cambios pendientes, y comprueba que
ejecutar() se puede probar simulando el inicio de sesión, sin pedir contraseñas.
"""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import archivo
import main
from archivo import cargar_archivo

REGISTRO = ["1", "DOC-1", "Constancia", "Persona ficticia", "31/10/2026"]


class BaseCierre(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = Path(carpeta.name) / "documentos.txt"
        self.intentos = 0

    def ejecutar(self, entradas, fallos_de_guardado):
        """Ejecuta ejecutar() con login simulado.

        Los primeros ``fallos_de_guardado`` intentos de guardar lanzan OSError.
        getpass queda bloqueado: si algo pidiera contraseña, la prueba falla.
        Devuelve (codigo_de_salida, salida_de_pantalla).
        """
        guardar_real = archivo.guardar_archivo

        def guardar(*args, **kwargs):
            self.intentos += 1
            if self.intentos <= fallos_de_guardado:
                raise OSError("Fallo simulado")
            return guardar_real(*args, **kwargs)

        with patch.object(main, "ARCHIVO_DATOS", str(self.ruta)), \
             patch.object(main, "iniciar_sesion", return_value="admin"), \
             patch("getpass.getpass", side_effect=AssertionError("pidió contraseña")), \
             patch.object(main, "guardar_archivo", side_effect=guardar), \
             patch("builtins.input", side_effect=entradas), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            codigo = main.ejecutar()
        return codigo, salida.getvalue()

    def guardados(self):
        return cargar_archivo(str(self.ruta)) if self.ruta.exists() else []


class PruebasCtrlCConPendientes(BaseCierre):
    def test_reintenta_guardar_y_conserva_los_cambios(self):
        codigo, salida = self.ejecutar([*REGISTRO, KeyboardInterrupt()], fallos_de_guardado=1)
        self.assertEqual(self.intentos, 2)           # guardado inicial + reintento
        self.assertEqual(len(self.guardados()), 1)
        self.assertIn("Reintentando el guardado", salida)
        self.assertIn("interrumpido", salida)
        self.assertNotIn("ERROR", salida)
        self.assertEqual(codigo, 0)

    def test_si_el_reintento_falla_informa_y_no_sale_como_normal(self):
        codigo, salida = self.ejecutar([*REGISTRO, KeyboardInterrupt()], fallos_de_guardado=2)
        self.assertEqual(self.intentos, 2)
        self.assertEqual(self.guardados(), [])        # no se guardó nada
        self.assertIn("ERROR: los cambios recientes NO se guardaron", salida)
        self.assertIn("Programa finalizado con errores.", salida)
        self.assertNotIn("Programa finalizado.\n", salida)
        self.assertNotIn("interrumpido por el usuario", salida)
        self.assertEqual(codigo, 1)

    def test_sin_cambios_pendientes_no_reintenta_y_sale_normal(self):
        codigo, salida = self.ejecutar([*REGISTRO, KeyboardInterrupt()], fallos_de_guardado=0)
        self.assertEqual(self.intentos, 1)            # solo el guardado automático
        self.assertEqual(len(self.guardados()), 1)
        self.assertIn("interrumpido", salida)
        self.assertEqual(codigo, 0)

    def test_ctrl_c_durante_el_reintento_tambien_informa_el_error(self):
        guardar_real = archivo.guardar_archivo
        llamadas = []

        def guardar(*args, **kwargs):
            llamadas.append(1)
            if len(llamadas) == 1:
                raise OSError("Fallo simulado")
            raise KeyboardInterrupt()

        with patch.object(main, "ARCHIVO_DATOS", str(self.ruta)), \
             patch.object(main, "iniciar_sesion", return_value="admin"), \
             patch.object(main, "guardar_archivo", side_effect=guardar), \
             patch("builtins.input", side_effect=[*REGISTRO, KeyboardInterrupt()]), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            codigo = main.ejecutar()
        self.assertEqual(codigo, 1)
        self.assertIn("Reintento de guardado interrumpido", salida.getvalue())
        self.assertIn("NO se guardaron", salida.getvalue())
        del guardar_real


class PruebasFinDeEntradaConPendientes(BaseCierre):
    def test_reintenta_guardar_y_termina_normal_si_funciona(self):
        codigo, salida = self.ejecutar([*REGISTRO, EOFError()], fallos_de_guardado=1)
        self.assertEqual(self.intentos, 2)
        self.assertEqual(len(self.guardados()), 1)
        self.assertIn("Entrada finalizada.", salida)
        self.assertIn("Programa finalizado.", salida)
        self.assertNotIn("ERROR", salida)
        self.assertEqual(codigo, 0)

    def test_si_el_reintento_falla_no_presenta_salida_normal(self):
        codigo, salida = self.ejecutar([*REGISTRO, EOFError()], fallos_de_guardado=2)
        self.assertEqual(self.guardados(), [])
        self.assertIn("ERROR: los cambios recientes NO se guardaron", salida)
        self.assertIn("Programa finalizado con errores.", salida)
        self.assertNotIn("Programa finalizado.\n", salida)
        self.assertEqual(codigo, 1)

    def test_sin_pendientes_termina_normal(self):
        codigo, salida = self.ejecutar([*REGISTRO, EOFError()], fallos_de_guardado=0)
        self.assertEqual(self.intentos, 1)
        self.assertIn("Programa finalizado.", salida)
        self.assertEqual(codigo, 0)

    def test_eof_al_preguntar_si_reintentar_en_la_salida(self):
        # Opción 9 con cambios pendientes y la entrada se cierra en la pregunta.
        codigo, salida = self.ejecutar([*REGISTRO, "9", EOFError()], fallos_de_guardado=2)
        self.assertIn("ADVERTENCIA: hay cambios sin guardar", salida)
        self.assertIn("Programa finalizado con errores.", salida)
        self.assertEqual(codigo, 1)


class PruebasEjecutarSinContrasena(BaseCierre):
    def test_el_menu_funciona_con_login_simulado_y_sin_pedir_contrasena(self):
        codigo, salida = self.ejecutar([*REGISTRO, "2", "doc-1", "9"], fallos_de_guardado=0)
        self.assertIn("Administrador           : admin", salida)
        self.assertIn("registrado correctamente", salida)
        self.assertIn("Persona ficticia", salida)
        self.assertEqual(len(self.guardados()), 1)
        self.assertEqual(codigo, 0)

    def test_el_login_simulado_se_usa_en_lugar_del_real(self):
        with patch.object(main, "ARCHIVO_DATOS", str(self.ruta)), \
             patch.object(main, "iniciar_sesion", return_value="admin") as login, \
             patch("builtins.input", side_effect=["9"]), \
             contextlib.redirect_stdout(io.StringIO()):
            main.ejecutar()
        login.assert_called_once()

    def test_main_devuelve_error_si_no_puede_cargar_los_datos(self):
        self.ruta.write_text("línea inválida sin separadores\n", encoding="utf-8")
        with patch.object(main, "ARCHIVO_DATOS", str(self.ruta)), \
             contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(main.main("admin"), main.ERROR_PERSISTENCIA)


if __name__ == "__main__":
    unittest.main()
