from collections.abc import Generator
from itertools import groupby, product
from pathlib import Path

import click
import PIL.Image
from PIL.Image import Image
import PIL.ImageDraw


type P = tuple[int, int]


def expanding_range(max_size: int) -> Generator[tuple[int, int], None, None]:
    """Produces all x, y values in a square of the given size ordered by Chebyshev
    distance to the point (0, 0).

    First, return points `p` for which `max(p) == 0`, then points for which
    `max(p) == 1`, then points for which `max(p) == 2`, etc.

    Example:
    >>> list(expanding_range(0))
    [(0, 0)]
    >>> list(expanding_range(1))
    [(0, 0), (1, 0), (1, 1), (0, 1)]
    >>> list(expanding_range(2))
    [(0, 0), (1, 0), (1, 1), (0, 1), (2, 0), (2, 1), (2, 2), (0, 2), (1, 2)]
    """
    for size in range(max_size + 1):
        for y in range(size + 1):
            yield (size, y)
        for x in range(size):
            yield (x, size)


def is_black(c: None | float | int | tuple[int, ...]) -> bool:
    """Is this colour essentially black?"""
    if c is None:
        return False
    if isinstance(c, float):
        return c <= 15 / 255
    if isinstance(c, int):
        return c <= 15
    # Ignore the alpha channel.
    return all(channel <= 15 for channel in c[:3])


def expand_grid(img: Image, tl: P) -> tuple[P, P, P, P]:
    """Expand the grid in the image with the given top-left corner.

    Returns the 4 corners of the grid found, starting at the top-left and going
    clockwise.
    """
    width, height = img.size
    x, y = tl
    nx = x
    while nx < width and is_black(img.getpixel((nx, y))):
        nx += 1
    nx -= 1
    ny = y
    while ny < height and is_black(img.getpixel((x, ny))):
        ny += 1
    ny -= 1
    # (x, y) is the top-left corner, (nx, y) is the top-right,
    # (x, ny) is the bottom-left, and (nx, ny) SHOULD be the bottom-right.
    if not is_black(img.getpixel((nx, ny))):
        return (tl, tl, tl, tl)  # Grid of size 0.

    # Ensure the edges are also there and valid.
    for _x in range(x, nx + 1):
        if not is_black(img.getpixel((_x, ny))):
            return (tl, tl, tl, tl)
    for _y in range(y, ny + 1):
        if not is_black(img.getpixel((nx, _y))):
            return (tl, tl, tl, tl)

    return (
        (x, y),  # top-left
        (nx, y),  # top-right
        (nx, ny),  # bottom-right
        (x, ny),  # bottom-left
    )


def check_grid_size(tl: P, br: P) -> bool:
    """Does the grid look approximately square of a large enough size?

    We don't check for an exact square because the border of the puzzle has some width
    and we need to account for a small error from the possibility that we didn't capture
    the exterior part of the border.
    """
    x1, y1 = tl
    x2, y2 = br
    width = abs(x1 - x2)
    height = abs(y1 - y2)
    return width >= 50 and height >= 50 and width * 0.95 <= height <= width * 1.05


def compute_grid_n(img: Image, tl: P, br: P) -> int:
    """Find how many cells the grid contains."""
    # Find a point that is not black.
    x1, y1 = tl
    x2, y2 = br
    width, height = abs(x2 - x1), abs(y2 - y1)
    size = min(width, height)
    delta = 0
    while delta < size:
        if not is_black(img.getpixel((x1 + delta, y1 + delta))):
            break
        delta += 1
    else:  # If we left the grid without finding a non-black pixel, error.
        raise RuntimeError("Can't find a non-black pixel in the grid!")

    # To count the number of cells along each direction we slice the image, determine
    # whether each pixel in the slice is black or not, and then use `groupby` to group
    # together sequences of black or non-black pixels.
    vertical_n = sum(
        not black  # The cells are groups that were not black.
        for black, _ in groupby(
            is_black(img.getpixel((x1 + delta, y))) for y in range(y1, y2 + 1)
        )
    )
    horizontal_n = sum(
        not black
        for black, _ in groupby(
            is_black(img.getpixel((x, y1 + delta))) for x in range(x1, x2 + 1)
        )
    )

    if vertical_n != horizontal_n:
        raise RuntimeError(f"{vertical_n = }, {horizontal_n = }")
    return vertical_n


def calibrate(img: Image) -> tuple[P, P]:
    """Find the grid in the puzzle image.

    Returns the top-left and bottom-right corners of the image."""
    width, height = img.size
    # Look for the top-left corner of the grid.
    for x, y in expanding_range(min(width, height) - 1):
        c = img.getpixel((x, y))
        if is_black(c):  # Is this the top-left corner of the grid?
            tl, _, br, _ = expand_grid(img, (x, y))
            if check_grid_size(tl, br):
                return tl, br

    raise RuntimeError("Can't find grid.")


def compute_cell_locations(tl: P, br: P, n: int) -> dict[tuple[int, int], P]:
    """Compute the (approximate) centres of the grid cells."""
    left, top = tl
    dx = (br[0] - tl[0]) // n
    dy = (br[1] - tl[1]) // n
    cells = {
        (x, y): (
            left + x * dx + dx // 2,
            top + y * dy + dy // 2,
        )  # Corner + previous cells + centre offset
        for x, y in product(range(n), repeat=2)
    }
    return cells


def solve(group_sets: list[set[tuple[int, int]]]) -> list[tuple[int, int]] | None:
    """Recursive auxiliary function that brute-forces the solution.

    This function takes the first coloured group and tries to place a queen on each
    position of that group, then removes all positions from the following groups that
    would clash with this queen, and then tries to solve the remainder of the puzzle
    recursively by ignoring the first coloured group.

    If we reach an impossible position, the function returns None to indicate failure.
    Upon success, the function returns a list of all the positions where queens must go.
    """
    if not group_sets:
        return []

    # Try to put the next queen at all positions of the next group.
    for tx, ty in group_sets[0]:
        new_group_sets: list[set[tuple[int, int]]] = [
            {
                (x, y)
                for x, y in gs
                if (
                    x != tx  # Can't be in the same column.
                    and y != ty  # Can't be in the same row.
                    and abs(x - tx) + abs(y - ty) > 2  # Can't touch diagonally.
                )
            }
            for gs in group_sets[1:]
        ]
        if not all(new_group_sets):  # 1+ empty group sets, skip this attempt.
            continue

        result = solve(new_group_sets)
        if result is not None:
            return [(tx, ty)] + result


def draw_solutions(
    img: Image, solution: list[tuple[int, int]], tl: P, cell_size: int
) -> None:
    """Draw the queens as black circles on the image."""
    drawable = PIL.ImageDraw.Draw(img)
    radius = cell_size // 3

    left, top = tl

    for x, y in solution:
        px = left + cell_size * x + cell_size // 2
        py = top + cell_size * y + cell_size // 2
        drawable.ellipse(
            [px - radius, py - radius, px + radius, py + radius], fill="black"
        )


def solve_puzzle_image(filename: Path) -> None:
    img = PIL.Image.open(filename)
    tl, br = calibrate(img)
    print(f"Found grid corners at {tl} and {br}.")
    n = compute_grid_n(img, tl, br)
    print(f"Grid is {n} x {n}.")

    cell_locations = compute_cell_locations(tl, br, n)
    cell_colours = {
        board_coords: img.getpixel(img_coords)
        for board_coords, img_coords in cell_locations.items()
    }

    unique_colours = list(set(cell_colours.values()))
    if (n_colours := len(unique_colours)) != n:
        raise RuntimeError(f"Found {n_colours} colours, expected {n}.")

    colour_groups = [
        {coords for coords, colour in cell_colours.items() if colour == current_colour}
        for current_colour in unique_colours
    ]

    solution = solve(colour_groups)
    if solution is None:
        raise RuntimeError("Couldn't find solution!")
    print("Found solution. Generating image.")

    cell_size = (br[0] - tl[0]) // n
    draw_solutions(img, solution, tl, cell_size)
    solved_filename = filename.with_stem(filename.stem + "_solved")
    img.save(solved_filename)
    print("Solution saved.")


@click.command()
@click.argument(
    "puzzle_path", type=click.Path(exists=True, readable=True, path_type=Path)
)
def main(puzzle_path: Path) -> None:
    solve_puzzle_image(puzzle_path)


if __name__ == "__main__":
    main()
