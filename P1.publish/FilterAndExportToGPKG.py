import geopandas as gpd
path = r'./_data/' 
filename_gpkg = 'ch.so.arp.nutzungsplanung.kommunal.gpkg' 
grundnutzung = gpd.read_file(path+filename_gpkg, layer='grundnutzung')
grundnutzung_wald_lwz=grundnutzung[grundnutzung['typ_bezeichnung'].isin(["Landwirtschaftszone", "Wald"])]
gwl_geom = grundnutzung_wald_lwz.geometry
invalid_count = (~gwl_geom.is_valid).sum()
print(f"Anzahl ungültiger Geometrien: {invalid_count}")
grundnutzung_wald_lwz['area'] = grundnutzung_wald_lwz['geometry'].area
grundnutzung_wald_lwz_max_1ha = grundnutzung_wald_lwz[grundnutzung_wald_lwz['area'] < 10000]
grundnutzung_wald_lwz_max_1ha.to_file(path+"grundnutzung_wald_lwz_max1ha.gpkg", driver="GPKG")