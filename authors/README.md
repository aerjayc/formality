#### Notes:
- `twain.txt` uses a weird unicode character not recognized by our parser, so we replaced it all with double quotes `"`.
- chapter/preface/etc. indicators removed on both texts.
- treat {';', '--'} as '.'
- if no. words in sentence > 21, break at the nearest punctuation in {',', ';', }
- remove underscores