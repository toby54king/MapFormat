#!/usr/bin/python3

__author__ = 'ISmileLi'

from osgeo import gdal, ogr, osr
from pyproj import Transformer

'''
osgeo底层坐标转换使用的库还是proj,下面函数中的espg值需要根据自己的需求进行修改，
下文测试使用的是wgs84与中国区高斯-克吕格EPSG码为21460区的转换
'''

def lonLat_to_gauss(lon, lat, from_epsg=4326, to_epsg=21460):
    '''
    经纬度转高斯
    :param lon:
    :param lat:
    :param from_epsg:
    :param to_EPSG:
    :return:
    '''

    from_spa = osr.SpatialReference()
    '''
    gdal版本大于3.0以后必须设置转换策略才能正确显示结果，否则结果将会输出'inf'
    可以了解官方的这个issue说明：https://github.com/OSGeo/gdal/issues/1546
    '''
    if int(gdal.__version__[0]) >= 3:
        from_spa.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    from_spa.ImportFromEPSG(from_epsg)
    to_spa = osr.SpatialReference()
    to_spa.ImportFromEPSG(to_epsg)
    coord_trans = osr.CoordinateTransformation(from_spa, to_spa)

    t = coord_trans.TransformPoint(lon, lat)
    return t[0], t[1]

def gauss_to_lonLat(x, y, from_epsg=21460, to_epsg=4326):
    '''
    高斯转经纬度
    :param x:
    :param y:
    :param from_epsg:
    :param to_EPSG:
    :return:
    '''

    from_spa = osr.SpatialReference()
    #if int(gdal.__version__[0]) >= 3:
        #from_spa.SetAxisMappingStrategy(osr.OAMS_TRADITIONAL_GIS_ORDER)
    from_spa.ImportFromEPSG(from_epsg)
    to_spa = osr.SpatialReference()
    to_spa.ImportFromEPSG(to_epsg)
    coord_trans = osr.CoordinateTransformation(from_spa, to_spa)

    t = coord_trans.TransformPoint(x, y)
    return t[0], t[1]


def lonLat_to_gauss_proj(lon, lat, from_epsg="EPSG:4326", to_epsg="EPSG:21460"):
    '''
    使用proj库经纬度转高斯
    :param lon:
    :param lat:
    :param from_epsg:
    :param to_epsg:
    :return:
    '''
    transfromer = Transformer.from_crs(from_epsg, to_epsg,always_xy=True)  # WGS-84对应码->EPSG:4326, 中国高斯对应码：EPSG:21460
    x, y = transfromer.transform(lon, lat)
    print('lonLat_to_gauss_proj x, y:',x, y)
    return x, y

def gauss_to_lonLat_proj(x, y, from_epsg="EPSG:21460", to_epsg="EPSG:4326"):
    '''
    使用proj库高斯转经纬度
    :param x:
    :param y:
    :param from_epsg:
    :param to_epsg:
    :return:
    '''
    transfromer = Transformer.from_crs(from_epsg, to_epsg, always_xy=True)  # WGS-84对应码->EPSG:4326, 中国高斯对应码：EPSG:21460
    lon, lat = transfromer.transform(x, y)
    print('lonLat_to_gauss_proj lon, lat:', lon, lat)
    return lon, lat

if __name__ == '__main__':
    lon = 116.2446370442708300
    lat = 40.0670713975694400
    x, y = lonLat_to_gauss(lon, lat)
    print('x, y: ', x, y)
    lat_t, lon_t = gauss_to_lonLat(x, y)
    print('lon_t, lat_t: ', lon_t, lat_t)

    '''
    这里要注意pyproj的转换会交换x/y返回，可以对比osgeo使用打印结果看出来，
    详细了解可以参考官网文档：https://pyproj4.github.io/pyproj/stable/api/transformer.html
    '''
    lon_t = 116.2446370442708300
    lat_t = 40.0670713975694400
    x_t, y_t = lonLat_to_gauss_proj(lon_t, lat_t)
    gauss_to_lonLat_proj(x_t, y_t)