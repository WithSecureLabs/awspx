[[https://raw.githubusercontent.com/wiki/FSecureLABS/awspx/uploads/Awspx.svg|width=600px]]

> auspex [ˈau̯s.pɛks] noun: An augur of ancient Rome, especially one who interpreted omens derived from the observation of birds.

![](https://img.shields.io/github/license/FSecureLABS/awspx)
![](https://img.shields.io/github/v/tag/FSecureLabs/awspx)
![](https://img.shields.io/github/contributors/FSecureLABS/awspx)

# Overview

**awspx** is a graph-based tool for visualizing effective access and resource relationships within AWS. It resolves policy information to determine *what* actions affect *which* resources, while taking into account how these actions may be combined to produce attack paths. Unlike tools like [Bloodhound](https://github.com/BloodHoundAD/BloodHound), awspx requires permissions to function — it is not expected to be useful in cases where these privileges have not been granted.

### Table of contents 

- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

*For more information, checkout the [awspx Wiki](Home.md)*

# Getting Started

*For detailed instructions, usage, and answers to frequently asked questions see: [Installation](Setup.md), [Data Collection](Data%20Collection.md), [Web Interface](Data%20Exploration.md), and [FAQs](FAQs.md).*

## Installation 

**awspx** can be [installed](Setup.md) on either Linux or macOS. *In each case [Docker](https://docs.docker.com/get-docker/) is required.*

1. Clone this repo
```bash
git clone https://github.com/FSecureLABS/awspx.git
```
2. Run the `INSTALL` script
```bash
cd awspx && ./INSTALL
```
    
## Usage 

**awspx** consists of two main components: the [**ingestor**](Data%20Collection.md#ingestion), *which collects AWS account data*; and the [**web interface**](Data%20Exploration.md#overview), *which allows you to explore it*. 

1. [Run the **ingestor**](Data%20Collection.md#ingestion) against an account of your choosing. _You will be prompted for [credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration)._

    ```bash
    awspx ingest
    ```
    _**OR** optionally forgo this step and [load the sample dataset](Data%20Collection.md#zip-files) instead._
    
    ```bash
    awspx db --load-zip sample.zip
    awspx attacks
    ```

2. Browse to the **web interface** — *<http://localhost> by default* — and [explore this environment](Data%20Exploration.md#using-the-interface). 

    </br>
    [[https://raw.githubusercontent.com/wiki/FSecureLABS/awspx/uploads/Awspx.gif]] 

# Contributing

This project is in its early days and there's still plenty that can be done. Whether its submitting a fix, identifying bugs, suggesting enhancements, creating or updating documentation, refactoring smell code, or even extending this list — all contributions help and are more than welcome. Please feel free to use your judgement and do whatever you think would benefit the community most.

*See [Contributing](Contributing.md) for more information.*

# License 

**awspx** is a graph-based tool for visualizing effective access and resource relationships within AWS. (C) 2018-2020 F-SECURE.

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details. 

You should have received a copy of the GNU General Public License along with this program. If not, see <https://www.gnu.org/licenses/>. 
