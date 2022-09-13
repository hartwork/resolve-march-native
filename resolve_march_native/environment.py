# Copyright (C) 2022 Sebastian Pipping <sebastian@pipping.org>
# Licensed under GPL v2 or later

def enforce_c_locale(env: dict) -> None:
    env.update({
        'LC_ALL': 'C',
    })
    for key in ('LANG', 'LANGUAGE'):
        env.pop(key, None)
