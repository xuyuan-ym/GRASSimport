import pyproj
import osr
wrfprj=pyproj.Proj(proj='lcc',lat_1=30,lat_2=60,lat_0=38.99996,lon_0=98,a=6370000,b=6370000)
#print(wrfprj)
epsgprj = pyproj.Proj(proj='latlong',datum='WGS84')
#print(epsgprj)
e,n=pyproj.transform(epsgprj,wrfprj,110,38.999996)
grasse,grassn=pyproj.transform(epsgprj,wrfprj,107,45)
grasse_max,grassn_max=pyproj.transform(epsgprj,wrfprj,122,45)
print(f"e is \"{e}\"n is \"{n}\"")
print(f"type of n is {type(n)}")
x0=e-(15000)*(172)/2
y0=n-(15000)*(142)/2
print(f"lower left is {x0},{y0} ")
lon_back,lat_back=pyproj.transform(wrfprj,epsgprj,x0,y0)
print(f"return lower left back is [{lon_back},{lat_back}]")
cenlon_b,cenlat_b=pyproj.transform(wrfprj,epsgprj,e,n)
print(f"return center back is [{cenlon_b},{cenlat_b}]")
grasseb,grassnb=pyproj.transform(wrfprj,epsgprj,grasse,grassn)
print(f"return grasslowerleft corner  back is [{grasseb},{grassnb}]")
grasse_maxb,grassn_maxb=pyproj.transform(wrfprj,epsgprj,grasse_max,grassn_max)
print(f"return grassupperleft corner  back is [{grasse_maxb},{grassn_maxb}]")


