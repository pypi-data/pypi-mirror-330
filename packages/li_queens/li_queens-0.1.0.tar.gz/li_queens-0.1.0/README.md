# LinkedIn Queens solver

[Read this blog post](https://mathspp.com/blog/beating-linkedin-queens-with-python) to learn about how this program works.

The CLI provided needs an image of a puzzle, like `puzzle.png` shown here:

![](puzzle.png)

It will then produce a second image `puzzle_solved.png` with the solution:

![](puzzle_solved.png)


## Running with uv

If you're using uv, you can run this CLI with

```bash
uvx --from li_queens queens puzzle.png
```

The argument `puzzle.png` should be a path to an image containing a LinkedIn Queens-like puzzle.
