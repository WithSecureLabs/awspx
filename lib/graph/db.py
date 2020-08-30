import os
import re
import shutil
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
                 password="neo4j",
                 console=None):

        if console is None:
            from lib.util.console import console
        self.console = console

        self.uri = f"bolt://{host}:{port}"
        self.username = username
        self.password = password

        try:
            self.open()

        except exceptions.AuthError as e:
            self.console.error(str(e))

        except exceptions.ServiceUnavailable as e:
            self.console.error(str(e))

    def _start(self):

        retries = 0
        max_retries = 10

        while retries < max_retries and not self.available():
            subprocess.Popen(["nohup", "/docker-entrypoint.sh", "neo4j", "&"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
            time.sleep(1)
            retries += 1

        if not self.running():
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

    def _load(self, archive, db):

        directory = archive.split('.')[0]
        shutil.unpack_archive(archive, directory, "zip")
        csvs = [f for f in os.listdir(directory) if f.endswith(".csv")]
        edges = [e for e in csvs if re.compile("([A-Z]+)\.csv").match(e)]
        nodes = [n for n in csvs if n not in edges]

        self._delete(db)

        with open(f"{directory}/config.txt", "w") as config:

            conf = ' '.join([
                "--report-file /dev/null",
                "--ignore-missing-nodes=true",
                f"--database {db}",
                ' '.join([f"--nodes {directory}/{n}" for n in nodes]),
                ' '.join(
                    [f"--relationships {directory}/{e}" for e in edges]),
            ])

            config.write(conf)

        stdout, _ = subprocess.Popen(["/docker-entrypoint.sh", "neo4j-admin", "import", "--f", f"{directory}/config.txt"],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT).communicate()

        subprocess.Popen(["rm", "-rf", f"{directory}/"])
        stats = re.compile("([0-9a-zA-Z]+)."
                           "Imported:([0-9]+)nodes"
                           "([0-9]+)relationships"
                           "([0-9]+)properties"
                           "[A-Za-z ]+:(.*)"
                           ).match(str(stdout).split("IMPORT DONE in ")[-1]
                                   .replace("\\n", "").replace(" ", ""))

        if stats is None:

            self.console.error(str(stdout).replace(
                "\\n", "\n").replace("\\t", "\t"))

            return False

        (time, nodes, edges, props, ram) = stats.groups()

        return str(f"Loaded {nodes} nodes, {edges} edges, and {props} properties "
                   f"into '{db}' from '{archive}'")

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

    def load_zip(self, archive):

        if not archive.startswith(f"{NEO4J_ZIP_DIR}/"):
            archive = f"{NEO4J_ZIP_DIR}/{archive}"

        db = f"{archive.split('/')[-1].split('_')[-1].split('.')[0]}.db"

        self.console.task("Stopping Neo4j",
                          self._stop, done="Stopped Neo4j")

        loaded = self.console.task(f"Creating database '{db}'",
                                   self._load, args=[archive, db],
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

        try:
            with self.driver.session() as session:
                results = session.run(cypher)
            return results

        except exceptions.CypherSyntaxError as e:
            self.console.error(str(e))
