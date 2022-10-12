from .matte import klimatmodell_kontroll as km
from .matte import sphere
from .matte import spherical_country_outlines


def create_1d_model(resolution,itterationer) -> km.klimatmodell_kontroll:
    klimatmodell_1d=km.klimatmodell_kontroll(klimatmodell=km.klimatmodell_start(resolution))
    klimatmodell_1d.itterera(itterationer)
    return klimatmodell_1d

def create_sphere(resolution):
    sphere_coords=sphere.sfär(resolution)
    country_outlines=spherical_country_outlines.country_outlines(1.05)
    return sphere_coords,country_outlines