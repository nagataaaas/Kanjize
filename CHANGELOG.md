# 1.6.1
- fix return type of (thanks to @yahiro-code)

# 1.6.0
- now uses `uv` for packaging
- significant performance improvement ( up to 8x faster )
- removed deprecated arguments `error`, `style` and `kanji_thousand` from `number2kanji` and `Number().to_kanji`

# 1.5.0

- more accurate error raising. (contributed by @ikedas)
- add `KanjizeConfiguration`
- add new style `FLAT`
- add new option `use_daiji`
- now `kanji2number` can parse number string with daiji.
- now you can choose '〇' as zero over '零' by setting `KanjiConfiguration(zero=KanjizeZero.SIGN)`

# 1.4.0

- support 0 for `kanji2number` and `number2kanji`

# 1.3.0

- Remove `kanji2int`
- Add `number2kanji` for compatibility with `number2kanji`

# v1.2.0

- Support negative value on `kanji2int` and `int2kanji`
- Added `kanji2number` and deprecated `kanji2int`

# v1.1.0

- Support float number

# v1.0.0

- Removed restrictions of maximum number. This now can handle number up to 10 ** 72 -1.

# v0.2.1

- Now this library can parse any kanji-number which has 千/百/十 in its inside.

# v0.2.0

- Changed algorithm to parse kanji
- fixed bug

# v0.1.0

- Added `Number` class.
- Added `style` argument to `kanji2int` and `int2kanji` that specifies style of formatting.
- Added `kanji_thousand` to `int2kanji` that specifies how thousand digits are kanjized.

# v0.0.2

- fixed bug Returns wrong answer in `kanji2int` when given number is greater than 10 ** 16

# v0.0.1

- Conception