"""
| Description: This is a base class for the storage or information as a collection of samples, a number of samples
per second and the start time of these samples.
| Contributors: Drs. Frank Mobley and Alan Wall, Conner Campbell, Gregory Bowers
"""
import sys
import numpy as np
from datetime import datetime, timedelta
from enum import Enum
from scipy.signal.windows import hamming, tukey
import scipy.signal
import statsmodels.api as sm
import colorednoise as cn
import warnings
from typing import Dict, Tuple
import numpy.typing as npt
from .yin import yin
import warnings
from python_speech_features import mfcc, ssc, fbank, logfbank


class WindowingMethods(Enum):
    """
    The available windowing methods for the waveform
    """

    hanning = 1
    hamming = 2
    tukey = 3
    rectangular = 4


class TrimmingMethods(Enum):
    """
    Trimming can be accomplished with either the samples or times. This enumeration defines whether to use the time to
    calculate the sample or just provide the samples.
    """

    samples = 1
    times_absolute = 2
    times_relative = 3


class ScalingMethods(Enum):
    """
    In scaling the waveform we can apply the level changes in either decibels or linear values. This will determine how
    the interface scales the signal when manipulating the sample magnitudes.
    """

    linear = 1
    logarithmic = 2


class WeightingFunctions(Enum):
    """
    This class provides the options on how to weight the calculation of the overall level values
    """

    unweighted = 0
    a_weighted = 1
    c_weighted = 2


class CorrelationModes(Enum):
    """
    This class defines the various modes for the cross-correlation function.
    """

    valid = 0
    full = 1
    same = 2


class NoiseColor(Enum):
    white = 0
    pink = 1
    brown = 2


class LeqDurationMode(Enum):
    """
    The available types of time scaling for conversion of a signal to equivalent levels
    """

    steady_state = 0
    transient = 1


class AnalysisMethod(Enum):
    """
    |Description: Method for processing impulse metrics.
    """

    NONE = 0
    MIL_STD_1474E = 1
    MIL_STD_1474E_AFRL_PREF = 2
    NO_A_DURATION_CORRECTIONS = 3


class AudioMetaData:
    def __init__(self, data: dict, path: str):
        """
        This class contains the information obtained from the audio file to describe the various elements within the
        header of the data file. From this all information for the specific properties can be obtained.
        :param data: the data from the header
        :type data: dictionary
        :param path: the path to the file
        :type path: str
        """

        self._data = data
        self._path = path

    @property
    def path(self):
        return self._path

    @property
    def filename(self):
        import os.path

        return os.path.basename(self.path)

    @property
    def header(self):
        return self._data


def from_db_to_pa(pressure_decibels):
    """
    Converts array of decibels to pressure in pascals
    :param pressure_decibels:
    :return: pressures in pascals
    """
    return 10 ** (pressure_decibels / 20) * 2e-5


class Waveform:
    """
    |Description: This is a generic base class that contains the start time, samples and sample rate for a waveform.
    Some limited operations exist within this class for manipulation of the base data within the class.

    #   TODO: Add convolution function
    #   TODO: Add function for SEL calculation
    #   TODO: Add filter array function
    Remarks
    2022-05-11 - FSM - added the function to determine whether the waveform is a calibration signal or not.
    """

    def __init__(
            self,
            pressures,
            sample_rate,
            start_time,
            remove_dc_offset: bool = True,
            is_continuous_wfm: bool = True,
            is_steady_state: bool = True,
            impulse_analysis_method: AnalysisMethod = AnalysisMethod.NO_A_DURATION_CORRECTIONS,
            header=None):
        """
        Default constructor
        :param pressures:
            float, array-like - the list of pressure values
        :param sample_rate:
            float - the number of samples per second
        :param start_time:
            float or datetime - the time of the first sample
        :param remove_dc_offset:
            bool, default = True - remove a DC offset from the samples
        :param is_continuous_wfm:
            bool - flag to determine whether this waveform is continuous or impulsive in nature. Default is True
        :param is_steady_state:
            bool - flag to determine whether this waveform is steady-state or transient in nature. Default is True
        :param impulse_analysis_method:
            Enumeration - this is a collection of the methods that might be used in the creation of impulse metrics.
        :param header:
            Dictionary - the collection of information regarding the StandardBinaryFile's properties.
        """
        warnings.filterwarnings('ignore')

        self._samples = pressures
        self.fs = sample_rate
        if isinstance(start_time, datetime):
            self.time0 = start_time
        else:
            self.time0 = float(start_time)
        if header is None:
            self._header = dict()
        else:
            self._header = header
        self._is_continuous = is_continuous_wfm
        self._is_steady_state = is_steady_state
        self._impulse_analysis_method = impulse_analysis_method
        self._forward_coefficients = None
        self._reverse_coefficients = None
        self._metadata = None

        self._coefficient_count = 12
        self._hop_size_seconds = 0.0029
        self._window_size_seconds = 0.0232
        self._cutoff_frequency = 5
        self._centroid_threshold = 0.15
        self._effective_duration_threshold = 0.4

        self._signal_envelope = None
        self._normal_signal_envelope = None
        self._log_attack = None
        self._increase = None
        self._decrease = None
        self._addresses = None
        self._amplitude_modulation = None
        self._frequency_modulation = None
        self._auto_correlation_coefficients = None
        self._zero_cross_rate = None
        self._temporal_centroid = None
        self._effective_duration = None
        self._temporal_feature_times = None
        self._temporal_threshold_finding = 3

        self._corrected_a_duration = None
        self._liaeqT = None
        self._liaeq100ms = None
        self._liaeq8hr = None
        self._SELA = None
        self._noise_dose = None

        #   Run some checks on the data based on the information in the constructors
        if remove_dc_offset or self.is_impulsive:
            self._samples -= np.mean(self._samples)

        if self.is_impulsive and np.max(pressures) < -1.0 * np.min(pressures):
            pressures *= -1.0

    # ---------------------- Collection of properties - this is both getters and setters -------------------------------

    @property
    def a_duration(self):
        """"
        -20220329 - SCC - Fixed code. Was flipping polairty of every signal and couldn't find right zero crossing.
        """
        p2 = self.samples
        p2 -= np.mean(p2[:400000])
        max_p = np.max(p2)
        max_p_idx = np.argmax(np.abs(p2))

        maximum_pressure = self.samples[max_p_idx]
        if maximum_pressure < 0:
            p2 *= -1

        #   Find the start time for the A-duration, whcih is the first zero-crossing before the peak pressure

        if (max_p_idx > 1) and (max_p_idx <= len(p2)):
            e1 = max_p_idx
        else:
            e1 = 0

        located = False
        while (not located) and (e1 > 0):
            e1 -= 1
            if p2[e1] <= 0:
                located = True
                break

        #   Interpolate to determine a more accurate representation of this time

        if (abs(p2[e1] - p2[e1 + 1]) >= 1e-12) and (located is True):
            at1 = (0 - p2[e1]) / (p2[e1 + 1] - p2[e1]) + e1 + 1
        else:
            at1 = e1

        #   find the end time for the A-duration, which is the last zero-crossing after the peak

        if (max_p_idx > 1) and (max_p_idx <= len(p2)):
            e1 = max_p_idx
        else:
            e1 = 1

        located = False
        while (not located) and (e1 < len(p2)):
            e1 += 1
            if p2[e1] <= 0:
                located = True
                break

        #   Interpolate to determine a more accurate representation of this time

        if (abs(p2[e1] - p2[e1 - 1]) >= 1e-12) and (located is True):
            at2 = (0 - p2[e1 - 1]) / (p2[e1] - p2[e1 - 1]) + e1
        else:
            at2 = e1

        return (at2 - at1) / self.sample_rate

    @property
    def amplitude_modulation(self):
        if self._amplitude_modulation is None:
            self._frequency_modulation, self._amplitude_modulation = self.calculate_modulation()
        return self._amplitude_modulation

    @property
    def attack(self):
        if self._addresses is None:
            self._calculate_signal_envelope()
            self._log_attack, self._increase, self._decrease, self._addresses = self.calculate_log_attack()

        return self._addresses[0]

    @property
    def attack_slope(self):
        """
        The attack slope is defined as the average temporal slope of the energy during the attack segment. We compute
        the local slopes of the energy corresponding to each effort w_i. We then compute a weighted average of the
        slopes. The weights are chosen in order to emphasize slope values in the middle of the attack (the weights are
        the values of a Gaussian function centered around the threshold = 50% and with a standard-deviation of 0.5).
        """
        if self._addresses is None:
            self._calculate_signal_envelope()
            self._log_attack, self._increase, self._decrease, self._addresses = self.calculate_log_attack()

        return self._increase

    @property
    def auto_correlation(self):
        if self._auto_correlation_coefficients is None:
            self._temporal_feature_times, self._auto_correlation_coefficients, self._zero_cross_rate = \
                self.instantaneous_temporal_features()
        return self._auto_correlation_coefficients

    @property
    def boominess(self):
        """
        This is an implementation of the hasimoto booming index feature. There are a few fudge factors with the code to
        convert between the internal representation of the sound using the same loudness calculation as the sharpness
        code.  The equation for calculating the booming index is not specifically quoted anywhere, so I've done the
        best I
        can with the code that was presented.

        Shin, SH, Ih, JG, Hashimoto, T., and Hatano, S.: "Sound quality evaluation of the booming sensation for
        passenger
        cars", Applied Acoustics, Vol. 70, 2009.

        Hatano, S., and Hashimoto, T. "Booming index as a measure for evaluating booming sensation",
        The 29th International congress and Exhibition on Noise Control Engineering, 2000.

        This function calculates the apparent Boominess of an audio Waveform.

        This version of timbral_booming contains self loudness normalising methods and can accept arrays as an input
        instead of a string filename. (FSM) This current version was modified from the original to use the PyTimbre
        features rather that the soundfile methods for reading the files and use the Waveform.

        Version 0.5

        Returns
        -------
        :returns:
            the boominess of the audio file

        Copyright 2018 Andy Pearce, Institute of Sound Recording, University of Surrey, UK.

        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.

        Refactored by Dr. Frank Mobley 2023
        """
        from pytimbre.spectral.acoustic_weights import AcousticWeights
        from pytimbre.spectral.fractional_octave_band import FractionalOctaveBandTools

        # window the audio file into 4096 sample sections
        wfm = self.normalize_loudness(-24, False)
        windowed_audio = wfm.split_by_time(4096 / wfm.sample_rate)

        #   Create the lists that will hold information regarding the various
        windowed_booming = []
        windowed_rms = []

        #   Loop through the windowed audio
        for i in range(windowed_audio.shape[0]):
            # get the rms value and append to list
            windowed_rms.append(np.sqrt(np.mean(windowed_audio[i].samples ** 2)))

            # calculate the specific loudness
            N_entire, N_single = windowed_audio[i].specific_loudness

            # calculate the booming index if it contains a level
            if N_entire > 0:
                BoomingIndex = AcousticWeights.calculate_boominess(N_single)
            else:
                BoomingIndex = 0

            windowed_booming.append(BoomingIndex)

        # get level of low frequencies
        ll, _ = FractionalOctaveBandTools.weighted_bark_level(wfm, 0, 70)

        ll = np.log10(ll)

        # convert to numpy arrays for fancy indexing
        windowed_booming = np.array(windowed_booming)
        windowed_rms = np.array(windowed_rms)

        # get the weighted average
        rms_boom = np.average(windowed_booming, weights=(windowed_rms * windowed_rms))
        rms_boom = np.log10(rms_boom)

        # perform the linear regression
        all_metrics = np.ones(3)
        all_metrics[0] = rms_boom
        all_metrics[1] = ll

        coefficients = np.array([43.67402696195865, -10.90054738389845, 26.836530575185435])

        return np.sum(all_metrics * coefficients)

    @property
    def centroid_threshold(self):
        return self._centroid_threshold

    @property
    def cutoff_frequency(self):
        return self._cutoff_frequency

    @cutoff_frequency.setter
    def cutoff_frequency(self, value):
        self._cutoff_frequency = value

    @property
    def coefficient_count(self):
        """
        The number of coefficients to generate for the available data
        """

        return self._coefficient_count

    @coefficient_count.setter
    def coefficient_count(self, value):
        """
        Set the number of coefficients for the analysis
        """

        self._coefficient_count = value

    @property
    def duration(self):
        """
        Determine the duration of the waveform by examining the number of samples and the sample rate
        :return: float - the total number of seconds within the waveform
        """
        return float(len(self._samples)) / self.fs

    @property
    def effective_duration_threshold(self):
        return self._effective_duration_threshold

    @property
    def end_time(self):
        """
        Determine the end time - if the start time was a datetime, then this returns a datetime.  Otherwise a floating
        point value is returned
        :return: float or datetime - the end of the file
        """
        if isinstance(self.time0, datetime):
            return self.time0 + timedelta(seconds=self.duration)
        else:
            return self.time0 + self.duration

    @property
    def forward_coefficients(self):
        return self._forward_coefficients

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, value):
        self._header = value

    @property
    def hop_size_samples(self):
        return int(round(self.hop_size_seconds * self.sample_rate))

    @property
    def hop_size_seconds(self):
        return self._hop_size_seconds

    @hop_size_seconds.setter
    def hop_size_seconds(self, value):
        self._hop_size_seconds = value

    @property
    def impulse_analysis_method(self):
        return self._impulse_analysis_method

    @impulse_analysis_method.setter
    def impulse_analysis_method(self, method):
        self._impulse_analysis_method = method
        self._liaeqT = None
        self._liaeq8hr = None
        self._noise_dose = None
        self._corrected_a_duration = None

    @property
    def is_continuous(self):
        return self._is_continuous

    @is_continuous.setter
    def is_continuous(self, value):
        self._is_continuous = value

    @property
    def is_impulsive(self):
        return not self.is_continuous

    @is_impulsive.setter
    def is_impulsive(self, value):
        """
        Set to True to enable properties and methods tailored to impulsive acoustic signals.
        """
        self.is_continuous = not value

    @property
    def is_steady_state(self):
        return self._is_steady_state

    @is_steady_state.setter
    def is_steady_state(self, value):
        self._is_steady_state = value

    @property
    def is_transient(self):
        return not self.is_steady_state

    @is_transient.setter
    def is_transient(self, value):
        self.is_steady_state = not value

    @property
    def meta(self):
        return self._metadata

    @meta.setter
    def meta(self, meta):
        self._metadata = meta

    @property
    def reverse_coefficients(self):
        return self._reverse_coefficients

    @property
    def samples(self):
        """
        The actual pressure waveform
        :return: float, array-like - the collection of waveform data
        """
        return self._samples

    @samples.setter
    def samples(self, array):
        self._samples = array

    @property
    def sample_rate(self):
        """
        The number of samples per second to define the waveform.
        :return: float - the number of samples per second
        """
        return self.fs

    @sample_rate.setter
    def sample_rate(self, value):
        self.fs = value

    @property
    def start_time(self):
        """
        The time of the first sample
        :return: float or datetime - the time of the first sample
        """

        return self.time0

    @start_time.setter
    def start_time(self, value):
        self.time0 = value

    @property
    def times(self):
        """
        This determines the time past midnight for the start of the audio and returns a series of times for each sample
        :return: float, array-like - the sample times for each element of the samples array
        """

        if isinstance(self.start_time, datetime):
            t0 = (60 * (60 * self.start_time.hour + self.start_time.minute) + self.start_time.second +
                  self.start_time.microsecond * 1e-6)
        else:
            t0 = self.start_time

        return np.arange(0, len(self.samples)) / self.sample_rate + t0

    @property
    def window_size_seconds(self):
        return self._window_size_seconds

    @window_size_seconds.setter
    def window_size_seconds(self, value):
        self._window_size_seconds = value

    @property
    def window_size_samples(self):
        return int(np.round(self.window_size_seconds * self.sample_rate))

    @property
    def temporal_threshold_finding(self):
        return self._temporal_threshold_finding

    @temporal_threshold_finding.setter
    def temporal_threshold_finding(self, value):
        self._temporal_threshold_finding = value

    @property
    def decrease(self):
        if self._addresses is None:
            self._calculate_signal_envelope()
            self._log_attack, self._increase, self._decrease, self._addresses = self.calculate_log_attack()

        return self._addresses[1]

    @property
    def release(self):
        if self._addresses is None:
            self._calculate_signal_envelope()
            self._log_attack, self._increase, self._decrease, self._addresses = self.calculate_log_attack()

        return self._addresses[4]

    @property
    def log_attack(self):
        """
        The log-attack-time is simply defined as LAT = log_10(t[-1]-t[0])
        """
        if self._addresses is None:
            self._calculate_signal_envelope()
            self._log_attack, self._increase, self._decrease, self._addresses = self.calculate_log_attack()

        return self._log_attack

    @property
    def decrease_slope(self):
        """
        The temporal decrease is a measure of the rate of decrease of the signal energy. It distinguishes non-sustained
        (e.g. percussive, pizzicato) sounds from sustained sounds. Its calculation is based on a decreasing exponential
        model of the energy envelope starting from it maximum.
        """
        if self._addresses is None:
            self._calculate_signal_envelope()
            self._log_attack, self._increase, self._decrease, self._addresses = self.calculate_log_attack()

        return self._decrease

    @property
    def temporal_centroid(self):
        """
        The temporal centroid is the center of gravity of the energy envelope. It distinguishes percussive from
        sustained sounds. It has been proven to be a perceptually important descriptor (Peeters et al., 2000).
        """
        if self._temporal_centroid is None:
            self._calculate_signal_envelope()
            self._temporal_centroid = self.calculate_temporal_centroid()

        return self._temporal_centroid

    @property
    def effective_duration(self):
        """
        The effective duration is a measure intended to reflect the perceived duration of the signal. It distinguishes
        percussive sounds from sustained sounds but depends on the event duration. It is approximated by the time the
        energy envelop is above a given threshold. After many empirical tests, we have set this threshold to 40%
        """
        if self._effective_duration is None:
            self._calculate_signal_envelope()
            self._effective_duration = self.calculate_effective_duration()

        return self._effective_duration

    @property
    def frequency_modulation(self):
        if self._frequency_modulation is None:
            self._frequency_modulation, self._amplitude_modulation = self.calculate_modulation()
        return self._frequency_modulation

    @property
    def zero_crossing_rate(self):
        if self._zero_cross_rate is None:
            self._temporal_feature_times, self._auto_correlation_coefficients, self._zero_cross_rate = \
                self.instantaneous_temporal_features()
        return self._zero_cross_rate

    @property
    def temporal_feature_times(self):
        if self._temporal_feature_times is None:
            self._temporal_feature_times, self._auto_correlation_coefficients, self._zero_cross_rate = \
                self.instantaneous_temporal_features()
        return self._temporal_feature_times

    @property
    def signal_envelope(self):
        if self._signal_envelope is None:
            self._calculate_signal_envelope()

        return self._signal_envelope

    @property
    def normal_signal_envelope(self):
        if self._normal_signal_envelope is None:
            self._calculate_signal_envelope()

        return self._normal_signal_envelope

    @property
    def loudness(self):
        return self.specific_loudness[0]

    @property
    def roughness(self):
        """
        This function is an implementation of the Vassilakis [2007] model of roughness.
        The peak picking algorithm implemented is based on the MIR toolbox's implementation.

        This version of timbral_roughness contains self loudness normalising methods and can accept arrays as an input
        instead of a string filename.

        Version 0.4


        Vassilakis, P. 'SRA: A Aeb-based researh tool for spectral and roughness analysis of sound signals', Proceedings
        of the 4th Sound and Music Computing Conference, Lefkada, Greece, July, 2007.

        Required parameter
        :param fname:                 string, Audio filename to be analysed, including full file path and extension.

        Optional parameters
        :param dev_output:            bool, when False return the roughness, when True return all extracted features
                                    (current none).
        :param phase_correction:      bool, if the inter-channel phase should be estimated when performing a mono sum.
                                    Defaults to False.

        :return:                      Roughness of the audio signal.

        Copyright 2018 Andy Pearce, Institute of Sound Recording, University of Surrey, UK.

        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.

        Refactored into Waveform class by Dr. Frank Mobley, 2023
        """
        from pytimbre.spectral.fractional_octave_band import FractionalOctaveBandTools as fob

        wfm = self.normalize_loudness(-24.0, False)
        # pad audio
        audio_samples = np.pad(wfm.samples, (512, 0), 'constant', constant_values=(0.0, 0.0))

        '''
          Reshape audio into time windows of 50ms.
        '''
        # reshape audio
        audio_len = len(audio_samples)
        time_step = 0.05
        step_samples = int(self.sample_rate * time_step)
        nfft = step_samples
        window = np.hamming(nfft + 2)
        window = window[1:-1]
        olap = nfft / 2
        num_frames = int(audio_len / (step_samples - olap))
        next_pow_2 = np.log(step_samples) / np.log(2)
        next_pow_2 = 2 ** int(next_pow_2 + 1)

        reshaped_audio = np.zeros([next_pow_2, num_frames])

        i = 0
        start_idx = int((i * (nfft / 2.0)))

        # check if audio is too short to be reshaped
        if audio_len > step_samples:
            # get all the audio
            while start_idx + step_samples <= audio_len:
                audio_frame = audio_samples[start_idx:start_idx + step_samples]

                # apply window
                audio_frame = audio_frame * window

                # append zeros
                reshaped_audio[:step_samples, i] = audio_frame

                # increase the step
                i += 1
                start_idx = int((i * (nfft / 2.0)))
        else:
            # reshaped audio is just padded audio samples
            reshaped_audio[:audio_len, i] = audio_samples

        spec = np.fft.fft(reshaped_audio, axis=0)
        spec_len = int(next_pow_2 / 2) + 1
        spec = spec[:spec_len, :]
        spec = np.absolute(spec)

        freq = self.sample_rate / 2 * np.linspace(0, 1, spec_len)

        # normalise spectrogram based from peak TF bin
        norm_spec = (spec - np.min(spec)) / (np.max(spec) - np.min(spec))

        ''' Peak picking algorithm '''
        _, no_segments = np.shape(spec)

        all_peak_levels = list()
        all_peak_frequency = list()

        for i in range(0, no_segments):
            # find peak candidates and add it to the lists for later usage
            _, peak_level, peak_x = fob.detect_peaks(
                norm_spec[:, i],
                cthr=0.01,
                unprocessed_array=spec[:, i],
                freq=freq
            )

            all_peak_frequency.append(peak_x)
            all_peak_levels.append(peak_level)

        all_roughness = list()

        for frame_index in range(len(all_peak_levels)):

            frame_frequency = all_peak_frequency[frame_index]
            frame_level = all_peak_levels[frame_index]

            #   Get the levels and frequencies that we will use to calculate the roughness
            if len(frame_frequency) > 1:
                f2 = np.kron(np.ones([len(frame_frequency), 1]), frame_frequency)
                f1 = f2.T
                v2 = np.kron(np.ones([len(frame_level), 1]), frame_level)
                v1 = v2.T

                X = v1 * v2
                Y = (2 * v2) / (v1 + v2)

                """
                Plomp's algorithm for estimating roughness.
                
                :param f1:  float, frequency of first frequency of the pair
                :param f2:  float, frequency of second frequency of the pair
                :return:
                """
                b1 = 3.51
                b2 = 5.75
                xstar = 0.24
                s1 = 0.0207
                s2 = 18.96
                s = np.tril(xstar / ((s1 * np.minimum(f1, f2)) + s2))
                Z = np.exp(-b1 * s * np.abs(f2 - f1)) - np.exp(-b2 * s * np.abs(f2 - f1))

                rough = (X ** 0.1) * (0.5 * (Y ** 3.11)) * Z

                all_roughness.append(np.sum(rough))
            else:
                all_roughness.append(0)

        mean_roughness = np.mean(all_roughness)

        '''
          Perform linear regression
        '''
        # cap roughness for low end
        if mean_roughness < 0.01:
            return 0
        else:
            roughness = np.log10(mean_roughness) * 13.98779569 + 48.97606571545886

            return roughness

    @property
    def sharpness(self):
        """
        This is an implementation of the matlab sharpness function found at:
        https://www.salford.ac.uk/research/sirc/research-groups/acoustics/psychoacoustics/sound-quality-making-products-sound-better/accordion/sound-quality-testing/matlab-codes

        This function calculates the apparent Sharpness of an audio file.
        This version of timbral_sharpness contains self loudness normalising methods and can accept arrays as an input
        instead of a string filename.

        Version 0.4

        Originally coded by Claire Churchill Sep 2004
        Transcoded by Andy Pearce 2018
        Refactored by Dr. Frank Mobley 2023

        :return                         Apparent sharpness of the audio file.


        Copyright 2018 Andy Pearce, Institute of Sound Recording, University of Surrey, UK.

        Licensed under the Apache License, Version 2.0 (the "License");
        you may not use this file except in compliance with the License.
        You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

        Unless required by applicable law or agreed to in writing, software
        distributed under the License is distributed on an "AS IS" BASIS,
        WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
        See the License for the specific language governing permissions and
        limitations under the License.

        """
        #   Prepare the audio file
        wfm = self.normalize_loudness(-24.0, False)
        wfm = wfm.split_by_time(4096 / wfm.sample_rate)

        windowed_sharpness = []
        windowed_rms = []
        for i in range(wfm.shape[0]):
            # calculate the rms and append to list
            windowed_rms.append(np.sqrt(np.mean(wfm[i].samples ** 2)))

            # calculate the specific loudness
            N_entire, N_single = wfm[i].specific_loudness

            # calculate the sharpness if section contains audio
            if N_entire > 0:
                """
                Calculates the sharpness based on FASTL (1991). Expression for weighting function obtained by fitting an
                equation to data given in 'Psychoacoustics: Facts and Models' using MATLAB basic fitting function.
                
                Original Matlab code by Claire Churchill Sep 2004
                Transcoded by Andy Pearce 2018
                
                Integrated into PyTimbre by Dr. Frank Mobley 2023
                """
                n = len(N_single)
                gz = np.ones(140)
                z = np.arange(141, n + 1)
                gzz = 0.00012 * (z / 10.0) ** 4 - 0.0056 * (z / 10.0) ** 3 + 0.1 * (z / 10.0) ** 2 - 0.81 * (
                        z / 10.0) + 3.5
                gz = np.concatenate((gz, gzz))
                z = np.arange(0.1, n / 10.0 + 0.1, 0.1)

                sharpness = 0.11 * np.sum(N_single * gz * z * 0.1) / np.sum(N_single * 0.1)
            else:
                sharpness = 0

            windowed_sharpness.append(sharpness)

        # convert lists to numpy arrays for fancy indexing
        windowed_rms = np.array(windowed_rms)
        windowed_sharpness = np.array(windowed_sharpness)

        # calculate the sharpness as the rms-weighted average of sharpness
        rms_sharpness = np.average(windowed_sharpness, weights=(windowed_rms * windowed_rms))

        # take the logarithm to better much subjective ratings
        rms_sharpness = np.log10(rms_sharpness)

        all_metrics = np.ones(2)
        all_metrics[0] = rms_sharpness

        # coefficients from linear regression
        coefficients = [102.50508921364404, 34.432655185001735]

        return np.sum(all_metrics * coefficients)

    @property
    def integrated_loudness(self):
        """
        As part of the determination of various values used in the Timbral_models the meter object from pyloudnorm is
        used to determine the integrated loudness. This function will replicate the signal function calculation without
        the majority of the error checking for the mono channel data within the waveform.

        Taken from pyloudnorm.meter.

        Returns
        -------
        Integrated loudness with filters for head and auditory system applied
        """

        wfm = self.apply_head_auditory_response_filters()
        if self.samples.ndim == 1:
            input_data = np.reshape(wfm.samples, (wfm.samples.shape[0], 1))
        else:
            input_data = wfm.samples

        numChannels = input_data.shape[1]
        numSamples = input_data.shape[0]
        block_size = 0.4

        G = [1.0, 1.0, 1.0, 1.41, 1.41]  # channel gains
        T_g = block_size  # 400 ms gating block standard
        Gamma_a = -70.0  # -70 LKFS = absolute loudness threshold
        overlap = 0.75  # overlap of 75% of the block duration
        step = 1.0 - overlap  # step size by percentage

        T = numSamples / self.sample_rate  # length of the input in seconds
        numBlocks = int(np.round(((T - T_g) / (T_g * step))) + 1)  # total number of gated blocks (see end of eq. 3)
        j_range = np.arange(0, numBlocks)  # indexed list of total blocks
        z = np.zeros(shape=(numChannels, numBlocks))  # instantiate array - trasponse of input

        for i in range(numChannels):  # iterate over input channels
            for j in j_range:  # iterate over total frames
                l = int(T_g * (j * step) * self.sample_rate)  # lower bound of integration (in samples)
                u = int(T_g * (j * step + 1) * self.sample_rate)  # upper bound of integration (in samples)
                # caluate mean square of the filtered for each block (see eq. 1)
                z[i, j] = (1.0 / (T_g * self.sample_rate)) * np.sum(np.square(input_data[l:u, i]))

        # loudness for each jth block (see eq. 4)
        l = [-0.691 + 10.0 * np.log10(np.sum([G[i] * z[i, j] for i in range(numChannels)])) for j in j_range]

        # find gating block indices above absolute threshold
        J_g = [j for j, l_j in enumerate(l) if l_j >= Gamma_a]

        # calculate the average of z[i,j] as show in eq. 5
        z_avg_gated = [np.mean([z[i, j] for j in J_g]) for i in range(numChannels)]
        # calculate the relative threshold value (see eq. 6)
        Gamma_r = -0.691 + 10.0 * np.log10(np.sum([G[i] * z_avg_gated[i] for i in range(numChannels)])) - 10.0

        # find gating block indices above relative and absolute thresholds  (end of eq. 7)
        J_g = [j for j, l_j in enumerate(l) if (l_j > Gamma_r and l_j > Gamma_a)]

        # calculate the average of z[i,j] as show in eq. 7 with blocks above both thresholds
        z_avg_gated = np.nan_to_num(np.array([np.mean([z[i, j] for j in J_g]) for i in range(numChannels)]))

        return -0.691 + 10.0 * np.log10(np.sum([G[i] * z_avg_gated[i] for i in range(numChannels)]))

    @property
    def specific_loudness(self):
        """
        This function originates with the timbral_models package. This is the specific_loudness function from the
        timbral_utils.py. This function calculuates loudness in one-third-octave bands based on ISO 532 B / DIN 45631
        source: BASIC code in Journal of Acoustical Society of Japan (E) 12, 1 (1991). This code always calculates the
        value for a free-field

        Returns
        -------
        N_entire = entire loudness[sone]
        N_single = partial loudness[sone / Bark]

        Original Matlab code by Claire Churchill Jun. 2004
        Transcoded by Andy Pearce 2018
        Refactored by Frank Mobley 2023
        """
        from pytimbre.spectral.fractional_octave_band import FractionalOctaveBandTools as fob

        # 'Generally used third-octave band filters show a leakage towards neighbouring filters of about -20 dB. This
        # means that a 70dB, 1 - kHz tone produces the following levels at different centre
        # frequencies: 10dB at 500Hz, 30dB at 630Hz, 50dB at 800Hz and 70dB at 1kHz.
        # P211 Psychoacoustics: Facts and Models, E.Zwicker and H.Fastl
        # (A filter order of 4 gives approx this result)

        # set default
        minimum_frequency = 25
        maximum_frequency = 12500

        #   If the values are too big for the sample rate of the waveform, we must decrease the maximum frequency
        if maximum_frequency > self.sample_rate / 2:
            #   Find the band that is closest to the Nyquist frequency, and decrement by one to ensure that we are
            #   below the theoretical limit
            band_idx = fob.exact_band_number(3, self.sample_rate / 2) - 1

            maximum_frequency = fob.center_frequency(3, band_idx)

        order = 4

        # filter the audio into appropriate one-third-octave representation
        total_pressure_decibels, band_pressures_decibels, frequencies = fob.filter_third_octaves_downsample(
            self, 100.0, minimum_frequency, maximum_frequency, order
        )

        # set more defaults for perceptual filters
        # Centre frequencies of 1 / 3 Oct bands(center_frequencies)
        center_frequencies = np.array(
            [25, 31.5, 40, 50, 63, 80, 100, 125, 160, 200, 250, 315, 400, 500, 630, 800,
             1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000, 6300, 8000, 10000, 12500]
        )

        # Ranges of 1 / 3 Oct bands for correction at low frequencies according to equal loudness contours
        low_frequency_corrections = np.array([45, 55, 65, 71, 80, 90, 100, 120])

        # Reduction of 1/3 Oct Band levels at low frequencies according to equal loudness contours
        # within the eight ranges defined by low_frequency_corrections(equal_loudness_corrections)
        equal_loudness_corrections = np.array(
            [[-32, -24, -16, -10, -5, 0, -7, -3, 0, -2, 0],
             [-29, -22, -15, -10, -4, 0, -7, -2, 0, -2, 0],
             [-27, -19, -14, -9, -4, 0, -6, -2, 0, -2, 0],
             [-25, -17, -12, -9, -3, 0, -5, -2, 0, -2, 0],
             [-23, -16, -11, -7, -3, 0, -4, -1, 0, -1, 0],
             [-20, -14, -10, -6, -3, 0, -4, -1, 0, -1, 0],
             [-18, -12, -9, -6, -2, 0, -3, -1, 0, -1, 0],
             [-15, -10, -8, -4, -2, 0, -3, -1, 0, -1, 0]]
        )

        # Critical band level at absolute threshold without taking into account the
        # transmission characteristics of the ear
        # Threshold due to internal noise Hearing thresholds for the excitation levels (each number corresponds to a
        # critical band 12.5kHz is not included)
        critical_band_threshold_noise = np.array([30, 18, 12, 8, 7, 6, 5, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3])

        # Attenuation representing transmission between free-field and our hearing system
        # Attenuation due to transmission in the middle ear
        # Moore et al disagrees with this being flat for low frequencies
        transmission_attenuation_delta = np.array(
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -0.5, -1.6, -3.2, -5.4, -5.6, -4,
             -1.5, 2, 5, 12]
        )

        # Level correction to convert from a free field to a diffuse field(last critical band 12.5 kHz is not included)
        diffuse_field_correction = np.array(
            [0, 0, 0.5, 0.9, 1.2, 1.6, 2.3, 2.8, 3, 2, 0, -1.4, -2, -1.9, -1, 0.5,
             3, 4, 4.3, 4]
        )

        # Correction factor because using third octave band levels(rather than critical bands)
        tob_level_corrections = np.array(
            [-0.25, -0.6, -0.8, -0.8, -0.5, 0, 0.5, 1.1, 1.5, 1.7, 1.8, 1.8, 1.7, 1.6,
             1.4, 1.2, 0.8, 0.5, 0, -0.5]
        )

        # Upper limits of the approximated critical bands
        critical_band_uppler_limits = np.array(
            [0.9, 1.8, 2.8, 3.5, 4.4, 5.4, 6.6, 7.9, 9.2, 10.6, 12.3, 13.8, 15.2,
             16.7, 18.1, 19.3, 20.6, 21.8, 22.7, 23.6, 24]
        )

        # Range of specific loudness for the determination of the steepness of the upper slopes in the specific loudness
        # - critical band rate pattern(used to plot the correct righthand_loudness_slope curve)
        specific_loudness_slopes = np.array(
            [21.5, 18, 15.1, 11.5, 9, 6.1, 4.4, 3.1, 2.13, 1.36, 0.82, 0.42, 0.30,
             0.22, 0.15, 0.10, 0.035, 0]
        )

        # This is used to design the right hand slope of the loudness
        righthand_loudness_slope = np.array(
            [[13.0, 8.2, 6.3, 5.5, 5.5, 5.5, 5.5, 5.5],
             [9.0, 7.5, 6.0, 5.1, 4.5, 4.5, 4.5, 4.5],
             [7.8, 6.7, 5.6, 4.9, 4.4, 3.9, 3.9, 3.9],
             [6.2, 5.4, 4.6, 4.0, 3.5, 3.2, 3.2, 3.2],
             [4.5, 3.8, 3.6, 3.2, 2.9, 2.7, 2.7, 2.7],
             [3.7, 3.0, 2.8, 2.35, 2.2, 2.2, 2.2, 2.2],
             [2.9, 2.3, 2.1, 1.9, 1.8, 1.7, 1.7, 1.7],
             [2.4, 1.7, 1.5, 1.35, 1.3, 1.3, 1.3, 1.3],
             [1.95, 1.45, 1.3, 1.15, 1.1, 1.1, 1.1, 1.1],
             [1.5, 1.2, 0.94, 0.86, 0.82, 0.82, 0.82, 0.82],
             [0.72, 0.67, 0.64, 0.63, 0.62, 0.62, 0.62, 0.62],
             [0.59, 0.53, 0.51, 0.50, 0.42, 0.42, 0.42, 0.42],
             [0.40, 0.33, 0.26, 0.24, 0.24, 0.22, 0.22, 0.22],
             [0.27, 0.21, 0.20, 0.18, 0.17, 0.17, 0.17, 0.17],
             [0.16, 0.15, 0.14, 0.12, 0.11, 0.11, 0.11, 0.11],
             [0.12, 0.11, 0.10, 0.08, 0.08, 0.08, 0.08, 0.08],
             [0.09, 0.08, 0.07, 0.06, 0.06, 0.06, 0.06, 0.05],
             [0.06, 0.05, 0.03, 0.02, 0.02, 0.02, 0.02, 0.02]]
        )

        # apply weighting factors
        Xp = np.zeros(11)
        Ti = np.zeros(11)
        for i in range(11):
            j = 0
            while ((band_pressures_decibels[i] > (low_frequency_corrections[j] - equal_loudness_corrections[j, i])) &
                   (j < 7)):
                j += 1
            Xp[i] = band_pressures_decibels[i] + equal_loudness_corrections[j, i]
            Ti[i] = 10.0 ** (Xp[i] / 10.0)

        # Intensity values in first three critical bands calculated
        critical_band_summation = np.array([np.sum(Ti[0:6]), np.sum(Ti[6:9]), np.sum(Ti[9:11])])

        if np.max(critical_band_summation) > 0.0:
            FNGi = 10 * np.log10(critical_band_summation)
        else:
            FNGi = -1.0 * np.inf
        LCB = np.zeros_like(critical_band_summation)
        for i in range(3):
            if critical_band_summation[i] > 0:
                LCB[i] = FNGi[i]
            else:
                LCB[i] = 0

        # Calculate the main loudness in each critical band
        Le = np.ones(20)
        Lk = np.ones_like(Le)
        Nm = np.ones(21)
        for i in range(20):
            Le[i] = band_pressures_decibels[i + 8]
            if i <= 2:
                Le[i] = LCB[i]
            Lk[i] = Le[i] - transmission_attenuation_delta[i]
            Nm[i] = 0
            if Le[i] > critical_band_threshold_noise[i]:
                Le[i] = Lk[i] - tob_level_corrections[i]
                S = 0.25
                MP1 = 0.0635 * 10.0 ** (0.025 * critical_band_threshold_noise[i])
                MP2 = (1 - S + S * 10 ** (0.1 * (Le[i] - critical_band_threshold_noise[i]))) ** 0.25 - 1
                Nm[i] = MP1 * MP2;
                if Nm[i] <= 0:
                    Nm[i] = 0
        Nm[20] = 0

        KORRY = 0.4 + 0.32 * Nm[0] ** 0.2
        if KORRY > 1:
            KORRY = 1

        Nm[0] = Nm[0] * KORRY

        # Add masking curves to the main loudness in each third octave band
        N = 0
        z1 = 0  # critical band rate starts at 0
        n1 = 0  # loudness level starts at 0
        j = 17
        iz = 0
        z = 0.1
        ns = []

        for i in range(21):
            # Determines where to start on the slope
            ig = i - 1
            if ig > 7:
                ig = 7
            control = 1
            while (z1 < critical_band_uppler_limits[i]) | (
                    control == 1):  # critical_band_uppler_limits is the upper limit of the approximated critical band
                # Determines which of the slopes to use
                if n1 < Nm[i]:  # Nm is the main loudness level
                    j = 0
                    while specific_loudness_slopes[j] > Nm[i]:  # the value of j is used below to build a slope
                        j += 1  # j becomes the index at which Nm(i) is first greater than specific_loudness_slopes

                # The flat portions of the loudness graph
                if n1 <= Nm[i]:
                    z2 = critical_band_uppler_limits[i]  # z2 becomes the upper limit of the critical band
                    n2 = Nm[i]
                    N = N + n2 * (z2 - z1)  # Sums the output(N_entire)
                    for k in np.arange(z, z2 + 0.01, 0.1):
                        if not ns:
                            ns.append(n2)
                        else:
                            if iz == len(ns):
                                ns.append(n2)
                            elif iz < len(ns):
                                ns[iz] = n2

                        if k < (z2 - 0.05):
                            iz += 1
                    z = k  # z becomes the last value of k
                    z = round(z * 10) * 0.1

                # The sloped portions of the loudness graph
                if n1 > Nm[i]:
                    n2 = specific_loudness_slopes[j]
                    if n2 < Nm[i]:
                        n2 = Nm[i]
                    dz = (n1 - n2) / righthand_loudness_slope[j, ig]  # righthand_loudness_slope = slopes
                    dz = round(dz * 10) * 0.1
                    if dz == 0:
                        dz = 0.1
                    z2 = z1 + dz
                    if z2 > critical_band_uppler_limits[i]:
                        z2 = critical_band_uppler_limits[i]
                        dz = z2 - z1
                        n2 = n1 - dz * righthand_loudness_slope[j, ig]  # righthand_loudness_slope = slopes
                    N = N + dz * (n1 + n2) / 2.0  # Sums the output(N_entire)
                    for k in np.arange(z, z2 + 0.01, 0.1):
                        if not ns:
                            ns.append(n1 - (k - z1) * righthand_loudness_slope[j, ig])
                        else:
                            if iz == len(ns):
                                ns.append(n1 - (k - z1) * righthand_loudness_slope[j, ig])
                            elif iz < len(ns):
                                ns[iz] = n1 - (k - z1) * righthand_loudness_slope[j, ig]
                        if k < (z2 - 0.05):
                            iz += 1
                    z = k
                    z = round(z * 10) * 0.1
                if n2 == specific_loudness_slopes[j]:
                    j += 1
                if j > 17:
                    j = 17
                n1 = n2
                z1 = z2
                z1 = round(z1 * 10) * 0.1
                control += 1

        if N < 0:
            N = 0

        if N <= 16:
            N = np.floor(N * 1000 + 0.5) / 1000.0
        else:
            N = np.floor(N * 100 + .05) / 100.0

        LN = 40.0 * (N + 0.0005) ** 0.35

        if LN < 3:
            LN = 3

        if N >= 1:
            LN = 10 * np.log10(N) / np.log10(2) + 40;

        N_single = np.zeros(240)
        for i in range(240):
            N_single[i] = ns[i]

        N_entire = N
        return N_entire, N_single

    @property
    def is_mono(self):
        """
        This function examines the size of the samples array within the function. If there is a second dimension then
        this function returns false. It is true otherwise.
        """
        return len(self.samples.shape) == 1

    @property
    def is_clipped(self):
        """
        This function attempts to determine whether there is clipping in the acoustic data represented in this waveform.
        """
        _, total_clipped_samples = Waveform._detect_clipping(self.samples)

        return (total_clipped_samples / len(self.samples)) >= 0.01

    @property
    def is_reverberant(self):
        """
        This function classifies the audio file as either not sounding reverberant.

        This is based on the RT60 estimation algorithm documented in:
        Jan, T., and Wang, W., 2012: "Blind reverberation time estimation based on Laplace distribution",
        EUSIPCO. pp. 2050-2054, Bucharest, Romania.

        Version 0.4

        Copyright 2019 Andy Pearce, Institute of Sound Recording, University of Surrey, UK.

        Refactored from timbral_models.timbral_reverb function by Dr. Frank Mobley, 2023
        """
        from pytimbre.temporal.temporal_metrics import TemporalMetrics

        # check for mono file
        if self.is_mono:
            # it's a mono file
            mean_RT60 = TemporalMetrics.estimate_RT60(self)
        else:
            # the file has channels, estimate RT for the first two and take the mean
            l_RT60 = TemporalMetrics.estimate_RT60(
                Waveform(
                    pressures=self.samples[:, 0],
                    sample_rate=self.sample_rate,
                    start_time=self.start_time
                )
            )
            r_RT60 = TemporalMetrics.estimate_RT60(
                Waveform(
                    pressures=self.samples[:, 1],
                    sample_rate=self.sample_rate,
                    start_time=self.start_time
                )
            )

            mean_RT60 = np.mean([l_RT60, r_RT60])

        '''
          need to develop a logistic regression model to test this.
        '''
        # apply linear coefficients
        coefficients = [2.97126461]
        intercept = -1.45082989
        attributes = [mean_RT60]
        logit_model = np.sum(np.array(coefficients) * np.array(attributes)) + intercept

        # apply inverse of Logit function to obtain probability
        probability = np.exp(logit_model) / (1.0 + np.exp(logit_model))

        if probability < 0.5:
            return 0
        else:
            return 1

    @property
    def fundamental_frequency(self):
        return np.median(
            yin(
                self.samples,
                self.sample_rate,
                F_max=10000,
                F_min=10,
                N=int(np.floor(self.sample_rate / 10)),
                H=int(np.floor(self.sample_rate / 10 / 4))
            )[0]
        )

    @property
    def peak_pressure(self):
        return np.max(self.samples)

    @property
    def peak_level(self):
        return 20 * np.log10(self.peak_pressure / 20e-6)

    @property
    def peak_time(self):
        return self.times[np.argmax(self.samples)]

    @property
    def leqT(self):
        if self.is_impulsive:
            # Sum and average energy across waveform for total recording time
            return self.equivalent_level(
                WeightingFunctions.unweighted, self.duration,
                leq_mode=LeqDurationMode.transient
            )

    @property
    def SEL(self):
        if self.is_impulsive:
            # Sum and average energy across waveform and scale to 1 second
            return self.equivalent_level(WeightingFunctions.unweighted, 1.0, leq_mode=LeqDurationMode.transient)
        elif self.is_continuous:
            raise NotImplementedError()

    @property
    def noise_dose(self):
        if self.is_impulsive:
            if self._noise_dose is None:
                self._process_analysis()
            return self._noise_dose
        else:
            raise ValueError("This waveform is not impulsive")

    @property
    def liaeqT(self):
        if self.is_impulsive:
            if self._liaeqT is None:
                self._process_analysis()
            return self._liaeqT
        else:
            raise ValueError("This waveform is not impulsive")

    @property
    def liaeq100ms(self):
        if self.is_impulsive:
            if self._liaeq100ms is None:
                self._process_analysis()
            return self._liaeq100ms
        else:
            raise ValueError("This waveform is not impulsive")

    @property
    def liaeq8hr(self):
        if self.is_impulsive:
            if self._liaeq8hr is None:
                self._process_analysis()
            return self._liaeq8hr
        else:
            raise ValueError("This waveform is not impulsive")

    @property
    def SELA(self):
        if self.is_impulsive:
            if self._SELA is None:
                self._process_analysis()
            return self._SELA
        else:
            raise NotImplementedError()

    @property
    def corrected_a_duration(self):
        if self.is_impulsive:
            if self._corrected_a_duration is None:
                self._process_analysis()
            return self._corrected_a_duration
        else:
            raise ValueError("This waveform is not impulsive")

    # ------------------ Static functions for the calculation of filter shapes and timbre features ---------------------
    @staticmethod
    def _detect_clipping(
            samples_array: npt.NDArray, max_threshold=0.995, min_threshold=0.995
    ) -> Tuple[Dict[str, int], int]:
        """
        Somewhat informed from https://www.sciencedirect.com/science/article/pii/S0167639321000832
        but without the sample-by-sample tagging. Intended to catch cases where clipped values have
        been normalized away.

        Returns the tagged clipped samples and the total number of clipped samples

        2023-04-06 - FSM - This function was extracted from the clipdetect project to minimize the dependency
        requirements of PyTimbre
        """
        if len(samples_array.shape) != 1:
            raise ValueError(
                "You must pass just the samples without any channel information"
            )
        max_sample = samples_array.max()
        min_sample = samples_array.min()
        max_threshold *= max_sample
        min_threshold *= min_sample
        clipping_sections = []
        total_clipped_samples = 0
        clip_end = 0
        for i, sample in enumerate(samples_array):
            if i > clip_end and sample in [max_sample, min_sample]:
                clipping_count = 0
                for new_sample in samples_array[i:]:
                    if new_sample >= max_threshold or new_sample <= min_threshold:
                        clipping_count += 1
                    else:
                        clipping_sections.append({"start": i, "end": i + clipping_count})
                        total_clipped_samples += clipping_count
                        clip_end = i + clipping_count
                        break
        return clipping_sections, total_clipped_samples

    @staticmethod
    def AC_Filter_Design(fs):
        """
        AC_Filter_Design.py

        Created on Mon Oct 18 19:27:36 2021

        @author: Conner Campbell, Ball Aerospace

        Description
        ----------
        Coeff_A, Coeff_C = AC_Filter_Design(fs)

        returns Ba, Aa, and Bc, Ac which are arrays of IRIR filter
        coefficients for A and C-weighting.  fs is the sampling
        rate in Hz.

        This progam is a recreation of adsgn and cdsgn
        by Christophe Couvreur, see	Matlab FEX ID 69.


        Parameters
        ----------
        fs : double
            sampling rate in Hz

        Returns
        -------

        Coeff_A: list
            List of two numpy arrays, feedforward and feedback filter
            coeffecients for A-weighting filter. Form of lits is [Ba,Aa]

        Coeff_c: list
            List of two numpy arrays, feedforward and feedback filter
            coeffecients for C-weighting filter. Form of lits is [Bc,Ac]

        Code Dependencies
        -------
        This program requires the following python packages:
        scipy.signal, numpy

        References
        -------
        IEC/CD 1672: Electroacoustics-Sound Level Meters, Nov. 1996.

        ANSI S1.4: Specifications for Sound Level Meters, 1983.

        ACdsgn.m: Christophe Couvreur, Faculte Polytechnique de Mons (Belgium)
        couvreur@thor.fpms.ac.be
        """

        # Define filter poles for A/C weight IIR filter according to IEC/CD 1672

        f1 = 20.598997
        f2 = 107.65265
        f3 = 737.86223
        f4 = 12194.217
        A1000 = 1.9997
        C1000 = 0.0619
        pi = np.pi

        # Calculate denominator and numerator of filter tranfser functions

        coef1 = (2 * pi * f4) ** 2 * (10 ** (C1000 / 20))
        coef2 = (2 * pi * f4) ** 2 * (10 ** (A1000 / 20))

        Num1 = np.array([coef1, 0.0])
        Den1 = np.array([1, 4 * pi * f4, (2 * pi * f4) ** 2])

        Num2 = np.array([1, 0.0])
        Den2 = np.array([1, 4 * pi * f1, (2 * pi * f1) ** 2])

        Num3 = np.array([coef2 / coef1, 0.0, 0.0])
        Den3 = scipy.signal.convolve(np.array([1, 2 * pi * f2]).T, (np.array([1, 2 * pi * f3])))

        # Use scipy.signal.bilinear function to get numerator and denominator of
        # the transformed digital filter transfer functions.

        B1, A1 = scipy.signal.bilinear(Num1, Den1, fs)
        B2, A2 = scipy.signal.bilinear(Num2, Den2, fs)
        B3, A3 = scipy.signal.bilinear(Num3, Den3, fs)

        Ac = scipy.signal.convolve(A1, A2)
        Aa = scipy.signal.convolve(Ac, A3)

        Bc = scipy.signal.convolve(B1, B2)
        Ba = scipy.signal.convolve(Bc, B3)

        Coeff_A = [Ba, Aa]
        Coeff_C = [Bc, Ac]
        return Coeff_A, Coeff_C

    @staticmethod
    def detect_local_extrema(input_v, lag_n):
        """
        This will detect the local maxima of the vector on the interval [n-lag_n:n+lag_n]

        Parameters
        ----------
        input_v : double array-like
            This is the input vector that we are examining to determine the local maxima
        lag_n : double, integer
            This is the number of samples that we are examining within the input_v to determine the local maximum

        Returns
        -------
        pos_max_v : double, array-like
            The locations of the local maxima
        """

        do_affiche = 0
        lag2_n = 4
        seuil = 0

        L_n = len(input_v)

        pos_cand_v = np.where(np.diff(np.sign(np.diff(input_v))) < 0)[0]
        pos_cand_v += 1

        pos_max_v = np.zeros((len(pos_cand_v),))

        for i in range(len(pos_cand_v)):
            pos = pos_cand_v[i]

            if (pos > lag_n) & (pos <= L_n - lag_n):
                tmp = input_v[pos - lag_n:pos + lag2_n]
                position = np.argmax(tmp)

                position = position + pos - lag_n - 1

                if (pos - lag2_n > 0) & (pos + lag2_n < L_n + 1):
                    tmp2 = input_v[pos - lag2_n:pos + lag2_n]

                    if (position == pos) & (input_v[position] > seuil * np.mean(tmp2)):
                        pos_max_v[i] = pos

        return pos_max_v

    @staticmethod
    def next_pow2(x: int):
        n = np.log2(x)
        return 2 ** (np.floor(n) + 1)

    @staticmethod
    def gps_audio_signal_converter(filename: str):
        """
        This function will convert the data from an audio file that captured the GPS signal and converted it to an
        audio channel.

        This function is adapted from the Python code delivered as part of the ESCAPE 2018 dataset (gps_wav.py)

        Parameters
        ----------
        filename: str - the full path to the audio file
        """
        import wave
        import struct
        import scipy.signal
        import re

        #   Initialize some parsing variables
        start_search = 2
        win = 1000
        thrE = 1000
        thr = 2500
        gap = 99

        #   Load the wave data
        wave_object = wave.open(filename, 'rb')
        channel_count = wave_object.getnchannels()
        bit_count = wave_object.getsampwidth()
        sample_rate = wave_object.getframerate()
        frame_count = wave_object.getnframes()
        temp_data = wave_object.readframes(frame_count)
        data = struct.unpack("<" + str(frame_count) + "h", temp_data)

        #   Filter the data with a high-pass filter to remove any DC offsets
        data = scipy.signal.lfilter([1.0, -1.0], 1.0, data)

        #   Find first complete GPS data burst
        energy = []
        filtered_data = []
        for i in range(0, start_search * sample_rate, win):
            energy = np.sum(np.square(data[i:i + win])) / win
            if energy < thrE:
                offset = i + win
                filtered_data.extend(data[offset:frame_count])
                frame_count = len(filtered_data)
                break

        # Detect pulse state transitions in audio signal
        state = True
        detect = []
        ind = []
        indPlus = []
        for i in range(1, np.min([250000, frame_count])):
            if (filtered_data[i] >= filtered_data[i + 1]) & (filtered_data[i] > filtered_data[i - 1]):
                if filtered_data[i] > thr:
                    detect.append(state)
                    state = not state
                    ind.append(i)
                    indPlus.append(i)
            elif (filtered_data[i] <= filtered_data[i + 1]) & (filtered_data[i] < filtered_data[i - 1]):
                if filtered_data[i] < -thr:
                    detect.append(state)
                    state = not state
                    ind.append(i)

        # Extract bit sequence and corresponding sample indices
        bits = []
        index = []
        index.append(ind[0])
        for i in range(len(ind) - 1):
            if (ind[i + 1] - ind[i]) > gap:
                bits.append(1)
                index.append(ind[i + 1])
                # print(ind[i+1])
                continue
            if detect[i]:
                bits.extend(np.zeros(int(round((ind[i + 1] - ind[i]) / 10.0)), dtype=int))
            else:
                bits.extend(np.ones(int(round((ind[i + 1] - ind[i]) / 10.0)), dtype=int))

        #   Extract NMEA 0183 sentences from bit sequence and write to file
        s = ''
        sent = ''
        cnt = 0
        for i in range(int(len(bits) / 10)):
            word = s.join(map(str, bits[cnt:cnt + 10]))
            cnt = cnt + 10
            if bool(int(word[0])) or bool(int(word[8])) or not (bool(int(word[9]))):
                # continue
                wordE = []
                for k in range(10):
                    wordE.append(str(int(not (bool(int(word[k]))))))
                word = s.join(wordE)
            sent = sent + chr(int('0b' + word[8:0:-1], 2))

        elements = sent.split('\r\n')

        for i in range(len(elements)):
            if elements[i].split(',')[0] == "$GPRMC":
                first_rmc = elements[i]
                break

        # Find start of 1st complete GPS data bursts
        indBurst = indPlus[0] + offset
        elements = first_rmc.split(',')
        hour = int(elements[1][:2])
        minute = int(elements[1][2:4])
        start_time = (60 * (60 * int(elements[1][:2]) + int(elements[1][2:4])) + float(elements[1][4:]) - indBurst /
                      sample_rate)
        date = datetime(int(elements[9][4:]) + 2000, int(elements[9][2:4]), int(elements[9][:2])) + \
               timedelta(seconds=start_time)

        return date

    @staticmethod
    def generate_tone(
            frequency: float = 100, sample_rate: float = 48000, duration: float = 1.0,
            amplitude_db: float = 94
    ):
        """
        This function generates a sine wave tone function with the specific frequency and duration specified in the
        argument list.

        Parameters
        ----------
        frequency: float, default: 100 - the linear frequency of the waveform
        sample_rate: float, default: 48000 - the number of samples per second
        duration: float, default: 1.0 - the total number of seconds in the waveform
        amplitude_db: float, default:94, this is the RMS amplitude of the waveform

        Returns
        -------
        A waveform this the generated data.
        """

        amplitude_rms = 10 ** (amplitude_db / 20) * 2e-5
        x = np.arange(0, duration, 1 / sample_rate)
        y = amplitude_rms * np.sqrt(2) * np.sin(2 * np.pi * frequency * x)

        return Waveform(y, sample_rate, 0)

    @staticmethod
    def generate_noise(
            sample_rate: float = 48000, duration: float = 1.0, amplitude_db: float = 94,
            noise_color=NoiseColor.pink
    ):
        samples = cn.powerlaw_psd_gaussian(noise_color.value, int(np.floor(duration * sample_rate)))

        wfm = Waveform(samples, sample_rate, 0)
        scaling = amplitude_db - wfm.overall_level()
        wfm.scale_signal(scaling, True, ScalingMethods.logarithmic)

        return wfm

    @staticmethod
    def generate_friedlander(
            peak_level: float = 165, a_duration: float = 0.005, duration: float = 3
            , sample_rate: float = 200e3, blast_time: float = 0.005 / 2.0, noise: bool = False
    ):
        """
        Generates a generic_time_waveform object containing a Friedlander waveform
        :param peak_level: float, defaults to 165dB.
        :param a_duration: float, defaults to 0.005s.
        :param duration: float, length of total waveform in s. Defaults to 3s.
        :param sample_rate: float, defaults to 200e3 Hz.
        :param blast_time: float, time when friedlander starts in signal. Defualts to half the default a_duration and
        must be less than the duration of the signal minus 2 * a_duration.
        :param noise: bool, if True adds +/-94dB random noise (1pa) to the signal.

        -20220325 - SCC - Created method.
        """
        # time array, sec.
        t0 = 0.0

        if blast_time >= duration - 2.0 * a_duration:
            raise ValueError("Blast time inout must be before the end of the duration of the signal!")

        else:

            t = np.arange(t0, duration + 1 / sample_rate, 1 / sample_rate)

            if noise is True:
                p = np.random.randint(-1, 1, size=(len(t) - 1,)) / 1.0

            else:
                p = np.zeros(len(t) - 1)

            t_fried = np.arange(t0 / sample_rate, duration - blast_time + 1 / sample_rate, 1 / sample_rate)

            p_fried = np.exp(-1.0 * t_fried / a_duration)
            p_fried = np.multiply(p_fried, (1.0 - t_fried / a_duration))
            p_fried = (10.0 ** (peak_level / 20.0) * 2e-5) * p_fried

            p[round(blast_time * sample_rate - 1):] = p_fried

            fried = Waveform(
                pressures=p, sample_rate=sample_rate, start_time=t0, is_continuous_wfm=False,
                is_steady_state=False
            )
            fried.is_impulsive = True

            return fried

    @staticmethod
    def irig_converter(signal):
        """
        Compute the time of the signal using the IRIG-B format as reference.

        Parameters
        ----------
        signal : double, array-like

        Returns
        -------
        datetime object for the start of the sample
        """

        irig = signal * 30.0 / np.max(signal)
        si = np.sign(irig - np.mean(irig))

        dsi = np.diff(si)

        rise = np.where(dsi == 2)[0]
        fall = np.where(dsi == -2)[0]

        if np.min(fall) < np.min(rise):
            fall = fall[1:]

        if np.max(rise) > np.max(fall):
            rise = rise[:-1]

        rf = np.stack([rise, fall]).transpose()

        index = np.round(np.mean(rf, axis=1, dtype='int'))
        top = irig[index]
        top2 = (top > 20) * 30 + (top < 20) * 10 - 10

        p0pr = np.array([30, 30, 30, 30, 30, 30, 30, 30, 10, 10, 30, 30, 30, 30, 30, 30, 30, 30]) - 10

        #   Locate this sequence in the top2 array

        pr = list()
        for i in range(len(top2) - len(p0pr)):
            located = True
            for j in range(len(p0pr)):
                if top2[i + j] != p0pr[j]:
                    located = False
                    break
            if located:
                pr.append(i + 10)

        prrise = rise[pr]
        sps = np.mean(np.diff(prrise))

        carr = np.mean(np.diff(pr))

        seconds = np.zeros((len(pr) - 1,))
        minutes = np.zeros((len(pr) - 1,))
        hours = np.zeros((len(pr) - 1,))
        day_of_year = np.zeros((len(pr) - 1,))
        dt = np.zeros((len(pr) - 1,))

        for j in range(len(pr) - 1):

            start_index = int(pr[j] + 0.01 * carr)
            stop_index = int(pr[j] + 0.01 * 2 * carr)

            values = np.array([1, 2, 4, 8, 0, 10, 20, 40])
            mask = np.zeros((len(values),))

            for i in range(len(mask)):
                if np.sum(top2[start_index:stop_index]) > 70:
                    mask[i] = 1

                start_index += 10
                stop_index += 10

            seconds[j] = np.sum(values * mask)

            start_index = int(pr[j] + 0.01 * carr * 10)
            stop_index = int(pr[j] + 0.01 * 11 * carr)

            values = np.array([1, 2, 4, 8, 0, 10, 20, 40])
            mask = np.zeros((len(values),))

            for i in range(len(mask)):
                if np.sum(top2[start_index:stop_index]) > 70:
                    mask[i] = 1

                start_index += 10
                stop_index += 10

            minutes[j] = np.sum(values * mask)

            start_index = int(pr[j] + 0.01 * carr * 20)
            stop_index = int(pr[j] + 0.01 * 21 * carr)

            values = np.array([1, 2, 4, 8, 0, 10, 20])
            mask = np.zeros((len(values),))

            for i in range(len(mask)):
                if np.sum(top2[start_index:stop_index]) > 70:
                    mask[i] = 1

                start_index += 10
                stop_index += 10

            hours[j] = np.sum(values * mask)

            start_index = int(pr[j] + 0.01 * carr * 30)
            stop_index = int(pr[j] + 0.01 * 31 * carr)

            values = np.array([1, 2, 4, 8, 0, 10, 20, 40, 80, 0, 100, 200])
            mask = np.zeros((len(values),))

            for i in range(len(mask)):
                if np.sum(top2[start_index:stop_index]) > 70:
                    mask[i] = 1

                start_index += 10
                stop_index += 10

            day_of_year[j] = np.sum(values * mask)

            #   Determine the linear adjustment for the zero cross over not occurring right on the sample

            dt[j] = (np.interp(0, [irig[prrise[j]], irig[prrise[j] + 1]], [prrise[j], prrise[j] + 1]) - prrise[j]) / sps

        #   Compute the time past midnight

        times = 60 * (60 * hours + minutes) + seconds - dt

        day_of_year = np.mean(day_of_year)

        index = np.arange(0, len(irig))
        timevector = times[0] + (index - prrise[0]) / sps

        return times[0] - prrise[0] / sps, day_of_year

    @staticmethod
    def irig_converter_for_arc(data, fs):
        """
        The timecode generators present at the Aeroacoustic Research Complex (ARC) produce the signal that defines
        the IRIG-
        B timecode differently. The previous methods do not return the correct information for the ARC data.


        """
        #   Find the index of the first minimum - which is assumed to occur within the first second of the waveform

        index = np.where(data[:fs] == np.min(data[:fs]))[0][0]

        #   The IRIG-B waveform is an amplitude modulated 1 kHz sine wave.  So we need to know the number of samples
        #   for a single period of the waveform

        frequency = 1000
        period = 1 / frequency
        period_samples = period * fs

        #   Now we can get the first set of signals and determine the amplitude for the minima

        amplitudes = np.zeros((3000,))

        for i in range(3000):
            amplitudes[i] = data[int(index + i * period_samples)]

            if index + (i + 1) * period_samples >= len(data):
                break

        maximum_index = i

        #   Scale by the smallest value in this array

        amplitudes /= np.min(amplitudes)

        #   Convert this to a binary array that will be used for the determination of the bit-wise elements of the
        #   signal

        binary_array = np.zeros((maximum_index,))

        for i in range(maximum_index):
            if amplitudes[i] >= 0.8:
                binary_array[i] = 1

        #   Now the start of a signal must be with a signal that is 8, so we need to locate the first 8 within the
        #   summation of the binary signal.

        first_eight = -1
        for i in range(3000):
            elements = binary_array[i:i + 10]

            if np.sum(elements) == 8 and binary_array[i] == 1 and binary_array[i + 9] == 0:
                first_eight = i
                break

        if first_eight < 0:
            return None, None

        #   Now that we have determined the location of the first 8, we can begin to sum the binary array in
        #   sections of 10 elements at a time

        summed_array = np.zeros((250,))

        for i in range(250):
            idx = first_eight + i * 10
            summed_array[i] = np.sum(binary_array[idx:idx + 10])

        #   Now we must find the first double-8 as this marks the beginning of the time code definition

        first_double_eight = -1
        for i in range(250):
            if summed_array[i] == 8 and summed_array[i + 1] == 8:
                first_double_eight = i + 1
                break

        if first_double_eight < 0:
            return None, None

        #   Now from this we need to extract the various parts of the time code

        timecode_elements = summed_array[first_double_eight:first_double_eight + 100]

        #   Get the hours

        hour_elements = timecode_elements[20:30]
        hour_elements[np.where(hour_elements < 5)[0]] = 0
        hour_elements[np.where(hour_elements >= 5)[0]] = 1

        weights = np.array([1, 2, 4, 8, 0, 10, 20, 0, 0, 0])

        hour = np.sum(hour_elements * weights)

        #   Get the minutes

        minute_elements = timecode_elements[10:20]
        minute_elements[np.where(minute_elements < 5)[0]] = 0
        minute_elements[np.where(minute_elements == 5)[0]] = 1
        weights = np.array([1, 2, 4, 8, 0, 10, 20, 40, 0, 0])

        minutes = np.sum(minute_elements * weights)

        #   Next the seconds

        seconds_elements = timecode_elements[:10]
        seconds_elements[np.where(seconds_elements < 5)[0]] = 0
        seconds_elements[np.where(seconds_elements == 5)[0]] = 1
        weights = np.array([0, 1, 2, 4, 8, 0, 10, 20, 40, 0])

        seconds = np.sum(seconds_elements * weights)

        #   And finally we get the julian date of the time code

        date_elements = timecode_elements[30:42]
        date_elements[np.where(date_elements != 5)[0]] = 0
        date_elements[np.where(date_elements == 5)[0]] = 1
        weights = np.array([1, 2, 4, 8, 0, 10, 20, 40, 80, 0, 100, 200])

        julian_date = np.sum(weights * date_elements)

        #   Now we know that the time code was not at the very beginning of the signal, so let's go ahead and
        #   determine the time offset to the beginning of the file.

        tpm = 60 * (60 * hour + minutes) + seconds

        file_start_adjustment = (((first_double_eight + 1) * 10 + first_eight) * (fs / 1000) + index) / fs

        tpm -= file_start_adjustment

        return tpm, julian_date

    @staticmethod
    def convert_stdbin_header(header_line):
        """
        This function will take the information within the header line and remove
        the semicolon in the front and all ellipsoid markers to determine the name
        of the property.  It also splits based on the colon to determine the value

        @author: Frank Mobley

        Parameters
        ----------
        header_line : STRING
            The line of text from the header of the file

        Returns
        -------
        name : STRING
            The name of the property or attribute

        value : STRING
            The value of the property

        """

        #   Split the string based on the colon

        elements = header_line.split(':')

        if len(elements) > 2:
            value = ':'.join(elements[1:])
        else:
            value = elements[1].strip()
        name = elements[0][1:].split('.')[0]

        return name, value

    @staticmethod
    def read_stdbin_header_line(binary_file):
        """
        Python does not provide the ability to read a line of text from a
        binary file.  This function will read from the current position in the
        file to the new line character.  The set of bytes is then converted to
        a string and returned to the calling function.

        @author: frank Mobley

        Parameters
        ----------
        binary_file : FILE
            The file pointer that will be read from

        Returns
        -------
        The string representing a line of ASCII characters from the file.

        """

        #   Get the current position within the file so that we can return here
        #   after determining where the end of the file is.

        current_position = binary_file.tell()

        #   Find the end of the file

        binary_file.seek(-1, 2)

        eof = binary_file.tell()

        #   Return to the point we were within the file

        binary_file.seek(current_position, 0)

        #   Read until the last character is a new line or we have reached the
        #   end of the file.

        characters = ''
        char = ' '
        while ord(char) != 10 or binary_file.tell() == eof - 1:
            char = binary_file.read(1)
            if ord(char) != 10:
                characters += char.decode()

        return characters

    @staticmethod
    def from_StandardBinaryFile(
            path: str,
            sample_rate_key: str = 'SAMPLE RATE (HZ)',
            start_time_key: str = 'TIME (UTC ZULU)',
            sample_format_key: str = 'SAMPLE FORMAT',
            data_format_key: str = 'DATA FORMAT',
            sample_count_key: str = 'SAMPLES TOTAL',
            s0=None,
            s1=None
            ):
        """
        This will create a waveform object from a Standard Binary File formatted file.
        :param s1: The end sample to read from the file. If it is None, then the last sample is read
        :type s1: int
        :param s0: The first or start sample to read from the file. If it is None, then the data is read from the first
        :type s0: int
        :param sample_count_key: The name of the header field that defines the sample count
        :type sample_count_key: string
        :param data_format_key: The name of the header field that defines the data format
        :type data_format_key: string
        :param sample_format_key: The name of the header field that defines the sample format
        :type sample_format_key: string
        :param start_time_key: The name of the header field that defines the start time of the first sample
        :type start_time_key: string
        :param sample_rate_key: The name of the header field that defines the number of samples per second
        :type sample_rate_key: string
        :param path: The full path to the file to read
        :type path: string
        :return: the contents of the file
        :rtype: Waveform
        """
        import struct

        try:
            #   Open the file for reading in binary format
            f_in = open(path, 'rb')

            #   Read the lines of header information
            name, value = Waveform.convert_stdbin_header(Waveform.read_stdbin_header_line(f_in))

            #   This is the header line, so now we can determine how many total lines of header information is
            #   present in the file
            header_line_count = int(value)

            #   Read through the lines and extract the data as command and values that are inserted into a
            #   dictionary.
            header = dict()
            for i in range(header_line_count - 1):
                #   Split the data in the header line
                name, value = Waveform.convert_stdbin_header(Waveform.read_stdbin_header_line(f_in))

                #   In effort to make the CSV representation of the data from the TimeHistory functions we need
                #   to ensure that the commas and extra carriage return/line feeds are removed.
                while ',' in name:
                    name = name.replace(',', ';')
                while ',' in value:
                    value = value.replace(',', ';')

                while '\r' in name:
                    name = name.replace('\r', '')
                while '\r' in value:
                    value = value.replace('\r', '')

                while '\n' in name:
                    name = name.replace('\n', '')

                #   Assign the key and value within the dictionary
                header[name] = value

            #   Now to effectively understand how to read the data from the binary portion, we must determine
            #   where specific data within the header exist. So look for the elements that were defined within
            #   the function prototype.
            #
            #   The sample rate
            fs = Waveform.read_sample_rate(header, sample_rate_key)

            #   The start time of the audio file
            t0 = Waveform.read_start_time(header, start_time_key)

            #   The number of samples in the waveform
            length = Waveform.read_sample_count(header, sample_count_key)

            #   At this point there should be no reason for the data to be stored as anything other than REAL*4
            #   Little Endian, but we do not account for any other formats, so we must now examine what is in the
            #   header and exit if it is not what we expect.
            Waveform.read_format(header, sample_format_key, data_format_key)

            data_offset = f_in.tell()

            if s0 is not None and s0 > 0:
                # At this point we should interrogate the header to determine the size of the data sample,
                # but we are only supporting floating point values, so we can just increment the current location
                # by four times the desired start sample. So let's move the counter from the current position.
                f_in.seek(s0 * 4, 1)

            #   Now we need to determine how many sample to read
            if s0 is not None and s1 is None:
                length -= s0
                if isinstance(t0, datetime):
                    t0 += timedelta(seconds=s0 / fs)
                elif isinstance(t0, float):
                    t0 += s0 / fs
            elif s0 is None and s1 is not None:
                length = s1
            elif s0 is not None and s1 is not None:
                length = s1 - s0
                if isinstance(t0, datetime):
                    t0 += timedelta(seconds=s0 / fs)
                elif isinstance(t0, float):
                    t0 += s0 / fs

            #   Read the data - At this point we only support 32-bit/4-byte data samples
            data = f_in.read(4 * length)

            #   Now unpack the data from the array of bytes into an array of floating point data
            samples = np.asarray(struct.unpack('f' * length, data))

            #   close the file
            f_in.close()

            return Waveform(pressures=samples, sample_rate=fs, start_time=t0, header=header)

        except IndexError:
            f_in.close()

            raise ValueError()
        except ValueError:
            f_in.close()

            raise ValueError()

    # ---------------------------- Protected functions for feature calculation -----------------------------------------

    @staticmethod
    def read_sample_rate(header, key):
        if key not in header.keys():
            raise ValueError(
                "The name of the sample rate element of the waveform is not located within the "
                "header dictionary. Please provide the correct name of the sample rate property"
                )
        else:
            return float(header[key])

    @staticmethod
    def read_start_time(header, key):
        from dateutil import parser

        if key not in header.keys() and "TIME (TPM)" not in header.keys():
            raise ValueError(
                "The name of the start time element of the waveform is not located within the "
                "header dictionary. Please provide the correct name of the start time property"
            )
        elif "TIME (TPM)" in header.keys():
            return float(header['TIME (TPM)'])
        else:
            return parser.parse(header[key])

    @staticmethod
    def read_sample_count(header, key):
        if key not in header.keys():
            raise ValueError(
                "The number of samples must be provided, and the expected header element is not "
                "found within the list of objects in the header."
                )
        else:
            return int(header[key])

    @staticmethod
    def read_format(header, sample_format_key, data_format_key):
        if sample_format_key not in header.keys():
            raise ValueError(
                "The name of the sample format element of the waveform is not located within the "
                "header dictionary. Please provide the correct name of the sample format property"
            )
        else:
            if header[sample_format_key].upper() != "LITTLE ENDIAN":
                raise ValueError("The expected format is not present in the header.")

        if data_format_key not in header.keys():
            raise ValueError(
                "The name of the data format element of the waveform is not located within the "
                "header dictionary. Please provide the correct name of the data format property"
            )
        else:
            if header[data_format_key].upper() != "REAL*4":
                raise ValueError("The required sample formate is not present in the header.")

    def _find_attack_endpoints(self, position_value, percent_step, method: int = 3):
        """
        Determine the start and stop positions based on selected method.
        Methods 1 and 2 are using fixed thresholds to estimate the end position. According to Peeters, these are found
        insufficiently robust with real signals. As such he proposed a "weakest-effort method" in 2004 to estimate
        the indices for the start and stop of the attack.

        Parameters
        ----------
        :param position_value:
        :param percent_step:
        :param method:
        """

        if method == 1:  # Equivalent to a value of 80%
            start_attack_position = position_value[0]
            end_attack_position = position_value[int(np.floor(0.8 / percent_step))]
        elif method == 2:  # Equivalent to a value of 100%
            start_attack_position = position_value[0]
            end_attack_position = position_value[int(np.floor(1.0 / percent_step))]
        elif method == 3:
            #   Calculate the position for each threshold
            percent_value_value = np.arange(percent_step, 1 + percent_step, percent_step)
            percent_value_position = np.zeros(percent_value_value.shape)

            for p in range(len(percent_value_value)):
                percent_value_position[p] = np.where(self.normal_signal_envelope >= percent_value_value[p])[0][0]

            #   Define parameters for the calculation of the search for the start and stop of the attack
            #
            #   The terminations for the mean calculation
            m1 = int(round(0.3 / percent_step)) - 1
            m2 = int(round(0.6 / percent_step))

            #   define the multiplicative factor for the effort
            multiplier = 3

            #   Terminations for the start attack correction
            s1att = int(round(0.1 / percent_step)) - 1
            s2att = int(round(0.3 / percent_step))

            #   Terminations for the end attack correction
            e1att = int(round(0.5 / percent_step)) - 1
            e2att = int(round(0.9 / percent_step))

            #   Calculate the effort as the effective difference in adjacent position values
            percent_position_value = np.diff(percent_value_position)

            #   Determine the average effort
            M = np.mean(percent_position_value[m1:m2])

            #   Start the start attack calculation
            #   we start just after the effort to be made (temporal gap between percent) is too large
            position2_value = np.where(percent_position_value[s1att:s2att] > multiplier * M)[0]

            if len(position2_value) > 0:
                index = int(np.floor(position2_value[-1] + s1att))
            else:
                index = int(np.floor(s1att))

            start_attack_position = percent_value_position[index]

            #   refinement: we are looking for the local minimum
            delta = int(np.round(0.25 * (percent_value_position[index + 1] - percent_value_position[index]))) - 1
            n = int(np.floor(percent_value_position[index]))

            if delta == 0:
                min_position = n
                end_attack_position = 2 * n
            elif n - delta >= 0:
                min_position = np.argmin(self.normal_signal_envelope[n - delta:n + delta])
                start_attack_position = min_position + n - delta - 1

            #   Start the end attack calculation
            #   we STOP JUST BEFORE the effort to be made (temporal gap between percent) is too large
            position2_value = np.where(percent_position_value[e1att:e2att] > multiplier * M)[0]

            if len(position2_value) > 0:
                index = int(np.floor(position2_value[0] + e1att))
            else:
                index = int(np.floor(e1att))

            end_attack_position = percent_value_position[index]

            #   refinement: we are looking for the local minimum
            delta = int(np.round(0.25 * (percent_value_position[index] - percent_value_position[index - 1])))
            n = int(np.floor(percent_value_position[index]))

            if delta == 0:
                min_position = n
                end_attack_position = 2 * n
            elif n - delta >= 0:
                min_position = np.argmax(self.normal_signal_envelope[n - delta:n + delta + 1])
                end_attack_position = min_position + n - delta

        return start_attack_position, end_attack_position

    def _calculate_signal_envelope(self):
        #   Calculate the energy envelope of the signal that is required for many of the features

        analytic_signal = scipy.signal.hilbert(self.samples)
        amplitude_modulation = np.abs(analytic_signal)
        normalized_freq = self.cutoff_frequency / (self.sample_rate / 2)
        sos = scipy.signal.butter(3, normalized_freq, btype='low', analog=False, output='sos')
        self._signal_envelope = scipy.signal.sosfilt(sos, amplitude_modulation)

        #   Normalize the envelope

        self._normal_signal_envelope = (self.signal_envelope - self.signal_envelope.min()) / np.ptp(
            self.signal_envelope
            )

    def _trim_by_samples(self, s0: int = None, s1: int = None):
        """
        This function will trim the waveform and return a subset of the current waveform based on sample indices within
        the 'samples' property within this class.

        Parameters
        __________
        :param s0: int - the start sample of the trimming. If s0 is None, then interface will use the first sample
        :param s1: int - the stop sample of the trimming. If s1 is None, then the interface uses the last sample

        Returns
        _______
        :returns: Waveform - a subset of the waveform samples
        """

        #   Handle the start/stop samples may be passed as None arguments
        if s0 is None:
            s0 = 0

        if s1 is None:
            s1 = self._samples.shape[0]

        #   Determine the new start time of the waveform
        if isinstance(self.start_time, datetime):
            t0 = self.start_time + timedelta(seconds=s0 / self.sample_rate)
        else:
            t0 = self.start_time + s0 / self.sample_rate

        #   Create the waveform based on the new time, and the subset of the samples
        wfm = Waveform(self.samples[np.arange(s0, s1)].copy(),
                       self.sample_rate,
                       t0,
                       remove_dc_offset=False,
                       header=self.header)

        #   Copy values that can be changed through properties, but are set in the constructor
        wfm.is_continuous = self.is_continuous
        wfm.is_steady_state = self.is_steady_state
        wfm.impulse_analysis_method = self.impulse_analysis_method
        wfm.cutoff_frequency = self.cutoff_frequency
        wfm.window_size_seconds = self.window_size_seconds
        wfm.hop_size_seconds = self.hop_size_seconds
        wfm.coefficient_count = self.coefficient_count
        wfm.temporal_threshold_finding = self.temporal_threshold_finding

        return wfm

    def _scale_waveform(self, scale_factor: float = 1.0, inplace: bool = False):
        """
        This function applies a scaling factor to the waveform's sample in a linear scale factor.

        Parameters
        __________
        :param scale_factor: float - the linear unit scale factor to change the amplitude of the sample values
        :param inplace: boolean - Whether to modify the samples within the current object, or return a new object

        Returns
        _______
        :returns: If inplace == True a new Waveform object with the sample magnitudes scaled, None otherwise
        """

        if inplace:
            self._samples *= scale_factor

            return None
        else:
            return Waveform(self._samples * scale_factor,
                            self.sample_rate,
                            self.start_time,
                            remove_dc_offset=False,
                            header=self.header)

    def _process_mil_std_1474e(self):
        # Process A-weighted equivalent energy metrics in accordance to MIL-STD 1474E B.5.3.2 EQ 1A
        # Sum and average energy across waveform for total recording time
        self._liaeqT = self.equivalent_level(
            weighting=WeightingFunctions.a_weighted,
            equivalent_duration=self.duration,
            leq_mode=LeqDurationMode.transient
        )
        self._liaeq100ms = self.equivalent_level(
            weighting=WeightingFunctions.a_weighted,
            equivalent_duration=0.1,
            leq_mode=LeqDurationMode.transient
        )

        # Limit A-duration according to Notes 1-3 in MIL-STD-1474E B.5.4.1
        if self.a_duration < 2e-4:
            self._corrected_a_duration = 2e-4
        elif self.a_duration > 2.5e-3:
            self._corrected_a_duration = 2.5e-3
        else:
            self._corrected_a_duration = self.a_duration

        # Process A-weighted 8-hour equivalent energy metric in accordance to MIL-STD 1474E B.5.4.1 EQ 3A and 3B

        self._liaeq8hr = self._liaeqT + 10.0 * np.log10(self.duration / 28800.0) - 1.5 * 10.0 * \
                         np.log10(self._corrected_a_duration / 2e-4)
        self._SELA = self._liaeq8hr + 10.0 * np.log10(28800.0 / 1.0)

        # Process noise dose with 3 db exchange rate, 85dBA limit for 8 hours from MIL-STD 1474E B.5.3.4.2 EQ 4
        self._noise_dose = 100.0 / (2 ** ((85 - self._liaeq8hr) / 3.0))

    def _process_mil_std_1474e_afrl_pref(self):
        # Process A-weighted equivalent energy metrics in accordance to MIL-STD 1474E B.5.3.2 EQ 1A
        # Sum and average energy across waveform for total recording time
        # Limit A-duration according to Notes 1-3 in MIL-STD-1474E B.5.4.1
        if self.a_duration < 2e-4:
            self._corrected_a_duration = 2e-4
        elif self.a_duration > 2.5e-3:
            self._corrected_a_duration = 2.5e-3
        else:
            self._corrected_a_duration = self.a_duration

        self._liaeqT = self.equivalent_level(
            weighting=WeightingFunctions.a_weighted,
            equivalent_duration=self.duration,
            leq_mode=LeqDurationMode.transient
        )
        self._liaeqT -= 1.5 * 10.0 * np.log10(self._corrected_a_duration / 2e-4)

        self._SELA = self._liaeqT + 10.0 * np.log10(self.duration / 1.0)

        self._liaeq100ms = self._liaeqT + 10.0 * np.log10(self.duration / 0.1)

        # Process A-weighted 8-hour equivalent energy metric in accordance to MIL-STD 1474E B.5.4.1 EQ 3A and 3B
        self._liaeq8hr = self._liaeqT + 10.0 * np.log10(self.duration / 28800.0)

        # Process noise dose with 3 db exchange rate, 85dBA limit for 8 hours from MIL-STD 1474E B.5.3.4.2 EQ 4
        self._noise_dose = 100.0 / (2 ** ((85 - self._liaeq8hr) / 3.0))

    def _process_no_a_duration_correction(self):
        self._corrected_a_duration = self.a_duration

        # Process A-weighted equivalent energy metrics in accordance to MIL-STD 1474E without a_duration corrections
        self._liaeqT = self.equivalent_level(
            weighting=WeightingFunctions.a_weighted,
            equivalent_duration=self.duration,
            leq_mode=LeqDurationMode.transient
        )

        self._SELA = self.equivalent_level(
            weighting=WeightingFunctions.a_weighted,
            equivalent_duration=1.0,
            leq_mode=LeqDurationMode.transient
        )

        self._liaeq100ms = self.equivalent_level(
            weighting=WeightingFunctions.a_weighted,
            equivalent_duration=0.1,
            leq_mode=LeqDurationMode.transient
        )

        self._liaeq8hr = self.equivalent_level(
            weighting=WeightingFunctions.a_weighted,
            equivalent_duration=8 * 60 * 60,
            leq_mode=LeqDurationMode.transient
        )

        # Process noise dose with 3 db exchange rate, 85dBA limit for 8 hours from MIL-STD 1474E B.5.3.4.2 EQ 4
        self._noise_dose = 100.0 / (2 ** ((85 - self._liaeq8hr) / 3.0))

    def _process_analysis(self):
        # Method with MIL STD 1474E
        if self.impulse_analysis_method == AnalysisMethod.MIL_STD_1474E:
            self._process_mil_std_1474e()

            # Method with MIL STD 1474E and a_durations corrected at liaegT instead of liaeq8hr.
        elif self.impulse_analysis_method == AnalysisMethod.MIL_STD_1474E_AFRL_PREF:
            self._process_mil_std_1474e_afrl_pref()

        # Method without a duration corrections in MIL STD 1474E
        elif self.impulse_analysis_method == AnalysisMethod.NO_A_DURATION_CORRECTIONS:
            self._process_no_a_duration_correction()

        elif self.impulse_analysis_method == AnalysisMethod.NONE:
            raise Warning("You should not call this function without declaring this as an impulsive waveform.")

    # -------------------- Public functions for operations on the samples within the Waveform --------------------------

    def determine_calibration_scale_factor(
            self, level: float = 114, frequency: float = 1000, frequency_tolerance:
            float = 25
            ):
        """
        This function will take the information within the current Waveform and determine the scaling factor that can be
        applied to this, or any other file, to ensure that the acoustic reference is obtained.

        Parameters
        ----------
        :param level: float
            default = 114 dB, this is the acoustic level at the specified frequency that we expect the calibration tone
            to generate
        :param frequency: float
            default = 1000 Hz, this is the acoustic frequency of the calibration device
        :param frequency_tolerance:
            The distance from the provided frequency that we are willing to go to ensure that this is a calibration tone
        """

        from .spectral.fractional_octave_band import FractionalOctaveBandTools as fob

        #   ensure that the calibration frequency is actually located within the Waveform.
        # calibration, detected_frequency = self.is_calibration()
        # if not calibration or abs(detected_frequency - frequency) > frequency_tolerance:
        #     raise ValueError(
        #         "The Waveform passed to the function does not contain a calibration tone or the tone is "
        #         "not at the expected frequency, based on the arguments of the function."
        #     )

        #   Now we need to calculate the scale factor required to adjust the level of the calibration Waveform to the
        #   desired magnitude.
        filtered_wfm = self.apply_bandpass(
            fob.lower_frequency(3, fob.exact_band_number(3, frequency)),
            fob.upper_frequency(3, fob.exact_band_number(3, frequency))
        )

        #   Now assuming that the data within the samples array is a pressure
        rms_level = 20 * np.log10(np.std(filtered_wfm.samples) / 20e-6)

        sens = level - rms_level
        sens /= 20
        sens *= -1
        sens = 10.0 ** sens

        return sens

    def apply_calibration(self, wfm, level: float = 114, frequency: float = 1000, inplace: bool = False):
        """
        This function assumes that the current Waveform, and the item provided as the first argument, possess the
        same parameters for the acquisition system. This assumes that the Waveform (wfm) is a calibration data that
        is collected with the same level and frequency passed to the function. This will scale the current samples to
        the same amplitude based on the data within the wfm.

        Parameters
        ----------
        wfm - The Waveform that possesses a calibration signal that can be analyzed to determine the scaling factor
        level: float, default = 114 - the expected acoustic level for the calibration signal in wfm
        frequency: float, default = 1000 - the frequency of the calibration signal in wfm
        inplace: bool, default = False - whether the manipulation is applied to the current Waveform,
            or a new Waveform object is returned to the user.
        """

        if not isinstance(wfm, Waveform):
            raise ValueError("The wfm is expected to be a Waveform object")

        sens = wfm.determine_calibration_scale_factor(level, frequency)

        #   Now scale the calibration signal and determine whether the overall level is close to the expected level
        scaled_calibration_wfm = wfm.scale_signal(1 / sens)

        if np.any(abs(scaled_calibration_wfm.overall_level() - level) > 2):
            raise ValueError("The method did not appropriately scale the calibration signal")

        return self.scale_signal(1 / sens, inplace=inplace)

    def normalize_loudness(self, target_loudness: float = -24.0, inplace: bool = True):
        """
        This function will normalize the data within the waveform to a specific loudness

        Parameters
        ----------
        :param target_loudness:
            The targeted loudness that we are normalizing this audio data to
        :param inplace:
            Boolean flag to determine whether the current object is modified, or a new object is retured

        Returns
        -------

        """

        #   The minimum number of samples is 0.4 seconds
        if self.duration < 0.4:
            additional_samples_required = int(np.floor(self.sample_rate * 0.4)) - len(self.samples)

            self.samples = np.pad(self.samples, (0, additional_samples_required), 'constant', constant_values=0.0)

        current_loudness = self.integrated_loudness
        gain = np.power(10.0, (target_loudness - current_loudness) / 20.0)

        if inplace:
            self.samples *= gain
        else:
            return Waveform(
                pressures=self.samples * gain, sample_rate=self.sample_rate, start_time=self.start_time,
                remove_dc_offset=False
                )

    def scale_signal(
            self, factor: float = 1.0, inplace: bool = False,
            scale_type: ScalingMethods = ScalingMethods.linear
    ):
        """
        This method will call the sub-function to scale the values of the waveform in linear fashion. If the scale
        factor is provided in logarithmic form, it will be converted to a linear value and sent to the sub-function.

        Parameters
        ----------
        :param factor: float - the scale factor that needs to be passed to the scaling sub-function, which will be
            multiplied by the unscaled signal (e.g. 1 divided by the sensitivity of a microphone in V/Pa)
        :param inplace: bool - whether to manipulate the data within the current class, or return a new instance
        :param scale_type: scaling_method - how to apply the scaling to the signal

        Returns
        -------

        :returns: output of sub-function
        """

        scale_factor = factor

        if scale_type == ScalingMethods.logarithmic:
            scale_factor = 10 ** (scale_factor / 20)

        return self._scale_waveform(scale_factor, inplace)

    def trim(self, s0: float = 0.0, s1: float = None, method: TrimmingMethods = TrimmingMethods.samples):
        """
        This function will remove the samples before s0 and after s1 and adjust the start time
        :param s0: float - the sample index or time of the new beginning of the waveform
        :param s1: float - the sample index or time of the end of the new waveform
        :param method: trimming_methods - the method to trim the waveform
        :return: generic_time_waveform object
        """

        #   Determine whether to use the time or sample methods

        if method == TrimmingMethods.samples:
            return self._trim_by_samples(int(s0), int(s1))
        elif method == TrimmingMethods.times_absolute:
            t0 = s0
            t1 = s1

            if isinstance(self.start_time, datetime):
                start_seconds = 60 * (60 * self.start_time.hour + self.start_time.minute) + self.start_time.second + \
                                self.start_time.microsecond / 1e6
            else:
                start_seconds = self.start_time

            s0 = (t0 - start_seconds) * self.sample_rate
            ds = (t1 - t0) * self.sample_rate
            s1 = s0 + ds

            return self._trim_by_samples(int(s0), int(s1))

        elif method == TrimmingMethods.times_relative:
            t0 = s0
            t1 = s1

            s0 = t0 * self.sample_rate
            s1 = t1 * self.sample_rate

            return self._trim_by_samples(int(s0), int(s1))

    def pad(self, pad_size, pad_value):
        """
        This function will insert values into the sample array according to the information in the pad_size object.
        The value that is inserted is defined by the value in pad_value (default = 0). If pad_value is an integer, then
        all values are inserted at the front of the sample array. If pad_value is a list or an array, the first entry
        is the pad size for the front; the second entry is the pad value for the back of the array.

        Parameters
        ----------
        pad_size: int or list/np.ndarray of ints
            The number of elements to add to the sample array. If the value is an integer, the points are added to the
            front of the sample array. Otherwise, the first entry is the front pad size, and the second entry is the
            rear pad size.

        pad_value: float or list/np.ndarray of floats
            The value to insert into the sample array based on the pad_size object

        Returns
        -------
        A new waveform with the increased size.

        """

        new_samples = np.pad(self.samples, pad_size, mode='constant', constant_values=pad_value)
        if isinstance(pad_size, list) or isinstance(pad_size, np.ndarray):
            front_pad_length = pad_size[0]
        else:
            front_pad_length = pad_size

        if isinstance(self.start_time, datetime):
            t0 = self.start_time - timedelta(seconds=front_pad_length / self.sample_rate)
        else:
            t0 = self.start_time - float(front_pad_length / self.sample_rate)

        return Waveform(pressures=new_samples, sample_rate=self.sample_rate, start_time=t0, remove_dc_offset=False)

    def apply_window(self, window: WindowingMethods = WindowingMethods.hanning, windowing_parameter=None):
        """
        This will apply a window with the specific method that is supplied by the window argument and returns a
        generic_time_waveform with the window applied

        :param window:windowing_methods - the enumeration that identifies what type of window to apply to the waveform
        :param windowing_parameter: int or float - an additional parameter that is required for the window
        :returns: generic_time_waveform - the waveform with the window applied
        """

        W = []

        if window == WindowingMethods.tukey:
            W = tukey(len(self.samples), windowing_parameter)

        elif window == WindowingMethods.rectangular:
            W = tukey(len(self.samples), 0)

        elif window == WindowingMethods.hanning:
            W = tukey(len(self.samples), 1)

        elif window == WindowingMethods.hamming:
            W = hamming(len(self.samples))

        return Waveform(self.samples * W, self.fs, self.start_time, remove_dc_offset=False)

    def apply_iir_filter(self, b, a):
        """
        This function will be able to apply a filter to the samples within the file and return a new
        generic_time_waveform object

        :param b: double, array-like - the forward coefficients of the filter definition
        :param a: double, array-like - the reverse coefficients of the filter definition
        """

        self._forward_coefficients = b
        self._reverse_coefficients = a
        return Waveform(
            scipy.signal.lfilter(b, a, self.samples), self.sample_rate, self.start_time,
            remove_dc_offset=False
            )

    def apply_a_weight(self):
        """
        This function specifically applies the a-weighting filter to the acoustic data, and returns a new waveform with
        the filter applied.

        :returns:
            generic_time_waveform - the filtered waveform
        """
        a, c = Waveform.AC_Filter_Design(self.sample_rate)

        return self.apply_iir_filter(a[0], a[1])

    def apply_c_weight(self):
        """
        This function specifically applies the a-weighting filter to the acoustic data, and returns a new waveform with
        the filter applied.

        :returns: generic_time_waveform - the filtered waveform
        """
        a, c = Waveform.AC_Filter_Design(self.sample_rate)

        return self.apply_iir_filter(c[0], c[1])

    def apply_lowpass(self, cutoff: float, order: int = 4):
        """
        This function applies a Butterworth filter to the samples within this class.

        :param cutoff: double - the true frequency in Hz
        :param order: double (default: 4) - the order of the filter that will be created and applied

        :returns: generic_time_waveform - the filtered waveform
        """

        #   Determine the nyquist frequency

        nyquist = self.sample_rate / 2.0

        #   Determine the normalized frequency

        normalized_cutoff = cutoff / nyquist

        #   Design the filter

        b, a = scipy.signal.butter(order, normalized_cutoff, btype='low', analog=False, output='ba')

        #   Filter the data and return the new waveform object

        return self.apply_iir_filter(b, a)

    def apply_head_auditory_response_filters(self):
        """
        To calculate the integrated loudness of the signal, we need to first filter the signal for a specific type of
        response due to the head and the auditory system. This originates in the pyloudnorm.meter class where the two
        filters are defined.

        """
        G = 4.0
        fc = 1500.0
        Q = np.sqrt(2.0) / 2.0

        A = 10 ** (G / 40.0)
        w0 = 2.0 * np.pi * (fc / self.sample_rate)
        alpha = np.sin(w0) / (2.0 * Q)

        #   Define the filter shape for the high shelf
        passband_gain = 1.0
        b0 = A * ((A + 1) + (A - 1) * np.cos(w0) + 2 * np.sqrt(A) * alpha)
        b1 = -2 * A * ((A - 1) + (A + 1) * np.cos(w0))
        b2 = A * ((A + 1) + (A - 1) * np.cos(w0) - 2 * np.sqrt(A) * alpha)
        a0 = (A + 1) - (A - 1) * np.cos(w0) + 2 * np.sqrt(A) * alpha
        a1 = 2 * ((A - 1) - (A + 1) * np.cos(w0))
        a2 = (A + 1) - (A - 1) * np.cos(w0) - 2 * np.sqrt(A) * alpha
        b = np.array([b0, b1, b2]) / a0
        a = np.array([a0, a1, a2]) / a0

        new_wfm = self.apply_iir_filter(b, a)
        new_wfm.samples *= passband_gain

        #   Now the high pass
        G = 0
        fc = 38.8
        Q = 0.5

        A = 10 ** (G / 40.0)
        w0 = 2.0 * np.pi * (fc / self.sample_rate)
        alpha = np.sin(w0) / (2.0 * Q)

        b0 = (1 + np.cos(w0)) / 2
        b1 = -(1 + np.cos(w0))
        b2 = (1 + np.cos(w0)) / 2
        a0 = 1 + alpha
        a1 = -2 * np.cos(w0)
        a2 = 1 - alpha

        b = np.array([b0, b1, b2]) / a0
        a = np.array([a0, a1, a2]) / a0

        new_wfm = new_wfm.apply_iir_filter(b, a)
        new_wfm.samples *= passband_gain

        return new_wfm

    def apply_highpass(self, cutoff: float, order: int = 4):
        """
        This function applies a Butterworth filter to the samples within this class.

        :param cutoff: double - the true frequency in Hz
        :param order: double (default: 4) - the order of the filter that will be created and applied

        :returns: Waveform - the filtered waveform
        """

        #   Determine the nyquist frequency

        nyquist = self.sample_rate / 2.0

        #   Determine the normalized frequency

        normalized_cutoff = cutoff / nyquist

        #   Design the filter

        b, a = scipy.signal.butter(order, normalized_cutoff, btype='high', analog=False, output='ba')

        #   Filter the data and return the new waveform object

        return self.apply_iir_filter(b, a)

    def apply_bandpass(self, low_cutoff: float, high_cutoff: float, order: int = 3):
        """
        This function determines the bandpass Butterworth filter coefficients and sends them and the current waveform
        into the function that will filter the data with an IIR filter coefficient set

        Parameters
        ----------
        low_cutoff: float - the regular frequency cutoff for the low edge of the band pass filter (Units: Hz)
        high_cutoff: float - the regular frequency cutoff for the upper edge of the band pass filter (Units: Hz)
        order: int - default: 3, the order of the filter
        """

        #   Determine the nyquist frequency for the upper and lower edges of the band
        nyquist = self.sample_rate / 2.0
        upper = high_cutoff / nyquist
        lower = low_cutoff / nyquist

        #   Design the filter
        b, a = scipy.signal.butter(order, [lower, upper], btype='bandpass', analog=False, output='ba')

        #   send this waveform and the coefficients into the filtering algorithm and return the filtered waveform
        return self.apply_iir_filter(b, a)

    def resample(self, new_sample_rate: int):
        """
        This function resamples the waveform and returns a new object with the correct sample rate and sample count.
        This function employs the resample function within scipy.signal to conduct the resampling.

        Parameters
        ----------
        new_sample_rate: int - the new sample rate that we want to create a signal for

        Returns
        -------
        Waveform - the new waveform object that contains the resampled data with the new sample rate.
        """

        #   Determine the ratio of the current sample rate to the new sample rate

        sr_ratio = new_sample_rate / self.sample_rate

        return Waveform(
            scipy.signal.resample(self.samples, int(np.floor(len(self.samples) * sr_ratio))),
            new_sample_rate,
            self.start_time,
            remove_dc_offset=False,
            header=self.header
        )

    def apply_tob_equalizer_filter(self, frequencies: np.ndarray, sound_pressure_levels: np.ndarray):
        from .spectral.fractional_octave_band import FractionalOctaveBandTools as fob
        import warnings

        """
        Pass the waveform through a series of filters adjusting the amplitude by the adjusted value of the arrays.

        Parameters
        ----------
        frequencies: np.ndarray - the collection of frequencies to generate filters
        sound_pressure_levels: np.ndarray - the collection of sound pressure levels to adjust the amplitude

        Returns
        -------
        Waveform - the summation of the n Waveforms that are generated by each of the filters.
        """
        #   Adjust the sound pressure level array by the average
        magnitude = sound_pressure_levels - np.mean(sound_pressure_levels)

        #   Determine the center frequency of the highest octave containing the upper frequency
        full_band = int(np.floor(fob.exact_band_number(1, frequencies[-1])))

        #   Now determine the upper edge of this full octave band
        f_hi = fob.upper_frequency(1, full_band)
        f_lo = fob.lower_frequency(1, full_band)

        #   With this information we can determine the band number of the highest one-third-octave band in this full
        #   octave band. This is used to determine the filter collection.
        b_coefficients = list()
        a_coefficients = list()

        f_band = int(np.floor(fob.exact_band_number(3, f_hi)))

        #   Create the collection of samples that we will add the output of the filter to create the final object
        samples = np.zeros((len(self.samples),))

        #   Now loop through the bands until we exit this full octave band
        while fob.lower_frequency(3, f_band) >= f_lo * 0.9:
            #   Define the window for the bandpass filter
            upper = fob.upper_frequency(3, f_band)
            lower = fob.lower_frequency(3, f_band)
            window = np.array([lower, upper]) / self.sample_rate / 2.0

            #   Create the filter coefficients for this frequency band and add it to the list for each coefficient set
            b, a = scipy.signal.butter(
                3,
                window,
                btype='bandpass',
                analog=False,
                output='ba'
            )

            b_coefficients.append(b)
            a_coefficients.append(a)

            #   Decrement the band number to move to the next band down.
            f_band -= 1

            #   With that we now need to determine the limits of the band calculations
            #   Determine the octave bands that will need to be calculated to cover the desired frequency range.
            low_band = int(np.floor(fob.exact_band_number(1, frequencies[0])))
            hi_band = int(np.floor(fob.exact_band_number(1, frequencies[-1])))

            #   Get the index of the band at the top of the full octave filter
            fob_band_index = int(np.floor(fob.exact_band_number(3, fob.upper_frequency(1, hi_band))))

            #   Make a copy of the waveform that can be decimated
            wfm = Waveform(
                pressures=self.samples.copy(),
                sample_rate=self.sample_rate,
                start_time=self.start_time,
                remove_dc_offset=False
            )

            #   Loop through the frequencies
            for band_index in range(hi_band, low_band - 1, -1):
                #   Loop through the filter definitions
                for filter_index in range(len(b_coefficients)):
                    filtered_waveform = wfm.apply_iir_filter(b_coefficients[filter_index], a_coefficients[filter_index])

                    band_index -= 1

                    #   Up sample the waveform
                    while filtered_waveform.sample_rate < self.sample_rate:
                        filtered_waveform = filtered_waveform.resample(filtered_waveform.sample_rate * 2)

                    #   Apply the amplification factor to the data
                    filtered_waveform.scale_signal(magnitude[band_index], scale_type=ScalingMethods.logarithmic)

                    #   Add the contents of the waveform to the sample list
                    if (fob.center_frequency(3, band_index) <= frequencies[-1]) and \
                            (fob.center_frequency(3, band_index) >= frequencies[0]):
                        samples += filtered_waveform.samples[:len(samples)]

                    #   Decimate the waveform, halving the sample rate and making the filter definitions move down a
                    #   full octave
                    if len(wfm.samples) / 2 < 3 * len(b_coefficients):
                        warnings.warn(
                            "The number of points within the Waveform are insufficient to calculate digital filters "
                            "lower than these frequencies"
                        )

                        break

                    wfm = Waveform(
                        pressures=scipy.signal.decimate(wfm.samples, 2),
                        sample_rate=wfm.sample_rate,
                        start_time=wfm.start_time,
                        remove_dc_offset=False
                    )

        return Waveform(
            pressures=samples,
            sample_rate=self.sample_rate,
            start_time=self.start_time,
            remove_dc_offset=False,
            header=self.header
            )

    def is_calibration(self):
        """
        This function examines the samples and determines whether the single contains a single pure tone.  If it does
        the function returns the approximate frequency of the tone.  This will examine every channel and determine
        whether each channel is a calibration tone

        :returns: bool - flag determining whether the signal was pure tone
                  float - the approximate frequency of the pure tone
        """
        from scipy.signal import find_peaks

        calibration = None
        freq = None

        #   Loop through the channels

        #   To remove high frequency transients, we pass the signal through a 2 kHz low pass filter

        wfm = self.apply_lowpass(2000)

        minimum_distance_between_peaks = wfm.sample_rate / 200

        peaks = find_peaks(wfm.samples, height=0.6 * np.max(wfm.samples))[0]

        if len(peaks) >= 2:
            calibration = False
            freq = -1

            #   Determine the distance between any two adjacent peaks

            distance_sample = np.diff(peaks)

            #   Determine the distance between the samples in time

            distance_time = distance_sample / self.sample_rate

            #   Determine the frequencies

            frequencies = 1 / distance_time

            freq = np.mean(frequencies)

            calibration = (abs(freq - 1000) < 0.1 * 1000) or \
                          (abs(freq - 250) < 0.1 * 250)

        return calibration, freq

    def get_features(
            self, include_temporal_features: bool = True,
            include_sq_metrics: bool = True,
            include_speech_features: bool = True
            ):
        """
        This function calculates the various features within the global time analysis and stores the results in the
        class object.  At the end, a dictionary of the values is available and returned to the calling function.

        Returns
        -------
        features : dict()
            The dictionary containing the various values calculated within this method.


        Remarks
        -------
        2024-Sept-10 - FSM Adjusted the function to take in the boolean on whether the temporal features were calculated
        and adjusted the creation of the data dictionary that is returned.
        """

        features = dict()

        if self.is_continuous:
            #   Create the dictionary that will hold the data for return to the user
            features['attack'] = self.attack
            features['decrease'] = self.decrease
            features['release'] = self.release
            features['log_attack'] = self.log_attack
            features['attack slope'] = self.attack_slope
            features['decrease slope'] = self.decrease_slope
            features['temporal centroid'] = self.temporal_centroid
            features['effective duration'] = self.effective_duration
            features['amplitude modulation'] = self.amplitude_modulation
            features['frequency modulation'] = self.frequency_modulation
            features['auto-correlation'] = self.auto_correlation
            features['zero crossing rate'] = self.zero_crossing_rate

            if include_sq_metrics:
                features['boominess'] = self.boominess
                features['loudness'] = self.loudness
                features['roughness'] = self.roughness
                features['sharpness'] = self.sharpness

            if include_speech_features:
                from python_speech_features import mfcc, fbank, ssc, logfbank
                window_length = 0.025
                nfft = 512
                frame_length = self.sample_rate * window_length
                if frame_length > nfft:
                    nfft = int(np.floor(2 ** (np.ceil(np.log2(frame_length)))))
                vect = np.mean(mfcc(self.samples, self.sample_rate, winlen=window_length, nfft=nfft), axis=0)
                for index in range(len(vect)):
                    features['mfcc_{:02.0f}'.format(index)] = vect[index]

                vect = np.mean(ssc(self.samples, self.sample_rate, winlen=window_length, nfft=nfft), axis=0)
                for index in range(len(vect)):
                    features['ssc_{:02.0f}'.format(index)] = vect[index]

        elif self.is_impulsive:
            features = {'a-duration': self.a_duration,
                        'equivalent level (T)': self.leqT,
                        'equivalent level a-weighted (T)': self.liaeqT,
                        'equivalent level a-weighted (8 hr)': self.liaeq8hr,
                        'equivalent level a-weighted (100ms)': self.liaeq100ms,
                        'peak level (dB)': self.peak_level,
                        'peak pressure (Pa)': self.peak_pressure,
                        'sound exposure level': self.SEL,
                        'a-weighted sound exposure level': self.SELA}

        return features

    def calculate_temporal_centroid(self):

        env_max_idx = np.argmax(self.signal_envelope)
        over_threshold_idcs = np.where(self.normal_signal_envelope > self.centroid_threshold)[0]

        over_threshold_start_idx = over_threshold_idcs[0]
        if over_threshold_start_idx == env_max_idx:
            over_threshold_start_idx = over_threshold_start_idx - 1

        over_threshold_end_idx = over_threshold_idcs[-1]

        over_threshold_TEE = self.signal_envelope[over_threshold_start_idx - 1:over_threshold_end_idx - 1]
        over_threshold_support = [*range(len(over_threshold_TEE))]
        over_threshold_mean = np.divide(
            np.sum(np.multiply(over_threshold_support, over_threshold_TEE)),
            np.sum(over_threshold_TEE)
        )

        temporal_threshold = ((over_threshold_start_idx + 1 + over_threshold_mean) / self.sample_rate)

        return temporal_threshold

    def calculate_effective_duration(self):

        env_max_idx = np.argmax(self.signal_envelope)
        over_threshold_idcs = np.where(self.normal_signal_envelope > self.effective_duration_threshold)[0]

        over_threshold_start_idx = over_threshold_idcs[0]
        if over_threshold_start_idx == env_max_idx:
            over_threshold_start_idx = over_threshold_start_idx - 1

        over_threshold_end_idx = over_threshold_idcs[-1]

        return (over_threshold_end_idx - over_threshold_start_idx + 1) / self.sample_rate

    def instantaneous_temporal_features(self):
        """
        This function will calculate the instantaneous features within the temporal analysis.  This includes the
        auto-correlation and the zero crossing rate.
        """
        count = 0
        temporal_feature_times = np.zeros(
            (int(np.floor((len(self.samples) - self.window_size_samples) / self.hop_size_samples) + 1),)
        )

        auto_coefficients = np.zeros((len(temporal_feature_times), self.coefficient_count))
        zero_crossing_rate = np.zeros((len(temporal_feature_times),))

        #   Loop through the frames

        for n in range(0, len(temporal_feature_times)):
            #   Get the frame

            frame_length = self.window_size_samples
            start = n * self.hop_size_samples
            frame_index = np.arange(start, frame_length + start)
            f_Frm_v = self.samples[frame_index] * np.hamming(self.window_size_samples)
            temporal_feature_times[n] = n * self.hop_size_seconds

            count += 1

            #   Calculate the auto correlation coefficients

            auto_coefficients[n, :] = sm.tsa.acf(f_Frm_v, nlags=self.coefficient_count, fft=False)[1:]

            #   Now the zero crossing rate

            i_Sign_v = np.sign(f_Frm_v - np.mean(f_Frm_v))
            i_Zcr_v = np.where(np.diff(i_Sign_v))[0]
            i_Num_Zcr = len(i_Zcr_v)
            zero_crossing_rate[n] = i_Num_Zcr / (len(f_Frm_v) / self.sample_rate)

        return temporal_feature_times, auto_coefficients, zero_crossing_rate

    def calculate_modulation(self):
        """
        Calculate the frequency/amplitude modulations of the signal.  This can be accomplished with either a Fourier or
        Hilbert method.

        Returns
        -------

        frequency_modulation : double
            A metric measuring the frequency modulation of the signal
        amplitude_modulation : double
            A metric measuring the amplitude modulation of the signal
        """

        sample_times = np.arange(len(self.signal_envelope) - 1) / self.sample_rate

        if self._addresses is None:
            self._log_attack, self._increase, self._decrease, self._addresses = self.calculate_log_attack()

        sustain_start_time = self._addresses[1]
        sustain_end_time = self._addresses[4]

        is_sustained = False

        if (sustain_end_time - sustain_start_time) > 0.02:
            pos_v = np.where((sustain_start_time <= sample_times) & (sample_times <= sustain_end_time))[0]
            if len(pos_v) > 0:
                is_sustained = True

        if not is_sustained:
            amplitude_modulation = 0
            frequency_modulation = 0
        else:
            envelop_v = self.normal_signal_envelope[pos_v].copy()
            envelop_v[envelop_v <= 0] = np.finfo(envelop_v.dtype).eps
            temps_sec_v = sample_times[pos_v]
            M = np.mean(envelop_v)

            #   Taking the envelope

            y_matrix = np.array([np.sum(np.log(envelop_v)), np.sum(temps_sec_v * np.log(envelop_v))])
            x_matrix = np.array(
                [len(temps_sec_v), np.sum(temps_sec_v),
                 np.sum(temps_sec_v), np.sum(temps_sec_v ** 2)]
                ).reshape((2, 2))
            mon_poly = np.linalg.pinv(x_matrix).dot(y_matrix)
            # mon_poly = np.polyfit(temps_sec_v, np.log(envelop_v), 1)
            hat_envelope_v = np.exp(np.polyval(mon_poly[::-1], temps_sec_v))
            signal_v = envelop_v - hat_envelope_v

            sa_v = scipy.signal.hilbert(signal_v)
            sa_amplitude_v = abs(signal_v)
            sa_phase_v = np.unwrap(np.angle(sa_v))
            sa_instantaneous_frequency = (1 / 2 / np.pi) * sa_phase_v / (len(temps_sec_v) / self.sample_rate)

            amplitude_modulation = np.median(sa_amplitude_v)
            frequency_modulation = np.median(sa_instantaneous_frequency)

        return frequency_modulation, amplitude_modulation

    def calculate_log_attack(self):
        """
        This calculates the various global attributes.

        In some cases the calculation of the attack did not return an array, so the error is trapped for when a
        single values is returned rather than an array.

        20230318 - FSM - According to the paper on the Timbre Toolbox, the thresholds were to be estimated on the
        maximum value of the energy envelope, not the values at the start and end of the attack. This was addressed
        in the determination of the value of the threshold.

        Returns
        -------
        attack_start : TYPE
            DESCRIPTION.
        log_attack_time : TYPE
            DESCRIPTION.
        attack_slope : TYPE
            DESCRIPTION.
        attack_end : TYPE
            DESCRIPTION.
        release : TYPE
            DESCRIPTION.
        release_slope : TYPE
            DESCRIPTION.

        """

        if self.normal_signal_envelope is None:
            self._calculate_signal_envelope()

        #   Define some specific constants for this calculation
        method = self.temporal_threshold_finding
        noise_threshold = 0.15
        decrease_threshold = 0.4
        percent_step = 0.1

        #   Detection of the start (start_attack_position) and stop (end_attack_position) of the attack
        position_value = np.where(self.normal_signal_envelope > noise_threshold)[0]
        start_attack_position, end_attack_position = self._find_attack_endpoints(position_value, percent_step, method=3)

        #   Calculate the Log-attack time
        if start_attack_position == end_attack_position:
            start_attack_position -= 1
        elif start_attack_position < 0 or end_attack_position < 0:
            for method_index in range(1, 3):
                start_attack_position, end_attack_position = self._find_attack_endpoints(
                    position_value, percent_step, method=method_index
                )
                if start_attack_position >= 0 and end_attack_position > 0:
                    break
            if not (start_attack_position >= 0 and end_attack_position > 0):
                raise ValueError("There was a problem determining the starting/ending index of the attack")

        rise_time_n = end_attack_position - start_attack_position
        log_attack_time = np.log10(rise_time_n / self.sample_rate)

        #   Calculate the temporal growth - New 13 Jan 2003
        #   weighted average (Gaussian centered on percent=50%) slopes between start_attack_position and
        #   end_attack_position
        start_attack_position = int(np.round(start_attack_position))
        end_attack_position = int(np.round(end_attack_position))

        if end_attack_position <= start_attack_position or end_attack_position == start_attack_position:
            end_attack_position = start_attack_position + 1

        start_attack_value = self.normal_signal_envelope[start_attack_position]
        end_attack_value = self.normal_signal_envelope[end_attack_position]

        #   Now that we have determined where the attack occurs, we must define a set of thresholds as a proportion
        #   of the maximum pf the energy envelop. To ensure that the value is within the attack range, we seek for
        #   the maximum within this region.
        threshold_value = np.arange(0.1, 1.1, 0.1)
        threshold_value *= np.max(self.normal_signal_envelope[start_attack_position:end_attack_position])
        threshold_position_seconds = np.zeros(np.size(threshold_value))
        for i in range(len(threshold_value)):
            #   Find the index within the envelope where the value is greater than the selected threshold value
            idx = np.where(
                self.normal_signal_envelope[start_attack_position:end_attack_position] >=
                threshold_value[i]
            )[0]

            if len(idx) > 0:
                threshold_position_seconds[i] = idx[0] / self.sample_rate

        slopes = np.divide(np.diff(threshold_value), np.diff(threshold_position_seconds) + sys.float_info.epsilon)

        #   Calculate the increase
        thresholds = (threshold_value[:-1] + threshold_value[1:]) / 2
        weights = np.exp(-(thresholds - 0.5) ** 2 / (0.5 ** 2))
        increase = np.sum(np.dot(slopes, weights)) / np.sum(weights)

        #   Calculate the time decay

        envelope_max_index = np.where(self.normal_signal_envelope == np.max(self.normal_signal_envelope))[0]
        envelope_max_index = int(np.round(0.5 * (envelope_max_index + end_attack_position)))

        stop_position = np.where(self.normal_signal_envelope > decrease_threshold)[0][-1]

        if envelope_max_index == stop_position:
            if stop_position < len(self.normal_signal_envelope):
                stop_position += 1
            elif envelope_max_index > 1:
                envelope_max_index -= 1

        #   Calculate the decrease

        X = np.arange(envelope_max_index, stop_position) / self.sample_rate
        X_index = np.arange(envelope_max_index, stop_position)
        env = self.normal_signal_envelope[X_index].copy()
        env[env <= 0] = np.finfo(env.dtype).eps
        Y = np.log(env)
        # try:
        #     polynomial_fit = np.polyfit(X, Y, 1)
        # except np.linalg.LinAlgError:
        y_matrix = np.array([np.sum(Y), np.sum(X * Y)])
        x_matrix = np.array([len(X), np.sum(X), np.sum(X), np.sum(X ** 2)]).reshape((2, 2))
        polynomial_fit = np.linalg.pinv(x_matrix).dot(y_matrix)
        decrease = polynomial_fit[0]

        #   Create the list of addresses that we are interested in storing for later consumption

        addresses = np.array([start_attack_position, envelope_max_index, 0, 0, stop_position]) / self.sample_rate

        return log_attack_time, increase, decrease, addresses

    def equivalent_level(
            self,
            weighting: WeightingFunctions = WeightingFunctions.a_weighted,
            equivalent_duration: float = 8 * 3600,
            start_sample: int = 0,
            stop_sample: int = None,
            leq_mode: LeqDurationMode = None,
            exposure_duration: float = None
    ):
        """
        This function computes the equivalent level on the pressures within the waveform. If there is a weighting
        function specified this is applied before the pressures are summed. Additionally, the duration of the summation
        is specified (in seconds) for the new value with a default of 8 hours. Finally, if there is a cause to exclude
        portions of the data (i.e. calculating the SEL for the 10 dB down points in community noise) you can specify
        the start and stop index. If the stop index is None, then the last pressure defines the limit of the summation.

        :param weighting:   WeightingFunctions
            The enumeration to determine filtering function applied to the waveform
        :param equivalent_duration:   float
            The denominator of the summation - in seconds - representing the desired length of total exposure
            time (e.g. an 8-hour duty day, or a 1-second sound exposure level)
        :param start_sample:   int
            default = 0. The start sample of the pressure summation
        :param stop_sample:   int
            default = None. The stop sample, if the value is None, then it is replaces with the last sample index
        :param leq_mode:   LeqDurationMode
            The enumeration to determine whether the input signal contains all energy
            of an exposure to the listener (transient) or the signal represents a sample of a longer-duration
            (steady_state) exposure
        :param exposure_duration:   float
            If leq_mode is steady_state, this is the actual time of noise exposure to the
            listener in seconds
        :return: float
            The sound pressure level in decibels equivalent to a constant level with the same total acoustic
            intensity spread over the equivalent_duration time window
        """

        if stop_sample is None:
            stop_sample = len(self.samples)

        number_of_samples = stop_sample - start_sample
        signal_duration = number_of_samples / self.sample_rate

        if weighting == WeightingFunctions.unweighted:
            s = np.sum(self.samples[start_sample:stop_sample] ** 2, axis=0)
        elif weighting == WeightingFunctions.a_weighted:
            s = np.sum(self.apply_a_weight().samples[start_sample:stop_sample] ** 2, axis=0)
        elif weighting == WeightingFunctions.c_weighted:
            s = np.sum(self.apply_c_weight().samples[start_sample:stop_sample] ** 2, axis=0)

        total_energy_in_signal = s / self.sample_rate

        if leq_mode == LeqDurationMode.transient:
            total_energy_of_exposure = total_energy_in_signal
        elif leq_mode == LeqDurationMode.steady_state:
            if exposure_duration is None:
                exposure_duration = signal_duration
            total_energy_of_exposure = total_energy_in_signal * (exposure_duration / signal_duration)
        elif leq_mode is None:
            raise ValueError("User must specify a signal duration mode of class LeqDurationMode.")

        average_energy_over_equivalent_duration = total_energy_of_exposure / equivalent_duration

        return 10.0 * np.log10(average_energy_over_equivalent_duration / 20e-6 / 20e-6)

    def overall_level(
            self, integration_time: float = None,
            weighting: WeightingFunctions = WeightingFunctions.unweighted
    ):
        """
        Integrate the levels within the waveform to generate the weighted level. This will permit different weighting
        functions to be applied before the calculation of the overall level.

        Parameters
        ----------
        integration_time: float, default: None - The amount of time that we will collect prior to determining the
            RMS level within the samples.
        weighting: weighting_function, default: unweighted - the weighting to be applied prior to determining the RMS
            value of the signal.

        Returns
        -------
        float, array-like - A collection of the overall levels, with applicable weighting, with the number being equal
            to the int(np.floor(duration / integration_time))

        Revision
        20221007 - FSM - updated the method when the start_time is a datetime rather than a floating point value
        """

        if integration_time is None:
            n = 1
            integration_time = self.duration
        else:
            n = int(np.floor(self.duration / integration_time))

        if weighting == WeightingFunctions.a_weighted:
            wfm = self.apply_a_weight()
        elif weighting == WeightingFunctions.c_weighted:
            wfm = self.apply_c_weight()
        else:
            wfm = Waveform(self.samples, self.sample_rate, self.start_time)
        level = list()

        t0 = self.start_time
        if isinstance(t0, datetime):
            t0 = 60 * (60 * t0.hour + t0.minute) + t0.second + t0.microsecond / 1e6

        for i in range(n):
            subset = wfm.trim(t0, t0 + integration_time, TrimmingMethods.times_absolute)
            level.append(np.std(subset.samples))

            t0 += integration_time

        return 20 * np.log10(np.array(level) / 20e-6)

    def cross_correlation(self, b, mode=CorrelationModes.valid, lag_limit=None):
        """
        This function determines the cross correlation between the current waveform and the waveform passed to the
        function.

        Parameters
        ----------
        b: Waveform - the signal to compare to the current waveform's samples
        mode: correlation_mode - the mode of the correlation that we want to execute for the correlation methods
        lag_limit: - the limit of the correlation analysis

        Returns
        -------

        value of the maximum correlation
        sample lag of the maximum correlation

        Remarks
        2022-12-01 - FSM - Added completed enumeration usage for different correlation modes
        """

        # TODO - @Alan - we need a test for this function.

        if not isinstance(b, Waveform):
            raise ValueError("The first argument is required to be a Waveform object")

        sig = b.samples
        ref_sig = self.samples
        if len(sig) > len(ref_sig):
            sig, ref_sig = ref_sig, sig

        M = len(ref_sig)
        N = len(sig)

        if lag_limit is None:
            correlation_values = np.correlate(ref_sig, sig, mode.name)
            if mode == CorrelationModes.valid:
                lags = np.arange(0, max(M, N) - min(M, N) + 1)
            elif mode == CorrelationModes.full:
                lags = np.arange(-(N - 1), M)
            elif mode == CorrelationModes.same:
                lags = np.arange(-np.floor(N / 2), M - np.floor(N / 2))
        else:
            ref_sig_pad = np.pad(ref_sig.conj(), lag_limit, mode='constant')
            correlation_values = np.zeros(2 * lag_limit + 1)
            for i in range(0, 2 * lag_limit + 1):
                correlation_values[i] = sum(ref_sig_pad[i:len(sig) + i] * sig)
            lags = np.arange(-lag_limit, lag_limit + 1)

        return np.max(correlation_values), lags[np.argmax(correlation_values)]

    def concatenate(self, wfm):
        """
        This will create a new audio file that contains the data from the current Waveform and adds the samples from the
        new Waveform to the list and then returns a new object.

        Parameters
        ----------
        :param wfm: This is the Waveform that we want to concatenate with the current samples

        Returns
        -------
        A new waveform that contains the audio from the argument tacked onto the end of the samples from the current
        waveform.
        """

        new_samples = np.concatenate([self.samples, wfm.samples])
        return Waveform(new_samples, self.sample_rate, self.start_time, header=self.header)

    def split_by_time(self, frame_duration: float = 0.25):
        """
       This will create a numpy array of waveform objects that have been split into segments controlled by the time
       window.

       Parameters
       ----------
       :param frame_duration: The amount of time in each new waveform segment -  float, defaults to 0.25 seconds.

       Returns
       -------
       A new waveform numpy array of waveform objects broken into segments equal to the window size.
       """
        N = int(np.floor(self.duration / frame_duration))
        frames = np.empty(N, dtype=Waveform)
        sample_size = int(np.floor(frame_duration * self.sample_rate))

        #   Set the starting sample
        s0 = 0
        for n in range(N):
            # Get individual frame with trim and set in array
            frames[n] = self.trim(s0, s0 + sample_size, TrimmingMethods.samples)
            s0 += sample_size

        return frames

    def plot(self, ax=None, marker='d', color='black', label: str = None):
        """
        Provided an axis, this function will plot the data on the axis provided
        :param ax:
            The axis object that will be used for the plotting.
        :param marker:
            The type of marker to be used for the samples
        :param color:
            The color of the marker
        :param label:
            The label that should be inserted into the legend, if the user decides to use it.
        :return:
            The function will return the figure and axis that were created for the display of the waveform.
        """
        import matplotlib.pyplot as plt

        if ax is None:
            fig, ax = plt.subplots()
        else:
            fig = ax.get_figure()

        ax.plot(self.times, self.samples, marker=marker, color=color)
        if label is not None:
            ax.set_label(label)

        return fig, ax

    def to_StandardBinaryFile(self, output_filename:str = ""):
        """
        This function writes the current data within the Waveform into a StandardBinaryFile.
        :param output_filename: the location to write the data to
        :type output_filename: str
        """
        import os.path
        import struct

        # Append sample format and encoding method if they don't exist to the header dict
        if 'SAMPLE RATE (HZ)' not in self.header.keys():
            self.header['SAMPLE RATE (HZ)'] = int(np.floor(self.sample_rate))

        if 'SAMPLES TOTAL' not in self.header.keys():
            self.header['SAMPLES TOTAL'] = len(self.samples)

        if isinstance(self.start_time, datetime) and 'TIME (UTC ZULU)' not in self.header.keys():
            self.header['TIME (UTC ZULU)'] = self.start_time.strftime('%Y/%m/%d %H:%M:%S.%f')
        elif isinstance(self.start_time, float) and 'TIME (TPM)' not in self.header.keys():
            self.header['TIME (TPM)'] = self.start_time

        if 'SAMPLE FORMAT' not in self.header.keys():
            self.header['SAMPLE FORMAT'] = "LITTLE ENDIAN"

        if 'DATA FORMAT' not in self.header.keys():
            self.header['DATA FORMAT'] = 'REAL*4'

        # Check to see if output path exist and open file if it doesn't exist
        if not os.path.exists(output_filename):
            f = open(output_filename, 'wb')

            # Write header info from dict

            header_line = ';{}'.format("HEADER SIZE").ljust(41, '.') + ': {}\n'.format(len(self.header.keys()) + 1)
            f.write(header_line.encode('utf-8'))

            for key in self.header.keys():
                header_line = ';{}'.format(key.upper()).ljust(41, '.') + ': {}\n'.format(self.header[key])
                f.write(header_line.encode('utf-8'))

            # Write pressure data to end of file

            for i in range(len(self.samples)):
                f.write(struct.pack('<f', self.samples[i]))
            f.close()

    #   ----------------------------------------------- Operators ------------------------------------------------------

    def __add__(self, other):
        """
        This function will add the contents of one waveform to the other. This feature checks the sample rate to ensure
        that they both possess the same sample times. Also, if the data starts at different times, this function will
        create a new object that is the addition of the samples, with the new sample times.

        Parameters
        ----------
        :param other: Waveform - the new object to add to this class's data

        Returns
        -------
        :returns: - A new Waveform object that is the sum of the two
        """

        warnings.warn(
            message='waveform.add not yet tested. Use at your own risk.'
        )

        if not isinstance(other, Waveform):
            raise ValueError("You must provide a new Waveform object to add to this object.")

        if self.sample_rate != other.sample_rate:
            raise ValueError("At this time, the two waveforms must possess the same sample rate to add them together")

        s0 = int(other.start_time * other.sample_rate)
        s1 = s0 + len(other.samples)

        return Waveform(self.samples[s0:s1] + other.samples, self.sample_rate, self.start_time,
                        remove_dc_offset=False, header=self.header)

    def __sub__(self, other):
        """
        This function subtracts another Waveform object from the current object and returns the value as a new
        Waveform. If the start times, durations, or sample rates are not equal then the function returns a ValueError

        """

        if self.start_time != other.start_time or self.duration != other.duration or self.sample_rate != \
                other.sample_rate:
            raise ValueError(
                "The meta-data of these two waveforms is inconsistent making it impossible to know how "
                "to subtract the information in the pressures."
            )

        return Waveform(self.samples - other.samples,
                        self.sample_rate,
                        self.start_time,
                        False,
                        header=self.header)


class FrameBuilder:
    """
    This class provides a method to store the start and stop samples/times for the Waveform.trim function. It
    overwrites the ability to create the subset of the waveform that is passed to the Spectrum object for the
    creation of the frequency spectrum.
    """

    def __init__(self, wfm: Waveform, overlap_pct: float = 0, frame_width_sec: float = 0.25):
        """
        This function creates the new windowing function to create the subsets of the Waveform with specific
        increments in the representation. The function is used within the TimeHistory classes to create the subset of
        audio that is passed to the Spectrum object. The length of the subset is defined by the frame_width_sec as a
        duration in seconds. The amount of time that we increment the start time is defined by the relationship
        between the frame width and the overlap.
        :param wfm: The object that contains the audio data
        :type wfm: Waveform
        :param overlap_pct: the amount of the frame length that we want the next frame to overlap the current frame
        :type overlap_pct: float
        :param frame_width_sec: the width of the frame in seconds
        :type frame_width_sec: float
        """

        if overlap_pct > 1.0:
            raise ValueError("The percentage must be normalized to 1.0")

        self._waveform = wfm
        self._overlap_pct = overlap_pct
        self._frame_length_sec = frame_width_sec
        self._s0 = 0
        self._s1 = self.frame_length_samples

    @property
    def sample_rate(self):
        return self._waveform.sample_rate

    @property
    def overlap_percentage(self):
        return self._overlap_pct

    @property
    def frame_length_samples(self):
        return int(np.floor(self._frame_length_sec * self.sample_rate))

    @property
    def overlap_samples(self):
        return self.frame_length_samples * self.overlap_percentage

    @property
    def time_increment(self):
        return self._frame_length_sec * (1 - self.overlap_percentage)

    @property
    def sample_increment(self):
        return int(np.floor(self.time_increment * self.sample_rate))

    @property
    def frame_length_seconds(self):
        return self._frame_length_sec

    @property
    def duration(self):
        return self._waveform.duration

    @property
    def excess_duration(self):
        """
        This is the amount of time that will contain only partial frames
        :return:
        :rtype: float
        """

        return self.frame_length_seconds * self.overlap_percentage

    @property
    def complete_frame_count(self):
        """
        This will determine the number of complete frames (all samples within the frame are filled from the original
        waveform).
        :return: the number of complete frames
        :rtype: int
        """

        return int(np.floor((self.duration - self.excess_duration) / self.time_increment))

    def get_next_waveform_subset(self):
        """
        This function takes the current starting and ending samples, increments them by the appropriate amount and
        returns the next subset of the waveform. It also increments the internal representation of the start and stop
        samples.
        :return:
            A new waveform that is the next increment in the waveform.
        :rtype: Waveform
        """

        wfm = self._waveform.trim(self._s0, self._s1, method=TrimmingMethods.samples)

        self._s0 += self.sample_increment
        self._s1 = self._s0 + self.frame_length_samples

        return wfm
