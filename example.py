from doppler import *

doppler = Doppler(
    source_frequency=300,
    v_observer=[0, 2],
    v_source=[3, 0],
    source_coordinate=[0, 0],
    observer_coordinates=[4, 3],
    v_sound=343
)

print(f"Speed of Sound = {doppler.v_sound} m/s")
print(f"Sound Wavelength = {doppler.wavelength} m")
print(f"Velocity of Source = {doppler.v_source} m/s")
print(f"Velocity of Observer = {doppler.v_observer} m/s")
print(f"Source Coordinate = {doppler.source_coordinate} m")
print(f"Observer Coordinate = {doppler.observer_coordinates} m")
print(f"Distance between Source and Observer = {doppler.distance} m")
print(f"Apparent Frequency = {doppler.apparent_frequency()} Hz")
print(f"Apparent Wavelength = {doppler.apparent_wavelength()} m")
