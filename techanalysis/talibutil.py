
"""
TalibFactors
=============================================================
Talib util provides useful functions for generates technical
analysis factors. We also provide a useful class manages talib
factors calculation for expanding time series.
"""

import talib
import numpy as np

# BBANDS - Bollinger Bands
def bbands(close, period):
    upperband, middleband, lowerband = \
        talib.BBANDS(close, timeperiod=period, nbdevup=2, nbdevdn=2,
                     matype=0)
    return [[upperband, middleband, lowerband],
            ['upperband', 'middleband', 'lowerband']]

# DEMA - Double Exponential Moving Average
def dema(close, period):
    real = talib.DEMA(close, timeperiod=period)
    return [real, 'dema']

# EMA - Exponetial Moving Average
def ema(close, period):
    real = talib.EMA(close, timeperiod=period)
    return [real, 'ema']

# HT_TRENDLINE - Hilbert Transform - Instantaneous Trendline
def ht(close, period=None):
    real = talib.HT_TRENDLINE(close)
    return [real, 'ht']

# KAMA - Kaufman Adaptive Moving Average
def kama(close, period):
    real = talib.KAMA(close, timeperiod=period)
    return [real, 'kama']

# MA - Moving average
def ma(close, period):
    real = talib.MA(close, timeperiod=period, matype=0)
    return [real, 'ma']

# MAMA - MESA Adaptive Moving Average
# mama, fama = talib.MAMA(close, fastlimit=0, slowlimit=0)


# MAVP - Moving average with variable period
# real = talib.MAVP(close, periods, minperiod=2, maxperiod=30, matype=0)


# MIDPOINT - MidPoint over period
def midpoint(close, period):
    real = talib.MIDPOINT(close, timeperiod=period)
    return [real, 'midpoint']

# MIDPRICE - Midpoint Price over period
# real = talib.MIDPRICE(high, low, timeperiod=14)

# SAR - Parabolic SAR
# real = talib.SAR(high, low, acceleration=0, maximum=0)

# SAREXT - Parabolic SAR - Extended
# real = SAREXT(high, low, startvalue=0, offsetonreverse=0, accelerationinitlong=0,
#               accelerationlong=0, accelerationmaxlong=0, accelerationinitshort=0,
#               accelerationshort=0, accelerationmaxshort=0)

# SMA - Simple Moving Average
def sma(close, period):
    real = talib.SMA(close, timeperiod=period)
    return [real, 'sma']

# T3 - Triple Exponential Moving Average (T3)
def t3ema(close, period):
    real = talib.T3(close, timeperiod=period, vfactor=0)
    return [real, 't3ema']

# TEMA - Triple Exponential Moving Average
def tema(close, period):
    real = talib.TEMA(close, timeperiod=period)
    return [real, 'tema']

# TRIMA - Triangular Moving Average
def trima(close, period):
    real = talib.TRIMA(close, timeperiod=period)
    return [real, 'trima']

# WMA - Weighted Moving Average
def wma(close, period):
    real = talib.WMA(close, timeperiod=period)
    return [real, 'wma']

# Momentum Indicator Functions
# ADX - Average Directional Movement Index
# real = talib.ADX(high, low, close, timeperiod=14)
# ADXR - Average Directional Movement Index Rating
# real = talib.ADXR(high, low, close, timeperiod=14)

# APO - Absolute Price Oscillator
def apo(close, period):
    real = talib.APO(close, fastperiod=period / 2,
                     slowperiod=period, matype=0)
    return [real, 'apo']

# AROON - Aroon
# aroondown, aroonup = talib.AROON(high, low, timeperiod=14)
# AROONOSC - Aroon Oscillator
# real = AROONOSC(high, low, timeperiod=14)
# BOP - Balance Of Power
# real = BOP(open, high, low, close)
# CCI - Commodity Channel Index
# real = talib.CCI(high, low, close, timeperiod=14)

# CMO - Chande Momentum Oscillator
def cmo(close, period):
    real = talib.CMO(close, timeperiod=period)
    return [real, 'cmo']

# DX - Directional Movement Index
# real = DX(high, low, close, timeperiod=14)

# MACD - Moving Average Convergence/Divergence
def macd(close, period):
    macd, macdsignal, macdhist = talib.MACD(close, fastperiod=period / 2,
                                            slowperiod=period, signalperiod=period / 4)
    return [[macd, macdsignal, macdhist],
            ['macd', 'macdsignal', 'macdhist']]

# MACDEXT - MACD with controllable MA type
def macd_ext(close, period):
    macd, macdsignal, macdhist = talib.MACDEXT(close, fastperiod=period / 2,
                                               fastmatype=0, slowperiod=period,
                                               slowmatype=0, signalperiod=period / 4,
                                               signalmatype=0)
    return [[macd, macdsignal, macdhist],
            ['macd_ext', 'macdsignal_ext', 'macdhist_ext']]

# MACDFIX - Moving Average Convergence/Divergence Fix 12/26
def macd_fix(close, period):
    macd, macdsignal, macdhist = talib.MACDFIX(close, signalperiod=period / 4)
    return [[macd, macdsignal, macdhist],
            ['macd_fix', 'macdsignal_fix', 'macdhist_fix']]

# MFI - Money Flow Index
# real = talib.MFI(high, low, close, volume, timeperiod=14)
# MINUS_DI - Minus Directional Indicator
# real = MINUS_DI(high, low, close, timeperiod=14)
# MINUS_DM - Minus Directional Movement
# real = MINUS_DM(high, low, timeperiod=14)

# MOM - Momentum
def mom(close, period):
    real = talib.MOM(close, timeperiod=period)
    return [real, 'mom']

# PLUS_DI - Plus Directional Indicator
# real = talib.PLUS_DI(high, low, close, timeperiod=14)
# PLUS_DM - Plus Directional Movement
# real = PLUS_DM(high, low, timeperiod=14)

# PPO - Percentage Price Oscillator
def pro(close, period):
    real = talib.PPO(close, fastperiod=period / 2, slowperiod=period, matype=0)
    return [real, 'pro']

# ROC - Rate of change : ((price/prevPrice)-1)*100
def roc(close, period):
    real = talib.ROC(close, timeperiod=period)
    return [real, 'roc']

# ROCP - Rate of change Percentage: (price-prevPrice)/prevPrice
def rocp(close, period):
    real = talib.ROCP(close, timeperiod=period)
    return [real, 'rocp']

# ROCR - Rate of change ratio: (price/prevPrice)
def rocr(close, period):
    real = talib.ROCR(close, timeperiod=period)
    return [real, 'rocr']

# ROCR100 - Rate of change ratio 100 scale: (price/prevPrice)*100
def rocr100(close, period):
    real = talib.ROCR100(close, timeperiod=period)
    return [real, 'rocr100']

# RSI - Relative Strength Index
def rsi(close, period):
    real = talib.RSI(close, timeperiod=period)
    return [real, 'rsi']

# STOCH - Stochastic
# def stoch(close, period):
#     slowk, slowd = talib.STOCH(high, low, close, fastk_period=5,
#                               slowk_period=period, slowk_matype=0,
#                               slowd_period=period / 2, slowd_matype=0)

# STOCHF - Stochastic Fast
# def stochf(close, period):
#     fastk, fastd = talib.STOCHF(high, low, close, fastk_period=5,
#                                 fastd_period=3, fastd_matype=0)
#     return fastk, fastd

# STOCHRSI - Stochastic Relative Strength Index
def stochrsi(close, period):
    fastk, fastd = talib.STOCHRSI(close, timeperiod=period, fastk_period=5,
                                  fastd_period=3, fastd_matype=0)
    return [[fastk, fastd], ['fastk', 'fastd']]

# TRIX - 1-day Rate-Of-Change (ROC) of a Triple Smooth EMA
def trix(close, period):
    real = talib.TRIX(close, timeperiod=period)
    return [real, 'trix']

# ULTOSC - Ultimate Oscillator
# def ultosc(close, period):
#     real = ULTOSC(high, low, close, timeperiod1=perido / 4, timeperiod2=period / 2,
#                   timeperiod3=period)
#     return real

# WILLR - Williams' %R
# def willr(close, period):
#     real = talib.WILLR(high, low, close, timeperiod=period)
#     return real

# Volume Indicator Functions
# AD - Chaikin A/D Line
# real = AD(high, low, close, volume)
# ADOSC - Chaikin A/D Oscillator
# real = talib.ADOSC(high, low, close, volume, fastperiod=3, slowperiod=10)
# OBV - On Balance Volume
# real = talib.OBV(volume)
# Volatility Indicator Functions
# ATR - Average True Range
# real = ATR(high, low, close, timeperiod=14)
# NATR - Normalized Average True Range
# real = NATR(high, low, close, timeperiod=14)
# TRANGE - True Range
# real = talib.TRANGE(high, low, close)
# Cycle Indicator Functions

# HT_DCPERIOD - Hilbert Transform - Dominant Cycle Period
def ht_dcperiod(close, period=None):
    real = talib.HT_DCPERIOD(close)
    return [real, 'ht_dcperiod']

# HT_DCPHASE - Hilbert Transform - Dominant Cycle Phase
def ht_dcphase(close, period=None):
    real = talib.HT_DCPHASE(close)
    return [real, 'ht_dcphase']

# HT_PHASOR - Hilbert Transform - Phasor Components
def ht_phasor(close, period=None):
    inphase, quadrature = talib.HT_PHASOR(close)
    return [[inphase, quadrature], ['inphase', 'quadrature']]

# HT_SINE - Hilbert Transform - SineWave
def ht_sine(close, period=None):
    sine, leadsine = talib.HT_SINE(close)
    return [[sine, leadsine], ['sine', 'leadsine']]

# HT_TRENDMODE - Hilbert Transform - Trend vs Cycle Mode
def ht_trendmode(close, period=None):
    integer = talib.HT_TRENDMODE(close)
    return [integer, 'ht_trendmode']

# Statistic Functions
# BETA - Beta
# real = BETA(high, low, timeperiod=5)
# CORREL - Pearson's Correlation Coefficient (r)
# real = CORREL(high, low, timeperiod=30)

# LINEARREG - Linear Regression
def linear_reg(close, period):
    real = talib.LINEARREG(close, timeperiod=period)
    return [real, 'linear_reg']

# LINEARREG_ANGLE - Linear Regression Angle
def linear_angle(close, period):
    real = talib.LINEARREG_ANGLE(close, timeperiod=period)
    return [real, 'linear_angle']

# LINEARREG_INTERCEPT - Linear Regression Intercept
def linear_reg_intercept(close, period):
    real = talib.LINEARREG_INTERCEPT(close, timeperiod=period)
    return [real, 'linear_reg_intercept']

# LINEARREG_SLOPE - Linear Regression Slope
def linear_reg_slope(close, period):
    real = talib.LINEARREG_SLOPE(close, timeperiod=period)
    return [real, 'linear_reg_slope']

# STDDEV - Standard Deviation
def std_dev(close, period):
    real = talib.STDDEV(close, timeperiod=period, nbdev=1)
    return [std_dev, 'std_dev']

# TSF - Time Series Forecast
def tsf(close, period):
    real = talib.TSF(close, timeperiod=period)
    return [real, 'tsf']

# VAR - Variance
def var(close, period):
    real = talib.VAR(close, timeperiod=period, nbdev=1)
    return [real, 'var']

# acos = talib.ACOS(series)
# asin = talib.ASIN(series)
# atan = talib.ATAN(series)
# ceil = talib.CEIL(series)
# cos = talib.COS(series)
# cosh = talib.COSH(series)
# exp = talib.EXP(series)

# FLOOR
def floor(close, period=None):
    floor = talib.FLOOR(close)
    return [floor, 'floor']

def ln(close, period=None):
    ln = talib.LN(close)
    return [ln, 'ln']

def log10(close, period=None):
    log10 = talib.LOG10(close)
    return [log10, 'log10']

def sin(close, period=None):
    sin = talib.SIN(close)
    return [sin, 'sin']

def sqrt(close, period=None):
    sinh = talib.SQRT(close)
    return [sinh, 'sinh']

def tan(close, period=None):
    tan = talib.TAN(close)
    return [tan, 'tan']

def tanh(close, period=None):
    tanh = talib.TANH(close)
    return [tanh, 'tanh']

def minmax(close, period):
    min_, max_ = talib.MINMAX(close, timeperiod=period)
    return [[min_, max_], ['min', 'max']]

def minmax_idx(close, period):
    min_idx, max_idx = talib.MINMAXINDEX(close, timeperiod=period)
    return [[min_idx, max_idx], ['min_idx', 'max_idx']]

def sum(close, period):
    sum_value = talib.SUM(close, timeperiod=period)
    return [sum_value, 'sum_value']

# talib_function_list = [
#     bbands, dema, ema, ht, kama, ma, midpoint, sma, t3ema,
#     tema, trima, wma, apo, cmo, macd, macd_ext, macd_fix,
#     mom, pro, roc, rocp, rocr, rocr100, rsi, stochrsi, trix,
#     minmax, minmax_idx, sum]
# floor, ln, log10, sin, sqrt, tan, tanh
#
talib_function_list = [ma, roc, macd]

def talib_extended_series(*args, **argv):
    """
    talib extended series accept the same type of
    params (close, period) as common talib functions.
    :param args:
    :param argv:
    :return:
    """
    factors, names = [], []
    for func in talib_function_list:
        new_factors = func(*args, **argv)[0]
        new_names = func(*args, **argv)[1]
        if type(new_names) == type([]) or \
           type(new_names) == type(()):
            factors += [v.tolist() for v in new_factors]
            names += new_names
        else:
            factors.append(new_factors.tolist())
            names.append(new_names)
    return list(zip(*factors)), names

class TechnicalFactors:
    def __init__(self, period_list):
        """
        Multiple periods extending using talib.
        :param period_list:
        """
        self._period_list = period_list

    @classmethod
    def generate_factors_ona_period(cls, series, period):
        """
        using talib_extended_series expands series into
        a talib technical vector for each series unit.
        :param series:
        :param period:
        :return: a list object contains arrays of factors(list)
        """
        technical_factors, _ = \
            talib_extended_series(np.array(series), period)
        return technical_factors

    def generate_factors_on_period_list(self, series):
        """
        we also allow extending factors with different period
        params. This function assembles them together.
        :param series:
        :return:
        """
        technical_factors_group_list = [
            self.generate_factors_ona_period(series, period)
            for period in self._period_list]
        # tips
        # some technical factors will be always nan, this
        # incurs something wrong.
        factors_list = []
        for factors in technical_factors_group_list[0]:
            factors_list.append(factors)
        for factors_series in technical_factors_group_list[1:]:
            for i, factors in enumerate(factors_series):
                factors_list[i] += factors
        return factors_list

    @classmethod
    def get_factors_names(cls):
        """
        This function obtains the technical series' names
        by constructing a 50-len time series with period 10.
        :return:
        """
        series = np.random.random(50)
        _, technical_names_group = \
            talib_extended_series(np.array(series), 10)
        return technical_names_group

if __name__ == '__main__':
    print TechnicalFactors.get_factors_names()