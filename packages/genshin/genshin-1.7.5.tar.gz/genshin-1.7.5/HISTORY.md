# [1.7.5](https://github.com/thesadru/genshin.py/compare/v1.7.4..v1.7.5) - 2025-02-28

## Bug Fixes

- Fix ChallengeBangboo model not found - ([1507701](https://github.com/thesadru/genshin.py/commit/15077010b36974fb40b60792191f5158a9009b15))
- Ensure error code is included in message only if not already present - ([4e89a7a](https://github.com/thesadru/genshin.py/commit/4e89a7acf8f7c7573839c49098f026fbf0397e79))

## Continuous Integrations

- Add biweekly release - ([4988c5b](https://github.com/thesadru/genshin.py/commit/4988c5be16a2d673211acd089f820e4e0e18c0aa))
- Create venv before installing gitpython - ([e6e3aae](https://github.com/thesadru/genshin.py/commit/e6e3aaea7c537fd325fbd63f099ca2c3360eb9a9))
- Change how repo version is obtained - ([c884a96](https://github.com/thesadru/genshin.py/commit/c884a960833d489540d64eaf5318491839e9ae74))
- Fix git user credentials - ([922ab38](https://github.com/thesadru/genshin.py/commit/922ab38ee43aed80289541be3a644f90b9351a2e))
- Fix git user credentials again - ([9fb4c86](https://github.com/thesadru/genshin.py/commit/9fb4c86105625f0b7973063547acbeebb6123ef5))
- Oh come on just let me commit - ([1200b7c](https://github.com/thesadru/genshin.py/commit/1200b7ca36a1fb43837e39ddf0b4aad63260e345))
- Please work - ([4133002](https://github.com/thesadru/genshin.py/commit/4133002370a0980c58818eed8cdf57c15ff09a7f))
- Work? - ([4aad6bd](https://github.com/thesadru/genshin.py/commit/4aad6bd839651dcba3c3f20f8b8251e458b019fe))
- Merge release and publish workflows - ([d7abba6](https://github.com/thesadru/genshin.py/commit/d7abba6b39ec8b89aa08b89742edd65f5023b29d))

## Features

- Implement exponential backoff for ratelimit handling - ([046c08c](https://github.com/thesadru/genshin.py/commit/046c08ccfee76bb9d9cfce9ed3bd25869670d345))
- Add request timeout handling and update dependencies - ([0994963](https://github.com/thesadru/genshin.py/commit/0994963d255c16ca41f55080e82bf191f4079661))
- Add error code 1028 for VisitsTooFrequently - ([c0a96fb](https://github.com/thesadru/genshin.py/commit/c0a96fb67215fa2a27108341f3333a42b18daf23))
- Add get_accompany_characters method and accompanying models - ([0651875](https://github.com/thesadru/genshin.py/commit/0651875fae113afcd38e13792b46a575d150ca0e))
- Enhance get_accompany_characters method to accept optional language parameter - ([cdfa9a4](https://github.com/thesadru/genshin.py/commit/cdfa9a43df283edae598b8fdb4c80af0e5dcc565))
- Add accompany_character method - ([a791590](https://github.com/thesadru/genshin.py/commit/a7915907917c6ec4010b2fc456ed9908396f3e6e))

## Miscellaneous Chores

- Enable Renovate ([#236](https://github.com/thesadru/genshin.py/issues/236)) - ([61e87d0](https://github.com/thesadru/genshin.py/commit/61e87d0a7e197a014dc07aefb4304f662b5d6083))

## Refactoring

- Centralize weapon type mapping in CALCULATOR_WEAPON_TYPES - ([d30957b](https://github.com/thesadru/genshin.py/commit/d30957b86579bb1db30372499824b5e2ffc9f34c))
- Add type annotations for DS_SALT constant - ([45b2950](https://github.com/thesadru/genshin.py/commit/45b29508ca558e124fa237c62b77dd1878a6be29))

## Style

- Format code - ([297af66](https://github.com/thesadru/genshin.py/commit/297af6662c538fdcb01ced6d81fce5175b37c7f7))

## Tests

- Update banner type assertion to include new type 500 - ([5e3863a](https://github.com/thesadru/genshin.py/commit/5e3863a4bf1ff0fd52c9b217b2bd7d590c7a799d))
- Rename test_accompany_characters to test_get_accompany_characters for clarity - ([8f5de2d](https://github.com/thesadru/genshin.py/commit/8f5de2daeb8f8d1310ad28c705b8a1178f8c9fd9))

