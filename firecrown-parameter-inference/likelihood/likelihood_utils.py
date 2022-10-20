
import firecrown.likelihood.gauss_family.statistic.source.weak_lensing as WL
import firecrown.likelihood.gauss_family.statistic.source.number_counts as NC

from firecrown.likelihood.gauss_family.statistic.two_point import TwoPoint


def get_n_tracer(sacc_data):
    source_names = set()
    lens_names = set()

    for data_type in sacc_data.get_data_types():
        tracers = sacc_data.get_tracer_combinations(data_type)
        for tracer_names in tracers:
            for tracer_name in tracer_names:
                if "source" in tracer_name:
                    source_names.add(tracer_name)
                elif "lens" in tracer_name:
                    lens_names.add(tracer_name)
                else:
                    raise ValueError(f"Unknown tracer type {tracer_name}!")

    n_source = len(source_names)
    n_lens = len(lens_names)

    return n_source, n_lens


def build_sources(n_source, systematics=None, params=None):
    if systematics is None:
        systematics = []

    if params is None:
        params = set()

    WL_systematics = []

    if WL.LinearAlignmentSystematic in systematics:
        params.add("ia_bias")
        params.add("alphaz")
        params.add("alphag")
        params.add("z_piv")

        lai_systematic = WL.LinearAlignmentSystematic(sacc_tracer="")

        WL_systematics.append(lai_systematic)

    sources = {}

    for i in range(n_source):
        if WL.MultiplicativeShearBias in systematics:
            mbias = WL.MultiplicativeShearBias(sacc_tracer=f"source_{i}")
            params.add(f"source_{i}_mult_bias")
            WL_systematics.append(mbias)

        if WL.PhotoZShift in systematics:
            pzshift = WL.PhotoZShift(sacc_tracer=f"source_{i}")
            params.add(f"source_{i}_delta_z")
            WL_systematics.append(pzshift)

        sources[f"source_{i}"] = WL.WeakLensing(
            sacc_tracer=f"source_{i}",
            systematics=WL_systematics
        )

    return sources, params


def build_lenses(n_lens, systematics=None, params=None):
    if systematics is None:
        systematics = []

    if params is None:
        params = set()

    NC_systematics = []

    sources = {}

    for i in range(n_lens):
        if NC.PhotoZShift in systematics:
            pzshift = NC.PhotoZShift(sacc_tracer=f"lens_{i}")
            params.add(f"lens_{i}_delta_z")
            NC_systematics.append(pzshift)

        sources[f"lens_{i}"] = NC.NumberCounts(
            sacc_tracer=f"lens_{i}",
            systematics=NC_systematics
        )
        params.add(f"lens_{i}_bias")

    return sources, params


def build_stats(sources, lenses, statistics, scale_cuts=None):
    stats = {}

    n_source = len(sources)
    n_lens = len(lenses)

    for stat in statistics:
        if isinstance(stat, str):
            # Use default bin combinations
            sacc_stat = stat
        else:
            # TODO: Implement custom bin combinations
            raise NotImplementedError(f"Statistic {stat} not supported. "
                                      f"It must be a sacc two-point statistic")

        if sacc_stat in ["galaxy_shear_cl_ee",
                         "galaxy_shear_xi_plus", "galaxy_shear_xi_minus"]:
            for i in range(n_source):
                for j in range(i+1):
                    source0 = f"source_{i}"
                    source1 = f"source_{j}"

                    if scale_cuts is not None:
                        if sacc_stat in ["galaxy_shear_cl_ee"]:
                            ell_or_theta_min = None
                            ell_or_theta_max = scale_cuts[f"{source0}-{source1}"]
                        if sacc_stat in ["galaxy_shear_xi_plus", "galaxy_shear_xi_minus"]:
                            ell_or_theta_min = scale_cuts[f"{source0}-{source1}"]
                            ell_or_theta_max = None
                    else:
                        ell_or_theta_min = None
                        ell_or_theta_max = None

                    if (ell_or_theta_min is None) and (ell_or_theta_max is None):
                        print(f"No overlap between redshift kernels for "
                              f"{source0}-{source1}")
                        continue


                    stats[f"{stat}{source0}_{source1}"] = TwoPoint(
                        source0=sources[source0],
                        source1=sources[source1],
                        sacc_data_type=sacc_stat,
                        ell_or_theta_min=ell_or_theta_min,
                        ell_or_theta_max=ell_or_theta_max,
                    )
        elif sacc_stat in ["galaxy_shearDensity_cl_e",
                           "galaxy_shearDensity_xi_t"]:
            for i in range(n_source):
                for j in range(n_lens):
                    source0 = f"source_{i}"
                    source1 = f"lens_{j}"

                    if scale_cuts is not None:
                        if sacc_stat in ["galaxy_shearDensity_cl_e"]:
                            ell_or_theta_min = None
                            ell_or_theta_max = scale_cuts[f"{source0}-{source1}"]
                        if sacc_stat in ["galaxy_shearDensity_xi_t"]:
                            ell_or_theta_min = scale_cuts[f"{source0}-{source1}"]
                            ell_or_theta_max = None

                    else:
                        ell_or_theta_min = None
                        ell_or_theta_max = None

                    if (ell_or_theta_min is None) and (ell_or_theta_max is None):
                        print(f"No overlap between redshift kernels for "
                              f"{source0}-{source1}")
                        continue

                    stats[f"{stat}{source0}_{source1}"] = TwoPoint(
                        source0=sources[source0],
                        source1=lenses[source1],
                        sacc_data_type=sacc_stat,
                        ell_or_theta_min=ell_or_theta_min,
                        ell_or_theta_max=ell_or_theta_max,
                    )
        elif sacc_stat in ["galaxy_density_cl",
                           "galaxy_density_xi"]:
            for i in range(n_lens):
                
                # TODO: Should add option for cross-correlations
                for j in range(i, i+1):
                    
                    source0 = f"lens_{i}"
                    source1 = f"lens_{j}"

                    if scale_cuts is not None:
                        if sacc_stat in ["galaxy_density_cl"]:
                            ell_or_theta_min = None
                            ell_or_theta_max = scale_cuts[f"{source0}-{source1}"]
                           

                        if sacc_stat in ["galaxy_density_xi"]:
                            ell_or_theta_min = scale_cuts[f"{source0}-{source1}"]
                            ell_or_theta_max = None
                    else:
                        ell_or_theta_min = None
                        ell_or_theta_max = None

                    if (ell_or_theta_min is None) and (ell_or_theta_max is None):
                            print(f"No overlap between redshift kernels for "
                                  f"{source0}-{source1}")
                            continue

                    stats[f"{stat}{source0}_{source1}"] = TwoPoint(
                        source0=lenses[source0],
                        source1=lenses[source1],
                        sacc_data_type=sacc_stat,
                        ell_or_theta_min=ell_or_theta_min,
                        ell_or_theta_max=ell_or_theta_max,
                    )

    return stats
