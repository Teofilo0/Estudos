CREATE TABLE IF NOT EXISTS Nomes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT
);

CREATE TABLE IF NOT EXISTS Idades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    idade INTEGER
);

CREATE TABLE IF NOT EXISTS Cursos(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    NOMECURSO TEXT NOT NULL
);