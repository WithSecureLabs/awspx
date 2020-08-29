import os
import re
import shutil
import subprocess
import time

from neo4j import GraphDatabase, exceptions
import os
import re
import shutil
import subprocess
import time

from neo4j import GraphDatabase, exceptions
import datetime


class Neo4j(object):

    driver = None
    databases = [db for db in os.listdir("/data/databases/")
                 if db.endswith(".db")
                 and os.path.isdir(f"/data/databases/{db}")]
    zips = [z for z in os.listdir("/opt/awspx/data/")
            if z.endswith(".zip")]

    def __init__(self, host="localhost", port="7687",
                 username="neo4j", password="neo4j"):

        self.uri = f"bolt://{host}:{port}"
        self.username = username
        self.password = password

        try:
            self.open()

        except exceptions.AuthError as e:
            print(f"[-] {e}")

        except exceptions.ServiceUnavailable as e:
            print(f"[-] {e}")

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
            print("[-] Neo4j failed to start")
            return False
        elif retries == 0:
            print("[+] Neo4j has already been started")
        else:
            print("[+] Neo4j has successfully been started")

        return True

    def _stop(self):

        retries = 0
        max_retries = 10

        while retries < max_retries and self.running():
            subprocess.Popen(["killall", "java"])
            time.sleep(1)
            retries += 1

        if self.running():
            print("[-] Neo4j failed to stop")
            return False
        elif retries == 0:
            print("[-]Neo4j has already been stopped")
        else:
            print("[+] Neo4j has successfully been stopped")

        return True

    def _delete(self, db):
        database = f"/data/databases/{db}"
        subprocess.Popen(["rm", "-rf", database])

    def _run(self, tx, cypher):
        results = tx.run(cypher)
        return results

    def _switch_database(self, db):

        subprocess.Popen([
            "sed", "-i",
            '/^\(#\)\{0,1\}dbms.active_database=/s/.*/dbms.active_database=%s/' % db,
            "/var/lib/neo4j/conf/neo4j.conf"],
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

            print(str(stdout).replace(
                "\\n", "\n").replace("\\t", "\t"))

            return False

        (time, nodes, edges, props, ram) = stats.groups()

        return str(f"[+] Loaded {nodes} nodes, {edges} edges, and {props} properties "
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

        self._stop()
        self._switch_database(db)
        self._start()

    def load_zip(self, archive):

        if not archive.startswith("/opt/awspx/data/"):
            archive = f"/opt/awspx/data/{archive}"

        db = f"{archive.split('/')[-1].split('_')[-1].split('.')[0]}.db"

        self._stop()
        loaded = self._load(archive, db)
        self._switch_database(db)
        self._start()

        print(loaded)

    def list(self):

        for db in self.databases:
            print(db)

    def run(self, cypher):

        try:
            with self.driver.session() as session:
                results = session.run(cypher)
            return results

        except exceptions.CypherSyntaxError as e:
            print(f"[-] {e}")
