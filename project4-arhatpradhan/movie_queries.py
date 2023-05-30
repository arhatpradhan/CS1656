from neo4j import GraphDatabase, basic_auth
import socket


class Movie_queries(object):
    def __init__(self, password):
        self.driver = GraphDatabase.driver("bolt://localhost", auth=("neo4j", password), encrypted=False)
        self.session = self.driver.session()
        self.transaction = self.session.begin_transaction()

    def q0(self):
        result = self.transaction.run("""
            MATCH (n:Actor) RETURN n.name, n.id ORDER BY n.birthday ASC LIMIT 3
        """)
        return [(r[0], r[1]) for r in result]

    def q1(self):
        result = self.transaction.run("""
            MATCH (a:Actor)-[:ACTS_IN]->(m:Movie)
            WITH a.name AS actor_name, count(m) AS number_of_films_acted_in
            ORDER BY number_of_films_acted_in DESC, actor_name ASC
            RETURN actor_name, number_of_films_acted_in
            LIMIT 20
        """)
        return [(r[0], r[1]) for r in result]

    def q2(self):
        result = self.transaction.run("""
            MATCH (m:Movie)<-[:RATED]-(:User)
            WITH m.title AS movie_title, size((m)<-[:ACTS_IN]-(:Actor)) AS number_of_cast_members
            ORDER BY number_of_cast_members DESC
            LIMIT 1
            RETURN movie_title, number_of_cast_members
        """)
        return [(r[0], r[1]) for r in result]

    def q3(self):
        result = self.transaction.run("""
            MATCH (d:Director)-[:DIRECTED]->(m:Movie)
            WITH d, count(DISTINCT m.genre) AS numGenres
            WHERE numGenres >= 2
            RETURN d.name AS directorName, numGenres
            ORDER BY numGenres DESC, directorName ASC
        """)
        return [(r[0], r[1]) for r in result]
        
    def q4(self):
        result = self.transaction.run("""
            MATCH (kb:Actor {name: "Kevin Bacon"})-[:ACTS_IN]->()<-[:ACTS_IN]-(coActor)-[:ACTS_IN]->()<-[:ACTS_IN]-(actor:Actor)
            WHERE actor <> kb AND NOT (actor)-[:ACTS_IN]->()<-[:ACTS_IN]-(kb) AND NOT actor = coActor
            RETURN DISTINCT actor.name
            ORDER BY actor.name
        """)
        return [(r[0]) for r in result]

if __name__ == "__main__":
    sol = Movie_queries("neo4jpass")
    print("---------- Q0 ----------")
    print(sol.q0())
    print("---------- Q1 ----------")
    print(sol.q1())
    print("---------- Q2 ----------")
    print(sol.q2())
    print("---------- Q3 ----------")
    print(sol.q3())
    print("---------- Q4 ----------")
    print(sol.q4())
    sol.transaction.close()
    sol.session.close()
    sol.driver.close()

