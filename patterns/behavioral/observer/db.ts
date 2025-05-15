import { Database } from 'bun:sqlite';

export const db = new Database(':memory:');

type User = {
    id: number;
    email: string;
};

export const initialData = () => {
    const query = `
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email VARCHAR(255) NOT NULL
    );
    `;
    db.query(query).run();

    const initialData = [
        {
            $email: 'luna@test.com',
        },
        {
            $email: 'stacia.dev@gmail.com',
        },
    ];

    for (const data of initialData) {
        const query = 'INSERT INTO users (email) VALUES ($email)';
        db.query(query).run(data);
    }
};

initialData();

export const getUsers = (): User[] => {
    const users = [];
    for (const user of db.query('SELECT * FROM users;')) {
        users.push(user as User);
    }
    return users;
};
