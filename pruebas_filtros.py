"""Casos CP01–CP09 y pruebas de integración, con expedientes ficticios."""

import contextlib
import copy
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from archivo import cargar_archivo, guardar_archivo
from consulta import consultar_pendientes, consultar_por_filtros, filtrar_expedientes


def datos_ficticios():
    tipos_estados = [
        ("Matrícula", "Pendiente"), ("Constancia", "Atendido"),
        ("Matrícula", "En proceso"), ("Constancia", "Pendiente"),
        ("Matrícula", "Atendido"),
    ]
    return [
        {"codigo": f"EXP-{i}", "tipo_documento": tipo,
         "estudiante": f"Usuario ficticio {i}", "fecha": "20/10/2026",
         "estado": estado}
        for i, (tipo, estado) in enumerate(tipos_estados, start=101)
    ]


class PruebasFiltros(unittest.TestCase):
    def setUp(self):
        self.registros = datos_ficticios()

    def codigos(self, **criterios):
        return [r["codigo"] for r in filtrar_expedientes(self.registros, **criterios)]

    def test_cp01_matriculas(self):
        self.assertEqual(self.codigos(tipo="Matrícula"), ["EXP-101", "EXP-103", "EXP-105"])

    def test_cp02_constancias(self):
        self.assertEqual(self.codigos(tipo="Constancia"), ["EXP-102", "EXP-104"])

    def test_cp03_pendientes(self):
        self.assertEqual(self.codigos(estado="Pendiente"), ["EXP-101", "EXP-104"])

    def test_cp04_combinacion(self):
        self.assertEqual(self.codigos(tipo="Matrícula", estado="Pendiente"), ["EXP-101"])

    def test_cp05_sin_coincidencias(self):
        self.assertEqual(self.codigos(tipo="Solicitud"), [])

    def test_cp06_normaliza_criterios(self):
        self.assertEqual(self.codigos(tipo="  MATRÍCULA  ", estado=" en   PROCESO "), ["EXP-103"])

    def test_cp06_normaliza_valores_almacenados(self):
        self.registros[0].update(tipo_documento="  mAtRíCuLa ", estado=" PENDIENTE ")
        self.assertEqual(self.codigos(tipo="Matrícula", estado="Pendiente"), ["EXP-101"])

    def test_cp07_lista_vacia(self):
        self.assertEqual(filtrar_expedientes([], tipo="Matrícula"), [])

    def test_cp08_persistencia(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "documentos.txt"
            guardar_archivo(self.registros, ruta)
            recuperados = cargar_archivo(ruta)
            self.assertEqual(recuperados, self.registros)
            self.assertEqual(
                [r["codigo"] for r in filtrar_expedientes(recuperados, "Matrícula", "Pendiente")],
                ["EXP-101"],
            )

    def test_cp09_no_modifica_datos_ni_orden(self):
        original = copy.deepcopy(self.registros)
        resultado = filtrar_expedientes(self.registros, estado="Pendiente")
        resultado.reverse()
        resultado.clear()
        self.assertEqual(self.registros, original)

    def test_criterios_vacios_devuelven_lista_nueva(self):
        resultado = filtrar_expedientes(self.registros, "  ", "\t")
        self.assertEqual(resultado, self.registros)
        self.assertIsNot(resultado, self.registros)

    def test_todos_los_estados(self):
        for estado, esperados in [
            ("En proceso", ["EXP-103"]), ("Atendido", ["EXP-102", "EXP-105"]),
        ]:
            with self.subTest(estado=estado):
                self.assertEqual(self.codigos(estado=estado), esperados)

    def test_tipo_personalizado_sigue_admitido(self):
        self.registros[0]["tipo_documento"] = "Solicitud de traslado"
        self.assertEqual(self.codigos(tipo=" solicitud  DE traslado "), ["EXP-101"])


class PruebasIntegracionFiltros(unittest.TestCase):
    def ejecutar_consulta(self, entradas, registros=None):
        if registros is None:
            registros = datos_ficticios()
        with patch("builtins.input", side_effect=entradas), \
             contextlib.redirect_stdout(io.StringIO()) as salida:
            consultar_por_filtros(registros)
        return salida.getvalue()

    def test_consulta_combinada_muestra_solo_coincidencias(self):
        salida = self.ejecutar_consulta(["Matrícula", "Pendiente"])
        self.assertIn("Código: EXP-101", salida)
        for codigo in ("EXP-102", "EXP-103", "EXP-104", "EXP-105"):
            self.assertNotIn(f"Código: {codigo}", salida)

    def test_mensaje_sin_coincidencias(self):
        self.assertIn("No existen registros que cumplan", self.ejecutar_consulta(["Solicitud", ""]))

    def test_estado_invalido(self):
        salida = self.ejecutar_consulta(["", "Archivado"])
        self.assertIn("El estado ingresado no es válido", salida)
        self.assertNotIn("Código:", salida)

    def test_lista_vacia_informa_sin_solicitar_entradas(self):
        self.assertIn("No existen registros almacenados", self.ejecutar_consulta([], []))

    def test_consulta_rapida_pendientes(self):
        with contextlib.redirect_stdout(io.StringIO()) as salida:
            consultar_pendientes(datos_ficticios())
        self.assertIn("Código: EXP-101", salida.getvalue())
        self.assertIn("Código: EXP-104", salida.getvalue())
        self.assertNotIn("Código: EXP-103", salida.getvalue())

    def test_consulta_rapida_sin_pendientes(self):
        registros = [r for r in datos_ficticios() if r["estado"] == "Atendido"]
        with contextlib.redirect_stdout(io.StringIO()) as salida:
            consultar_pendientes(registros)
        self.assertIn("No existen registros que cumplan", salida.getvalue())

    def test_consulta_rapida_lista_vacia(self):
        with contextlib.redirect_stdout(io.StringIO()) as salida:
            consultar_pendientes([])
        self.assertIn("No existen registros almacenados", salida.getvalue())

    def test_menu_consultas_no_escriben_archivo_y_funcionan_tras_reinicio(self):
        with tempfile.TemporaryDirectory() as carpeta:
            ruta = Path(carpeta) / "documentos.txt"
            guardar_archivo(datos_ficticios(), ruta)
            original = ruta.read_bytes()
            for intento in range(2):
                with self.subTest(reinicio=intento), \
                     patch.object(main, "ARCHIVO_DATOS", str(ruta)), \
                     patch.object(main, "guardar_archivo") as guardar, \
                     patch("builtins.input", side_effect=["4", "Matrícula", "Pendiente", "5", KeyboardInterrupt]), \
                     contextlib.redirect_stdout(io.StringIO()) as salida:
                    with self.assertRaises(KeyboardInterrupt):
                        main.main()
                    guardar.assert_not_called()
                    self.assertIn("CONSULTA POR FILTROS", salida.getvalue())
                    self.assertIn("EXPEDIENTES PENDIENTES", salida.getvalue())
                    self.assertIn("Código: EXP-101", salida.getvalue())
                    self.assertIn("Código: EXP-104", salida.getvalue())
                    self.assertEqual(ruta.read_bytes(), original)


if __name__ == "__main__":
    unittest.main()
