from datetime import datetime, timedelta
import os


def process_file(file_path: str, process_line):
    """
    Reads the file line by line, applies the passed `process_line` function
    and returns a dictionary.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            result = {}
            for line in file.read().splitlines():
                key, value = process_line(line)
                result[key] = value
            return result
    except (IOError, PermissionError) as e:
        raise RuntimeError(f"Unable to open or read file: {file_path}. Error: {e}")

def process_abbrev_line(line: str):
    """
    Processes a string from a file "abbreviations" and returns data in the required format.
    """
    parts = line.split('_')
    if len(parts) ==3:
        return parts[0], [parts[1], parts[2]]
    raise ValueError(f"Invalid line format in abbreviation.txt: {line}")


def process_log_line(line: str):
    """
    Processes a string from a log file  and returns data in the required format.
    """
    if len(line) < 3:
        raise ValueError(f"Invalid log line format: {line}")
    abbreviation = line[:3]
    time_str = line[3:].strip()
    return abbreviation, datetime.strptime(time_str, '%Y-%m-%d_%H:%M:%S.%f')

def parse_logs(folder_path: str):
    """
    Reads and parses log files in the specified folder.
    """
    abbreviations_file = os.path.join(folder_path, 'abbreviations.txt')
    start_log = os.path.join(folder_path, 'start.log')
    end_log = os.path.join(folder_path, 'end.log')
    abbreviations = process_file(abbreviations_file, process_abbrev_line)
    start_times = process_file(start_log, process_log_line)
    end_times = process_file(end_log, process_log_line)
    first_start_time = next(iter(start_times.values()))
    date = first_start_time.date()
    return {
        'abbreviations': abbreviations,
        'start_times': start_times,
        'end_times': end_times,
        'date': date
    }

def calculate_lap_times(data: dict):
    """
    Function to calculate lap times based on start and end times.
    """
    lap_times = []
    for driver, start_time in data['start_times'].items():
        if driver in data['end_times']:
            end_time = data['end_times'][driver]
            lap_time = end_time - start_time
            lap_times.append({
                'abbreviation': driver,
                'name': data['abbreviations'].get(driver,
                        ["Unknown", "Unknown"])[0].strip(),
                'team': data['abbreviations'].get(driver,
                        ["Unknown", "Unknown"])[1].strip(),
                'lap_time': lap_time,
                'date': data['date']
            })
    return sorted(lap_times, key=lambda x: x['lap_time'])

def build_report(folder_path: str, order: str = 'asc') -> list:
    """
    Function to build a report of the race.
    """
    data = parse_logs(folder_path)
    lap_times = calculate_lap_times(data)
    if order == 'desc':
        lap_times.reverse()
    return lap_times

def format_time(lap_time: timedelta) -> str:
    """
    Function to format the lap time into a readable string.
    """
    total_seconds = lap_time.total_seconds()
    minutes = int(total_seconds // 60)
    seconds = total_seconds % 60
    return f'{minutes}:{seconds:06.3f}'

def print_report(report):
    """
    Function to format and print the race report.
    """
    print("Top 15 Racers:")
    for idx, racer in enumerate(report[:15], 1):
        print(f"{idx}. {racer['name']:20} | {racer['team']:40} | {format_time(racer['lap_time'])}")
    print("-" * 80)
    print("Rest of the Racers:")
    for idx, racer in enumerate(report[15:], 16):
        print(f"{idx}. {racer['name']:20} | {racer['team']:40} | {format_time(racer['lap_time'])}")

def driver_report(report: list, driver: str):
    """
    Function to print the report for a specific driver.
    """
    for racer in report:
        if racer['name'].lower() == driver.lower():
            print(f"Driver: {racer['name']}\nTeam: {racer['team']}\nLap Time: {format_time(racer['lap_time'])}")
            return
    print(f"No data found for driver: {driver}")
