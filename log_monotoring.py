import time
import signal
import logging
import re
from collections import Counter

logging.basicConfig(filename='monitor.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

def monitor_log(log_file):
    try:
        with open(log_file, 'r') as f:
            f.seek(0, 2) 
            while True:
                line = f.readline()
                if line:
                    print(f"New log entry: {line}")
                    logging.info(f"New log entry: {line.strip()}")
                    analyze_log(line)
                time.sleep(0.1)
    except FileNotFoundError:
        logging.error("Log file not found. Please specify a valid log file path.")
        exit(1)
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")
        exit(0)

def analyze_log(log_entry):
    keywords = ['ERROR', 'WARNING', 'INFO']  
    for keyword in keywords:
        if re.search(keyword, log_entry):
            logging.debug(f"Found keyword: {keyword}")
            save_analysis_result(keyword)


def save_analysis_result(keyword):
    with open('analysis_results.txt', 'a') as f:
        f.write(f"{keyword}\n")

def generate_report(log_file):
    try:
        with open(log_file, 'r') as f:
            log_entries = f.readlines()
            error_messages = [entry.strip() for entry in log_entries if 'ERROR' in entry]
            top_errors = Counter(error_messages).most_common(3) 
            with open('summary_report.txt', 'w') as report_file:
                report_file.write("Top Error Messages:\n")
                for error, count in top_errors:
                    report_file.write(f"{error}: {count} occurrences\n")
                logging.info("Summary report generated.")
    except FileNotFoundError:
        logging.error("Log file not found. Cannot generate report.")
        exit(1)

def signal_handler(sig, frame):
    print("\nMonitoring stopped by user.")
    logging.info("Monitoring stopped by user.")
    exit(0)

def main():
    log_file = 'example.log'  
    signal.signal(signal.SIGINT, signal_handler)  #handler for Ctrl+C
    logging.info("Monitoring started.")
    monitor_log(log_file)

if _name_ == "_main_":
    main()
