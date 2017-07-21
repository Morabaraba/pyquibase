# Copyright 2017 Eun Woo Song

# Licensed under the Apache License, Version 2.0 (the "License");^i
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging

from pyquibase.liquibase_executor import LiquibaseExecutor

class Pyquibase(object):
    def __init__(self, config):
        self.liquibase       = LiquibaseExecutor(config)
        self.change_log_file = config['change_log_file']
        self.logger          = logging.getLogger(__name__)

    @classmethod
    def mysql(cls, host, port, db_name, username, password, change_log_file, log_level = 'info'):
        config = { 
            'host'            : host,
            'port'            : port,
            'db_name'         : db_name,
            'username'        : username,
            'password'        : password,
            'change_log_file' : change_log_file,
            'log_level'       : log_level,
            'database'        : 'mysql'
        }

        return cls(config)

    @classmethod
    def postgresql(cls, host, port, db_name, username, password, change_log_file, log_level = 'info'):
        config = { 
            'host'            : host,
            'port'            : port,
            'db_name'         : db_name,
            'username'        : username,
            'password'        : password,
            'change_log_file' : change_log_file,
            'log_level'       : log_level,
            'database'        : 'mysql'
        }

        return cls(config)


    @classmethod
    def sqlite(cls, db_name, change_log_file, log_level = 'info'):
        config = {
            'db_name'         : db_name,
            'change_log_file' : change_log_file,
            'log_level'       : log_level,
            'database'        : 'sqlite'
        }

        return cls(config)

    def update(self): 
        self.logger.info("Executing liquibase update") 
        output = self.liquibase.execute(self.change_log_file, "update")
        self.logger.info(output)
    
    def rollback(self, tag): 
        self.logger.info("Rolling back to %s" % tag)
        output = self.liquibase.execute(self.change_log_file, "rollback", tag)
        self.logger.info(output)

    def rollback_to_datetime(self, datetime):
        self.logger.info("Rolling back to %s on %s/%s/%s" % datetime) 
        output = self.liquibase.execute(self.change_log_file, "rollbackToDate", datetime)
        self.logger.info(output)
