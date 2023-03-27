# Twenty Four Seven (Four-in-One)
https://www.janestreet.com/puzzles/current-puzzle/

The first concept that comes to mind when seeing a problem like this one is **backtracking**. Backtracking consists of recursively and incrementally generating candidate solutions until we find a solution that satisfies our criteria, and then stopping the recursion.

## Reducing the search space

In writing a backtracking algorithm it's often useful to fail early. You should do your best to identify wrong solutions early on, so that you don't loose time exploring the branches of a wrong path.

To give an example of this, let's say we wanted to write the most naive brute force solution to solve a single board of Twenty Four Seven: generating all $8^{7\times7}$ board instances where each of the squares in the 7 by 7 board is either assigned a number from 1 to 7 or is left empty, and then checking whether each board is valid. This corresponds to a search space of approximately $1.78 \times 10^{44}$ boards, which some would say is big number. It would be virtually impossible to generate this many boards.

We can make our search space a lot smaller if we add some constraints that make our recursion fail earlier. For example, one of the rules is that there must not be more than one 1, two 2s, etc. in the board. If we stop recursing as soon as our current board has three 2s, we'll save time because there's no point in exploring that solution. With this restriction, our search space gets reduced to ${49 \choose 24} \frac{24!}{7!6!5!...1!}$, which is the number of ways to arrange one 1, two 2’s, etc., up to seven 7’s in a 7 by 7 board, or approximately $3.13 \times 10^{26}$. Still pretty big! But at least we're making some progress.

If we add the constraint that each of the 7 rows must have exactly 4 numbers we can stop recursing as soon as we complete a row that doesn't have 4 numbers. This decreases our search space even more, down to ${7 \choose 4}^7 \times \frac{24!}{7!6!5!...1!}$, or approximately $7.42 \times 10^{18}$. The more we add restrictions, the smaller is our search space, and the faster is our algorithm. You get the idea.

## Recursion

In our backtracking recursion we'll visit each cell sequentially (all cells in a row, and then all rows) as long as the board remains valid. In each cell visit we are going to:

1. Fill the cell with all values from 1 to 7 and recurse, if the cell is empty
2. Leave the cell empty and recurse
3. Leave the cell with the pre-set board value and recurse

After the recursion is done one level below and we return to the same call stack, we need to update the board to reflect the state it was in before the recursion.

In pseudocode:
```
def recurse(position):
	if is_board_invalid(position):
		return
	if position == end_of_board:
		print_board()
	if is_cell_blank(position):
		recurse(next(position))
		for value in {1,2,...,7}:
			if can_place_value_at_position(value, position)
				update_cell(value, position)
				recurse(next(position))
				erase_cell(position)
	elif valid_static(position):
		recurse(next(position))
```

When we reach the end of the board we'll print the board's state.

For this problem it's best to recurse separately on each of the 4 sub boards instead of the full board. If we were to recurse on the on all cells of the full board at once, we'd be exploring 5 extra columns for each row of the first sub board, which would make exploring each branch of the first sub board more expensive. So the best strategy is to solve the top left, then the top right, then the bottom left, and finally the bottom right sub board.

## Board representation

A good way to represent the board is with a 2 dimensional matrix of integers. An array of arrays in Python will do:
```
board = [["__" for j in range(12)] for i in range(12)]
```
For the numbers outside the board, which represent either the sum of a row/column or the first number visible from that cell, we can use four arrays:
```
outside_top = ["--"] * 12
outside_left = ["--"] * 12
outside_right = ["--"] * 12
outside_bottom = ["--"] * 12
```
We need to keep of track of the sum of each row and column. We can use an array for the rows of the two left sub boards, one for the rows of the two right sub boards, one for the columns of the two top sub boards and one of the columns of the two bottom sub boards. Every time a new value is written to a cell we add the value of the newly added cell to the corresponding array cells. Correspondingly, when the cell is erased we substract from the array cells.
```
left_row_sum = [0] * 12
right_row_sum = [0] * 12
top_column_sum = [0] * 12
bottom_column_sum = [0] * 12
```
And the count of numbers in each row and column. We increment or decrement the corresponding array by one each time a cell gets a new value or is erased:
```
left_row_count = [0] * 12
right_row_count = [0] * 12
top_column_count = [0] * 12
bottom_column_count = [0] * 12
```
We also need to keep track of how many numbers of each type are present in each sub board, i.e. how many 1s, how many 2s, etc. Instead of a dictionary we can just use an array for each sub board since the keys will all be from 1 to 7. If `square_top_left[7] == 2` that means there are 2 number sevens in the top left sub board.
```
square_top_left = [0] * (7+1)
square_top_right = [0] * (7+1)
square_bottom_left = [0] * (7+1)
square_bottom_right = [0] * (7+1)
```
Lastly we also need to keep track of the current closest element as seen from outside the board for a row or a column. For that we can use an arrays of stacks:
```
top_most_stack = [[12] for j in range(12)]
left_most_stack = [[12] for i in range(12)]
```
`top_most_stack[j][-1]` is the top of the `j`-th stack and contains the index of the element which has the highest position in the `j`-th column. We start by initializing all column stacks with a single element of value 12 (the index of the lowest position in a column in 11, so 12 means there are no elements in this column). As we read the starting values for the board and as we update the board during our recursion we'll also update the stack. The stack allows us to perform the three operations of appending, popping and peeking the top element all in constant `O(1)` time. This will be useful for making our `is_board_valid()` function efficient.

