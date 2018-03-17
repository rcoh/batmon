import click
import time
import os
import logging
from subprocess import call

logging.basicConfig(filename=os.path.expanduser('~/.batmon.log'), level=logging.DEBUG)
POWER_SUPPLY = '/sys/class/power_supply'
CURRENT_CHARGE = 'charge_now'
TOTAL_CHARGE = 'charge_full'

@click.command()
@click.argument('battery', required=True)
@click.option('--poll-interval', default=5, help='Default polling interval in seconds')
@click.option('--warn-percentage', default=20, help='Percentage full to display a warning')
@click.option('--panic-percentage', default=10, help='Percentage full to display a panic')
def main(battery, poll_interval, warn_percentage, panic_percentage):
    battery = BatteryMonitor(battery)
    is_charging = battery.is_charging()
    should_warn = not is_charging 
    should_panic = not is_charging
    while True:
        try:
            if battery.is_charging() != is_charging:
                is_charging = battery.is_charging()
                if battery.is_charging():
                    should_warn = False
                    should_panic = False
                else:
                    should_warn = battery.percentage() > warn_percentage
                    should_panic = battery.percentage > panic_percentage
            percentage = battery.percentage()
            if percentage < panic_percentage and should_panic:
                should_panic = False
                notify_panic()
            elif percentage < warn_percentage and should_warn:
                should_warn = False
                notify_warn()
            
            logging.info('Current battery charge: {}'.format(percentage))
        except Exception:
            logging.error('Error while checking battery levels', exc_info=True)
        finally:
            time.sleep(poll_interval)

def notify_warn():
    call(["notify-send", "Warning! Battery power is low"])

def notify_panic():
    call(["notify-send", "Battery power is critically low"])

class BatteryMonitor:
    def __init__(self, battery):
        self.battery = battery

    def is_charging(self):
        with open(os.path.join(POWER_SUPPLY, self.battery, 'status')) as f:
            return f.read() == 'Discharging'

    def percentage(self):
        with open(os.path.join(POWER_SUPPLY, self.battery, CURRENT_CHARGE)) as f:
            current_charge = int(f.read())

        with open(os.path.join(POWER_SUPPLY, self.battery, TOTAL_CHARGE)) as f:
            total_charge = int(f.read())

        return int((current_charge * 1.0 / total_charge) * 100)


if __name__ == "__main__":
    main()
