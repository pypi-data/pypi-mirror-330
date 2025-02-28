import pandas as pd
from scipy.stats import gamma, halfnorm, uniform

from astro_prost.associate import associate_sample, prepare_catalog
from astro_prost.helpers import SnRateAbsmag
from astropy.coordinates import SkyCoord
import importlib.resources as pkg_resources
import astropy.units as u
import time
import numpy as np

def test_associate_decals_dr10():
    np.random.seed(42)
    
    # associate one known to fail in dr9 but succeed in dr10
    transient_catalog = pd.DataFrame({'IAUID':['AT 2024abyq'], 'RA':[184.912263333], 'Dec':[-29.0635322222]}, index=[0])

    # define priors for properties
    priorfunc_z = halfnorm(loc=0.0001, scale=0.5)
    priorfunc_offset = uniform(loc=0, scale=10)
    priorfunc_absmag = uniform(loc=-30, scale=20)

    likefunc_offset = gamma(a=0.75)
    likefunc_absmag = SnRateAbsmag(a=-30, b=-10)

    priors = {"offset": priorfunc_offset, "absmag": priorfunc_absmag}
    likes = {"offset": likefunc_offset, "absmag": likefunc_absmag}

    # set up properties of the association run
    verbose = 2
    parallel = False
    save = False
    progress_bar = False
    cat_cols = False

    # list of catalogs to search -- options are (in order) glade, decals, panstarrs
    catalogs = [("decals", "dr10")]

    # the name of the coord columns in the dataframe
    transient_coord_cols = ("RA", "Dec")

    # the column containing the transient names
    transient_name_col = "IAUID"

    transient_catalog = prepare_catalog(
        transient_catalog, transient_name_col=transient_name_col, transient_coord_cols=transient_coord_cols
    )

    # cosmology can be specified, else flat lambdaCDM is assumed with H0=70, Om0=0.3, Ode0=0.7
    hostTable = associate_sample(
        transient_catalog,
        run_name="decals_test",
        priors=priors,
        likes=likes,
        catalogs=catalogs,
        parallel=parallel,
        verbose=verbose,
        save=save,
        log_path='./',
        progress_bar=progress_bar,
        cat_cols=cat_cols,
        calc_host_props=False,
    )

    host_coord = SkyCoord(hostTable['host_ra'].values[0], hostTable['host_dec'].values[0], unit=(u.deg, u.deg))
    true_coord = SkyCoord(184.90550975, -29.06745087, unit=(u.deg, u.deg))
    assert (host_coord.separation(true_coord).arcsec <= 1) and (hostTable['best_cat_release'].values[0] == 'dr10')

