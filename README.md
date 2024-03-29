# Pyramid

By Jonathan Chan (jonathanchan@u.northwestern.edu)

## Rules

[Pyramid][Pyramid] is a solitare card game of luck and strategy.

The goal is to clear the pyramid before you run out of cards. Only a handful of cards are shown on the pyramid. Within the shown cards, you must select pairs of them whose value add up to 13 (with A=1, J=11, Q=12, and K=13). Of course, this means that any K card can be taken away on its own immediately. When cards are cleared, they are taken away, and the cards underneath them are shown, if any.

But what if none of the cards on the pyramid can be paired? Then, you may draw a card from the deck, and see if that card can be paired with any on the pyramid. Once you draw a card, however, all of the previous cards that you drew cannot be used anymore (akin to a stack), unless you use that card up. So, draw wisely!

If you clear the pyramid before going through the deck, then you've won. Happy clearing!

## Running

Requires that Python 3.7 and pip are installed.

- `pip install -r requirements.txt`
- `./main` or `python3 main`

## Technical Notes

This application is written with Python 3.7 and uses a third party library called [blessed][Blessed] to create the TUI. I chose this stack because Python is fast to work with and the TUI library made the interface a lot more user-friendly. There are other TUI libraries and stacks, but I thought those were overkill. (In particular, I had considered using the unrelated blessed JavaScript library, but it came with many features I didn't need.)

The product was tested by hand on MacOS.

Data structures used in this program include a stack of undrawn cards, a stack of drawn cards, and a 2D list for the pyramid. The pyramid data structure implements a recursive linear search to determine which cards are hidden and which are not. The TUI draws ASCII art by calculating coordinates and re-rendering as needed when user interaction occurs.

[Blessed]: https://pypi.org/project/blessed/1.9.1/#description

[Pyramid]: https://en.wikipedia.org/wiki/Pyramid_(card_game)