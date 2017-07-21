# Copyright 2017 Eun Woo Song

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import subprocess

from pkg_resources import resource_filename

LIQUIBASE_COMMAND = """java -jar %s \
    --driver=%s \
    --classpath=%s \
    --changeLogFile=%s \
    --url="%s" \
    --username=%s \
    --password=%s \
    --logLevel=%s \
"""

SQLITE_LIQUIBASE_COMMAND = """java -jar %s \
    --driver=%s \
    --classpath=%s \
    --changeLogFile=%s \
    --url="%s" \
"""

SUPPORTED_DATABASES = {
    'mysql' : {
        'url'          : 'jdbc:mysql://%s:%s/%s',
        'driver'       : "com.mysql.jdbc.Driver",
        'db_connector' : resource_filename(__package__, "db-connectors/mysql-connector-java-5.1.42-bin.jar"),
        'command'      : LIQUIBASE_COMMAND

    },
    'postgresql' : {
        'url'          : 'jdbc:postgresql://%s:%s/%s',
        'driver'       : "org.postgresql.Driver",
        'db_connector' : resource_filename(__package__, "db-connectors/postgresql-42.1.3.jar"),
        'command'      : LIQUIBASE_COMMAND

    },
    'sqlite': {
        'url'          : 'jdbc:sqlite:%s',
        'driver'       : "org.sqlite.JDBC",
        'db_connector' : resource_filename(__package__, "db-connectors/sqlite-jdbc-3.18.0.jar"),
        'command'      : SQLITE_LIQUIBASE_COMMAND
    }
}

class LiquibaseExecutor(object):

  def __init__(self, config):
    if config['database'] not in SUPPORTED_DATABASES: 
        raise Exception("%s is not a supported database" % database) 
  
    self.config       = config
    self.db           = SUPPORTED_DATABASES[config['database']]
    self.liquibaseJar = resource_filename(__package__, "liquibase/liquibase.jar")
    self.logger       = logging.getLogger(__name__)

  def execute(self, changeLogFilePath, *args): 
      config = self.config
      db     = self.db

      if config['database'] != 'sqlite':
          url               = db['url'] % (config['host'], config['port'], config['db_name'])
          liquibase_command = db['command'] % (
              self.liquibaseJar, 
              db['driver'],
              db['db_connector'], 
              config['change_log_file'],
              url,
              config['username'],
              config['password'],
              config['log_level']
          )
      else:
          url               = db['url'] % config['db_name']
          liquibase_command = self.db['command'] % (
              self.liquibaseJar, 
              db['driver'],
              db['db_connector'], 
              config['change_log_file'],
              url
          )
    
      args              = " ".join(args)
      liquibase_command = liquibase_command + args

      output = subprocess.check_output(
          liquibase_command,
          stderr = subprocess.STDOUT,
          shell  = True
      )

      print(output)

      return output#.decoding('utf-8')
