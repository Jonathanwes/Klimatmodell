# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 10:46:12 2022

@author: Jonat
"""

import numpy as np
from mpl_toolkits.basemap import Basemap

def country_outlines(radie=1.1):
    
    def degree2radians(degree):
        #convert degrees to radians
        return degree*np.pi/180
    
    def mapping_map_to_sphere(lon, lat, radius=1):
        #this function maps the points of coords (lon, lat) to points onto the  sphere of radius radius
        
        lon=np.array(lon, dtype=np.float64)
        lat=np.array(lat, dtype=np.float64)
        lon=degree2radians(lon)
        lat=degree2radians(lat)
        xs=radius*np.cos(lon)*np.cos(lat)
        ys=radius*np.sin(lon)*np.cos(lat)
        zs=radius*np.sin(lat)
        return xs, ys, zs

    def polygons_to_traces(poly_paths, N_poly):
        ''' 
        pos arg 1. (poly_paths): paths to polygons
        pos arg 2. (N_poly): number of polygon to convert
        '''
        # init. plotting list
        lons=[]
        lats=[]
    
        for i_poly in range(N_poly):
            poly_path = poly_paths[i_poly]
            
            # get the Basemap coordinates of each segment
            coords_cc = np.array(
                [(vertex[0],vertex[1]) 
                 for (vertex,code) in poly_path.iter_segments(simplify=False)]
            )
            
            # convert coordinates to lon/lat by 'inverting' the Basemap projection
            lon_cc, lat_cc = m(coords_cc[:,0],coords_cc[:,1], inverse=True)
            lats.extend(lat_cc.tolist()+[None]) 
            lons.extend(lon_cc.tolist()+[None])
            
           
        return lons, lats
    
    # Function generating coastline lon/lat 
    def get_coastline_traces():
        poly_paths = m.drawcoastlines().get_paths() # coastline polygon paths
        N_poly = 91  # use only the 91st biggest coastlines (i.e. no rivers)
        cc_lons, cc_lats= polygons_to_traces(poly_paths, N_poly)
        return cc_lons, cc_lats
    
    # Function generating country lon/lat 
    def get_country_traces():
        poly_paths = m.drawcountries().get_paths() # country polygon paths
        N_poly = len(poly_paths)  # use all countries
        country_lons, country_lats= polygons_to_traces(poly_paths, N_poly)
        return country_lons, country_lats

    m = Basemap()
    cc_lons, cc_lats=get_coastline_traces()
    country_lons, country_lats=get_country_traces()
    lons=cc_lons+[None]+country_lons
    lats=cc_lats+[None]+country_lats

    xs, ys, zs=mapping_map_to_sphere(lons, lats, radius=1.1)
    
    return xs, ys , zs
