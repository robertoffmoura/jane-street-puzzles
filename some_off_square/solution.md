The straighforward approach would be to consider all $(p_1, p_2)$ pairs of points inside the unit square, and integrate the probability that the circle fits inside the square for every pair.

$$
\begin{align}
    P(\text{fits}) &= \int_{[0,1]\times[0,1]}\int_{[0,1]\times[0,1]}P(\text{fits}|p_1,p_2)p(p_1,p_2)dp_1dp_2 \\
    &= \int_0^1\int_0^1\int_0^1\int_0^1P(\text{fits}|x_1,y_1,x_2,y_2)p(x_1,y_1,x_2,y_2)dx_1dy_1dx_2dy_2
\end{align}
$$

Where the density $p(x_1,y_1,x_2,y_2)$ is 1 because they're uniformly distributed and 

$$
P(\text{fits}|p_1,p_2) = \mathbb{1}\left\lbrace \text{center ± radius is inside } [0,1]^2 \right\rbrace
$$

$$
P(\text{fits}|x_1,y_1,x_2,y_2) = \mathbb{1}\lbrace \cap \left.
\begin{cases}
\frac{x_1 + x_2}{2} - \frac{\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}}{2} > 0\\
\frac{x_1 + x_2}{2} + \frac{\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}}{2} < 1\\
\frac{y_1 + y_2}{2} - \frac{\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}}{2} > 0\\
\frac{y_1 + y_2}{2} + \frac{\sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}}{2} < 1\\
\end{cases}
\right\rbrace \rbrace
$$

The integrand is not that straightforward so, instead of integrating over all pairs of points $(p_1,p_2)$, let's consider all pairs $(c, r)$ of circle center and radius (vector).  We'll use this conversion:

$$
\begin{align}
c &= \frac{p_1 + p_2}{2} \\
r &= \frac{p_1 - p_2}{2}
\end{align}
$$

The domain of integration for the center $c$ is easy, it's just the whole unit square: $[0,1]^2$. The domain for the radius is a bit trickier, because it will depend on the center.  

To simplify things and avoid making repeated calculations, let's divide the the unit square in 8 equal triangles and focus only on the one formed by the points $\{(0,0), (1/2,1/2), (1/2,0)\}$. In other words, $c_x <  1/2$ and $c_x > c_y$. Let's also only consider the vector radii in the first quadrant ($r_x < 0$ and $r_y < 0$). Under these conditions, and from the bounds of $p_1$ and $p_2$, we find that the domain for the radius is $[-c_x, 0]\times[-c_y, 0]$

This means that the probability density of a center $c$ is proportional to the product $c_x c_y$.

$$
p(c) = k c_x c_y
$$

This makes sense, since a center $c$ close to the corner of the square will have fewer radii than a center $c$ close to the center of the unit square. To find the constant of the probability density function of the center, we just need to remember that its integral over the whole domain must be 1.

$$
\begin{align}
    \int_0^\frac{1}{2}\int_0^x k x y dy dx &= 1\\
    k &= 2^7
\end{align}
$$

Now, given the center $c$, what is the probability that the radius $r$ will be such that the circle fits entirely inside the unit square? We just need the magnitude of $r$ to be smaller than the distance fron the center $c$ to the nearest wall of the unit square. In our smaller domain (the triangle $\{(0,0), (1/2,1/2), (1/2,0)\}$), this distance always corresponds to $c_y$.  

The radii that satisfy this property are inside a circle sector of area $\pi \frac{c_y^2}{4}$, while all radii are inside a rectangle of area $c_x c_y$. The probability is then

$$
P(\text{fits} | c) = \frac{\frac{\pi c_y^2}{4}}{c_x c_y}
$$

Now we have all the parts necessary to compute this integral

$$
\begin{align}
P(\text{fits}) &= \int P(\text{fits} | c) p(c) dc\\
        &= \int_0^\frac{1}{2}\int_0^x \frac{\frac{\pi y^2}{4}}{x y} (kxy) dy dx\\
        &= \frac{\pi}{6}
\end{align}
$$

Finally, the probability that the circle has a part that is off the square is

$$
P(\text{doesn't fit}) = 1 - P(\text{fits}) = 1 - \frac{\pi}{6}
$$

