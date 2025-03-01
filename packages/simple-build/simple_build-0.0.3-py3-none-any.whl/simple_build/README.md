# Package builder

The builder is based in <https://github.com/chrisjsewell/pymonorepo>,
and with some hooks added to allow for modifying files, before they are written to the wheel.

We roll our own builder to obfuscate the source code when packaging it,
in order to make it harder for others to copy our work.
