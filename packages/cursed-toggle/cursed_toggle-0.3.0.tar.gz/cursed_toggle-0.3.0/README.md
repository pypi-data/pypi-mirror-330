# cursed-toggle
This library is intended to implement a toggle function for Boolean values in a very bad or even the worst and most unmaintainable way, following the KISS ("Keep it sophisticated, specialist!") principle.

# Preamble
The variable `b` can be True (1) or False (0). One of the most basic implementation to get a toggle is
```
f(b) = not b
```

But this is way too simple and efficient and something cooler looking might be
```
f(b) = b^1
```

A trivial linear function is also possible
```
f(b) = 1 - b
```

and this sounds like a good start.

# The complication
## Initception
Only 1 `__init__` file is too straight forward. Why not add another 3 instead? We can start by naming them properly
- `__init_1__.py`: The list of the init files starts with 1...
- `__init_b__.py`: ...and continues with b...
- `__init_Ω__.py`: ...and ends with an Omega (Ω) (Wow, this even makes sense, pathetic!)

Well... So... Ahm... Basically `__init__.py` imports from `__init_Ω__.py`[^1], which imports from `__init_1__.py`, which imports from `__init_b__.py`, which imports the cursed_toggle.

[^1]: Note from the author: I am not sure whether I should be impressed or frightened, especially when `__init__.py` in Spyder looks like that `from .__init_Î©__ [...]`.

TODO: rename `__init_1__.py` to `1)__init__.py` and make it somehow work. Maybe with importlib?

## SSOT / SPOT
In common enterprise IT, several sources of truth (SSOT) or several points of truth (SPOT) is a typical architecture. Since this repo should be enterprise grade, there is no chance not to implement something like that. That is why
- `cursed_toggle_v1_deprecated.py` and
- `cursed_toggle_v2.py` and
- `cursed_toggle_just_a_temp_little_experiment.py` and
- `cursed_toggle_high_school.py` (WARNING: explicit sexual content) and
- `cursed_toggle_todo.py`

exist. When using the cursed_toggle library, it is randomly choosen which cursed_toggle function will be used. Even if this looks a bit stupid, it is very important that all possible imports work. That's why there is proper testing. Further, only a fool thinks, that v1 is no longer beeing developed.

When accidentally - yes "accidentally" - a new `cursed_toggle....py` is created, make sure to implement this new implementation. Just add the possibility for the import to `__init_b__.py`. Just follow the scheme, it is self-explanatory. ALSO DONT FORGET THE README!

## Testing
All `cursed_toggle....py` must be tested. If a new `cursed_toggle....py` is created, don't forget the to test it.
1) Copy a test file from tests/. But don't choose `test.py`, copy another file.
1) Rename the copied file that one can associate it with its corresponding `cursed_toggle....py` file.
1) Change the line for the env variable `SECRET_ENV_FOR_TESTING_ONLY_DO_NOT_USE` so that it fits to the `__init_b__.py`. This is self-explanatory.
1) Add the test to ci.yml. This is self-explanatory.

With this method, when the overall tests change, one have to copy and paste these changes to all test files. This complies with Copy-and-paste programming philosophy.

## Midamble
Not even sure whether this is a word. Anyway, after each modification, there should be a $\LaTeX$-like representation of the "math" and after, the correspdoning python syntax (needed for testing this readme).

## The toggle function
The start function looks too negative and too simple. Let's make it positve and more complex, because $i^2 = -1$

$$ f(b) = 1 + i^2 \cdot b $$
```
f(b) = 1 + 1j**2 * b
```

The single lonely 1 in the beginning is also a bit boring. And since $e^{i\pi} + 1 = 0$, we know what to do.

$$ f(b) = -e^{i\pi} + i^2 \cdot b $$
```
f(b) = -(math.e**(1j * math.pi)).real + 1j**2 * b
```

Square 2. Two. 2 is 2 lame. Shifting 1234567 19 times to the right is also two. So, we will rightshift it 13 and 6 times.

$$ f(b) = -e^{i\pi} + i^{1234567 >> 13 >> 6} \cdot b $$
```
f(b) = -(math.e**(1j * math.pi)).real + 1j**(1234567 >> 13 >> 6) * b
```

$3! = 6$, so let's get rid of the 6.

$$ f(b) = -e^{i\pi} + i^{1234567 >> 13 >> 3!} \cdot b $$
```
f(b) = -(math.e**(1j * math.pi)).real + 1j**(1234567 >> 13 >> math.factorial(3)) * b
```

During my research, I stumbled across the DRY-principle, that means "Do repeat yourself" or "duplication is excellent". Here we go with the Euler's idendity. For the 3. Three. Times.

$$ f(b) = -e^{i\pi} + i^{1234567 >> 13 >> \left(-e^{i\pi} - e^{i\pi} - e^{i\pi}\right)!} \cdot b $$
```
f(b) = -(math.e**(1j * math.pi)).real + 1j**(1234567 >> 13 >> math.factorial(int((-math.e**(1j * math.pi) - math.e**(1j * math.pi) - math.e**(1j * math.pi)).real))) * b
```

### Time inindependence
No, this is not a typo. The function is already time independent, because it does not use any time. We could add something that is based on a time, so we make it time dependent, but this is bad... Like, why should this function just work on a defined time. So we should use the time but make it stable about it. And since the name time independent is already taken (for this case), we make it time inindependent. So it depends on the time but it doesn't matter.

Let's start with a randomly guessed function of third order

$$ f_1(t) = -24 \cdot t^3 + 432 \cdot t^2 - 2568 \cdot t + 5053 $$

Surprisingly, $f_1(5) = f_1(6) = f_1(7) = 13$. So we just need something that results in 5, 6 or 7 and needs the time. What about `int(time.time()) % 3 + 5`? YEEEP, that's it- stupid simple.

So, `13` becomes (with $t$ as the current unix time as int, or more like $t$ can be any int)

$$ 13(t) = -24 \cdot (t \mod 3+5)^3 + 432 \cdot (t \mod 3+5)^2 - 2568 \cdot (t \mod 3+5) + 5053 $$

and the function of interest turns into

$$ f(b,t) = -e^{i\pi} + i^{1234567 >> -24 \cdot (t \mod 3+5)^3 + 432 \cdot (t \mod 3+5)^2 - 2568 \cdot (t \mod 3+5) + 5053 >> \left(-e^{i\pi} - e^{i\pi} - e^{i\pi}\right)!} \cdot b $$
```
f(b) = -(math.e**(1j * math.pi)).real + 1j**(1234567 >> -24*(t % 3+5)**3 + 432*(t % 3+5)**2 - 2568*(t % 3+5) + 5053 >> math.factorial(int((-math.e**(1j * math.pi) - math.e**(1j * math.pi) - math.e**(1j * math.pi)).real))) * b
```

### Docstring dependence
The number `1234567` can be calculated as $3487 \cdot 354 + 169$. What a luck that the docstring of `_cursed_toggle` is 354 chars long. Easy substitution (with $d$ as length of the docstring of `_cursed_toggle`):

$$ f(b,t,d_{354}) = -e^{i\pi} + i^{3487 \cdot d + 169 >> -24 \cdot (t \mod 3+5)^3 + 432 \cdot (t \mod 3+5)^2 - 2568 \cdot (t \mod 3+5) + 5053 >> \left(-e^{i\pi} - e^{i\pi} - e^{i\pi}\right)!} \cdot b $$
```
f(b) = -(math.e**(1j * math.pi)).real + 1j**(3487 * len(_cursed_toggle.__doc__.__str__()) + 169 >> -24*(t % 3+5)**3 + 432*(t % 3+5)**2 - 2568*(t % 3+5) + 5053 >> math.factorial(int((-math.e**(1j * math.pi) - math.e**(1j * math.pi) - math.e**(1j * math.pi)).real))) * b
```

*The `.__str__()` in `cursed_toggle.__doc__.__str__()` is to satisfy mypy.*
