import yaml
import sacc

import firecrown.likelihood.gauss_family.statistic.source.weak_lensing as WL
import firecrown.likelihood.gauss_family.statistic.source.number_counts as NC

from firecrown.likelihood.gauss_family.gaussian import ConstGaussian

import sys
import os
sys.path.append(os.path.split(__file__)[0])
import likelihood_utils


sacc_file = "../gaussian-sims-srd-sample/data-vector/summary_statistics_real.sacc" 
scale_cut_file = "likelihood/scale_cuts_srd_real.yaml"

statistics = [
              "galaxy_shear_xi_plus",
              "galaxy_shear_xi_minus",
              "galaxy_shearDensity_xi_t",
              "galaxy_density_xi"
              ]

sacc_data = sacc.Sacc.load_fits(sacc_file)
with open(scale_cut_file, "r") as f:
    theta_min_arcmin = yaml.safe_load(f)

n_source, n_lens = likelihood_utils.get_n_tracer(sacc_data)

sources, source_params = likelihood_utils.build_sources(
                                            n_source,
                                            systematics=[
                                                WL.LinearAlignmentSystematic,
                                                WL.PhotoZShift,
                                                WL.MultiplicativeShearBias
                                                ])

lenses, lens_params = likelihood_utils.build_lenses(
                                        n_lens,
                                        systematics=[
                                            NC.PhotoZShift,
                                            ])
stats = likelihood_utils.build_stats(sources, lenses,
                                     statistics=statistics,
                                     scale_cuts=theta_min_arcmin
                                     )

lk = ConstGaussian(statistics=list(stats.values()))

lk.read(sacc_data)
lk.set_params_names(source_params | lens_params)

likelihood = lk
