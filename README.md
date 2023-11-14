# MedWay
MedWay: An IoT system for tracking medicines and vaccines from production to use, ensuring their safety and integrity, promoting global health security through transparency and accountability.

## Quickstar guide

The project depends on several things...
MySQL
PDFlatex
Python3 (and the packages listed in requirements.txt)

Somethings to introduce the new user...

Download [MySQL](https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-22-04) for local server.

---

### Analysis

The data analysis of the system is based on a mahcine learning approach...

### Data acquisition

The data acquisition part of the project corresponds to a ESP...

### Databases

There are two databases in use, one for the sensor readings of the data acquisition system and the numerical results of the analysis, which correspond to a relational database in [Firebase](https://www.mongodb.com/) and a non-relational database in [MongoDB](https://www.mongodb.com/) for the PDF reports generated after the analysis.

### Testing tools

Here we provide some scripts that may aid the new user to understand and test the system, without having to recolect lots of readings from a real harware module.