<img src="images/awspx-logo.svg" width="600px">

<br/>
<br/>
<br/>

> **auspex** [ˈau̯s.pɛks] *noun*: An augur of ancient Rome, especially one who interpreted omens derived from the observation of birds.

**awspx** is a graph-based tool for visualizing effective access and resource relationships within AWS. It resolves policy information to determine _what_ actions affect _which_ resources, while taking into account how these actions may be combined to produce attack paths. Unlike tools like Bloodhound, awspx requires permissions to function. It is not expected to be useful in cases where these privileges have not been granted. 


# Quick start

Install (see installation), load the sample database, and search for attacks:

```
awspx db --load-zip sample.zip
awspx attacks
```

OR run it against an environment of your own (attack information is included by default in this case):

```
awspx ingest
```

Browse to localhost and see what you can find!


<img src="images/awspx.gif" width="800px">

# Installation

awspx requires Docker.

```
git clone git@github.com:FSecureLABS/awspx.git
cd awspx && ./INSTALL 
```

## If it doesn't work out of the box, here are some things to check: 

* The docker container runs a Neo4j database that will forward TCP ports 7687, 7373 and 7474 to these same ports on localhost. If an existing Neo4j installation is present  (e.g. BloodHound) `awspx` will fail. You will need to disable this service before continuing. Alternatively, you can modify network mappings yourself by editing `INSTALL`.
* The docker container also forwards to TCP port 80, resulting in similar issues.
* SELinux may prevent the docker container from doing everything it needs to. If you are running SELinux (props) and encounter issues, check SELinux. 
* Docker makes changes to iptables. You may need to adjust your iptables configuration to get awspx to work.  

# AWS permissions

The following AWS-managed policies can be used.

* `SecurityAudit` will allow you to ingest everything except S3 objects.
* Add `ReadOnlyAccess` to also ingest S3 objects (warning: this can be very slow).

# Data collection

Once awspx has been installed, you can create a profile by running `awspx profile --create my-account`, or invoke the ingestor by running `awspx ingest` on the command line. By default the ingestor will utilise a profile called _default_ unless you specify something else using `--profile`: 

```
awspx ingest --profile my-other-account
```

If the profile _my-other-account_ does not exist, you will prompted to enter a AWS access key ID and secret for it. You will also be prompted an output format, which you can ignore, and a region which is not important for IAM but required for other services. You can also create a profile this without ingesting any data by using `awspx profile`:

```
awspx profile --create work
```

Further commands and arguments are provided for tweaking ingestion and attack path computation, and for managing AWS profiles and Neo4j databases. Run `awspx -h` and `awspx {profile|ingest|attacks|db} -h` to learn more.

**Supported services:** IAM, EC2, S3, Lambda

### Examples

```
awspx ingest --profile my-account --services S3
```

The ingestor will pull only S3 data using the `my-account` profile and store it in a database named `my-account.db`. Resource based policies (and Bucket ACLs in this case) will be processed automatically. Identify based policies will be ignored since IAM has been omitted from this list of services. 

```
awspx ingest --profile my-account --services IAM EC2 --database db-for-ec2
```

The ingestor will pull only IAM and EC2 data, using the `my-account` profile, and store it in a database named `db-for-ec2.db`. Since IAM includes Identity based policies and assume role policy documents, this infromation will be included in `db-for-ec2.db`

```
awspx ingest --profile my-account \
    --except-types AWS::S3::Object \
    --except-arns arn:aws:s3:::broken-bucket arn:aws:ec2:eu-west-1:123456789012:instance/i-1234
```
awspx will pull data for all supported services using the `my-account` profile but will not attempt to load S3 objects. It will also skip the bucket named `broken-bucket` and the EC2 instance named `i-1234`. A full list of recognised resource types can be found in `lib/aws/resources.py`.

```
awspx ingest --profile my-account --skip-attacks
```

awspx will pull data for all supported services using the `my-account` profile but will not compute attacks. This can be useful for large environments. Attacks can be computed separately later on by running `awspx attacks`.

```
awspx attacks --only-attacks AssumeRole CreateGroup
```

Using the current database, awspx will only compute only the Assume Role and Create Group attacks.

```
awspx db --load-zip sample.zip
```

awspx will create a new database named `sample` from sample ZIP file. Files must be placed in `/opt/awspx/data` so that they can be accessed by the docker container. Note that attack information is not included with zip data. To include this information `awspx attacks` must be run after a zip has been loaded. 

```
awspx db --use my-other-account
```

awspx will switch the database to `my-other-account`. You will need to refresh your browser to see the changes.

# Using the frontend

Once you've loaded a database (hint: load the sample data by running `awspx db --load-zip sample.zip`) you can explore it by visiting localhost in your browser. 

To get started, find a Resource (or Action) you're interested in and see where the path takes you (right click on Resources to bring up the context menu, left click to see its properties).

## Action colors

Action Effect color palette:

* Allow:       Green edges
* Deny:        Red edges
* Conditional: Dashed edges

Action Access Type color palette:

* List:                   Yellow
* Read:                   Pink 
* Write:                  Indigo
* Tagging:                Teal
* Permissions Management: Purple

Actions are represented visually using a linear gradient comprised of the Effect and Access colors (in that order). Conditional attacks are presented using a dotted line. 

## Shortcut keys

| Key               | Action                                           |
| ----------------- | ------------------------------------------------ |
| Alt + Enter       | Rerun Layout                                     |
| Tab               | Switch between Actions and Resources search view |
| Ctrl + Drag       | Box select                                       |
| Ctrl + Left Click | toggle selection                                 |
| Delete            | Remove selected nodes                            |
| Escape            | Close properties                                 |
| Ctrl + C          | Copy selection properties (JSON)                 |
| Ctrl + A          | Select all                                       |
| Ctrl + S          | Open search bar                                  |

# About 

awspx was developed by Craig Koorn and David Yates using Python (ingestor); Neo4j (DB); and Vue (front-end); and Cytoscape (front-end graph visualization).  


# License 

awspx is a graph-based tool for visualizing effective access and resource relationships in AWS environments. (C) 2018-2019 F-SECURE CYBER SECURITY LIMITED.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. 

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
