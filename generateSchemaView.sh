sqlite3 database.db -init sqlite-schema-diagram.sql "" > schema.dot
dot -Tsvg schema.dot > schema.svg