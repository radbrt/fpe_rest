# FFX encryption API

This is a test of an encryption api, using pyffx and flask. The application also contains a dictionary with definitions of the types of tokens that can be encrypted.

The container needs an environment variable, "FFXKEY", a string containing the encryption key.

## Usage

Build image: `docker build -t pyffx .`

Run image: `docker run -p 80:80 pyffx`
