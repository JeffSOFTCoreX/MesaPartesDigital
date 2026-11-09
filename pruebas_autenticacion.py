"""Pruebas del inicio y cierre de sesión del administrador (Integrante 1)."""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import autenticacion
import main

USUARIO = "admin"
CLAVE = "Clave-Segura-2026"


class BaseAutenticacion(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.ruta = str(Path(self.tmp.name) / "credenciales.json")
        self.datos_ruta = str(Path(self.tmp.name) / "documentos.txt")
        # Pocas iteraciones solo para que las pruebas sean rápidas.
        self.datos = autenticacion.generar_credenciales(USUARIO, CLAVE, iteraciones=1000)
        autenticacion.guardar_credenciales(self.datos, self.ruta)

    def iniciar(self, usuarios_y_claves, **kwargs):
        """Simula teclear usuario/clave en orden; devuelve (resultado, salida)."""
        entradas = [x for par in usuarios_y_claves for x in par[:1]]
        claves = [par[1] for par in usuarios_y_claves]
        with patch("builtins.input", side_effect=entradas), \
             patch.object(autenticacion, "_pedir_contrasena", side_effect=claves), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            resultado = autenticacion.iniciar_sesion(self.ruta, **kwargs)
        return resultado, salida.getvalue()


class PruebasHash(BaseAutenticacion):
    def test_la_contrasena_no_se_guarda_en_texto_plano(self):
        contenido = Path(self.ruta).read_text(encoding="utf-8")
        self.assertNotIn(CLAVE, contenido)
        self.assertEqual(set(json.loads(contenido)),
                         {"usuario", "algoritmo", "iteraciones", "sal", "hash"})

    def test_misma_contrasena_genera_hash_distinto_por_la_sal(self):
        otro = autenticacion.generar_credenciales(USUARIO, CLAVE, iteraciones=1000)
        self.assertNotEqual(self.datos["sal"], otro["sal"])
        self.assertNotEqual(self.datos["hash"], otro["hash"])

    def test_contrasena_corta_se_rechaza(self):
        with self.assertRaises(ValueError):
            autenticacion.generar_credenciales(USUARIO, "corta")

    def test_usuario_vacio_se_rechaza(self):
        with self.assertRaises(ValueError):
            autenticacion.generar_credenciales("   ", CLAVE)

    def test_credenciales_correctas_se_verifican(self):
        self.assertTrue(autenticacion.verificar_credenciales(USUARIO, CLAVE, self.datos))

    def test_usuario_no_distingue_mayusculas_ni_espacios(self):
        self.assertTrue(autenticacion.verificar_credenciales("  ADMIN ", CLAVE, self.datos))

    def test_contrasena_distingue_mayusculas(self):
        self.assertFalse(autenticacion.verificar_credenciales(USUARIO, CLAVE.lower(), self.datos))

    def test_usuario_incorrecto_con_clave_correcta_se_rechaza(self):
        self.assertFalse(autenticacion.verificar_credenciales("otro", CLAVE, self.datos))

    def test_archivo_inexistente_devuelve_none(self):
        self.assertIsNone(autenticacion.cargar_credenciales(self.ruta + ".no"))

    def test_archivo_danado_lanza_error(self):
        Path(self.ruta).write_text("{no es json", encoding="utf-8")
        with self.assertRaises(ValueError):
            autenticacion.cargar_credenciales(self.ruta)

    def test_archivo_con_campos_faltantes_lanza_error(self):
        Path(self.ruta).write_text(json.dumps({"usuario": "admin"}), encoding="utf-8")
        with self.assertRaises(ValueError):
            autenticacion.cargar_credenciales(self.ruta)


class PruebasInicioSesion(BaseAutenticacion):
    def test_credenciales_correctas_conceden_acceso(self):
        resultado, salida = self.iniciar([(USUARIO, CLAVE)])
        self.assertEqual(resultado, USUARIO)
        self.assertIn("Acceso concedido", salida)

    def test_credenciales_incorrectas_rechazan_el_acceso(self):
        resultado, salida = self.iniciar([("admin", "mala1"), ("admin", "mala2"), ("admin", "mala3")])
        self.assertIsNone(resultado)
        self.assertIn(autenticacion.MENSAJE_RECHAZO, salida)
        self.assertNotIn("Acceso concedido", salida)

    def test_el_mensaje_no_revela_si_falla_usuario_o_contrasena(self):
        _, salida_usuario = self.iniciar([("nadie", CLAVE)] * 3)
        _, salida_clave = self.iniciar([("admin", "xxxxxxxx")] * 3)
        self.assertIn(autenticacion.MENSAJE_RECHAZO, salida_usuario)
        self.assertIn(autenticacion.MENSAJE_RECHAZO, salida_clave)
        self.assertNotIn("no existe", salida_usuario.lower())

    def test_se_bloquea_tras_tres_intentos_fallidos(self):
        resultado, salida = self.iniciar([("a", "1"), ("b", "2"), ("c", "3")])
        self.assertIsNone(resultado)
        self.assertIn("Intentos restantes: 2", salida)
        self.assertIn("Intentos restantes: 1", salida)
        self.assertIn("Acceso bloqueado", salida)

    def test_con_clave_correcta_en_el_tercer_intento_entra(self):
        resultado, _ = self.iniciar([("a", "1"), ("b", "2"), (USUARIO, CLAVE)])
        self.assertEqual(resultado, USUARIO)

    def test_no_pide_un_cuarto_intento(self):
        # Solo hay 3 pares de entradas: un cuarto intento agotaría el mock.
        resultado, _ = self.iniciar([("a", "1")] * 3)
        self.assertIsNone(resultado)

    def test_limite_de_intentos_configurable(self):
        resultado, salida = self.iniciar([("a", "1")], max_intentos=1)
        self.assertIsNone(resultado)
        self.assertIn("Acceso bloqueado", salida)

    def test_credenciales_danadas_deniegan_el_acceso(self):
        Path(self.ruta).write_text("basura", encoding="utf-8")
        resultado, salida = self.iniciar([])
        self.assertIsNone(resultado)
        self.assertIn("Acceso denegado", salida)

    def test_sin_cuenta_y_sin_crearla_no_hay_acceso(self):
        Path(self.ruta).unlink()
        with patch("builtins.input", side_effect=["n"]), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            resultado = autenticacion.iniciar_sesion(self.ruta)
        self.assertIsNone(resultado)
        self.assertIn("python autenticacion.py", salida.getvalue())

    def test_primera_ejecucion_permite_crear_la_cuenta_e_ingresar(self):
        Path(self.ruta).unlink()
        with patch("builtins.input", side_effect=["s", "jefe", "jefe"]), \
             patch.object(autenticacion, "_pedir_contrasena",
                          side_effect=["NuevaClave-99", "NuevaClave-99", "NuevaClave-99"]), \
             contextlib.redirect_stdout(io.StringIO()):
            resultado = autenticacion.iniciar_sesion(self.ruta)
        self.assertEqual(resultado, "jefe")


class PruebasConfiguracion(BaseAutenticacion):
    def configurar(self, entradas, claves):
        with patch("builtins.input", side_effect=entradas), \
             patch.object(autenticacion, "_pedir_contrasena", side_effect=claves), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            resultado = autenticacion.configurar_administrador(self.ruta)
        return resultado, salida.getvalue()

    def test_cambiar_cuenta_exige_la_contrasena_actual(self):
        resultado, salida = self.configurar([], ["incorrecta"])
        self.assertFalse(resultado)
        self.assertIn("incorrecta", salida)
        self.assertTrue(autenticacion.verificar_credenciales(
            USUARIO, CLAVE, autenticacion.cargar_credenciales(self.ruta)))

    def test_cambiar_cuenta_con_contrasena_actual_correcta(self):
        resultado, _ = self.configurar(["nuevo"], [CLAVE, "OtraClave-123", "OtraClave-123"])
        self.assertTrue(resultado)
        datos = autenticacion.cargar_credenciales(self.ruta)
        self.assertTrue(autenticacion.verificar_credenciales("nuevo", "OtraClave-123", datos))
        self.assertFalse(autenticacion.verificar_credenciales(USUARIO, CLAVE, datos))

    def test_confirmacion_distinta_no_guarda_nada(self):
        resultado, salida = self.configurar(["nuevo"], [CLAVE, "OtraClave-123", "Distinta-123"])
        self.assertFalse(resultado)
        self.assertIn("no coinciden", salida)
        self.assertTrue(autenticacion.verificar_credenciales(
            USUARIO, CLAVE, autenticacion.cargar_credenciales(self.ruta)))


class PruebasIntegracionMain(BaseAutenticacion):
    """Inicio de sesión + menú: acceso, rechazo, cierre de sesión y funciones."""

    def ejecutar(self, entradas, claves):
        with patch.object(main, "ARCHIVO_DATOS", self.datos_ruta), \
             patch.object(main, "iniciar_sesion",
                          lambda: autenticacion.iniciar_sesion(self.ruta)), \
             patch.object(autenticacion, "_pedir_contrasena", side_effect=claves), \
             patch("builtins.input", side_effect=entradas), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            main.ejecutar()
        return salida.getvalue()

    def test_sin_credenciales_correctas_no_se_muestra_el_menu(self):
        salida = self.ejecutar(["a", "b", "c"], ["1", "2", "3"])
        self.assertNotIn("MENÚ PRINCIPAL", salida)
        self.assertIn("Programa finalizado.", salida)

    def test_con_credenciales_correctas_se_muestra_el_menu_y_el_usuario(self):
        salida = self.ejecutar([USUARIO, "9"], [CLAVE])
        self.assertIn("MENÚ PRINCIPAL", salida)
        self.assertIn("Administrador           : admin", salida)
        self.assertIn("[10] Cerrar sesión", salida)

    def test_el_login_se_muestra_antes_que_el_menu(self):
        salida = self.ejecutar([USUARIO, "9"], [CLAVE])
        self.assertLess(salida.index("INICIO DE SESIÓN"), salida.index("MENÚ PRINCIPAL"))

    def test_cerrar_sesion_vuelve_al_login_y_no_al_menu(self):
        # Entra, cierra sesión (10) y falla 3 veces: no debe volver al menú.
        salida = self.ejecutar(
            [USUARIO, "10", "x", "y", "z"], [CLAVE, "1", "2", "3"])
        self.assertIn("Sesión cerrada.", salida)
        self.assertEqual(salida.count("INICIO DE SESIÓN"), 2)
        self.assertEqual(salida.count("MENÚ PRINCIPAL"), 1)
        self.assertIn("Acceso bloqueado", salida)

    def test_cerrar_sesion_permite_volver_a_entrar(self):
        salida = self.ejecutar(
            [USUARIO, "10", USUARIO, "9"], [CLAVE, CLAVE])
        self.assertEqual(salida.count("MENÚ PRINCIPAL"), 2)
        self.assertEqual(salida.count("Acceso concedido"), 2)
        self.assertIn("Programa finalizado.", salida)

    def test_registro_busqueda_y_actualizacion_tras_iniciar_sesion(self):
        salida = self.ejecutar(
            [USUARIO,
             "1", "EXP01", "Matrícula", "Ana", "01/10/2026",   # registrar
             "2", "exp01",                                     # buscar
             "6", "EXP01", "2",                                # actualizar
             "2", "EXP01",                                     # verificar
             "9"],
            [CLAVE])
        self.assertIn("registrado correctamente", salida)
        self.assertIn("Estado actualizado a 'En proceso'", salida)
        self.assertIn("Estado: En proceso", salida)
        self.assertEqual(Path(self.datos_ruta).read_text(encoding="utf-8").strip(),
                         "EXP01|Matrícula|Ana|01/10/2026|En proceso")

    def test_ctrl_d_en_el_login_sale_sin_traceback(self):
        salida = self.ejecutar(EOFError(), [CLAVE])
        self.assertIn("Programa finalizado.", salida)
        self.assertNotIn("MENÚ PRINCIPAL", salida)


if __name__ == "__main__":
    unittest.main()
