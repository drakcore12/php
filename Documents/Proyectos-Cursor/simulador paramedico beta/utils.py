"""
utils.py
---------
Utilidades para manejo de mensajes y logging en la aplicación simulador paramédico.
Centraliza la gestión de mensajes emergentes y el registro de logs.

Ejemplo de uso:
    from utils import mostrar_error, mostrar_info, mostrar_advertencia
    mostrar_error("Ocurrió un error grave")
    mostrar_info("Operación exitosa")
    mostrar_advertencia("Campo obligatorio vacío")
"""

import logging
import tkinter as tk
from tkinter import messagebox


def setup_logger(logfile: str = 'simulador.log') -> None:
    """
    Configura el logger para registrar errores en un archivo.
    Args:
        logfile: Nombre del archivo de log.
    """
    logging.basicConfig(
        filename=logfile,
        level=logging.ERROR,
        format='%(asctime)s %(levelname)s:%(message)s'
    )


def mostrar_error(msg: str, titulo: str = "Error") -> None:
    """
    Muestra un mensaje de error en un messagebox y lo registra en el log.
    Args:
        msg: Mensaje a mostrar al usuario.
        titulo: Título de la ventana del mensaje.
    """
    messagebox.showerror(titulo, msg)
    logging.error(msg)


def mostrar_info(msg: str, titulo: str = "Información") -> None:
    """
    Muestra un mensaje informativo en un messagebox y lo registra en el log.
    Args:
        msg: Mensaje a mostrar al usuario.
        titulo: Título de la ventana del mensaje.
    """
    messagebox.showinfo(titulo, msg)
    logging.info(msg)


def mostrar_advertencia(msg: str, titulo: str = "Advertencia") -> None:
    """
    Muestra un mensaje de advertencia en un messagebox y lo registra en el log.
    Args:
        msg: Mensaje a mostrar al usuario.
        titulo: Título de la ventana del mensaje.
    """
    messagebox.showwarning(titulo, msg)
    logging.warning(msg)
