import mysql.connector
import flask
import sqlite3

def connect():

    database = mysql.connector.connect(
    user="root",
    password="Spiderman80!",
    host="localhost",
    database="politics_database",
    auth_plugin="mysql_native_password"
)

def main():

    database = connect()
    #create cursor to collect data from db
    conn = sqlite3.connect('database.sqlite')
    cur = conn.cursor()
    #drops table project if exists
    cur.execute("DROP TABLE IF EXISTS projects")
    #runs create table script
    cur.execute("""CREATE TABLE IF NOT EXISTS candidates (
                can_id INT PRIMARY KEY NOT NULL,
                firstname VARCHAR NOT NULL,
                surname VARCHAR NOT NULL,
                party_name VARCHAR NOT NULL,
                gender VARCHAR NOT NULL,
                sitting_mp VARCHAR NOT NULL,
                votes INT NOT NULL
            );""")

    
    cur.execute("""CREATE TABLE IF NOT EXISTS parties (
                par_id INT PRIMARY KEY NOT NULL,
                party_name VARCHAR NOT NULL
            );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS constituencies (
                con_id INT PRIMARY KEY NOT NULL,
                constituency_name VARCHAR NOT NULL
            );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS counties (
                county_id INT PRIMARY KEY NOT NULL,
                county_name VARCHAR NOT NULL
            );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS regions (
                reg_id INT PRIMARY KEY NOT NULL,
                region_name VARCHAR NOT NULL
            );""")

    cur.execute("""CREATE TABLE IF NOT EXISTS countries (
                country_id INT PRIMARY KEY NOT NULL,
                country_name VARCHAR NOT NULL
            );""")

def FPTP(cur):
    cur.execute("""
        SELECT c.constituency_name, c.con_id, ca.party_name, MAX(ca.votes) as total_votes
        FROM constituencies c
        JOIN candidates ca ON c.con_id = ca.con_id
        ORDER BY co.constituency_name, ca.votes DESC
    """)

    # Fetch all rows
    rows = cur.fetchall()

    mostvotes = [
        (constituency_name, con_id, party_name, total_votes)
        for constituency_name, con_id, party_name, total_votes in rows
    ]

    for constituency_info in mostvotes:
        print(constituency_info)


    return mostvotes



def Proportion(cur):

    cur.execute("""
        SELECT c.con_id, SUM(ca.votes) as total_votes
        FROM constituencies c
        JOIN candidates ca ON c.con_id = ca.con_id
        GROUP BY c.con_id
    """)

    constituency_sum = dict(cur.fetchall())

    cur.execute("""
        SELECT c.constituency_name, c.con_id, ca.party_name,
               ca.votes, (ca.votes / total_votes) * 100 as voting_percentage
        FROM constituencies c
        JOIN candidates ca ON c.con_id = ca.con_id
        JOIN (
            SELECT con_id, SUM(votes) as total_votes
            FROM candidates
            GROUP BY con_id
        ) con_votes
        ON c.con_id = con_votes_id
        ORDER BY c.constituency_name, ca.party_name
    """)

    p_results = [
        (constituency_name, con_id, party_name, votes, voting_percentage)
        for constituency_name, con_id, party_name, votes, voting_percentage in cur.fetchall()
        if voting_percentage >= 5
    ]

    return p_results
    
    #closes connection
    cur.close()

    



if __name__ == '__main__':
    main()


