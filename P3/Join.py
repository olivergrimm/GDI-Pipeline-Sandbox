from osgeo import ogr

# Pfad zur FileGeodatabase
GDB_PATH = "C:/GIS/data.gdb"

# Namen der Layer
BASE_LAYER_NAME = "Parzellen"
JOIN_LAYER_NAME = "Eigentümer"

# Gemeinsames Feld für den Join
JOIN_FIELD = "Flurstueck_ID"

# Name des neuen Layer mit Join
OUTPUT_LAYER_NAME = "Parzellen_mit_Eigentuemer"

def join_layers():
    # FileGeodatabase öffnen
    driver = ogr.GetDriverByName("OpenFileGDB")
    datasource = driver.Open(GDB_PATH, 1)  # 1 = Schreibmodus

    if datasource is None:
        print(f"Fehler: FileGDB '{GDB_PATH}' konnte nicht geöffnet werden.")
        return

    # Layer abrufen
    base_layer = datasource.GetLayerByName(BASE_LAYER_NAME)
    join_layer = datasource.GetLayerByName(JOIN_LAYER_NAME)

    if base_layer is None or join_layer is None:
        print(f"Fehler: Ein oder beide Layer ({BASE_LAYER_NAME}, {JOIN_LAYER_NAME}) existieren nicht.")
        return

    # Join ausführen
    print(f"Führe Join zwischen '{BASE_LAYER_NAME}' und '{JOIN_LAYER_NAME}' über '{JOIN_FIELD}' aus...")
    base_layer.SetAttributeFilter(f"{JOIN_FIELD} IN (SELECT {JOIN_FIELD} FROM {JOIN_LAYER_NAME})")

    # Neues Layer für das Join-Ergebnis erstellen
    output_layer = datasource.CreateLayer(OUTPUT_LAYER_NAME, base_layer.GetSpatialRef(), base_layer.GetGeomType())

    # Felder aus dem Basistable übernehmen
    layer_defn = base_layer.GetLayerDefn()
    for i in range(layer_defn.GetFieldCount()):
        output_layer.CreateField(layer_defn.GetFieldDefn(i))

    # Felder aus der Eigentümer-Tabelle hinzufügen