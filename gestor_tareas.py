"""
=============================================================
  GESTOR DE TAREAS PERSONALES EN PYTHON
  Instituto Superior Universitario Espíritu Santo - TES
  Carrera: Desarrollo de Aplicaciones Web
  Módulo I - Fundamentos de Programación - 2026
  Autores: Salazar Delgado Duverly Sebastián
           Vera Quiles Ronald Anibal
  Profesora: MSIG. Yessica María Armijos Farez
=============================================================
"""

import os
import datetime

# ─────────────────────────────────────────────────────────────
#  SEÑAL DE CANCELACIÓN (opción 0 dentro de sub-menús)
# ─────────────────────────────────────────────────────────────
class Cancelar(Exception):
    """Se lanza cuando el usuario escribe 0 para volver al menú principal."""
    pass

# ─────────────────────────────────────────────────────────────
#  CONSTANTES
# ─────────────────────────────────────────────────────────────
ARCHIVO_TAREAS = "tareas.txt"
PRIORIDADES    = {"1": "Alta", "2": "Media", "3": "Baja"}
LINEA          = "=" * 65


# ─────────────────────────────────────────────────────────────
#  FUNCIONES DE PERSISTENCIA (archivos de texto)
# ─────────────────────────────────────────────────────────────
def cargar_tareas():
    """Lee el archivo y devuelve la lista de tareas (diccionarios)."""
    tareas = []
    if not os.path.exists(ARCHIVO_TAREAS):
        return tareas
    try:
        with open(ARCHIVO_TAREAS, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split("|")
                if len(partes) == 5:
                    tareas.append({
                        "id":          int(partes[0]),
                        "titulo":      partes[1],
                        "descripcion": partes[2],
                        "prioridad":   partes[3],
                        "completada":  partes[4] == "True",
                        "fecha":       ""
                    })
                elif len(partes) == 6:
                    tareas.append({
                        "id":          int(partes[0]),
                        "titulo":      partes[1],
                        "descripcion": partes[2],
                        "prioridad":   partes[3],
                        "completada":  partes[4] == "True",
                        "fecha":       partes[5]
                    })
    except Exception as e:
        print(f"  [!] Error al leer tareas: {e}")
    return tareas


def guardar_tareas(tareas):
    """Escribe todas las tareas en el archivo de texto."""
    try:
        with open(ARCHIVO_TAREAS, "w", encoding="utf-8") as f:
            for t in tareas:
                f.write(
                    f"{t['id']}|{t['titulo']}|{t['descripcion']}|"
                    f"{t['prioridad']}|{t['completada']}|{t['fecha']}\n"
                )
    except Exception as e:
        print(f"  [!] Error al guardar tareas: {e}")


def siguiente_id(tareas):
    """Genera el próximo identificador único."""
    return max((t["id"] for t in tareas), default=0) + 1


# ─────────────────────────────────────────────────────────────
#  VALIDACIONES
# ─────────────────────────────────────────────────────────────
def validar_opcion(prompt, opciones_validas, cancelable=False):
    """Solicita al usuario una opción hasta que sea válida.
    Si cancelable=True y escribe '0', lanza Cancelar para volver al menú."""
    while True:
        valor = input(prompt).strip()
        if cancelable and valor == "0":
            raise Cancelar
        if valor in opciones_validas:
            return valor
        print(f"  [!] Opción inválida. Elija entre: {', '.join(opciones_validas)}"
              + ("  |  0 = volver al menú" if cancelable else ""))


def validar_texto(prompt, minimo=3):
    """Solicita texto no vacío con longitud mínima.
    Si el usuario escribe '0', lanza Cancelar."""
    while True:
        valor = input(prompt).strip()
        if valor == "0":
            raise Cancelar
        if len(valor) >= minimo:
            return valor
        print(f"  [!] Debe ingresar al menos {minimo} caracteres.  |  0 = volver al menú")


def validar_id_tarea(tareas, prompt="  Número de tarea (0 = menú): "):
    """Solicita un ID de tarea válido. Escribe 0 para volver al menú."""
    ids_validos = [str(t["id"]) for t in tareas]
    while True:
        valor = input(prompt).strip()
        if valor == "0":
            raise Cancelar
        if valor in ids_validos:
            return int(valor)
        print("  [!] ID no encontrado. Verifique el número de tarea.  |  0 = volver al menú")


# ─────────────────────────────────────────────────────────────
#  MÓDULOS PRINCIPALES
# ─────────────────────────────────────────────────────────────
def agregar_tarea(tareas):
    """Permite al usuario crear una nueva tarea."""
    print("\n  ── NUEVA TAREA ──  (escriba 0 en cualquier momento para volver al menú)")
    titulo      = validar_texto("  Título        : ")
    descripcion = validar_texto("  Descripción   : ")
    print("  Prioridad → 1=Alta  2=Media  3=Baja  |  0=menú")
    opcion      = validar_opcion("  Seleccione    : ", ["1", "2", "3"], cancelable=True)
    prioridad   = PRIORIDADES[opcion]
    fecha       = datetime.date.today().strftime("%d/%m/%Y")

    tarea = {
        "id":          siguiente_id(tareas),
        "titulo":      titulo,
        "descripcion": descripcion,
        "prioridad":   prioridad,
        "completada":  False,
        "fecha":       fecha
    }
    tareas.append(tarea)
    guardar_tareas(tareas)
    print(f"\n  ✔ Tarea #{tarea['id']} agregada correctamente.")


def listar_tareas(tareas, solo_pendientes=False):
    """Muestra la lista de tareas con formato tabular."""
    filtradas = [t for t in tareas if not t["completada"]] if solo_pendientes else tareas

    if not filtradas:
        print("\n  (No hay tareas para mostrar.)")
        return

    encabezado = f"  {'#':>3}  {'TÍTULO':<25}  {'PRIORIDAD':<8}  {'ESTADO':<12}  {'FECHA'}"
    print(f"\n{LINEA}")
    print(encabezado)
    print(LINEA)
    for t in filtradas:
        estado = "✔ Completada" if t["completada"] else "⏳ Pendiente"
        print(
            f"  {t['id']:>3}  {t['titulo'][:25]:<25}  {t['prioridad']:<8}  {estado:<12}  {t['fecha']}"
        )
    print(LINEA)
    print(f"  Total: {len(filtradas)} tarea(s).\n")


def marcar_completada(tareas):
    """Marca una tarea como completada."""
    pendientes = [t for t in tareas if not t["completada"]]
    if not pendientes:
        print("\n  (No hay tareas pendientes.)")
        return
    print("  (escriba 0 para volver al menú)")
    listar_tareas(pendientes)
    tid = validar_id_tarea(pendientes)
    for t in tareas:
        if t["id"] == tid:
            t["completada"] = True
            guardar_tareas(tareas)
            print(f"\n  ✔ Tarea #{tid} marcada como completada.")
            return


def eliminar_tarea(tareas):
    """Elimina una tarea de la lista."""
    if not tareas:
        print("\n  (No hay tareas registradas.)")
        return
    print("  (escriba 0 para volver al menú)")
    listar_tareas(tareas)
    tid = validar_id_tarea(tareas)
    while True:
        confirmacion = input(f"  ¿Eliminar tarea #{tid}? (sí / no): ").strip().lower()
        if confirmacion == "0":
            raise Cancelar
        if confirmacion in ("sí", "si"):
            tareas[:] = [t for t in tareas if t["id"] != tid]
            guardar_tareas(tareas)
            print(f"\n  ✔ Tarea #{tid} eliminada.")
            return
        if confirmacion == "no":
            print("  Operación cancelada.")
            return
        print("  [!] Responda sí o no  |  0 = volver al menú")


def buscar_tarea(tareas):
    """Busca tareas por palabra clave en el título o descripción."""
    if not tareas:
        print("\n  (No hay tareas registradas.)")
        return
    palabra = input("  Palabra clave (0 = menú): ").strip().lower()
    if palabra == "0":
        raise Cancelar
    resultados = [
        t for t in tareas
        if palabra in t["titulo"].lower() or palabra in t["descripcion"].lower()
    ]
    if resultados:
        listar_tareas(resultados)
    else:
        print(f"\n  No se encontraron tareas con '{palabra}'.")


def editar_tarea(tareas):
    """Permite modificar el título, descripción o prioridad de una tarea."""
    if not tareas:
        print("\n  (No hay tareas para editar.)")
        return
    print("  (escriba 0 para volver al menú)")
    listar_tareas(tareas)
    tid = validar_id_tarea(tareas)
    for t in tareas:
        if t["id"] == tid:
            print(f"\n  Editando: {t['titulo']}")
            print("  (Deje en blanco para conservar el valor actual  |  0 = volver al menú)")
            nuevo_titulo = input(f"  Nuevo título [{t['titulo']}]: ").strip()
            if nuevo_titulo == "0": raise Cancelar
            nueva_desc   = input(f"  Nueva descripción [{t['descripcion']}]: ").strip()
            if nueva_desc == "0": raise Cancelar
            print("  Prioridad → 1=Alta  2=Media  3=Baja  (Enter para mantener  |  0=menú)")
            nueva_prio   = input(f"  Prioridad actual [{t['prioridad']}]: ").strip()
            if nueva_prio == "0": raise Cancelar

            if nuevo_titulo:
                t["titulo"]      = nuevo_titulo
            if nueva_desc:
                t["descripcion"] = nueva_desc
            if nueva_prio in PRIORIDADES:
                t["prioridad"]   = PRIORIDADES[nueva_prio]

            guardar_tareas(tareas)
            print(f"\n  ✔ Tarea #{tid} actualizada.")
            return


def estadisticas(tareas):
    """Muestra un resumen estadístico de las tareas."""
    total       = len(tareas)
    completadas = sum(1 for t in tareas if t["completada"])
    pendientes  = total - completadas
    alta        = sum(1 for t in tareas if t["prioridad"] == "Alta"   and not t["completada"])
    media       = sum(1 for t in tareas if t["prioridad"] == "Media"  and not t["completada"])
    baja        = sum(1 for t in tareas if t["prioridad"] == "Baja"   and not t["completada"])

    print(f"\n{LINEA}")
    print(f"  ESTADÍSTICAS DEL GESTOR DE TAREAS")
    print(LINEA)
    print(f"  Total de tareas     : {total}")
    print(f"  Completadas         : {completadas}")
    print(f"  Pendientes          : {pendientes}")
    print(f"  ─ Prioridad Alta    : {alta}")
    print(f"  ─ Prioridad Media   : {media}")
    print(f"  ─ Prioridad Baja    : {baja}")
    if total > 0:
        porcentaje = (completadas / total) * 100
        print(f"  Progreso general    : {porcentaje:.1f}%")
    print(LINEA)


# ─────────────────────────────────────────────────────────────
#  MENÚ PRINCIPAL
# ─────────────────────────────────────────────────────────────
def mostrar_menu():
    print(f"\n{LINEA}")
    print(f"   GESTOR DE TAREAS PERSONALES  —  TES  2026")
    print(LINEA)
    print("   1. Agregar nueva tarea")
    print("   2. Listar todas las tareas")
    print("   3. Listar tareas pendientes")
    print("   4. Marcar tarea como completada")
    print("   5. Editar tarea")
    print("   6. Eliminar tarea")
    print("   7. Buscar tarea")
    print("   8. Ver estadísticas")
    print("   0. Salir")
    print(LINEA)


def main():
    tareas = cargar_tareas()
    print("\n  Bienvenido al Gestor de Tareas Personales - TES 2026")

    while True:
        mostrar_menu()
        opcion = validar_opcion(
            "  Seleccione una opción [1-8] (0 = Salir): ",
            [str(i) for i in range(0, 9)]
        )

        try:
            if   opcion == "1": agregar_tarea(tareas)
            elif opcion == "2": listar_tareas(tareas)
            elif opcion == "3": listar_tareas(tareas, solo_pendientes=True)
            elif opcion == "4": marcar_completada(tareas)
            elif opcion == "5": editar_tarea(tareas)
            elif opcion == "6": eliminar_tarea(tareas)
            elif opcion == "7": buscar_tarea(tareas)
            elif opcion == "8": estadisticas(tareas)
            elif opcion == "0":
                print("\n  ¡Hasta luego! Sesión finalizada.\n")
                break
        except Cancelar:
            print("\n  ↩  Volviendo al menú principal...")


# ─────────────────────────────────────────────────────────────
#  PUNTO DE ENTRADA
# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
