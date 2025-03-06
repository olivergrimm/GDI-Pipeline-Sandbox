import subprocess
import argparse

def convert_sde_to_gpkg(sde_connection, feature_class, gpkg_path, layer_name):
    """
    Konvertiert eine Feature Class aus ArcSDE in ein GeoPackage (.gpkg)
    """
    print(f"🚀 Starte Konvertierung von Feature Class '{feature_class}' nach '{gpkg_path}'...")

    # OGR2OGR-Befehl für die Konvertierung
    ogr_command = [
        "ogr2ogr",
        "-f", "GPKG",  # Ziel-Format: GeoPackage
        gpkg_path,  # Ziel-Datei
        sde_connection,  # ArcSDE Verbindungsstring
        feature_class,  # Name der Feature Class
        "-progress",  # Fortschritt anzeigen
        "-overwrite",  # Falls das Layer existiert, wird es überschrieben
        "-nlt", "PROMOTE_TO_MULTI"  # Sicherstellen, dass alle Geometrien als MultiPolygon/MultiLine gespeichert werden
    ]

    # Befehl ausführen
    try:
        result = subprocess.run(ogr_command, check=True, capture_output=True, text=True)
        print("✅ Konvertierung erfolgreich abgeschlossen!")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("❌ Fehler bei der Konvertierung!")
        print(e.stderr)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Konvertiert eine Feature Class aus ArcSDE in ein GeoPackage.")
    parser.add_argument("sde_connection", type=str, help="ArcSDE Verbindungsstring (z. B. PG:... oder MSSQL:...)")
    parser.add_argument("feature_class", type=str, help="Name der Feature Class in ArcSDE")
    parser.add_argument("gpkg_path", type=str, help="Pfad zur GeoPackage-Datei (.gpkg)")
    parser.add_argument("--layer_name", type=str, default=None, help="Name des Ziel-Layers im GeoPackage (optional)")

    args = parser.parse_args()
    
    layer_name = args.layer_name if args.layer_name else args.feature_class

    convert_sde_to_gpkg(args.sde_connection, args.feature_class, args.gpkg_path, layer_name)
