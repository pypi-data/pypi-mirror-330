# Lazy Evaluation

Lazy evaluation is a programming technique where values are computed only when they are needed, rather than being calculated in advance. This approach offers significant benefits, particularly in terms of efficiency, as it avoids unnecessary computations for values that are never utilized.

One of the most intriguing aspects of lazy evaluation is its ability to support infinite data structures. These data structures can theoretically expand infinitely, but in practice, they remain manageable because only the necessary elements are computed as they are accessed. This means that while the data structure may be conceptually infinite, it does not consume infinite resources.

Despite its advantages, lazy evaluation is not widely adopted in mainstream programming languages. Most languages follow a strictly evaluated approach, where values are computed eagerly, even if they may never be used. However, functional programming languages like OCaml embrace lazy evaluation as a core feature, enabling developers to leverage its benefits for certain use cases.

## Reference video

[Lazy Evaluation by Philipp Hagenlocher](https://www.youtube.com/watch?v=KniIeHiEzdo "Lazy Evaluation in Python")

