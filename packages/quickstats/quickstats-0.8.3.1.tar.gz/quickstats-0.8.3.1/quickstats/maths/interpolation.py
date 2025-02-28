from typing import Optional, Union

import numpy as np

def get_intervals(x:np.ndarray, y:np.ndarray, level:float, delta:float=0.0001):
    from scipy.interpolate import interp1d
    sort_idx = np.argsort(x)
    x = x[sort_idx]
    y = y[sort_idx]
    func_interp = interp1d(x, y, fill_value="extrapolate")
    x_interp = np.arange(min(x), max(x), delta)
    y_interp = func_interp(x_interp)
    # remove points that are nan
    mask = np.argwhere(~np.isnan(y_interp))
    x_interp = x_interp[mask]
    y_interp = y_interp[mask]
    asign = np.sign(y_interp - level)
    sign_change   = (np.roll(asign, 1) - asign) != 0
    # first point can not have a sign change
    sign_change[0][0] = False
    intersections = x_interp[sign_change]
    sign_slope    = asign[sign_change]
    # no intersections
    if len(intersections) == 0:
        return []
    if len(intersections) == 1:
        if sign_slope[0] == -1:
            return np.array([[intersections[0], np.inf]])
        else:
            return np.array([[-np.inf, intersections[0]]])
    else:
        if sign_slope[0] == 1:
            intersections = np.insert(intersections, 0, -np.inf)
        if sign_slope[-1] == -1:
            intersections = np.insert(intersections, intersections.shape[0], np.inf)
        if len(intersections) & 1:
            raise RuntimeError("number of intersections can not be odd")
        n_pairs = len(intersections) // 2
        return intersections.reshape((n_pairs, 2))
    
def get_regular_meshgrid(*xi, n):
    reg_xi = [np.linspace(np.min(x), np.max(x), n) for x in xi]
    return np.meshgrid(*reg_xi)
    
def get_x_intersections(x1, y1, x2, y2):
    """Get x intersections of two curves
    """
    interp_y1 = np.interp(x2, x1, y1) 

    diff = interp_y1 - y2 
    # determines what index intersection points are at 
    idx = np.argwhere(np.diff(np.sign(diff))).flatten()

    #linear interpolation to get exact intercepts: x = x1 + (x2-x1)/(y2-y1) * (y-y1)
    #y = 0 -> x = x1 - (x2-x1)/(y2-y1) * y1
    intersections = [x2[i] - (x2[i + 1] - x2[i])/(diff[i + 1] - diff[i]) * diff[i] for i in idx]
    return intersections

def get_roots(x:np.ndarray, y:np.ndarray, y_ref:float=0,
              delta:Optional[float]=None):
    """
    Root finding algorithm of a curve from 2D data points
    """
    x, y = np.asarray(x), np.asarray(y)
    sort_idx = np.argsort(x)
    x, y = x[sort_idx], y[sort_idx]
    if delta is None:
        x_interp, y_interp = x, y
    else:
        x_interp = np.arange(np.min(x), np.max(x), delta)
        y_interp = np.interp(x_interp, x, y)
    # remove points that are nan
    mask = np.argwhere(~np.isnan(y_interp))
    x_interp, y_interp = x_interp[mask], y_interp[mask]
    rel_sign = np.sign(y_interp - y_ref)
    sign_change  = (np.roll(rel_sign, 1) - rel_sign) != 0
    # first point can not have a sign change
    sign_change[0][0] = False
    roots = x_interp[sign_change]
    return roots

def get_intervals_between_curves(x1, y1, x2, y2):
    """Get x intervals of intersection between two curves
    """
    interp_y1 = np.interp(x2, x1, y1) 

    diff = interp_y1 - y2 
    sign_change = np.diff(np.sign(diff))
    # determines what index intersection points are at 
    idx = np.argwhere(sign_change).flatten()
    #linear interpolation to get exact intercepts: x = x1 + (x2-x1)/(y2-y1) * (y-y1)
    #y = 0 -> x = x1 - (x2-x1)/(y2-y1) * y1
    intersections = np.array([x2[i] - (x2[i + 1] - x2[i])/(diff[i + 1] - diff[i]) * diff[i] for i in idx])
    # no intersection
    if len(intersections) == 0:
        return intersections
    # one-sided interval
    elif len(intersections) == 1:
        sign = sign_change[idx[0]]
        if sign < 0:
            return np.array([-np.inf, intersections[0]])
        return np.array([intersections[0], np.inf])
    elif len(intersections == 2):
        if (sign_change[idx[0]] + sign_change[idx[1]]) != 0:
            raise RuntimeError('found discontinuous curves')
        return intersections
    raise RuntimeError('found multiple intervals')
    
def interpolate_2d(x:np.ndarray, y:np.ndarray, z:np.ndarray, method:str='cubic', n:int=500):
    from scipy import interpolate
    mask = ~np.isnan(z)
    x, y, z = x[mask], y[mask], z[mask]
    X, Y = get_regular_meshgrid(x, y, n=n)
    Z = interpolate.griddata(np.stack((x, y), axis=1), z, (X, Y), method)
    return X, Y, Z


def additive_piecewise_linear(
    x: Union[float, np.ndarray], nominal: float, low: float, high: float, boundary: Optional[float] = None, res: Optional[float] = None
) -> Union[float, np.ndarray]:
    x = np.asarray(x, dtype=np.float64)
    mod = np.where(
        x > 0, x * (high - nominal), x * (nominal - low)
    )
    return mod


def multiplicative_piecewise_exponential(
    x: Union[float, np.ndarray], nominal: float, low: float, high: float, boundary: Optional[float] = None, res: Optional[float] = None
) -> Union[float, np.ndarray]:
    x = np.asarray(x, dtype=np.float64)
    res = nominal if res is None else res
    mod = np.where(
        x >= 0,
        res * (np.power(high / nominal, x) - 1),
        res * (np.power(low / nominal, -x) - 1),
    )
    return mod


def additive_quadratic_linear_extrapolation(
    x: Union[float, np.ndarray], nominal: float, low: float, high: float, boundary: float, res: Optional[float] = None
) -> Union[float, np.ndarray]:
    x = np.asarray(x, dtype=np.float64)
    # parabolic with linear
    a = 0.5 * (high + low) - nominal
    b = 0.5 * (high - low)
    mod = np.where(
        x > 1,
        (2 * a + b) * (x - 1) + high - nominal,
        np.where(
            x < -1,
            -1 * (2 * a - b) * (x + 1) + low - nominal,
            a * x**2 + b * x,
        ),
    )
    return mod

def additive_polynomial_linear_extrapolation(
    x: Union[float, np.ndarray], nominal: float, low: float, high: float, boundary: float, res: Optional[float] = None
) -> Union[float, np.ndarray]:
    x = np.asarray(x, dtype=np.float64)
    mod = np.zeros_like(x)
    mask1 = x >= boundary
    mask2 = x <= -boundary
    mask3 = ~(mask1 | mask2)

    mod[mask1] = x[mask1] * (high - nominal) / boundary
    mod[mask2] = x[mask2] * (nominal - low) / boundary
    if np.any(mask3):
        t = x[mask3] / boundary
        eps_plus = (high - nominal) / boundary
        eps_minus = (nominal - low) / boundary
        S = 0.5 * (eps_plus + eps_minus)
        A = 0.0625 * (eps_plus - eps_minus)
        mod[mask3] = x[mask3] * (S + t * A * (15 + t**2 * (-10 + t**2 * 3)))
        
    return mod

def multiplicative_polynomial_exponential_extrapolation(
    x: Union[float, np.ndarray], nominal: float, low: float, high: float, boundary: float, res: Optional[float] = None
) -> Union[float, np.ndarray]:
    x = np.asarray(x, dtype=np.float64)
    mod = np.zeros_like(x)
    mask1 = x >= boundary
    mask2 = x <= -boundary
    mask3 = ~(mask1 | mask2)

    mod[mask1] = np.power(high / nominal, x[mask1])
    mod[mask2] = np.power(low / nominal, -x[mask2])

    if np.any(mask3):
        x0 = boundary
        high /= nominal
        low /= nominal

        pow_up = np.power(high, x0)
        pow_down = np.power(low, x0)
        log_hi = np.log(high)
        log_lo = np.log(low)

        pow_up_log = pow_up * log_hi if high > 0 else 0.0
        pow_down_log = -pow_down * log_lo if low > 0 else 0.0
        pow_up_log2 = pow_up_log * log_hi if high > 0 else 0.0
        pow_down_log2 = -pow_down_log * log_lo if low > 0 else 0.0

        S0 = 0.5 * (pow_up + pow_down)
        A0 = 0.5 * (pow_up - pow_down)
        S1 = 0.5 * (pow_up_log + pow_down_log)
        A1 = 0.5 * (pow_up_log - pow_down_log)
        S2 = 0.5 * (pow_up_log2 + pow_down_log2)
        A2 = 0.5 * (pow_up_log2 - pow_down_log2)

        a = (15 * A0 - 7 * x0 * S1 + x0**2 * A2) / (8 * x0)
        b = (-24 + 24 * S0 - 9 * x0 * A1 + x0**2 * S2) / (8 * x0**2)
        c = (-5 * A0 + 5 * x0 * S1 - x0**2 * A2) / (4 * x0**3)
        d = (12 - 12 * S0 + 7 * x0 * A1 - x0**2 * S2) / (4 * x0**4)
        e = (3 * A0 - 3 * x0 * S1 + x0**2 * A2) / (8 * x0**5)
        f = (-8 + 8 * S0 - 5 * x0 * A1 + x0**2 * S2) / (8 * x0**6)

        value = 1.0 + x[mask3] * (a + x[mask3] * (b + x[mask3] * (c + x[mask3] * (d + x[mask3] * (e + x[mask3] * f)))))
        mod[mask3] = value

    return res * (mod - 1.0)
    
def multiplicative_polynomial_linear_extrapolation(
    x: Union[float, np.ndarray], nominal: float, low: float, high: float, boundary: float, res: Optional[float] = None
) -> Union[float, np.ndarray]:
    x = np.asarray(x, dtype=np.float64)
    res = nominal if res is None else res
    mod = np.zeros_like(x)

    high = high / nominal
    low = low / nominal
    
    mask1 = x >= boundary
    mask2 = x <= -boundary
    mask3 = ~(mask1 | mask2)

    mod[mask1] = x[mask1] * (high - nominal) / boundary
    mod[mask2] = x[mask2] * (nominal - low) / boundary

    if np.any(mask3):
        t = x[mask3] / boundary
        eps_plus = (high - nominal) / boundary
        eps_minus = (nominal - low) / boundary
        S = 0.5 * (eps_plus + eps_minus)
        A = 0.0625 * (eps_plus - eps_minus)
        mod[mask3] = x[mask3] * (S + t * A * (15 + t**2 * (-10 + t**2 * 3)))

    return mod * res
    
piecewise_interp_func_map = {
    0: additive_piecewise_linear,
    1: multiplicative_piecewise_exponential,
    2: additive_quadratic_linear_extrapolation,
    4: additive_polynomial_linear_extrapolation,
    5: multiplicative_polynomial_exponential_extrapolation,
    6: multiplicative_polynomial_linear_extrapolation
}

def piecewise_interpolate(
    x: Union[float, np.ndarray],
    nominal: float,
    low: float,
    high: float,
    boundary: float,
    code: int = 4,
    res: Optional[float] = None
) -> Union[float, np.ndarray]:
    return piecewise_interp_func_map[code](x=x, nominal=nominal, low=low, high=high, boundary=boundary, res=res)