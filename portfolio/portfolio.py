
import numpy as np
from util import Logger
from cvxpy import *

def simplex_projection(v, b=1):
    """Projection vectors to the simplex domain
    Implemented according to the paper: Efficient projections onto the
    l1-ball for learning in high dimensions, John Duchi, et al. ICML 2008.
    Implementation Time: 2011 June 17 by Bin@libin AT pmail.ntu.edu.sg
    Optimization Problem: min_{w}\| w - v \|_{2}^{2}
    s.t. sum_{i=1}^{m}=z, w_{i}\geq 0
    Input: A vector v \in R^{m}, and a scalar z > 0 (default=1)
    Output: Projection vector w
    Original matlab implementation: John Duchi (jduchi@cs.berkeley.edu)
    Python-port: Copyright 2013 by Thomas Wiecki (thomas.wiecki@gmail.com).
    """
    v = np.asarray(v)
    p = len(v)

    # Sort v into u in descending order
    v = (v > 0) * v
    u = np.sort(v)[::-1]
    sv = np.cumsum(u)

    rho = np.where(u > (sv - b) / np.arange(1, p + 1))[0][-1]
    theta = np.max([0, (sv[rho] - b) / (rho + 1)])
    w = (v - theta)
    w[w < 0] = 0
    return w

class Portfolio:
    def __init__(self,
                 org_w,
                 asset_num,
                 assets_return,
                 assets_covariance,
                 adjust_thres=0.3,
                 risk_thres=1):
        # Factor model portfolio optimization.
        self._asset_num = asset_num
        self._assets_return = np.array(assets_return)
        self._assets_covariance = np.array(assets_covariance)

        self._logger = Logger()
        # control_thres = (sum(assets_return) / np.ones((1, asset_num))
        #                  .dot(np.array(assets_covariance))
        #                  .dot(np.ones((asset_num, 1))) * asset_num)[0][0]
        # abs(control_thres).value * control_coef

        self._logger.info(module='portfolio',
                          file='portfolio.py',
                          content="Doing portfolio optimization with params: adjust_thres is %f, risk_thres is %f"
                                  % (adjust_thres, risk_thres))
        w = Variable(self._asset_num)
        w_old = np.array(org_w)

        gamma = Parameter(sign='positive')
        gamma.value = risk_thres
        ret = self._assets_return * w
        risk = quad_form(w, self._assets_covariance)

        prob_factor = Problem(Maximize(ret - gamma*risk),
                              [w >= 0,
                               sum_entries(w) == 1,
                               norm(w - w_old, 1) < adjust_thres])

        prob_factor.solve(verbose=True)
        self._asset_weight = w.value.T.tolist()[0]

    @property
    def asset_weight(self):
        return self._asset_weight
