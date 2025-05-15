import { Database } from 'bun:sqlite';

interface CacheStrategy {
    get(key: string): any;
    set(key: string, data: Record<string, any>): void;
    delete(key: string): boolean;
}

class MemoryCache implements CacheStrategy {
    private readonly cache: Map<string, any>;

    constructor() {
        this.cache = new Map();
    }

    get(key: string) {
        return this.cache.get(key);
    }

    set(key: string, data: Record<string, any>) {
        this.cache.set(key, data);
    }

    delete(key: string): boolean {
        return this.cache.delete(key);
    }
}

class SQLiteCache implements CacheStrategy {
    private readonly db: Database;

    constructor() {
        this.db = new Database(':memory:');
        this.db
            .query(
                'CREATE TABLE IF NOT EXISTS cache (key TEXT PRIMARY KEY, value TEXT);',
            )
            .run();
    }

    get(key: string) {
        type ReturnType = { value: string };
        type Queury = { $key: string };
        const query = this.db.query<ReturnType, Queury>(
            'SELECT value FROM cache WHERE key = $key',
        );
        const data = query.get({ $key: key });
        if (!data) {
            return null;
        }
        return JSON.parse(data.value);
    }

    set(key: string, data: Record<string, any>) {
        const query = this.db.query(`
            INSERT INTO cache
                (key, value)
            VALUES
                ($key, $value)
            ON CONFLICT(key)
            DO UPDATE SET value = $value;
        `);
        try {
            query.run({ $key: key, $value: JSON.stringify(data) });
        } catch (e) {
            console.error(e);
        }
    }

    delete(key: string): boolean {
        const query = this.db.query('DELETE FROM cache WHERE key = $key');
        return Boolean(query.run({ $key: key }).changes);
    }
}

class CacheManager {
    private strategy: CacheStrategy;

    constructor(strategy: CacheStrategy | null = null) {
        this.strategy = strategy ? strategy : new MemoryCache();
    }

    setStrategy(strategy: CacheStrategy) {
        this.strategy = strategy;
    }
    get(key: string) {
        return this.strategy.get(key);
    }

    set(key: string, data: Record<string, any>) {
        this.strategy.set(key, data);
    }

    delete(key: string): boolean {
        return this.strategy.delete(key);
    }
}

async function main() {
    const cache = new CacheManager();

    cache.setStrategy(new MemoryCache());
    cache.set('1', {
        id: 1,
        name: 'STACiA - memory',
    });
    cache.set('2', {
        id: 2,
        name: 'LUNA - memory',
    });

    console.log('1: ', cache.get('1'));
    console.log('2: ', cache.get('2'));
    console.log('3: ', cache.get('3'));

    console.log('-'.repeat(30));

    cache.setStrategy(new SQLiteCache());
    cache.set('1', {
        id: 1,
        name: 'STACiA - sqlite',
    });
    cache.set('2', {
        id: 2,
        name: 'LUNA - sqlite',
    });

    console.log('1: ', cache.get('1'));
    console.log('2: ', cache.get('2'));
    console.log('3: ', cache.get('3'));
}

await main();
