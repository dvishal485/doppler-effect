import numpy as np


class Doppler:
    def __init__(self, v_observer: list[float], v_source: list[float], source_coordinate: list[float], observer_coordinates: list[float], v_sound: float = 330.0, source_frequency: float = None, wavelength: float = None):
        if wavelength == None:
            wavelength = v_sound/source_frequency
        if v_sound == None:
            v_sound = wavelength*source_frequency
        if source_frequency == None:
            source_frequency = v_sound/wavelength
        self.source_frequency = source_frequency
        self.source_coordinate = np.array(source_coordinate)
        self.observer_coordinates = np.array(observer_coordinates)
        self.v_source = np.array(v_source)
        self.v_observer = np.array(v_observer)
        self.v_sound = v_sound
        self.wavelength = wavelength

        def component_along_line(vector: list[float]) -> float:
            line_vector: np.ndarray = self.source_coordinate - self.observer_coordinates
            return (np.dot(line_vector, vector)/np.sqrt(np.dot(line_vector, line_vector)))
        self.component_along_vector = component_along_line

    def apparent_frequency(self) -> float:
        vs = self.component_along_vector(self.v_source)
        vo = self.component_along_vector(self.v_observer)
        return self.source_frequency * ((self.v_sound+vo)/(self.v_sound+vs))

    def apparent_wavelength(self) -> float:
        vs = self.component_along_vector(self.v_source)
        return self.wavelength * (1-vs/self.v_sound)
