from dataclasses import dataclass
import math
from .state import State

class Animatable(State[float]):
    value: float
    final_position: float 
    velocity: float

    def __init__(self, value: float):
        super().__init__(value)
        self.final_position = value
        self.velocity = 0

    def animate_to(self, final_position: float, speed: float):
        self.final_position = final_position
        self.velocity = speed

    def update(self, dt: float = 1000 / 60):
        if self.value != self.final_position:
            diff = self.final_position - self.value
            self.value += diff * min(1, dt * self.velocity)
            if abs(diff) < 0.01:
                self.value = self.final_position

    @property
    def rounded(self):
        return round(self.value)

class Spring(Animatable):
    # Stiffness is natural frequency squared
    def __init__(self, value: float, damping_ratio: float = 1.0, natural_freq: float = 20.0):
        super().__init__(value)
        self.damping_ratio = damping_ratio
        self.natural_freq = natural_freq

    def animate_to(self, final_position: float, initial_velocity: float = 0.0):
        self.final_position = final_position
        self.velocity = initial_velocity

    # This is a modified version of the spring animation from the jetpack compose source code
    def update(self, dt = 1000 / 60):
        if not self.is_animating:
            self.value = self.final_position
            return 
        
        dt = dt / 1000 # Convert to seconsds
        adjusted_displacement = self.value - self.final_position
        k = self.damping_ratio ** 2
        r = -self.damping_ratio * self.natural_freq

        displacement = 0.0
        current_velocity = 0.0

        if self.damping_ratio > 1.0:
            # Over damping
            s = self.natural_freq * math.sqrt(k - 1.0)
            gamma_plus = r + s
            gamma_minus = r - s

            # Overdamped
            coeff_b = (gamma_minus * adjusted_displacement - self.velocity) / (gamma_minus - gamma_plus)
            coeff_a = adjusted_displacement - coeff_b
            displacement = coeff_a * math.exp(gamma_minus * dt) + coeff_b * math.exp(gamma_plus * dt)
            current_velocity = coeff_a * gamma_minus * math.exp(gamma_minus * dt) + coeff_b * gamma_plus * math.exp(gamma_plus * dt)
        elif self.damping_ratio == 1.0:
            # Critically damped
            coeff_a = adjusted_displacement
            coeff_b = self.velocity + self.natural_freq * adjusted_displacement
            n_fd_t = -self.natural_freq * dt
            displacement = (coeff_a + coeff_b * dt) * math.exp(n_fd_t)
            current_velocity = ((coeff_a + coeff_b * dt) * math.exp(n_fd_t) * (-self.natural_freq)) + coeff_b * math.exp(n_fd_t)
        else:
            damped_freq = self.natural_freq * math.sqrt(1.0 - k)
            # Underdamped
            cos_coeff = adjusted_displacement
            sin_coeff = (1.0 / damped_freq) * ((-r * adjusted_displacement) + self.velocity)
            d_fd_t = damped_freq * dt
            displacement = math.exp(r * dt) * (cos_coeff * math.cos(d_fd_t) + sin_coeff * math.sin(d_fd_t))
            current_velocity = displacement * r + (math.exp(r * dt) * (-damped_freq * cos_coeff * math.sin(d_fd_t) + damped_freq * sin_coeff * math.cos(d_fd_t)))

        self.value = displacement + self.final_position
        self.velocity = current_velocity

    @property
    def is_animating(self):
        return abs(self.value - self.final_position) > 0.1 or abs(self.velocity) > 0.1
