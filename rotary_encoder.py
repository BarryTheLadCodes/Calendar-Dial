from machine import Pin  # type: ignore
from rotary_irq_esp import RotaryIRQ # type: ignore
import time

STEPS_PER_REV = 30  # Depends on your encoder

# Create a RotaryIRQ object
r = RotaryIRQ(pin_num_clk=4,
              pin_num_dt=5,
              min_val=0,
              max_val=STEPS_PER_REV - 1,
              reverse=False,
              range_mode=RotaryIRQ.RANGE_WRAP,
              pull_up=True,
              half_step=True)

while True:
    val = r.value()
    angle = val * (360 / STEPS_PER_REV)  # 20 steps per full turn
    print("Angle:", angle)
    time.sleep(0.1)