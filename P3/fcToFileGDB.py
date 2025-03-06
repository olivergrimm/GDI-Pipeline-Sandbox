from osgeo import ogr
from loguru import logger

# Log-Datei konfigurieren
logger.add("/Logs/fcToFileGDB.log", rotation="1 MB", level="INFO")

# ArcSDE Datenbankverbindung (DSN oder direkt als Connection-String)
SDE_CONNECTION = "PG:dbname='arcgisdb' host='sde-server' user='myuser' password='mypassword' port='5432'"

# Quelle: ArcSDE Feature Class
SDE_LAYER_NAME = "sde.MY_FEATURECLASS"

# Ziel: FileGeodatabase
GDB_PATH = "C:/GIS/output.gdb"
GDB_LAYER_NAME = "MY_FEATURECLASS_COPY"

def convert_sde_to_gdb():
    # Öffne die ArcSDE-Datenquelle
    source_ds = ogr.Open(SDE_CONNECTION)
    if source_ds is None:
        print("Fehler: ArcSDE-Datenquelle konnte nicht geöffnet werden.")
        logger.error(f"Fehler: ArcSDE-Datenquelle konnte nicht geöffnet werden.")
        return

    # Lade das Feature Class-Layer
    source_layer = source_ds.GetLayerByName(SDE_LAYER_NAME)
    if source_layer is None:
        print(f"Fehler: Layer '{SDE_LAYER_NAME}' wurde nicht gefunden.")
        return

    # Öffne die FileGeodatabase oder erstelle sie
    driver = ogr.GetDriverByName("OpenFileGDB")  # Alternativ: "FileGDB"
    target_ds = driver.Open(GDB_PATH, 1)  # 1 = Schreibmodus

    if target_ds is None:
        print("FileGeodatabase existiert nicht, erstelle neue GDB...")
        driver = ogr.GetDriverByName("FileGDB")
        target_ds = driver.CreateDataSource(GDB_PATH)
        if target_ds is None:
            print("Fehler: Konnte FileGeodatabase nicht erstellen.")
            return

    # Erstelle eine neue Feature Class in der GDB
    target_layer = target_ds.CreateLayer(GDB_LAYER_NAME, source_layer.GetSpatialRef(), source_layer.GetGeomType())

    # Kopiere die Feldstrukturen (Attribute)
    layer_defn = source_layer.GetLayerDefn()
    for i in range(layer_defn.GetFieldCount()):
        target_layer.CreateField(layer_defn.GetFieldDefn(i))

    # Kopiere die Features (Geometrien und Attribute)
    for feature in source_layer:
        new_feature = ogr.Feature(target_layer.GetLayerDefn())
        new_feature.SetGeometry(feature.GetGeometryRef())
        for i in range(layer_defn.GetFieldCount()):
            new_feature.SetField(i, feature.GetField(i))
        target_layer.CreateFeature(new_feature)
        new_feature = None  # Speicher freigeben

    print(f"✅ Erfolgreich '{SDE_LAYER_NAME}' nach '{GDB_LAYER_NAME}' konvertiert!")
    logger.success(f"Erfolgreich '{SDE_LAYER_NAME}' nach '{GDB_LAYER_NAME}' konvertiert!")

    # Schließe die Verbindungen
    source_ds = None
    target_ds = None

if __name__ == "__main__":
    convert_sde_to_gdb()
