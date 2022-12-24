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
proj_wrf.SetPS(38.999996,110,1,30,60)
proj_gcp=osr.SpatialReference()
proj_gcp.ImportFromEPSG(4326)
####test tranfermation using center###########
####basically the transform is using meter as unit and it means how far meter is goes from the input coordinate
transf=osr.CoordinateTransformation(proj_gcp, proj_wrf)
#cc=transf.TransformPoint(float(40),float(122))
##############################################

#concer transfer #the output order is (x,y,z)
ul=transf.TransformPoint(float(lats[0,0]),float(longs[0,0])) #order longs , lat, but not understand why this order
ur=transf.TransformPoint(float(lats[0,172]),float(longs[0,172]))
ll=transf.TransformPoint(float(lats[142,0]),float(longs[142,0]))
lr=transf.TransformPoint(float(lats[142,172]),float(longs[142,172]))
print('after transfer\n')
print(f"upper left corner [0,0] lats moving {ul[0]}, longs moving {ul[1]}")
print(f"upper right corner [0,172] lats moving {ur[0]}, longs moving {ur[1]}")
print(f"lower left corner [142,0] lats moving {ll[0]}, longs moving {ll[1]}")
print(f"lower right corner [142,172] lats moving {lr[0]}, longs moving {lr[1]}")

#define the upper boundary x direction resolution (upper and lower boundary share the same resolution).
#https://www.usgs.gov/faqs/how-much-distance-does-degree-minute-and-second-cover-your-maps 
# longitude 1 degree = 54.6 miles = 87870 meter
x1=ul[0]
x2=(ur[0]-x1)/len(longs[0])/87870
print(f"upper boundary x resolution = {x2} with len {len(longs[0])}")
#define the left boundary y direction resolution (left and right boundary share the same reolution).
# latitude 1 degree = 69 miles = 111045
y1=ul[1]
y2=(ll[1]-y1)/len(longs)/111045
print(f"left boundary y resolution = {y2} with len {len(longs)}")


