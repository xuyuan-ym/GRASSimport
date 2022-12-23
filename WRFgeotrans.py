from osgeo import gdal
from osgeo import osr
import pyproj
import osr
filename='wrfout_d01_2013-05-11_02:00:00'
#######read metadata its kinda mess but if we try , we can find somthing useful.....
print(f"procssing file {filename}")
ds_in=gdal.Open(filename)
metadata=ds_in.GetMetadata()
#print(f"metadata is {metadata.MY_PROJ}")
#######read XLAT and XLONG data set
xlat_in=gdal.Open('NETCDF:"'+filename+'":XLAT')
lats = xlat_in.GetRasterBand(1).ReadAsArray()
########## the order L->R is (z,y(lat),x(long)) 
#print(lats[142,172])  
########## the map read is from lefup [0,0] rightup[0,sizeoflong] leftlow[sizeoflat] rightlow[sizeoflat,sizeoflong]
xlong_in=gdal.Open('NETCDF:"'+filename+'":XLONG')
longs = xlong_in.GetRasterBand(1).ReadAsArray()




#setting the input wrfproj->proj_wrf and target proj proh->gcp in this case EPSG:4326 
proj_wrf=osr.SpatialReference()
proj_wrf.SetPS(39,110,1,0,0)
proj_gcp=osr.SpatialReference()
proj_gcp.ImportFromEPSG(4326)

transf=osr.CoordinateTransformation(proj_gcp, proj_wrf)
ll=transf.TransformPoint(float(longs[0,0]),float(lats[0,0])) #order longs , lat, but not understand why this order
print('after transfer\n')
print(ll)


