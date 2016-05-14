#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3
import config

con = sqlite3.connect(config.PERSISTENCE_LOCATION)

with con:
    cur = con.cursor()    
    cur.execute("""
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY,
    email VARCHAR(255) NOT NULL,
    forename VARCHAR(50) NOT NULL,
    surname VARCHAR(50) NOT NULL,
    created DATETIME
);
""")
