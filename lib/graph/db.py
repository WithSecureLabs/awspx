import os
import re
import shutil
import subprocess
import time

from neo4j import GraphDatabase
from neobolt import exceptions


class Neo4j(object):

    connection = "bolt://localhost:7687"
    username = "neo4j"
    password = "neo4j"

    @staticmethod
    def run(cypher):
        driver = GraphDatabase.driver(
            Neo4j.connection,
            auth=(Neo4j.username, Neo4j.password))
        with driver.session() as session:
            results = session.run(cypher)
        driver.close()
        return results

    @staticmethod
    def isrunning():

        stdout, _ = subprocess.Popen(['pgrep', 'java'],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT).communicate()

        pids = [int(i) for i in stdout.split()]

        return len(pids) > 0

    @staticmethod
    def isavailable():
        try:
            GraphDatabase.driver(
                Neo4j.connection,
                auth=(Neo4j.username, Neo4j.password)
            ).session()

        except exceptions.ServiceUnavailable:
            return False
        return True

    @staticmethod
    def start():
        if not Neo4j.isrunning():
            subprocess.Popen(["nohup", "/docker-entrypoint.sh", "neo4j", "&"],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
            for _ in range(10):
                time.sleep(1)
                if Neo4j.isavailable():
                    return (True, "[+] Neo4j has successfully been started.")
            return(True, "[-] Neo4j failed to start.")

        return(True, "[!] Neo4j has already been started.")

    @staticmethod
    def stop():
        if Neo4j.isrunning():
            subprocess.Popen(["killall", "java"])
            for _ in range(10):
                time.sleep(1)
                if not Neo4j.isavailable():
                    return (True, "[+] Neo4j has successfully been stopped.")
            return(False, "[-] Neo4j failed to stop.")
        return(True, "[!] Neo4j has already been stopped.")

    @staticmethod
    def restart():
        Neo4j.stop()
        time.sleep(1)
        Neo4j.start()

    @staticmethod
    def switch_database(db):
        subprocess.Popen([
            "sed", "-i",
            '/^\(#\)\{0,1\}dbms.active_database=/s/.*/dbms.active_database=%s/' % db,
            "/var/lib/neo4j/conf/neo4j.conf"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT).communicate()

    @staticmethod
    def load(archive, db):

        Neo4j.stop()
        Neo4j.delete(db)

        directory = archive.split('.')[0]
        shutil.unpack_archive(archive, directory, "zip")
        csvs = [f for f in os.listdir(directory) if f.endswith(".csv")]
        edges = [e for e in csvs if re.compile("([A-Z]+)\.csv").match(e)]
        nodes = [n for n in csvs if n not in edges]

        with open(f"{directory}/config.txt", "w") as config:

            conf = ' '.join([
                "--report-file /dev/null",
                "--ignore-missing-nodes=true",
                f"--database {db}",
                ' '.join([f"--nodes {directory}/{n}" for n in nodes]),
                ' '.join([f"--relationships {directory}/{e}" for e in edges]),
            ])

            config.write(conf)

        stdout, _ = subprocess.Popen(["/docker-entrypoint.sh", "neo4j-admin", "import", "--f", f"{directory}/config.txt"],
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.STDOUT).communicate()
        stats = re.compile(
            "([0-9a-zA-Z]+)."
            "Imported:([0-9]+)nodes"
            "([0-9]+)relationships"
            "([0-9]+)properties"
            "[A-Za-z ]+:(.*)"
        ).match(str(stdout).split("IMPORT DONE in ")[-1]
                .replace("\\n", "").replace(" ", "")
                )

        if stats is None:
            Neo4j().start
            return (False, str(stdout).replace("\\n", "\n").replace("\\t", "\t"))

        subprocess.Popen(["rm", "-rf", f"{directory}/"])

        Neo4j.switch_database(db)
        Neo4j.start()

        (time, nodes, edges, props, ram) = stats.groups()

        return (True, "[+] Loaded {nodes} nodes, {edges} edges, and {props} properties into '{db}'.".format(
            nodes=nodes,
            edges=edges,
            props=props,
            db=db))

    @staticmethod
    def delete(db):
        subprocess.Popen(["rm", "-rf", "/data/databases/%s" % db])

    @staticmethod
    def _run(tx, cypher):
        results=tx.run(cypher)
        return results
