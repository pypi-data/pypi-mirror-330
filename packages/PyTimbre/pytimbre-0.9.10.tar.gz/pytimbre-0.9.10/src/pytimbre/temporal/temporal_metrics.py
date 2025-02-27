import datetime
import numpy as np
import warnings


from pytimbre.waveform import Waveform, WeightingFunctions, LeqDurationMode, from_db_to_pa


class TemporalMetrics:

    # TODO: Frank - make this more generic
    @staticmethod
    def sound_exposure_level(times, levels, decibel_down) -> float:
        """
        The sound exposure level attempts to determine the equivalent level of the acoustic energy placed within a
        single second of the acoustic level.  The dB_down parameter determines how far below the peak that the algorithm
        seeks to integrate the data.

        times : datetime, array-like
            a collection of datetime objects that represent the times for the acoustic levels
        levels : double, array-like
            a collection of acoustic levels that are selected at the same time values as the times array
        dB_down : double
            the number of decibels below the peak that we will integrate the acoustics levels

        returns : double
            the integrated level between the times marking the location of the dB_down levels.
        """

        #   Find the indices for the integration

        start_index, stop_index = TemporalMetrics.find_decibel_down_limits(levels, decibel_down)

        #   Determine the equivalent level between these times
        if isinstance(times[0], datetime.datetime):
            tin = (times[stop_index] - times[start_index]).total_seconds()
        else:
            tin = times[stop_index] - times[start_index]

        return TemporalMetrics.leq(
            levels,
            tin,
            1,
            start_index,
            stop_index)

    @staticmethod
    def find_decibel_down_limits(levels, decibel_down_level):
        """
        Examine the array of levels and determine the points that were above the peak - dB_down_level

        levels : double, array-like
            the acoustic levels in an array that will be examined
        dB_down_level : double
            the level below the peak that will set the limits of the integration

        returns: double, tuple
            the start and stop index of the points to integrate
        """

        #   Find the maximum level

        max_level = max(levels)

        #   Find the index of the maximum value

        max_index = np.argmax(levels)

        #   Determine the start_index

        start_index = -1
        for i in range(max_index, -1, -1):
            if levels[i] <= (max_level - decibel_down_level):
                start_index = i
                break

        #   Determine the stop_index

        stop_index = -1
        for i in range(max_index, len(levels), 1):
            if levels[i] <= (max_level - decibel_down_level):
                stop_index = i
                break

        #   Apply some constraints to ensure that we are within the limits of the array

        if start_index < 0:
            start_index = 0
        if stop_index < 0:
            stop_index = len(levels) - 1

        #   Return the arrays

        return start_index, stop_index

    @staticmethod
    def leq_convert_duration(level: float, tin: float = 1.0, tout: float = 1.0):
        """
        Rescales the energy of a level from one equivalent time duration to another.  The equivalent durations tin
        and tout should be in the same units of time.

        :param level: float
            The sound pressure level representing the total acoustic intensity averaged evenly over the
            equivalent duration tin
        :param tin: float
            The equivalent duration time of the input level
        :param tout: float
            The desired equivalent duration time over which the total acoustic intensity is to be averaged.
         :return: The sound pressure level in decibels converted to the new equivalent duration
         :rtype: float
        """

        return level + 10 * np.log10(tin / tout)

    @staticmethod
    def leq(levels, tin, tout, start_index, stop_index):
        """
        The equivalent level is an integration of levels changing the temporal resolution of the acoustic levels.

        levels : double, array-like
            the list of acoustic levels
        tin : double
            the temporal integration of the input level
        tout : double
            the resultant temporal integration of the output level
        start_index : int
            the index within the levels array that we will begin the integration
        stop_index : int
            the index within the levels array that we will stop the integration

        returns : double
            the integrated, equivalent level
        """

        #   Initialize the acoustic equivalent level

        total_intensity_scaled = 0.0

        #   Sum the linear elements units of sound

        for i in range(start_index, stop_index + 1, 1):
            total_intensity_scaled += 10.0 ** (levels[i] / 10.0)

        total_intensity_level = 10 * np.log10(total_intensity_scaled)
        #   apply the logarithmic conversion and the application of the temporal ratio

        return TemporalMetrics.leq_convert_duration(total_intensity_level, tin, tout)

    @staticmethod
    def equivalent_level(
            times,
            levels,
            equivalent_duration: float = 8 * 3600,
            start_sample: int = 0,
            stop_sample: int = None,
            leq_mode: LeqDurationMode = None,
            exposure_duration: float = None
    ):

        """
        This function computes the equivalent level on a level time history. The duration of the summation
        is specified (in seconds) for the new value with a default of 8 hours. Finally, if there is a cause to exclude
        portions of the data (i.e. calculating the SEL for the 10 dB down points in community noise) you can specify
        the start and stop index. If the stop index is None, then the last level defines the limit of the summation.

        :param double, array-like times:
            The times in seconds corresponding to each sample in levels
        :param levels: double, array-like
            The sound pressure levels time history in decibels
        :param equivalent_duration:   float
            The denominator of the energy averaging - in seconds - representing the desired length of total exposure
            time (e.g. an 8-hour duty day, or a 1-second sound exposure level)
        :param start_sample:   int
            default = 0. The start sample of the pressure summation
        :param stop_sample:   int
            default = None. The stop sample, if the value is None, then it is replaced with the last sample index
        :param leq_mode:   LeqDurationMode --> Enum
            The enumeration to determine whether the input signal contains all energy
            of an exposure to the listener (transient) or the signal represents a sample of a longer-duration
            (steady_state) exposure
        :param exposure_duration:   float
            If leq_mode is steady_state, this is the actual time of noise exposure to the
            listener in seconds
       :return:
            The equivalent sound pressure level representing the total acoustic intensity averaged over
            equivalent_duration
        :raises ValueError: if the times and levels arrays are different lengths

        """

        if len(times) != len(levels):
            raise ValueError(
                f"times and levels must have same length, but have shapes {times.shape} and {levels.shape}")

        if stop_sample is None:
            stop_sample = len(times) - 1

        number_of_samples = stop_sample - start_sample + 1
        dt = np.mean(np.diff(times))
        signal_duration = number_of_samples * dt

        if leq_mode == LeqDurationMode.transient:
            tin = dt
        elif leq_mode == LeqDurationMode.steady_state:
            if exposure_duration is None:
                exposure_duration = signal_duration
            tin = dt * (exposure_duration / signal_duration)
        elif leq_mode is None:
            raise ValueError("User must specify a signal duration mode of class LeqDurationMode.")

        return TemporalMetrics.leq(
            levels=levels,
            tin=tin,
            tout=equivalent_duration,
            start_index=start_sample,
            stop_index=stop_sample
        )

    @staticmethod
    def estimate_RT60(wfm: Waveform):

        #   Initialize the calculation
        # ---------------------------------------------

        par = TemporalMetrics._init_rt_estimate_e(wfm.sample_rate)  # struct with all parameters and buffers for frame-wise processing
        BL = par['N'] * par['down']  # to simplify notation

        Laudio = len(wfm.samples)

        # check audio file is long enough for analysis
        if BL < Laudio:
            rt_est = []  # np.zeros(int(round(Laudio / par['N_shift'])))
            RT_final = []

            '''
             frame-wise processing in the time-domain
            '''
            # ---------------------------------------------

            k = 0
            n_array = np.arange(0, Laudio - BL + 1, par['N_shift'])
            for n in n_array:
                k += 1  # frame counter
                ind = np.arange(n, n + BL)  # indices of current frame

                # Actual RT estimation
                RT, par, finalrt = TemporalMetrics._rt_estimate_frame_my(wfm.samples[ind[np.arange(0, len(ind), par['down'])]], par)

                rt_est.append(RT)  # store estimated value
                RT_final.append(finalrt)
        else:
            # audio too short for analysis, for returning smallest Rt value
            return par['Tquant'][0]

        RT_final = np.clip(RT_final, 0, max(RT_final))
        aaa = RT_final[np.where(RT_final > 0)]

        RT_temp_new = []
        for i in range(1, len(aaa)):
            RT_temp_new.append(0.49 * aaa[i - 1] + (1 - 0.49) * np.max(aaa))

        if aaa.size:
            RTfinal_value = np.min(aaa)

            RT_temp_new = []
            for i in range(1, len(aaa)):
                RT_temp_new.append(0.49 * aaa[i - 1] + (1 - 0.49) * np.max(aaa))

        else:
            RTfinal_value = par['Tquant'][0]

        rt_est = np.array(rt_est)
        rt_est = rt_est[np.where(RT_final > 0)]
        if rt_est.size:
            return np.mean(rt_est)
        else:
            return par['Tquant'][0]

    @staticmethod
    def _init_rt_estimate_e(fs=24000):
        """
        par = init_rt_estimate_e(fs)
        executes initialization for the function
        rt_estimate_frame.m to perform a blind estimation of the reverberation time
        (RT) by frame-wise processing in the time-domain.

        INPUT
        fs: sampling frequency(default=24 kHz)

        OUTPUT
        par: struct containing all parameters and buffer for executing the
        function rt_estimate_frame.m

        author: Heiner Loellmann, IND, RWTH Aachen University

        created: August 2011

        general paraemters
        """
        par = {"fs": fs}
        no = par['fs'] / 24000.0  # correction factor to account for different sampling frequency

        # pararmeters for pre-selection of suitable segments
        if par['fs'] > 8e3:
            par['down'] = 2  # rate for downsampling applied before RT estimation to reduce computational complexity
        else:
            par['down'] = 1

        par['N_sub'] = int(round(no * 700 / par['down']))  # sub-frame length(after downsampling)
        par['N_shift'] = int(round(no * 200 / par['down']))  # frame shift(before downsampling)
        par['nos_min'] = 3  # minimal number of subframes to detect a sound decay
        par['nos_max'] = 7  # maximal number of subframes to detect a sound decay
        par['N'] = int(par['nos_max'] * par['N_sub'])  # maximal frame length(after downsampling)

        # parameters for ML - estimation
        Tmax = 1.1  # max RT being considered
        Tmin = 0.2  # min RT being considered
        par['bin'] = 0.1  # step-size for RT estimation
        par['Tquant'] = np.arange(
            Tmin, Tmax + par['bin'] / 2, par['bin']
        )  # set of qunatized RTs considered for maximum search
        par['a'] = np.exp(
            -3.0 * np.log(10) / (par['Tquant'] * (par['fs'] / par['down']))
        )  # corresponding decay rate factors
        par['La'] = len(par['a'])  # num of considered decay rate factors( = no of.RTs)

        # paramters for histogram - based approach to reduce outliers (order statistics)
        par['buffer_size'] = int(round(no * 800 / par['down']))  # buffer size
        par['buffer'] = np.zeros(par['buffer_size'])  # buffer with previous indices to update histogram
        par['no_bins'] = int(par['La'])  # no. of histogram bins
        par['hist_limits'] = np.arange(
            Tmin - par['bin'] / 2.0, Tmax + par['bin'], par['bin']
        )  # limits of histogram bins
        par['hist_rt'] = np.zeros(par['no_bins'])  # histogram with ML estimates
        par['hist_counter'] = 0  # counter increased if histogram is updated

        # paramters for recursive smoothing of final RT estimate
        par['alpha'] = 0.995  # smoothing factor
        par['RT_initial'] = 0.3  # initial RT estimate
        par['RT_last'] = par['RT_initial']  # last RT estimate
        par['RT_raw'] = par['RT_initial']  # raw RT estimate obtained by histogram - approach

        return par

    @staticmethod
    def _rt_estimate_frame_my(frame, par):
        """
        performs an efficient blind estimation of the reverberation time(RT) for frame-wise
        processing based on Laplacian distribution.

        INPUT
        frame: (time-domain) segment with reverberant speech
        par: struct with all parameters and buffers created by the function
        init_binaural_speech_enhancement_e.m

        OUTPUT
        RT: estimated RT
        par: struct with updated buffers to enable a frame-wise processing
        RT_pre: raw RT estimate(for debugging and analysis of the algorithm)

        Reference:  LAllmann, H.W., Jeub, M., Yilmaz, E., and Vary, P.:
        An Improved Algorithm for Blind Reverberation Time Estimation, a
        International Workshop on Acoustic Echo and Noise Control(IWAENC), Tel Aviv, Israel, Aug. 2010.

        Tariqullah Jan and Wenwu Wang:
        Blind reverberation time estimation based on Laplacian distribution
        European Signal Processing Conference(EUSIPCO), 2012.

        The codes were adapted based on the original codes by Heinrich Loellmann, IND, RWTH Aachen

        Authors: Tariqullah Jan, moderated by Wenwu Wang, University of Surrey(2012)
        """
        if len(np.shape(np.squeeze(frame))) > 1:
            raise ValueError('Something went wrong...')

        cnt = 0  # sub-frame counter for pre-selection of possible sound decay
        RTml = -1  # default RT estimate (-1 indicates no new RT estimate)

        # calculate variance, minimum and maximum of first sub-frame
        seg = frame[:par['N_sub']]

        var_pre = np.var(seg)
        min_pre = np.min(seg)
        max_pre = np.max(seg)

        for k in range(2, par['nos_max']):
            # calculate variance, minimum and maximum of succeding sub-frame
            seg = frame[(k - 1) * par['N_sub']: k * par['N_sub'] + 1]
            var_cur = np.var(seg)
            max_cur = max(seg)
            min_cur = min(seg)

            # -- Pre-Selection of suitable speech decays --------------------
            if (var_pre > var_cur) and (max_pre > max_cur) and (min_pre < min_cur):
                # if variance, maximum decraease, and minimum increase
                # = > possible sound decay detected

                cnt += 1

                # current values becomes previous values
                var_pre = var_cur
                max_pre = max_cur
                min_pre = min_cur

            else:
                if cnt >= par['nos_min']:
                    # minimum length for assumed sound decay achieved?
                    # -- Maximum Likelihood(ML) Estimation of the RT
                    RTml, _ = TemporalMetrics._max_loglf(frame[:cnt * par['N_sub']], par['a'], par['Tquant'])

                break

            if k == par['nos_max']:
                # maximum frame length achieved?
                RTml, _ = TemporalMetrics._max_loglf(frame[0:cnt * par['N_sub']], par['a'], par['Tquant'])

        # end of sub-frame loop

        if RTml >= 0:  # new ML estimate calculated

            # apply order statistics to reduce outliers
            par['hist_counter'] += 1

            for i in range(par['no_bins']):

                # find index corresponding to the ML estimate
                # find index corresponding to the ML estimate
                if (RTml >= par['hist_limits'][i]) and (RTml <= par['hist_limits'][i + 1]):
                    index = i
                    break

            # update histogram with ML estimates for the RT
            par['hist_rt'][index] += 1

            if par['hist_counter'] > par['buffer_size'] + 1:
                # remove old values from histogram
                par['hist_rt'][int(par['buffer'][0])] = par['hist_rt'][int(par['buffer'][0])] - 1

            par['buffer'] = np.append(par['buffer'][1:], index)  # % update buffer with indices
            idx = np.argmax(par['hist_rt'])  # find index for maximum of the histogram

            par['RT_raw'] = par['Tquant'][idx]  # map index to RT value

        # final RT estimate obtained by recursive smoothing
        RT = par['alpha'] * par['RT_last'] + (1 - par['alpha']) * par['RT_raw']
        par['RT_last'] = RT

        RT_pre = RTml  # intermediate ML estimate for later analysis

        return RT, par, RT_pre

    @staticmethod
    def _max_loglf(h, a, Tquant):
        '''
        [ML, ll] = max_loglf(h, a, Tquant)

        returns the maximum of the log-likelihood(LL) function and the LL
        function itself for a finite set of decay rates

        INPUT
        h: input frame
        a: finite set of values for which the max.should be found
        T: corresponding RT values for vector a

        OUTPUT
        ML: ML estimate for the RT
        ll: underlying LL - function
        '''

        N = len(h)
        n = np.arange(0, N)  # indices for input vector
        ll = np.zeros(len(a))

        # transpose?
        h_square = h.transpose()

        for i in range(len(a)):
            sum1 = np.dot((a[i] ** (-1.0 * n)), np.abs(h_square))
            sum2 = np.sum(np.abs(h_square))
            sigma = (1 / N) * sum1
            ll[i] = -N * np.log(2) - N * np.log(sigma) - np.sum(np.log(a[i] ** n)) - (1 / sigma) * sum1

        idx = np.argmax(ll)  # maximum of the log-likelihood function
        ML = Tquant[idx]  # corresponding ML estimate for the RT

        return ML, ll


class EquivalentLevel:
    def __init__(self,
                 equivalent_pressure_decibels: float,
                 equivalent_duration: datetime.timedelta,
                 weighting: WeightingFunctions = WeightingFunctions.unweighted
                 ):
        """
        A container class for an equivalent sound pressure level, or acoustic energy averaged over some total duration.
        Commonly abbreviated Leq. Often includes the spectral weighting and equivalent duration in the
        abbreviation, e.g., LAeq8hr.

        :param equivalent_pressure_decibels: Leq in decibels
        :ptype equivalent_pressure_decibels: float, int
        :param equivalent_duration: Time duration over which acoustic energy is averaged.
        :ptype equivalent_duration: datetime.timedelta
        :param weighting: Specifies the spectral weighting applied to the acoustic signal prior to conversion to Leq.
        :ptype weighting: pytimbre.waveform.WeightingFunctions

        Examples:

        Represent one half (50%) of a total allowed daily noise exposure
        >>> import numpy as np
        >>> from pytimbre.temporal.temporal_metrics import EquivalentLevel
        >>> leq = EquivalentLevel(85., datetime.timedelta(hours=4), WeightingFunctions.a_weighted)
        >>> np.round(leq.leq8hr, decimals=1)
        82.0
        >>> np.round(leq.noise_dose_pct, decimals=1)
        49.9

        What is the sound exposure level for a 30-second exposure to an A-weighted SPL of 120 dB?
        >>> leq = EquivalentLevel(120., datetime.timedelta(seconds=30), WeightingFunctions.a_weighted)
        >>> np.round(leq.sel, decimals=1)
        134.8

        If the logarithmic average SPL of a passing train from a 1-minute recording is 95 dB, what is
        the SPL for the same noise event averaged over 1 hour?
        >>> np.round(EquivalentLevel.leq_convert_duration(95., 60, 60 * 60), decimals=1)
        77.2
        """
        self._equivalent_pressure_decibels = equivalent_pressure_decibels
        self._equivalent_duration = equivalent_duration
        self._weighting = weighting

    @property
    def equivalent_pressure_decibels(self):
        return self._equivalent_pressure_decibels

    @property
    def equivalent_pressure_pascals(self):
        return from_db_to_pa(self._equivalent_pressure_decibels)

    @property
    def equivalent_duration(self):
        return self._equivalent_duration

    @property
    def weighting(self):
        return self._weighting

    @property
    def sel(self):
        """
        Sound exposure level, or the equivalent level for all acoustic energy compressed into 1 second.
        :rtype: float
        """
        return self.leq_convert_duration(
            level=10 * np.log10(np.sum(10 ** (self._equivalent_pressure_decibels / 10))),
            tin=self._equivalent_duration.total_seconds(),
            tout=1
        )

    @property
    def leq8hr(self):
        """
        Eight-hour equivalent level, a common metric for quantifying total daily noise exposure.
        :rtype: float
        """
        if self._weighting != WeightingFunctions.a_weighted:
            warnings.warn("8-hour equivalent levels are typically A-weighted to quantify human exposure. Note that "
                          "this equivalent level may have the weighting of {}".format(self._weighting))

        return self.leq_convert_duration(
            level=10 * np.log10(np.sum(10 ** (self._equivalent_pressure_decibels / 10))),
            tin=self._equivalent_duration.total_seconds(),
            tout=8 * 60 * 60
        )

    @property
    def noise_dose_pct(self):
        """
        Total daily noise dose in units of percent, based on an A-weighted 85-db 8-hour equivalent energy criteria
        with 3 dB per doubling.
        """
        if self.weighting != WeightingFunctions.a_weighted:
            raise AttributeError("Noise dose calculation requires A-weighting. The current equivalent level "
                                 "property weighting is {}".format(self.weighting))
        return 100.0 * 2 ** ((self.leq8hr - 85) / 3.0)

    @staticmethod
    def leq_convert_duration(level, tin: float = 1.0, tout: float = 1.0):
        """
        Rescales the energy of a level from one equivalent time duration to another.  The equivalent durations tin
        and tout should be in the same units of time.

        :param level: float, ndarray
            The sound pressure level representing the total acoustic intensity averaged evenly over the
            equivalent duration tin
        :param tin: float
            The equivalent duration time of the input level
        :param tout: float
            The desired equivalent duration time over which the total acoustic intensity is to be averaged.
        :return: The equivalent sound pressure level in decibels converted to the new equivalent duration
        :rtype: float
        """
        return level + 10 * np.log10(tin / tout)


if __name__ == "__main__":
    import doctest
    doctest.testmod()