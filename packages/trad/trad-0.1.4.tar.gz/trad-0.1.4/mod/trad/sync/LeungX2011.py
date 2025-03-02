# Copyright 2022 Chi-kwan Chan
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Synchrotron emission and bsorption used in Leung et al. (2011)."""


from astropy import constants as c, units as u
from scipy.special import kn # jax does not support kn
from phun import phun

from ..plasma       import u_T_me, gyrofrequency
from ..specradiance import blackbody


@phun({
    'si' : ((u.W      ) / u.sr / u.m**3  / u.Hz, u.m **-1),
    'cgs': ((u.erg/u.s) / u.sr / u.cm**3 / u.Hz, u.cm**-1),
})
def coefficients(u_nu, u_ne, u_Te, u_B, u_theta, u_res='si', backend=None, pol=False):
    r"""Computing the synchrotron emission and absorption.

    An approximation of the synchrotron emissivity and absorptivity at
    given
    frequency               :math:`\nu`,
    electron number density :math:`n_e`,
    electron temperature    :math:`T_e`,
    magnetic field strength :math:`B`, and
    magnetic pitch angle    :math:`\theta`,
    derived by Leung et al. (2011):

    .. math::
        j_\nu
        &= n_e
        \frac{\sqrt{2}\pi e^2 \nu_\mathrm{s}}{3 K_2(1/\Theta_e)c}
        (X^{1/2} + 2^{11/12} X^{1/6})^2 \exp(-X^{1/3}), \\
        \alpha_\nu
        &= j_\nu / B_\nu

    where
    :math:`\Theta_e = k_\mathrm{B}T_e / m_e c^2` is the dimensionless
    electron temperature,
    :math:`\nu_\mathrm{s} = (2/9)\nu_\mathrm{c}\Theta_e^2` is a
    synchrotron characteristic frequency,
    :math:`X = \nu/\nu_\mathrm{s}` is a scaled frequency, and
    :math:`\nu_\mathrm{c} = eB/2\pi m_e` is the electron cyclotron
    frequency.
    The symbols :math:`k_\mathrm{B}`, :math:`m_e`, :math:`e`,
    :math:`c`, :math:`K_2`, and :math:`B_\nu` are the Boltzmann
    constant, electron mass, electron charge, speed of light, modified
    Bessel function of the second kind of order 2, and the Planck's
    law, respectively.

    """
    if pol:
        raise NotImplementedError(
            "`Leung2011` does not implement polarized emissivities")

    pi  = backend.pi
    exp = backend.exp
    sin = backend.sin
    nuc = gyrofrequency(u_B)
    Bnu = blackbody(u_nu, u_Te)

    assert u_res[0] / Bnu.unit == u_res[1]

    r = float(u_theta.to(u.rad))
    t = float(u_T_me.to(u_Te))

    s = float((2/9) / t**2)
    A = float(2**0.5 * (pi/3) * (c.cgs.e.gauss**2/c.c/u.sr) * u_ne * nuc.unit / u_res[0])
    x = float(1 * u_nu / nuc.unit)

    def pure(nu, ne, Te, B, theta):
        nus = s * Te**2 * nuc(B) * sin(theta * r)
        X = x * nu / nus
        Y = (X**(1/2) + 2**(11/12) * X**(1/6))**2 * exp(-X**(1/3))
        K = kn(2, t/Te)
        j = A * (ne*nus) * (Y/K)
        return j, j/Bnu(nu, Te)

    return pure
