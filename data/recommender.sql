CREATE TABLE IF NOT EXISTS teammates (
    id TEXT PRIMARY KEY,
    name TEXT,
    CONSTRAINT teammates_id_name_un
        UNIQUE (id, name)
        ON CONFLICT IGNORE
);
CREATE TABLE IF NOT EXISTS restaurants (
    id TEXT PRIMARY KEY,
    name TEXT,
    imageUrl TEXT,
    price TEXT,
    rating REAL,
    CONSTRAINT res_id_name_imageUrl_price_rating_un
        UNIQUE (id, name, imageUrl, price, rating)
        ON CONFLICT IGNORE
);
CREATE TABLE IF NOT EXISTS ratings (
    teammateId TEXT REFERENCES teammates (id),
    restaurantId TEXT REFERENCES restaurants (id),
    rating TEXT,
    CONSTRAINT ratings_teammateId_restaurantId_un
        UNIQUE (teammateId, restaurantId)
        ON CONFLICT REPLACE
);
CREATE TABLE IF NOT EXISTS categories (
    restaurantId TEXT REFERENCES restaurants (id),
    alias TEXT,
    title TEXT,
    CONSTRAINT cat_restaurantId_alias_title_un
        UNIQUE (restaurantId, alias, title)
        ON CONFLICT IGNORE
);
