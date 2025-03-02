import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from enum import Enum
from pathlib import Path

from gpiozero import OutputDevice
from sane_rich_logging import setup_logging
from typer import Option, Typer

setup_logging()

app = Typer()


class ServiceAction(str, Enum):
    INSTALL = "install"
    REMOVE = "remove"
    START = "start"
    STOP = "stop"


class LogLevel(str, Enum):
    debug = "DEBUG"
    info = "INFO"
    warning = "WARNING"
    error = "ERROR"
    critical = "CRITICAL"


def append_new_line(file_name: Path, text_to_append: str, header: str | None = None):
    """Append given text as a new line at the end of file"""
    file_exists = file_name.exists()

    with file_name.open("a+") as file_object:
        if not file_exists and header:
            file_object.write(header + "\n")
        file_object.write(text_to_append + "\n")


def get_temp() -> float:
    """Get the core temperature.

    Read file from /sys to get CPU temp in temp in C *1000

    Returns:
        float: The core temperature in degrees Celsius.
    """
    with open("/sys/class/thermal/thermal_zone0/temp") as f:
        temp_str = f.read()

    try:
        return float(temp_str) / 1000
    except (IndexError, ValueError) as err:
        raise RuntimeError("Could not parse temperature output.") from err


@app.command()
def service(
    action: ServiceAction,
    on_threshold: float | None = Option(
        60,
        "-on",
        "--on-threshold",
        envvar="ON_THRESHOLD",
        help="The temperature threshold (in degrees Celsius) at which to turn the fan on.",
    ),
    off_threshold: float | None = Option(
        50,
        "-off",
        "--off-threshold",
        envvar="OFF_THRESHOLD",
        help="The temperature threshold (in degrees Celsius) at which to turn the fan off.",
    ),
    sleep_interval: int | None = Option(
        10,
        "-s",
        "--sleep-interval",
        envvar="SLEEP_INTERVAL",
        help="The interval (in seconds) at which to check the temperature.",
    ),
    gpio_pin: int | None = Option(
        17,
        "-p",
        "--gpio-pin",
        envvar="GPIO_PIN",
        help="The GPIO pin to use to control the fan.",
    ),
    log_level: LogLevel = Option(
        "INFO",
        case_sensitive=False,
        envvar="LOG_LEVEL",
        help="Set the log level. Available options: DEBUG, INFO, WARNING, ERROR, CRITICAL",
    ),
):
    """Manage the service for this application (install, start, stop)."""
    service_name = "fan_control"
    user_service_path = Path.home() / f".config/systemd/user/{service_name}.service"
    venv_bin_path = Path(sys.executable).parent / "pi-fan"
    if action == ServiceAction.INSTALL:
        unit_content = f"""[Unit]
Description=Fan Control Service
After=network.target

[Service]
Environment="ON_THRESHOLD={on_threshold}"
Environment="OFF_THRESHOLD={off_threshold}"
Environment="SLEEP_INTERVAL={sleep_interval:d}"
Environment="GPIO_PIN={gpio_pin:d}"
Environment="LOG_LEVEL={log_level.value}"
ExecStart={venv_bin_path} monitor
Restart=always

[Install]
WantedBy=default.target
"""
        user_service_path.parent.mkdir(parents=True, exist_ok=True)
        user_service_path.write_text(unit_content)
        subprocess.run(["systemctl", "--user", "daemon-reload"], check=True)
        subprocess.run(["systemctl", "--user", "enable", service_name], check=True)
        logging.info(f"Service {service_name} installed successfully.")
    elif action == ServiceAction.START:
        subprocess.run(["systemctl", "--user", "start", service_name], check=True)
        logging.info(f"Service {service_name} started.")
    elif action == ServiceAction.STOP:
        subprocess.run(["systemctl", "--user", "stop", service_name], check=True)
        logging.info(f"Service {service_name} stopped.")
    elif action == ServiceAction.REMOVE:
        subprocess.run(["systemctl", "--user", "disable", service_name], check=True)
        logging.info(f"Service {service_name} disabled.")
    else:
        logging.error("Invalid action. Use 'install', 'start', 'remove', or 'stop'.")


@app.command()
def monitor(
    on_threshold: float | None = Option(
        60,
        "-on",
        "--on-threshold",
        envvar="ON_THRESHOLD",
        help="The temperature threshold (in degrees Celsius) at which to turn the fan on.",
    ),
    off_threshold: float | None = Option(
        50,
        "-off",
        "--off-threshold",
        envvar="OFF_THRESHOLD",
        help="The temperature threshold (in degrees Celsius) at which to turn the fan off.",
    ),
    sleep_interval: int | None = Option(
        10,
        "-s",
        "--sleep-interval",
        envvar="SLEEP_INTERVAL",
        help="The interval (in seconds) at which to check the temperature.",
    ),
    gpio_pin: int | None = Option(
        17,
        "-p",
        "--gpio-pin",
        envvar="GPIO_PIN",
        help="The GPIO pin to use to control the fan.",
    ),
    data_dump: Path | None = Option(
        None,
        "--data-dump",
        envvar="DATA_DUMP",
        help="Optional file name to dump temperature data.",
    ),
    log_level: LogLevel = Option(
        "INFO",
        case_sensitive=False,
        envvar="LOG_LEVEL",
        help="Set the log level. Available options: DEBUG, INFO, WARNING, ERROR, CRITICAL",
    ),
) -> None:
    """Monitor the core temperature of a Raspberry Pi and control a fan based on the temperature."""
    os.environ["LOG_LEVEL"] = log_level.value

    if off_threshold >= on_threshold:
        raise RuntimeError("OFF_THRESHOLD must be less than ON_THRESHOLD")

    fan = OutputDevice(gpio_pin)
    header = "Datetime\tTemperature(C)\tFan State\tOn Threshold\tOff Threshold"

    while True:
        temp = get_temp()
        fan_state = "on" if fan.value else "off"
        logging.debug(f"Temperature: {temp:.2f}C\tFan: {fan_state}")

        if data_dump:
            append_new_line(
                data_dump,
                f"{datetime.now()}\t{temp}\t{fan.value}\t{on_threshold}\t{off_threshold}",
                header=header,
            )

        if temp > on_threshold and not fan.value:
            logging.info(f"Turning fan on - Temperature: {temp:.2f}C > {on_threshold}C")
            fan.on()
        elif fan.value and temp < off_threshold:
            logging.info(f"Turning fan off - Temperature: {temp:.2f}C < {off_threshold}C")
            fan.off()

        time.sleep(sleep_interval)


if __name__ == "__main__":
    app()
