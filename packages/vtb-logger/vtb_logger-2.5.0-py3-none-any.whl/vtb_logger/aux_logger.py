import json
import re
from datetime import datetime, timezone
import sys
import time


class Logger:
    class FunctionLogger():
        def __init__(self, outer_instance, function_name: str, identifier: str = "NONE"):

            # Function name
            self.function_name = function_name
            self.validator = outer_instance
            self.identifier = identifier

            pass

        def start_function(self, data):
            # Function start time
            log = self.__log_formatter(level='INFO', data=data)
            self.validator._Logger__log_controller(log)
            self.start_time = time.time()
            pass

        def end_function(self, data):
            log = self.__log_formatter(level='INFO', data=data, ending=True)
            self.validator._Logger__log_controller(log)

        def get_elapsed_time(self, elapsed_time):
            """
            Calculates the elapsed time from start_time and converts it to milliseconds,
            seconds, or minutes based on the value.

            :param start_time: The recorded start time (from time.time()).
            :return: A tuple containing the elapsed time and its unit.
            """
            if elapsed_time < 1:
                return round(elapsed_time * 1000, 2), "milliseconds"
            elif elapsed_time < 60:
                return round(elapsed_time, 2), "seconds"
            else:
                return round(elapsed_time / 60, 2), "minutes"

        def info(self, level='INFO', data=""):
            log = self.__log_formatter(level=level, data=data)
            self.validator._Logger__log_controller(log)
            pass

        def debug(self, level='DEBUG', data=""):
            log = self.__log_formatter(level=level, data=data)
            self.validator._Logger__log_controller(log)
            pass

        def warn(self, level='WARN', data=""):
            log = self.__log_formatter(level=level, data=data)
            self.validator._Logger__log_controller(log)
            pass

        def error(self, level='ERROR', data=""):
            log = self.__log_formatter(level=level, data=data, ending=True)
            self.validator._Logger__log_controller(log)
            pass

        def sensitive(self, level='SENSITIVE', data=""):
            log = self.__log_formatter(level=level, data=data)
            self.validator._Logger__log_controller(log)
            pass

        def __log_formatter(self, level, data: str, ending: bool = False):
            format = self.validator._Logger__detect_data_format(data)
            match format:
                case "json":
                    log = self.__generate_function_json_log_format(
                        log_level=level, data=data, ending=ending)
                    return log
                case "sskv":
                    log = self.__generate_function_space_separated_key_value_format(
                        log_level=level, data=data, ending=ending)
                    return log
                case "cskv":
                    log = self.__generate_function_comma_separated_key_value_format(
                        log_level=level, data=data, ending=ending)
                    return log
                case _:
                    raise ValueError("unsupported data format")

        def __generate_function_json_log_format(self, log_level: str, data, ending: bool = False):
            timestamp = self.validator._Logger__generate_time_stamp()
            log = {}

            log['timestamp'] = timestamp
            log['log_level'] = log_level
            log['function'] = self.function_name
            log['identifier'] = self.identifier

            if ending:
                elapsed_time = time.time() - self.start_time
                calc_time, units = self.get_elapsed_time(elapsed_time)
                log['completion_time'] = f'{calc_time}{units}'

            if isinstance(data, dict):
                log.update(data)
                return f'{log}'

            data = json.loads(data)
            log.update(data)

            return f'{log}'

        def __generate_function_space_separated_key_value_format(self, log_level: str, data, ending: bool = False):
            timestamp = self.validator._Logger__generate_time_stamp()
            if ending:
                elapsed_time = time.time() - self.start_time
                calc_time, units = self.get_elapsed_time(elapsed_time)
                log = f"{timestamp:<35} {log_level:<10} function:{self.function_name} identifier:{self.identifier} completion_time:{calc_time}{units} {data}"
                return log

            log = f"{timestamp:<35} {log_level:<10} function:{self.function_name} {data}"
            return log

        def __generate_function_comma_separated_key_value_format(self, log_level: str, data, ending: bool = False):
            timestamp = self.validator._Logger__generate_time_stamp()

            if ending:
                elapsed_time = time.time() - self.start_time
                calc_time, units = self.get_elapsed_time(elapsed_time)
                log = f"{timestamp:<35} {log_level:<10} function:{self.function_name} identifier:{self.identifier} completion_time:{calc_time}{units} {data}"
                return log

            log = f"{timestamp:<35} {log_level:<10} function:{self.function_name} {data}"
            return log
    # timestamp and log level information are set by default.

    # supported data types: "key:value key:value key:value"(space-separated key-value pairs), "key:value, key:value, key:value"(comma-separated key-value pairs), "{key:value, key:value, key:value}" (json or direct object)
    def __init__(self, service_id="", log_type="file"):
        # Log types available stdout is default you don't need to set that you can save to a file 'file' or forward to a que 'que' both options include stdout
        self.log_type = log_type
        self.service_id = service_id  # NB service id is <system-name>:<service-name>
        if self.log_type == 'que' and service_id == "":
            raise ValueError("Queing requires service id.")

    # Levels available 'INFO'(info), 'WARN'(warn), 'DEBUG'(debug), and 'ERROR' (error)
    def info(self, level='INFO', data=""):
        log = self.__log_formatter(level, data)
        self.__log_controller(log)
        pass

    def warn(self, level='WARN', data=""):
        log = self.__log_formatter(level, data)
        self.__log_controller(log)
        pass

    def debug(self, level='DEBUG', data=""):
        log = self.__log_formatter(level, data)
        self.__log_controller(log)
        pass

    def error(self, level='ERROR', data=""):
        log = self.__log_formatter(level, data)
        self.__log_controller(log)
        pass

    def sensitive(self, level='SENSITIVE', data=""):
        log = self.__log_formatter(level, data)
        self.__log_controller(log)
        pass

    def __detect_data_format(self, data):
        if isinstance(data, dict):
            return "json"

        if isinstance(data, str):
            try:
                # Check if it's JSON
                parsed_json = json.loads(data)
                if isinstance(parsed_json, dict):
                    return "json"
            except json.JSONDecodeError:
                pass

            if re.fullmatch(r'(\w+:["\']?\w+["\']?\s*)+', data):
                return "sskv"

            # Check if it's comma-separated key-value pairs
            if re.fullmatch(r'(\w+:["\']?\w+["\']?,\s*)*\w+:["\']?\w+["\']?', data):
                return "cskv"

        # If none match, return an error
        return "unsupported"

    def __log_formatter(self, level, data: str):
        format = self.__detect_data_format(data)
        match format:
            case "json":
                log = self.__generate_json_log_format(level, data)
                return log
            case "sskv":
                log = self.__generate_space_separated_key_value_format(
                    level, data)
                return log
            case "cskv":
                log = self.__generate_comma_separated_key_value_format(
                    level, data)
                return log
            case _:
                raise ValueError("unsupported data format")

    def __log_to_stdout(self, log):
        sys.stdout.write(f'{log} \n')
        pass

    def __log_to_file(self, log):
        from vtb_logger.aux import ensure_file_exists, write_to_file, generate_current_date
        file = 'app.log'
        current_date = generate_current_date()
        log_file_path = f'tmp/{current_date}/{file}'
        ensure_file_exists(file_path=log_file_path)
        write_to_file(log=log, file_path=log_file_path)

    def __push_to_que(self, log):
        from vtb_logger.aux import publish_message
        topic = 'message_key_generator'
        publish_message(topic=topic, value=log, key=self.service_id)
        pass

    def __generate_time_stamp(self):
        timestamp = datetime.now(timezone.utc).isoformat()
        return timestamp

    def __generate_json_log_format(self, log_level: str, data):
        timestamp = self.__generate_time_stamp()
        log = {}

        log['timestamp'] = timestamp
        log['log_level'] = log_level

        if isinstance(data, dict):
            log.update(data)
            return f'{log}'

        data = json.loads(data)
        log.update(data)

        return f'{log}'

    def __generate_space_separated_key_value_format(self, log_level: str, data):
        timestamp = self.__generate_time_stamp()
        log = f"{timestamp:<35} {log_level:<10} {data}"
        return log

    def __generate_comma_separated_key_value_format(self, log_level: str, data):
        timestamp = self.__generate_time_stamp()
        log = f"{timestamp:<35} {log_level:<10} {data}"
        return log

    def __log_controller(self, log):
        match self.log_type:
            case "file":
                self.__log_to_stdout(log)
                self.__log_to_file(log)

                return
            case "que":
                self.__log_to_stdout(log)
                self.__push_to_que(log)

                return
            case _:
                self.__log_to_stdout(log)
        pass

    def get_function_logger(self, function_name: str, identifier: str = "NONE"):
        return self.FunctionLogger(outer_instance=self, function_name=function_name, identifier=identifier)
