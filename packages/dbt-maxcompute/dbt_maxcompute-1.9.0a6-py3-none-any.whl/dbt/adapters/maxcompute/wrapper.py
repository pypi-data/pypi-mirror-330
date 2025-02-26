import time
from datetime import datetime, date
from decimal import Decimal

from dbt.adapters.events.logging import AdapterLogger
from odps.dbapi import Cursor, Connection
from odps.errors import ODPSError
import re


class ConnectionWrapper(Connection):
    def cursor(self, *args, **kwargs):
        return CursorWrapper(
            self,
            *args,
            hints=self._hints,
            **kwargs,
        )

    def cancel(self):
        self.close()


logger = AdapterLogger("MaxCompute")


class CursorWrapper(Cursor):
    def execute(self, operation, parameters=None, **kwargs):
        def replace_sql_placeholders(sql_template, values):
            if not values:
                return sql_template
            if operation.count("%s") != len(parameters):
                raise ValueError("参数数量与SQL模板中的占位符数量不匹配")
            return operation % tuple(parameters)

        def param_normalization(params):
            if not params:
                return None
            normalized_params = []
            for param in params:
                if param is None:
                    normalized_params.append("NULL")
                elif isinstance(param, Decimal):
                    normalized_params.append(f"{param}BD")
                elif isinstance(param, datetime):
                    normalized_params.append(f"TIMESTAMP'{param.strftime('%Y-%m-%d %H:%M:%S')}'")
                elif isinstance(param, date):
                    normalized_params.append(f"DATE'{param.strftime('%Y-%m-%d')}'")
                elif isinstance(param, str):
                    normalized_params.append(f"'{param}'")
                else:
                    normalized_params.append(f"{param}")
            return normalized_params

        def remove_comments(input_string):
            # Use a regular expression to remove comments
            result = re.sub(r"/\*[^+].*?\*/", "", input_string, flags=re.DOTALL)
            return result

        # operation = remove_comments(operation)
        parameters = param_normalization(parameters)
        operation = replace_sql_placeholders(operation, parameters)

        def parse_settings(sql):
            properties = {}
            index = 0

            while True:
                end = sql.find(";", index)
                if end == -1:
                    break
                s = sql[index:end]
                if re.match(r"(?i)^\s*SET\s+.*=.*?\s*$", s):
                    # handle one setting
                    i = s.lower().find("set")
                    pair_string = s[i + 3 :]
                    pair = pair_string.split("=")
                    properties[pair[0].strip()] = pair[1].strip()
                    index = end + 1
                else:
                    # break if there is no settings before
                    break

            return properties

        # retry ten times, each time wait for 10 seconds
        retry_times = 10
        for i in range(retry_times):
            try:
                super().execute(operation)
                self._instance.wait_for_success()
                return
            except ODPSError as e:
                # 0130201: view not found, 0110061, 0130131: table not found
                if (
                    e.code == "ODPS-0130201"
                    or e.code == "ODPS-0130211"  # Table or view already exists
                    or e.code == "ODPS-0110061"
                    or e.code == "ODPS-0130131"
                    or e.code == "ODPS-0420111"
                ):
                    if i == retry_times - 1:
                        raise e
                    logger.warning(f"Retry because of {e}, retry times {i + 1}")
                    time.sleep(15)
                    continue
                else:
                    o = self.connection.odps
                    if e.instance_id:
                        instance = o.get_instance(e.instance_id)
                        logger.error(instance.get_logview_address())
                    raise e
