import subprocess
import argparse

# Konstante Werte für die ArcSDE-Verbindung
SDE_DATABASE = "arcgisdb"  # Name der ArcSDE Enterprise Geodatabase
SDE_USER = "sde"  # ArcSDE-Benutzer
SDE_PASSWORD = "geodb"  # Passwort für den ArcSDE-Benutzer
SDE_HOST = "localhost"  # ArcSDE-Server
SDE_PORT = "5432"  # PostgreSQL-Port

# Verbindung zu ArcSDE je nach Datenbanktyp
PG_CONNECTION = f"PG:dbname={SDE_DATABASE} user={SDE_USER} password={SDE_PASSWORD} host={SDE_HOST} port={SDE_PORT}"

def convert_gdb_to_arcsde(gdb_path):
    """
    Konvertiert eine FileGeodatabase (.gdb) in eine ArcSDE Enterprise Geodatabase.
    """
    print(f"🚀 Starte Konvertierung von '{gdb_path}' nach ArcSDE PostgreSQL...")

    # OGR2OGR-Befehl für den Import
    ogr_command = [
        "ogr2ogr",
        "-f", "PostgreSQL",
        PG_CONNECTION,
        gdb_path,
        "-nlt", "PROMOTE_TO_MULTI",  # Konvertiert Geometrien in MultiPolygon/MultiLineString
        "-progress",  # Fortschritt anzeigen
        "-overwrite",  # Falls Layer bereits existiert, wird er überschrieben
        "-lco", "SCHEMA=sde",  # Speichert Daten in ArcSDE-Schema
        "-lco", "GEOMETRY_NAME=shape",  # Setzt die Geometriespalte als "shape"
        "-lco", "FID=id"  # Setzt die ID-Spalte als Primary Key
    ]

    # Befehl ausführen
    try:
        result = subprocess.run(ogr_command, check=True, capture_output=True, text=True)
        print("✅ Import erfolgreich abgeschlossen!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Fehler beim Import!")
        print(e.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Importiert eine FileGeodatabase (.gdb) in ArcSDE.")
    parser.add_argument("gdb_path", type=str, help="Pfad zur FileGeodatabase (.gdb)")
    
    args = parser.parse_args()
    convert_gdb_to_arcsde(args.gdb_path)