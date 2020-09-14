import os
import re
import shutil
import sys
import subprocess
import time

from neo4j import GraphDatabase, exceptions
import datetime


NEO4J_DB_DIR = "/data/databases"
NEO4J_ZIP_DIR = "/opt/awspx/data"
NEO4J_CONF_DIR = "/var/lib/neo4j/conf"


class Neo4j(object):

    driver = None

    zips = [z for z in os.listdir(f"{NEO4J_ZIP_DIR}/")
            if z.endswith(".zip")]

    databases = [db for db in os.listdir(f"{NEO4J_DB_DIR}/")
                 if os.path.isdir(f"{NEO4J_DB_DIR}/{db}")
                 and db.endswith(".db")]

    def __init__(self,
                 host="localhost",
                 port="7687",
                 username="neo4j",
                 password=str(os.environ['NEO4J_AUTH'][6:]
                              if 'NEO4J_AUTH' in os.environ else "password"),
                 console=None):

        if console is None:
            from lib.util.console import console
        self.console = console

        self.uri = f"bolt://{host}:{port}"
        self.username = username
        self.password = password

    def _start(self):

        retries = 0
        max_retries = 60

        while retries < max_retries and not self.available():

            if retries == 0:
                subprocess.Popen(["nohup", "/docker-entrypoint.sh", "neo4j", "console", "&"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.STDOUT)
            time.sleep(1)
            retries += 1

        if not self.available():
            self.console.critical("Neo4j failed to start")
            return False
        elif retries == 0:
            self.console.info("Neo4j has already been started")
        else:
            self.console.info("Neo4j has successfully been started")

        return True

    def _stop(self):

        retries = 0
        max_retries = 10

        while retries < max_retries and self.running():
            subprocess.Popen(["killall", "java"])
            time.sleep(1)
            retries += 1

        if self.running():
            self.console.critical("Neo4j failed to stop")
            return False
        elif retries == 0:
            self.console.info("Neo4j has already been stopped")
        else:
            self.console.info("Neo4j has successfully been stopped")

        return True

    def _delete(self, db):

        subprocess.Popen(["rm", "-rf", f"{NEO4J_DB_DIR}/{db}"])

    def _run(self, tx, cypher):
        results = tx.run(cypher)
        return results

    def _switch_database(self, db):

        subprocess.Popen([
            "sed", "-i",
            '/^\(#\)\{0,1\}dbms.active_database=/s/.*/dbms.active_database=%s/' % db,
            f"{NEO4J_CONF_DIR}/neo4j.conf"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT).communicate()

    def _load(self, archives, db):

        ARCHIVES = {}

        for archive in archives:

            ARCHIVES[archive] = {
                "DIR": None,
                "CSV": None,
            }

            ARCHIVES[archive]["DIR"] = archive.split('.')[0]
            shutil.unpack_archive(archive, ARCHIVES[archive]["DIR"], "zip")

            ARCHIVES[archive]["CSV"] = [f for f in os.listdir(ARCHIVES[archive]["DIR"])
                                        if f.endswith(".csv")]

        for c in set([c for a in ARCHIVES
                      for c in ARCHIVES[a]["CSV"]
                      if len(ARCHIVES) > 0]):

            keys = set()

            for i in range(2):

                for _, v in ARCHIVES.items():

                    if c not in v["CSV"]:
                        continue

                    else:

                        with open(f'{v["DIR"]}/{c}', 'r') as f:
                            headers = [h.strip()
                                       for h in f.readline().split(',')]

                        if i == 0:
                            keys.update(headers)
                            continue

                        additional = [k for k in keys if k not in headers]

                        if not len(additional) > 0:
                            continue

                        self.console.debug(f"Adding columns {additional} "
                                           f'to {v["DIR"]}/{c}')

                        with open(f'{v["DIR"]}/{c}', 'r') as f:
                            rows = f.read().splitlines()

                            rows[0] = ','.join(rows[0].split(',') + additional)

                            for i in range(1, len(rows)):
                                rows[i] = ','.join(rows[i].split(
                                    ',') + ['' for _ in additional])

                        with open(f'{v["DIR"]}/{c}', 'w') as f:
                            f.write('\n'.join(rows))

        directory = ARCHIVES[list(ARCHIVES.keys())[0]]["DIR"]

        csvs = [f"{a['DIR']}/{csv}"
                for a in ARCHIVES.values()
                for csv in a["CSV"]]

        edges = [e for e in csvs
                 if re.compile("(.*/)?([A-Z]+)\.csv").match(e)]
        nodes = [n for n in csvs
                 if n not in edges]

        self._delete(db)

        with open(f"{directory}/config.txt", "w") as config:

            conf = ' '.join([
                "--report-file /dev/null",
                "--ignore-missing-nodes=true",
                "--ignore-duplicate-nodes=true",
                f"--database {db}",
                ' '.join([f"--nodes={n}" for n in nodes]),
                ' '.join([f"--relationships={e}" for e in edges]),
            ])

            config.write(conf)

        stdout, _ = subprocess.Popen(["/docker-entrypoint.sh", "neo4j-admin", "import", "--f", f"{directory}/config.txt"],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT).communicate()

        subprocess.Popen(["rm", "-rf", *[a["DIR"] for a in ARCHIVES.values()]])
        stats = re.compile("([0-9a-zA-Z]+)."
                           "Imported:([0-9]+)nodes"
                           "([0-9]+)relationships"
                           "([0-9]+)properties"
                           "[A-Za-z ]+:(.*)"
                           ).match(str(stdout).split("IMPORT DONE in ")[-1]
                                   .replace("\\n", "").replace(" ", ""))

        if stats is None:
            self.console.critical(str(stdout).replace(
                "\\n", "\n").replace("\\t", "\t"))

        (time, nodes, edges, props, ram) = stats.groups()

        return str(f"Loaded {nodes} nodes, {edges} edges, and {props} properties "
                   f"into '{db}' from: {', '.join([re.sub(f'^{NEO4J_ZIP_DIR}/', '', a) for a in archives])}")

    def running(self):

        stdout, _ = subprocess.Popen(['pgrep', 'java'],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT).communicate()

        pids = [int(i) for i in stdout.split()]

        return len(pids) > 0

    def open(self):

        self.driver = GraphDatabase.driver(
            self.uri,
            auth=(self.username, self.password)
        )

    def close(self):
        if self.driver is not None:
            self.driver.close()

    def available(self):
        try:
            self.open()
        except Exception:
            return False
        return True

    def use(self, db):

        self.console.task("Stopping Neo4j",
                          self._stop, done="Stopped Neo4j")

        self.console.task(f"Switching database to {db}",
                          self._switch_database, args=[db],
                          done=f"Switched database to '{db}'")

        self.console.task("Starting Neo4j",
                          self._start, done="Started Neo4j")

    def load_zips(self, archives=[], db='default.db'):

        archives = [f"{NEO4J_ZIP_DIR}/{a}"
                    if not a.startswith(f"{NEO4J_ZIP_DIR}/") else a
                    for a in archives]

        self.console.task("Stopping Neo4j",
                          self._stop, done="Stopped Neo4j")

        loaded = self.console.task(f"Creating database '{db}'",
                                   self._load, args=[archives, db],
                                   done=f"Created database '{db}'")

        self.console.task(f"Switching active database to '{db}'",
                          self._switch_database, args=[db],
                          done=f"Switched active database to '{db}'")

        self.console.task("Starting Neo4j",
                          self._start, done="Started Neo4j")

        self.console.notice(loaded)

    def list(self):

        self.console.list([{
            "Name": db,
            "Created": datetime.datetime.strptime(
                time.ctime(os.path.getctime(f"{NEO4J_DB_DIR}/{db}")),
                "%a %b %d %H:%M:%S %Y"
            ).strftime('%Y-%m-%d %H:%M:%S')
        } for db in self.databases])

    def run(self, cypher):

        if not self.available():
            self._start()

        try:
            with self.driver.session() as session:
                results = session.run(cypher)
            return results

        except exceptions.CypherSyntaxError as e:
            self.console.error(str(e))
