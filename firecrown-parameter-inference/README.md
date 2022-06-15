The likelihoods are defined in
- `likelihood/star_3x2pt.py`: the 3x2pt setup
- `likelihood/star_EE_only.py`: cosmic shear only
- `likelihood/star_nn_only.py`: galaxy clustering only

The likelihoods make use of a set of common routines in `likelihood/likelihood_utils.py`.

The scale cuts are being computed with `utils/scale_cuts.ipynb`.

The `sacc` file is currently a Frankensteinian abomination that hacks together the "data" and covariance until TXPipe can do this consistently.

Chains/Fisher forecast/test runs are run with CosmoSIS from this directory (adjust the sampler in the .ini files accordingly):
```
cosmosis cosmosis/star_3x2pt.ini
```
```
cosmosis cosmosis/star_EE_only.ini
```
```
cosmosis cosmosis/star_nn_only.ini
```