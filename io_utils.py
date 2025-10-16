# io_utils.py
"""
Basisfunktionen für Dateihandling und IO-Operationen
"""

from pathlib import Path
import shutil
import pandas as pd
from typing import Any


# -------------------------
# Lesen
# -------------------------
def load_file(filepath: str | Path) -> Any:
    """
    Intelligentes Einlesen einer Datei basierend auf der Dateiendung.

    Unterstützt:
    - .csv -> pandas.DataFrame

    Best Effort:
    - Unbekannte Endung -> als Text einlesen und String zurückgeben.
    - Falls Datei fehlt -> FileNotFoundError.
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")

    ext = filepath.suffix.lower()

    if ext == ".csv":
        return pd.read_csv(filepath)

    # Fallback: Text lesen
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


# -------------------------
# Schreiben
# -------------------------
def save_file(
    data: Any,
    folder: str | Path,
    filename: str,
    filetype: str = "csv",
    overwrite: bool = False
) -> Path:
    """
    Intelligentes Speichern einer Datei basierend auf dem angegebenen Typ.

    Unterstützt:
    - "csv" -> pandas.DataFrame.to_csv()

    Best Effort:
    - Wenn Typ nicht unterstützt -> als Plaintext .txt speichern.

    Parameters
    ----------
    data : Any
        Datenobjekt (z. B. DataFrame oder String).
    folder : str | Path
        Zielordner.
    filename : str
        Dateiname (ohne Extension).
    filetype : str
        Dateityp ("csv", "txt", ...). Default: "csv".
    overwrite : bool
        Falls True -> bestehende Datei überschreiben.

    Returns
    -------
    Path
        Pfad zur gespeicherten Datei.
    """
    folder = Path(folder)
    create_folderpath(folder)

    filepath = folder / f"{filename}.{filetype}"

    if filepath.exists() and not overwrite:
        raise FileExistsError(f"File already exists: {filepath}")

    if filetype == "csv" and isinstance(data, pd.DataFrame):
        data.to_csv(filepath, index=False)
    else:
        # Fallback: Text speichern
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(str(data))

    return filepath


# -------------------------
# Existence Checks
# -------------------------
def file_exists(filepath: str | Path) -> bool:
    """
    Prüft, ob eine Datei existiert.
    """
    return Path(filepath).is_file()


def folder_exists(folderpath: str | Path) -> bool:
    """
    Prüft, ob ein Ordner existiert.
    """
    return Path(folderpath).is_dir()


# -------------------------
# Move
# -------------------------
def move_file(
    src: str | Path,
    dst: str | Path,
    overwrite: bool = False
) -> Path:
    """
    Verschiebt eine Datei an einen Zielpfad.

    - Falls Ordner im Zielpfad nicht existiert -> automatisch erstellen.
    - Falls Datei existiert:
        - overwrite=False -> Exception
        - overwrite=True -> ersetzen
    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    create_folderpath(dst.parent)

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Target file already exists: {dst}")

    shutil.move(str(src), str(dst))
    return dst



def copy_file(
    src: str | Path,
    dst: str | Path,
    overwrite: bool = False
) -> Path:
    """
    Kopiert eine Datei an einen Zielpfad.

    - Falls Ordner im Zielpfad nicht existiert -> automatisch erstellen.
    - Falls Datei existiert:
        - overwrite=False -> Exception
        - overwrite=True -> ersetzen

    Parameters
    ----------
    src : str | Path
        Quellpfad.
    dst : str | Path
        Zielpfad (inkl. Dateiname).
    overwrite : bool
        Verhalten bei existierender Datei.

    Returns
    -------
    Path
        Zielpfad der kopierten Datei.
    """
    src = Path(src)
    dst = Path(dst)

    if not src.exists():
        raise FileNotFoundError(f"Source file does not exist: {src}")

    create_folderpath(dst.parent)

    if dst.exists() and not overwrite:
        raise FileExistsError(f"Target file already exists: {dst}")

    shutil.copy2(str(src), str(dst))  # copy2 -> behält Metadaten
    return dst


# -------------------------
# Folder Creation
# -------------------------
def create_folderpath(path: str | Path) -> Path:
    """
    Erstellt alle fehlenden Ordner im angegebenen Pfad (rekursiv).
    Wenn Ordner schon existiert, passiert nichts.
    """
    path = Path(path)
    path.mkdir(parents=True, exist_ok=True)
    return path
