Solving Rastrigin
=================
In this sub folder I've used (1, $\lambda$) strategy combined with Self Adaptation
to maximize the [Rastrigin function](https://en.wikipedia.org/wiki/Rastrigin_function) namely:

$f(\mathbf {x} )=-(An+\sum _{i=1}^{n}\left[x_{i}^{2}-A\cos(2\pi x_{i})\right])$

Results
-------

Fixing $\lambda = 1000$ in 1000 epocs the optimization algorithm gets extremely close to the global maxium.
The y axis is in a logarithmic scale so to avoid errors I am plotting the negative of the rastrigin function.
![Rastrigin optimization iterations](https://user-images.githubusercontent.com/25415885/197713675-3fa7015d-3ab3-47ba-b738-82854e7151a4.png)


