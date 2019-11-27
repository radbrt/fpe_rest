# FFX encryption API

This is a test of an encryption api, using pyffx and flask. The application also contains a dictionary with definitions of the types of tokens that can be encrypted.

The container needs an environment variable, "FFXKEY", a string containing the encryption key.

## Build & Run

Build image: `docker build -t pyffx .`

Run image: `docker run -p 80:80 -e FFXKEY='supersecretkey' pyffx`

## Usage

The API has two endpoints: `/encrypt` and `/bulkencrypt`. The encrypt endpoint accepts a list of objects (dictionaries with `tokentype` and `string` keys, where the tokentype must be defined in the dictionary, and the string is the string to be encrypted. This string can not contain characters outside the defined alphabet of the token type. The bulk encrypt endpoint accepts an object with a tokentype and a list of strings to be encrypted.

For examples, see the included postman collection.

***FOR DEMONSTRATION PURPOSES ONLY DO NOT USE IN PRODUCTION***
