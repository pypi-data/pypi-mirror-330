# kule-ko
The billionth package for terminal colors!

## Basic Use
First, do 
```python
import kule_ko as k
```
to put the module in yor program.

To color text, it's as simple as calling a variable.
```python
print(f"{k.R}Hello world!{k.RESET})
```
This will cause the print to appear red.
There are some other functions too, probably.
```python
k.clear()
```
will clear the screen.

The list of color codes:
```python
B = Black text.
R = Red text.
G = Green text.
Y = Yellow text.
B = Blue text.
M = Magenta text.
C = Cyan text.
W = White text.
UNDERLINE = Underlines.
DOUBLE_UNDERLINE = Double underlines.
CURLY_UNDERLINE = Curly underlines.
BLINK = Blinks the text.
REVERSE = Reverses the text.
HIDDEN = Hides the text.
STRIKETHROUGH = Strikes the text through.
OVERLINE = Overlines the text.
BOLD = Bolds.
DIM = Dims.
ITALIC = Italicizes.
RESET = Resets the formatting.
```

This project's code will be released on Github soon!

## Changelog
1.0.0:
- Release!

1.0.1:
- Added more info to the README
- Added more info to the pyproject.toml (description)
- Added the MIT License

1.1.0:
- Actually made it so you can use the darn thing ☠️
- Rectified a mistake in the README (import as kule_ko, not kule-ko)