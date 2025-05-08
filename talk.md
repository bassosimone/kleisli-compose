# Wait, it's all monads? Always has been!

> How I accidentally implemented monadic composition in Python.

**TL;DR** We’ll build a monad from scratch in Python using
website measurements and exceptions. By the end, we’ll show
how systems like Bash and GitHub workflows exhibit monadic
behavior—even if they don’t use the word.

## Introduction: Explaining Monads at Gunpoint

![Friendly reminder: never lie at gunpoint!](docs/meme.png
"Friendly reminder: never lie at gunpoint!")


The year is 2030. You're walking through a dark alley. Out
of nowhere, a sketchoid approaches, points a gun at you,
and mumbles:

> "Explain monads to me. Now. Or die."

My goal today is to increase your chances of survival. This
talk is your escape hatch. More seriously, our objective here
is to understand monads and monadic composition in Python.

## What is a Monad?

As GPT-4o eloquently puts it:

> "A monad is a way of sequencing computations where each step
may fail or produce effects, while keeping the plumbing out
of your core logic."

Let's make this definition intuitive, real, and practical.

Think of a monad as an astral prism. What happens inside the
prism stays inside the prism. The outside world remains unaffected.

![My iPhone's auto-correct likes to change monadi with monaci 😅](docs/monks.png
"My iPhone's auto-correct likes to change monadi with monaci 😅")

We'll use the 💎 symbol to represent a monadic context.

Consider this equation, where `[` and `]` brackets represent "that
which is inside the prism":

```python
💎[x / y] := 💎[x] / 💎[y]
```

If you divide by zero in ordinary Python, you get an immediate
`ZeroDivisionError`. With a monad, you won't get an error until
you try to extract the result from the monad.

## Formal Definition (Haskell-Style)

We're using a simplified version of Haskell notation based
on [Kleisli category](https://en.wikipedia.org/wiki/Kleisli_category).

A type `💎` is a monad if:

1. There is a "constructor" operation to put something inside the monad:

```haskell
💎 :: a -> 💎 a
```

The `::` reads as "has type". The `->` is a function that takes in
input the type on its left and returns the type on its right.

2. There is a "composition" operation for functions that operate on monads:

```haskell
f :: a -> 💎 b
g :: b -> 💎 c
f 🐡 g :: a -> 💎 c
```

The `🐡` symbol denotes composition (in Haskell, this is `>=>` or "fish").

## Case Study: Website Measurement

Let's illustrate incrementally building monads using a real-world example.

We aim to measure the reachability of websites. This is perfect for
demonstrating monads because of the inherent possibility of failure at
multiple stages. As such, it allows us to manually construct and
illustrate the behaviour of the [Result type](
https://doc.rust-lang.org/std/result/).

If you don't know much about how the internet works, don't worry. Just
take as postulate that we can measure a website by its domain name. Also,
keep in mind that accessing a website is a two step process:

1. DNS lookup: Convert a domain name to an IP address.
2. Web fetch: Download a webpage using an IP address.

We can model these operations using:

```python
def dns(domain: str) -> IpAddr: ...
def fetch(addr: IpAddr) -> WebPage: ...
```

Examples:

```
>>> dns("www.example.com")
IpAddr("130.192.91.211")

>>> dns("www.instagram.com")
Traceback (most recent call last):
  ...
    raise DNSError("no such host")
DNSError("no such host")

>>> fetch(IpAddr("130.192.91.211"))
WebPage("Hello world!")

>>> fetch(IpAddr("130.192.91.231"))
Traceback (most recent call last):
  ...
    raise FetchError("connection reset by peer")
FetchError("connection reset by peer")
```

As you can see, both operations can fail and succeed.

The corresponding code is in [mocks.py](kleisli_compose/mocks.py).

## How to Accidentally Build a Monad

We will start with a simple solution to the problem and
increasingly refactor it to make it monadic.

### Step 0: The Naive Approach

```python
def measure(domain: str) -> WebPage:
    return fetch(dns(domain))

def measure_list(domains: List[str]) -> List[WebPage]:
    result = []
    for domain in domains:
        result.append(measure(domain))
    return result
```

Problem: Any exception breaks our entire flow:

```
>>> measure_list(["www.example.com", "www.instagram.com", "www.kernel.org"])
Traceback (most recent call last):
  ...
    raise DNSError("no such host")
DNSError("no such host")
```

The corresponding code is in [base.py](kleisli_compose/base.py).

### Step 1: Add Try/Catch

```python
def measure_list(domains: List[str]) -> List[WebPage]:
    result = []
    for domain in domains:
        try:
            result.append(measure(domain))
        except Exception:
            pass  # ignore the exception
    return result
```

Problem: We lose information about failures:

```
>>> measure_list(["www.example.com", "www.instagram.com", "www.kernel.org"])
[WebPage("Hello world!"), WebPage("Hello kernel!")]
```

The corresponding code is in [catcher.py](kleisli_compose/catcher.py).

### Step 2: Return Success or Exception

```python
def measure_list(domains: list[str]) -> list[WebPage | Exception]:
    result = []
    for domain in domains:
        try:
            result.append(measure(domain))
        except Exception as e:
            result.append(e)
    return result
```

The corresponding code is in [bettercatcher.py](kleisli_compose/bettercatcher.py).

Now we're approaching a monad: `💎 T = T | Exception` is equivalent to the
[Result type](https://doc.rust-lang.org/std/result/) in Rust.

Accordingly, we now get a result for each domain:

```
>>> measure_list(["www.example.com", "www.instagram.com", "www.kernel.org"])
[WebPage("Hello world!"), DNSError("no such host"), WebPage("Hello kernel!")]
```

But we're still mixing computation structure with error handling.

### Step 3: Move Try/Catch Down

```python
def measure(domain: str) -> WebPage | Exception:
    try:
        return fetch(dns(domain))
    except Exception as exc:
        return exc

def measure_list(domains: list[str]) -> list[WebPage | Exception]:
    result = []
    for domain in domains:
        result.append(measure(domain))
    return result
```

The `measure_list` function is now clearer, but the error handling logic
is still mixed with the computation inside `measure`.

### Step 4: Wrap Primitives

```python
def dnsx(domain: str) -> IpAddr | Exception:
    try:
        return dns(domain)
    except Exception as exc:
        return exc

def fetchxy(addr: IpAddr) -> WebPage | Exception:
    try:
        return fetch(addr)
    except Exception as exc:
        return exc

def fetchx(addr: IpAddr | Exception) -> WebPage | Exception:
    if isinstance(addr, Exception):
        return addr
    return fetchxy(addr)

def measure(domain: str) -> WebPage | Exception:
    return fetchx(dnsx(domain))
```

The corresponding code is in [landing.py](kleisli_compose/landing.py).

Now we've fully separated the error handling from the computation flow.

The only unclean part is `fetchx`, which glues together the two
functions `dnsx` and `fetchxy`. We will fix this by replacing the
`fetchx` function with the monadic composition operator, `🐡`.

### Step 5: Implement Monadic Composition

```python
class Compose[A, B, C]:
    """Implements monadic function composition."""

    def __init__(
        self,
        fx: Callable[[A], B | Exception],
        gx: Callable[[B], C | Exception],
    ):
        self.fx, self.gx = fx, gx

    def __call__(self, a: A) -> C | Exception:
        rv = self.fx(a)
        if isinstance(rv, Exception):
            return rv
        return self.gx(rv)
```

This is our `🐡` operator! Now we can compose functions cleanly:

```python
def measure(domain: str) -> WebPage | Exception:
    return Compose(dnsx, fetchxy)(domain)
```

The corresponding code is in [full.py](kleisli_compose/full.py).

### Step 6: Syntactic Pipelines

```python
class Func[A, B]:
    """Generic monad-aware function."""

    def __init__(self, fx: Callable[[A], B | Exception]):
        self.fx = fx

    def __call__(self, a: A) -> B | Exception:
        return self.fx(a)

    def __or__[C](self, other: Func[B, C]) -> Func[A, C]:
        return Func(Compose(self.fx, other.fx))

dns_func = Func(dnsx)
fetch_func = Func(fetchxy)
```

This class overrides `__or__` to allow chaining functions
with the `|` operator, so we can write:

```python
def measure_list(domains: list[str]) -> list[WebPage | Exception]:
    return list(map(dns_func | fetch_func, domains))
```

This gets us as close to `f 🐡 g` as Python reasonably allows.

## Real-World Monads

Monad-like design patterns are everywhere, even if not named as such:

### GitHub Workflows

* Jobs depend on each other
* Output of one becomes input to the next
* Failure is isolated and propagated

### Bash Pipelines

* `|` chains commands: monadic composition
* Failures propagate through the pipeline

## Final Reflection

So, what’s a monad (in this context)? It’s a structure that lets you
chain operations that might fail, without having to constantly
check for failure. You just describe what you want to do—one step
at a time—and the monad handles the shock.

We aim to build robust systems by accepting failure as part of the computation.

Monads let us express complex behavior with simple, composable
structures. They isolate the messy parts—errors, side effects—while
keeping our core logic clean.

Is this fun? Maybe the point of engineering (as opposed to just
hacking) is not to make things fun, but to make them robust. This
frees up time, hopefully, to play more computer games.

I want to conclude by quoting [Joy Division's Disorder](
https://www.youtube.com/watch?v=fhCLalLXHP4):

```
I've got the spirit
I've lost the feeling
Take the shock away
```

That's what monads are for.

Thank you!
