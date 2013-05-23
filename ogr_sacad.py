from osgeo import ogr
import sys
import csv

shpfile='C:\ms4w\Apache\htdocs\sacad\maps\idprov.shp'
datafile='C:\ms4w\Apache\htdocs\sacad\maps\pusair.csv'
outfile='C:\ms4w\Apache\htdocs\sacad\maps\outpusair1.csv'
ds=ogr.Open(shpfile)

#res = ds.ExecuteSQL("select * from idprov where PROVINSI LIKE 'JAWA%'")
#resfeat = res.GetNextFeature()
#while resfeat:
#    print resfeat.GetField('KODE')
#    resfeat = res.GetNextFeature()    


objlyrs=ds.GetLayer() # ambil layer pertama
#objlyrs.SetAttributeFilter("provinsi like 'JAWA%'") # filtering

# iterate fields
#lyrs = objlyrs.GetLayerDefn()
#nc = lyrs.GetFieldCount()
#for i in range(nc):
#    print lyrs.GetFieldDefn(i).GetName()
features=[]
for feat in objlyrs:
        attributes = feat.items()
        provinsi = attributes['PROVINSI']
        print provinsi
        features.append(feat)
#print "======================================"
#pt.AddPoint(-7.252134,109.589996)

#feat = objlyrs.GetFeature(0)
#attributes = feat.items()
#geom = feat.GetGeometryRef()
#print attributes
#print geom.Contains(pt)

#fid = open(datafile,'r')
fout = open(outfile,'w')
#while True:
for line in csv.reader(open(datafile),delimiter=','):
    #line = fid.readline()
    #data = line.split(",")
    if len(line)==0:
        break
    noreg = line[0]
    nosta = line[1]
    nasta = line[2]
    region = line[3]
    owner = line[4]
    ltg = float(line[5])
    bjr = float(line[6])
    tgi = line[7]
    kodeprov = line[8]
    pt = ogr.Geometry(ogr.wkbPoint)
    pt.AddPoint(bjr,ltg)
    isketemu=False
    provinsi=''
    #print nosta,kodeprov,bjr,ltg
    for i in range(len(features)):
        attributes = features[i].items()
        provinsi = attributes['PROVINSI']
        geom = features[i].GetGeometryRef()
        res = geom.Contains(pt)
        dis = geom.Distance(pt)
        #print res
        if (res==True or dis<=0.05):
            isketemu=True
            break
            #print "====================================================="
        #if (dis<=0.05):
        #    isketemu=True
    
    tmpl="%s,%s,%s,%s,%s,%.4f,%.4f,%s,%s,%s,%f\n"
    if isketemu==True:
        tmp=tmpl % (noreg,nosta,nasta,region,owner,ltg,bjr,tgi,kodeprov,isketemu,dis)
        print "+++++++++++++++++++++++++++"
    else:
        dis=-9999
        print "------------------------------------"
        tmp=tmpl % (noreg,nosta,nasta,region,owner,ltg,bjr,tgi,kodeprov,isketemu,dis)
    fout.write(tmp)

fout.close()
