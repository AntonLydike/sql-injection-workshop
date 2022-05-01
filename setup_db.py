import sqlite3

conn = sqlite3.connect("data.sqlite")

conn.executescript("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER NOT NULL,
    name TEXT NOT NULL,
    written TEXT NOT NULL,
    authors TEXT NOT NULL,
    description TEXT NOT NULL
);
    
CREATE TABLE IF NOT EXISTS users (
    username TEXT NOT NULL,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS sessions (
    token TEXT NOT NULL
);

INSERT INTO users (username, password) VALUES ('user1', 'password');

INSERT INTO books (id, name, written, authors, description) VALUES 
(1, "1984", "1949", "George Orwell", "1984 is a dystopian novella by George Orwell published in 1949, which follows the life of Winston Smith, a low ranking member of 'the Party', who is frustrated by the omnipresent eyes of the party, and its ominous ruler Big Brother. 'Big Brother' controls every aspect of people's lives."),
(2, "Fermats Last Theorem", "1997", "Simon Singh", "Fermat's Last Theorem is a popular science book (1997) by Simon Singh. It tells the story of the search for a proof of Fermat's Last Theorem, first conjectured by Pierre de Fermat in 1637, and explores how many mathematicians such as Évariste Galois had tried and failed to provide a proof for the theorem. Despite the efforts of many mathematicians, the proof would remain incomplete until 1995, with the publication of Andrew Wiles' proof of the Theorem."),
(3, "Jesus Video", "1998", "Andreas Eschbach", "Bei Ausgrabungsarbeiten in Israel wird in einem zweitausend Jahre alten Grab eine Plastikhülle gefunden, die die Bedienungsanleitung einer japanischen Videokamera enthält. Eine C14-Analyse zeigt, daß das Papier der Broschüre tatsächlich zweitausend Jahre alt ist. Und die darin beschriebene Kamera wird erst in drei Jahren auf den Markt kommen.");

""")

conn.commit()