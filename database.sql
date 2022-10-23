CREATE TABLE users(
    id INT NOT NULL PRIMARY KEY,
    name VARCHAR(50),
    email VARCHAR(255),
    password VARCHAR(255),
    verified INT
);

CREATE TABLE verification_code(
    id INT NOT NULL PRIMARY KEY,
    vc VARCHAR(255),
    user_id INT,
    gen_date TIMESTAMP
    FOREIGN KEY (user_id) REFERENCES users(id)
);