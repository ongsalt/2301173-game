import math
from pygame import Rect

def lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t

class Animatable:
    value: float
    final_position: float 
    velocity: float

    def __init__(self, value: float):
        self.value = value
        self.final_position = value
        self.velocity = 0

    def animate_to(self, final_position: float, speed: float):
        self.final_position = final_position
        self.velocity = speed

    def update(self, dt: float = 1000 / 60):
        if self.value != self.final_position:
            diff = self.final_position - self.value
            self.value += diff * min(1, dt * self.velocity)
            if abs(self.value - self.final_position):
                self.value = self.final_position
                self.velocity = 0

    @property
    def is_animating(self):
        return self.value != self.final_position

    @property
    def rounded(self):
        return round(self.value)
    
    def __hash__(self):
        return hash((self.value, self.final_position, self.velocity))

    def __repr__(self):
        return f"{self.__class__.__name__}(value={self.value}, final_position={self.final_position}, velocity={self.velocity})"

class Loop(Animatable):
    def __init__(self, min_value: float, max_value: float, initial_value: float | None = None, angular_frequency: float = 1.0):
        value = initial_value if initial_value is not None else min_value
        super().__init__(value)
        self.min_value = min_value
        self.max_value = max_value
        self.angular_frequency = angular_frequency
        self.time = 0

    def animate_to(self, final_position: float, speed: float):
        pass

    def update(self, dt: float = 1000 / 60):
        self.time += dt / 100
        amplitude = (self.max_value - self.min_value) / 2
        normalized = math.sin(self.time * self.angular_frequency)
        self.value = normalized * amplitude + self.min_value + amplitude

        # clamping
        if self.value < self.min_value:
            self.value = self.min_value
        elif self.value > self.max_value:
            self.value = self.max_value

        # self.velocity: ignored

    @property
    def is_animating(self):
        return True

class Spring(Animatable):
    # Stiffness is natural frequency squared
    def __init__(self, value: float, damping_ratio: float = 1.0, natural_freq: float = 20.0):
        super().__init__(value)
        self.damping_ratio = damping_ratio
        self.natural_freq = natural_freq

    def animate_to(self, final_position: float, initial_velocity: float | None = None):
        self.final_position = final_position
        if initial_velocity is not None:
            self.velocity = initial_velocity

    # This is a modified version of the spring animation from the jetpack compose source code
    def update(self, dt = 1000 / 60):
        if not self.is_animating:
            return 
        
        # print(f"Updating spring: {self}")
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

        if abs(self.value - self.final_position) < 0.1 and abs(self.velocity) < 0.1:
            self.value = self.final_position
            self.velocity = 0

class Acceleration(Animatable):
    def __init__(self, value: float, acceleration: float = 1000, max_speed: float = 1000, initial_velocity: float | None = None):
        super().__init__(value)
        self.acceleration = abs(acceleration)
        self.max_speed = abs(max_speed)
        self.velocity = initial_velocity or 0

    def animate_to(self, final_position: float, acceleration: float | None = None, max_speed: float | None = None, initial_velocity: float | None = None):
        self.final_position = final_position 
        self.acceleration = abs(acceleration or self.acceleration)
        self.max_speed = abs(max_speed or self.max_speed)
        self.velocity = initial_velocity or 0

    def update(self, dt: float = 1000 / 60):
        if not self.is_animating:
            return
        
        dt /= 1000
        
        direction = 1 if self.final_position > self.value else -1
        self.velocity += self.acceleration * dt
        self.velocity = min(self.max_speed, self.velocity)
        # print(self.velocity, self.acceleration, dt)
        self.value += (self.velocity * dt + 0.5 * self.acceleration * dt ** 2) * direction


class SpringRect:
    def __init__(self, x=0, y=0, w=0, h=0, natural_freq=15, damping_ratio=1):
        self.x = Spring(0, damping_ratio, natural_freq)
        self.y = Spring(0, damping_ratio, natural_freq)
        self.w = Spring(0, damping_ratio, natural_freq)
        self.h = Spring(0, damping_ratio, natural_freq)

    def update(self, dt: float):
        self.x.update(dt)
        self.y.update(dt)
        self.w.update(dt)
        self.h.update(dt)

    @property
    def rect(self):
        return Rect(self.x.value, self.y.value, self.w.value, self.h.value)
    
    @property
    def rect_value(self):
        return (self.x.value, self.y.value, self.w.value, self.h.value)

    def animate_to(self, x: int | None = None, y: int | None = None, w: int | None = None, h: int | None = None):
        if x is not None:
            self.x.animate_to(x)
        if y is not None:
            self.y.animate_to(y)
        if w is not None:
            self.w.animate_to(w)
        if h is not None:
            self.h.animate_to(h)    
