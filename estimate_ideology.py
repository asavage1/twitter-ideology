import numpy as np
import rpy2.robjects as robjects

robjects.r['load'](r'/path/to/refdataCA.rdata')  # TODO: Edit path to file
refdataCAr = robjects.r['refdataCA']


def supplementaryRows(res, points):
    svphi = np.array(res['sv'][:res['nd']])

    supcol = np.where(np.isnan(res['colmass']))
    res['colmass'][supcol] = np.nanmean(res['colmass'])

    cs = res['colmass']
    gam00 = res['colcoord']
    SR = np.array(points)
    rs_sum = np.sum(points, axis=0)
    base2 = np.transpose(SR/(np.ones(SR.shape[0]) * rs_sum))
    cs0 = np.array(cs)  # shape should be base2 * base2, but it will already be
    base2 -= cs0
    phi2 = np.transpose(np.matmul(np.transpose(gam00), base2)) / svphi
    return phi2


refdataCA = {'nd': int(refdataCAr[0][0]),
             'sv': np.array(refdataCAr[1]),
             'colmass': np.array(refdataCAr[2]),
             'colcoord': np.array(refdataCAr[3]),
             'colnames': np.array(refdataCAr[4]),
             'id': np.array(refdataCAr[5]),
             'qs': {'value': np.array(refdataCAr[6][0]),
                    'theta': np.array(refdataCAr[6][1])}}  # Id, handle


def estimateIdeology2(user, friends, verbose=True, exact=False):
    y = np.isin(refdataCA['colnames'], friends).astype(int)

    if np.sum(y) == 0:  # user follows 0 elites
        return None

    values = supplementaryRows(refdataCA, y)
    theta = refdataCA['qs']['theta'][np.argmin(
        np.abs(values[0] - refdataCA['qs']['value']))]  # 2,0 == qs, theta

    if abs(theta) == np.inf:  # for analysis
        theta = None

    if not exact:
        pass

    return theta
