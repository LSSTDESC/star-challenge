import yaml
import sacc

import firecrown.likelihood.gauss_family.statistic.source.weak_lensing as WL
import firecrown.likelihood.gauss_family.statistic.source.number_counts as NC

from firecrown.likelihood.gauss_family.gaussian import ConstGaussian

import sys
import os
sys.path.append(os.path.split(__file__)[0])
import likelihood_utils


#sacc_file = "../gaussian-sims-srd-sample/data-vector/twopoint_theory_fourier_with_cov.sacc"   # noqa: E501
sacc_file = "../gaussian-sims-srd-sample/data-vector/summary_statistics_fourier_shot_noise_scaled.sacc"   # noqa: E501
scale_cut_file = "likelihood/scale_cuts_srd.yaml"

statistics = [
              "galaxy_shear_cl_ee",
              "galaxy_shearDensity_cl_e",
              "galaxy_density_cl"
              ]

sacc_data = sacc.Sacc.load_fits(sacc_file)
with open(scale_cut_file, "r") as f:
    ell_max = yaml.safe_load(f)

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
                                     scale_cuts=ell_max
                                     )

lk = ConstGaussian(statistics=list(stats.values()))

lk.read(sacc_data)
lk.set_params_names(source_params | lens_params)

likelihood = lk
