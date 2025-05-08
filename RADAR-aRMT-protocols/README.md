# Protocols

Each directory is analogous to a RADAR project in the Management Portal, where a specific protocol applies.

The documentation on the protocol structure can be found on <https://radar-base.github.io/RADAR-aRMT-protocols/>.

More documentation to come.

## Protocol validation

The protocol format is described by a JSON Schema, in docs/protocol-schema.json. The current version of the format is 0.0.2. All protocols in this repository should follow that schema. A technical way to achieve this, is by JSON Schema validation.

Protocol validation requires Bash and [Yarn](https://yarnpkg.com/lang/en/docs/install). To validate the protocols in this directory, run
```shell
./validate
```

