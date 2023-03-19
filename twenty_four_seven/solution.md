# Twenty Four Seven (Four-in-One)
https://www.janestreet.com/puzzles/current-puzzle/

The first concept that comes to mind when seeing a problem like this one is **backtracking**. Backtracking consists of recursively and incrementally generating candidate solutions until we find a solution that satisfies our criteria, and then stopping the recursion.

## Reducing the search space

In writing a backtracking algorithm it's often useful to fail early. You should do your best to identify wrong solutions early on, so that you don't loose time exploring the branches of a wrong path.

To give an example of this, let's say we wanted to write the most naive brute force solution to solve a single board of Twenty Four Seven: generating all $8^{7\times7}$ board instances where each of the squares in the 7 by 7 board is either assigned a number from 1 to 7 or is left empty, and then checking whether each board is valid. This corresponds to a search space of approximately $1.78 \times 10^{44}$ boards, which some would say is big number.

We can make our search space a lot smaller if we add some constraints that make our recursion fail earlier. For example, one of the rules is that there must not be more than one 1, two 2s, etc. in the board. If we stop recursing as soon as our current board has three 2s, we'll save time because there's no point in exploring that solution. With this restriction, our search space gets reduced to ${49 \choose 24} \frac{24!}{7!6!5!...1!}$, which is the number of ways to arrange one 1, two 2’s, etc., up to seven 7’s in a 7 by 7 board, or approximately $3.13 \times 10^{26}$. Still pretty big! But at least we're making some progress.

If we add the constraint that each of the 7 rows must have exactly 4 numbers we can stop recursing as soon as we complete a row that doesn't have 4 numbers. This decreases our search space even more, down to ${7 \choose 4}^7 \times \frac{24!}{7!6!5!...1!}$, or approximately $7.42 \times 10^{18}$. The more we add restrictions, the smaller is our search space, and the faster is our algorithm. You get the idea.

