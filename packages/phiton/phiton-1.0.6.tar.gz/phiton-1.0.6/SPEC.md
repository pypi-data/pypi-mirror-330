# Phiton specification

Phiton is a symbolic notation for Python that uses Unicode characters to represent Python syntax in a more concise form. It's designed to compress Python code while maintaining readability for those familiar with math or physics notation.

## 1. Phiton syntax (concise spec)

---

Phiton compresses Python into Unicode symbols. Control flow symbols (⇐ for return, ↥ for yield, ⟳ for while, ∀ for for, ⋔ for if, ⋮ for else, ⊘ for pass, ⊠ for break, ⋯ for continue), operators (≔ for =, ≡ for ==, ≠ for !=, ∈ for in, ∉ for not in, ∧ for and, ∨ for or, ¬ for not, ≤ for <=, ≥ for >=), special values (∅ for None, ⊤ for True, ⊥ for False), function definitions (ƒ for def, λ for lambda, Σ for class, ⊡ for async/await), block structure (⟨...⟩ for indented blocks, → for statement separator), common functions (ℓ for len, ℜ for range, ℯ for enumerate, φ for filter, ℤ for zip, ς for sorted, ℛ for reversed), domain prefixes (№ for numpy, ℗ for pandas, χ for sklearn, μ for matplotlib, Ψ for torch, Φ for tensorflow), and literals (#123 for numbers, $text for strings).

---

## 2. Phiton syntax (detailed spec)

### 2.1. Introduction

Phiton is a symbolic notation system that represents Python code using Unicode characters, designed to create more concise and visually distinctive code while maintaining readability for those familiar with the notation. It serves as both a compression format and an alternative syntax that can highlight the structural and functional aspects of Python code.

### 2.2. Rationale

The development of Phiton is motivated by several goals:

1. **Code Compression**: Reduce the physical size of Python source code while preserving its semantic meaning
2. **Visual Distinctiveness**: Make code patterns more immediately recognizable through unique symbols
3. **Semantic Clarity**: Use mathematical and logical symbols that closely match their programming concepts
4. **Pattern Recognition**: Standardize common Python idioms into concise symbolic patterns
5. **Domain-Specific Optimization**: Provide shorthand notation for common library operations
6. **Flexible Compression**: Support different levels of compression based on needs

### 2.3. Core Language Elements

#### 2.3.1. Control Flow

Control flow symbols are chosen to visually represent their function:

| Phiton | Python | Description | Rationale |
|--------|--------|-------------|-----------|
| `⇐` | `return` | Return statement | Arrow indicating value return |
| `↥` | `yield` | Yield statement | Upward arrow suggesting value generation |
| `↥⋮` | `yield from` | Yield from statement | Yield with continuation |
| `↑` | `raise` | Raise exception | Upward arrow for exception propagation |
| `⟳` | `while` | While loop | Circular arrow indicating repetition |
| `∀` | `for` | For loop | Universal quantifier from mathematics |
| `⋔` | `if` | If statement | Branch symbol suggesting condition |
| `⋮` | `else` | Else statement | Vertical dots indicating continuation |
| `⚟` | `try` | Try statement | Shield symbol for protection |
| `↦` | `match` | Match statement | Arrow indicating pattern matching |
| `≐` | `case` | Case statement | Similarity symbol for pattern cases |
| `⊪` | `assert` | Assert statement | Mathematical assertion symbol |
| `⊘` | `pass` | Pass statement | Empty set suggesting no operation |
| `⋯` | `continue` | Continue statement | Horizontal ellipsis for continuation |
| `⊠` | `break` | Break statement | Crossed box indicating stop |

#### 2.3.2. Operators and Assignments

Mathematical and logical symbols are used for operators:

| Phiton | Python | Description | Rationale |
|--------|--------|-------------|-----------|
| `≔` | `=` | Assignment | Mathematical definition symbol |
| `≡` | `==` | Equality | Triple bar for exact equality |
| `≠` | `!=` | Inequality | Standard mathematical inequality |
| `∈` | `in` | Membership test | Set membership symbol |
| `∉` | `not in` | Negative membership | Negated set membership |
| `∑` | `sum` | Sum function | Summation symbol |
| `∫` | `map` | Map function | Integration symbol suggesting transformation |
| `⨁` | `reduce` | Reduce function | Circle plus for accumulation |
| `△` | `+=` | Add and assign | Triangle suggesting increment |
| `▽` | `-=` | Subtract and assign | Inverted triangle for decrement |
| `◊` | `*=` | Multiply and assign | Diamond for multiplication |
| `◆` | `/=` | Divide and assign | Filled diamond for division |
| `≝` | `:=` | Walrus operator | Definition symbol |
| `≤` | `<=` | Less than or equal | Standard mathematical symbol |
| `≥` | `>=` | Greater than or equal | Standard mathematical symbol |
| `∧` | `and` | Logical AND | Logical conjunction symbol |
| `∨` | `or` | Logical OR | Logical disjunction symbol |
| `¬` | `not` | Logical NOT | Logical negation symbol |

#### 2.3.3. Special Values

Core Python values have distinct symbols:

| Phiton | Python | Description | Rationale |
|--------|--------|-------------|-----------|
| `∅` | `None` | None value | Empty set symbol |
| `⊤` | `True` | Boolean true | Top element symbol |
| `⊥` | `False` | Boolean false | Bottom element symbol |

#### 2.3.4. Functions and Classes

Object-oriented and functional programming constructs:

| Phiton | Python | Description | Rationale |
|--------|--------|-------------|-----------|
| `ƒ` | `def` | Function definition | Function symbol from mathematics |
| `λ` | `lambda` | Lambda function | Lambda calculus symbol |
| `Σ` | `class` | Class definition | Summation suggesting aggregation |
| `⊙` | `@property` | Property decorator | Circle dot for property access |
| `⊡` | `async`/`await` | Async/await | Square suggesting parallel execution |
| `⊞` | `@staticmethod` | Static method | Plus in box for standalone method |
| `⊟` | `@classmethod` | Class method | Minus in box for class binding |
| `⍟` | `@abstractmethod` | Abstract method | Star in circle for interface |
| `⛋` | `@dataclass` | Dataclass | Box suggesting data structure |

#### 2.3.5. Built-in Functions

Common Python built-ins have mathematical equivalents:

| Phiton | Python | Description | Rationale |
|--------|--------|-------------|-----------|
| `ℓ` | `len` | Length function | Script l for length |
| `ℜ` | `range` | Range function | Real numbers symbol |
| `ℯ` | `enumerate` | Enumerate function | Mathematical e |
| `φ` | `filter` | Filter function | Phi for filtering |
| `ℤ` | `zip` | Zip function | Integers symbol |
| `ς` | `sorted` | Sorted function | Sigma for sorting |
| `ℛ` | `reversed` | Reversed function | Script R |
| `∃` | `any` | Any function | Existential quantifier |
| `∀` | `all` | All function | Universal quantifier |
| `↓` | `min` | Min function | Down arrow for minimum |
| `↑` | `max` | Max function | Up arrow for maximum |
| `○` | `round` | Round function | Circle for rounding |
| `∥` | `abs` | Absolute value | Parallel lines |
| `^` | `pow` | Power function | Caret for exponentiation |

#### 2.3.6. Object Operations

Object manipulation symbols:

| Phiton | Python | Description | Rationale |
|--------|--------|-------------|-----------|
| `∋` | `isinstance` | Type check | Reverse membership |
| `∌` | `hasattr` | Attribute check | Negated membership |
| `⊳` | `getattr` | Get attribute | Right triangle |
| `⊲` | `setattr` | Set attribute | Left triangle |
| `⊗` | `delattr` | Delete attribute | Cross product |
| `↰` | `super` | Super function | Up-left arrow |
| `→` | `next` | Next function | Right arrow |
| `⟲` | `iter` | Iterator function | Circular arrow |
| `·` | `.` | Attribute access | Center dot |

#### 2.3.7. Block Structure

Code structure symbols:

| Phiton | Python | Description | Rationale |
|--------|--------|-------------|-----------|
| `⟨...⟩` | Indented block | Code block | Angle brackets |
| `→` | Newline | Statement separator | Right arrow |
| `⦂` | `:` | Type annotation | Double colon |

#### 2.3.8. Literals and Containers

Data structure notation:

| Phiton | Python | Description | Rationale |
|--------|--------|-------------|-----------|
| `#123` | `123` | Numeric literal | Hash prefix |
| `$text` | `"text"` | String literal | Dollar prefix |
| `⟦...⟧` | `{...}` | Dict/set comprehension | Double brackets |
| `⟬...⟭` | `[...]` | List comprehension | Mathematical brackets |
| `⦅...⦆` | `(...)` | Tuple | Parentheses |
| `⟮...⟯` | `(...)` | Grouping | Curved brackets |

#### 2.3.9. String Operations

String manipulation symbols:

| Phiton | Python | Description | Rationale |
|--------|--------|-------------|-----------|
| `⌿` | `strip` | Strip whitespace | Slash suggesting removal |
| `⇌` | `replace` | Replace substring | Reversing arrow |
| `⨍` | `format` | Format string | Function symbol |
| `「...」` | `f'...'` | F-string | Japanese quotes |

#### 2.3.10. Collection Operations

Collection manipulation:

| Phiton | Python | Description | Rationale |
|--------|--------|-------------|-----------|
| `⊕` | `append` | Append to list | Plus in circle |
| `⊖` | `pop` | Pop from list | Minus in circle |
| `⊚` | `values` | Dictionary values | Circle |
| `⊛` | `items` | Dictionary items | Star in circle |

### 2.4. Domain-Specific Prefixes

| Phiton | Python | Description |
|--------|--------|-------------|
| `№` | `numpy` | NumPy library |
| `℗` | `pandas` | Pandas library |
| `χ` | `sklearn` | Scikit-learn library |
| `μ` | `matplotlib` | Matplotlib library |
| `Ψ` | `torch` | PyTorch library |
| `Φ` | `tensorflow` | TensorFlow library |
| `φ` | `flask` | Flask library |
| `ɗ` | `django` | Django library |
| `ϱ` | `fastapi` | FastAPI library |
| `α` | `os` | OS library |
| `Ω` | `io` | IO library |
| `τ` | `typing` | Typing library |
| `Δ` | `math` | Math library |
| `Γ` | `collections` | Collections library |
| `Λ` | `itertools` | Itertools library |
| `Θ` | `datetime` | Datetime library |
| `ζ` | `sqlalchemy`/`zlib` | SQLAlchemy/zlib library |
| `η` | `requests` | Requests library |
| `ξ` | `json` | JSON library |
| `π` | `pathlib` | Pathlib library |
| `®` | `re` | Regex library |
| `γ` | `asyncio` | Asyncio library |
| `ϝ` | `functools` | Functools library |
| `ω` | `operator` | Operator library |
| `ρ` | `random` | Random library |
| `σ` | `string` | String library |
| `ψ` | `sys` | System library |
| `θ` | `time` | Time library |
| `υ` | `uuid` | UUID library |
| `ϒ` | `yaml` | YAML library |

### 2.5. Pattern Replacements

Phiton includes many pattern replacements for common Python idioms:

| Python Pattern | Phiton Equivalent |
|----------------|-------------------|
| `if x is not None` | `⋔x≠∅` |
| `if x is None` | `⋔x≡∅` |
| `for i in range(n)` | `∀i∈ℜ(n)` |
| `for i, x in enumerate(xs)` | `∀i,x∈ℯ(xs)` |
| `return [x for x in xs if p(x)]` | `⇐[x∀x∈xs⋔p(x)]` |
| `lambda x: f(x)` | `λx⇒f(x)` |
| `with open(f) as h` | `⊢⊣⊗(f)⇒h` |
| `try: x\nexcept E: y` | `⚟⟨x⟩⋔E⟨y⟩` |
| `if p: return x` | `⋔p⇐x` |
| `if not p: return` | `⋔¬p⇐` |
| `x if p else y` | `p?x:y` |
| `[f(x) for x in xs]` | `∫(f,xs)` |
| `sum(x for x in xs)` | `∑(xs)` |
| `all(p(x) for x in xs)` | `∀(p,xs)` |
| `any(p(x) for x in xs)` | `∃(p,xs)` |

### 2.6. Advanced Patterns

Phiton includes advanced pattern replacements for common Python idioms:

| Python Pattern | Phiton Equivalent |
|----------------|-------------------|
| `df.groupby(X).agg(Y)` | `§df·Γ(X)·A(Y)` |
| `np.array(X).reshape(Y)` | `№·A(X)·R(Y)` |
| `pd.DataFrame(X).reset_index()` | `℗·D(X)·R()` |
| `[x for x in X if C]` | `[x∀x∈X⋔C]` |
| `{k:v for k,v in X.items()}` | `{k:v∀k,v∈X·⊙}` |
| `list(map(F, X))` | `∫(F,X)` |
| `next(x for x in X if P)` | `→(x∀x∈X⋔P)` |
| `sorted(X, key=lambda x: x.Y)` | `ς(X,λx:x·Y)` |
| `if x is not None: return x\nelse: return y` | `⇐x≢∅?x:y` |
| `try:\n    x\nexcept E as e:\n    y` | `⚟⟨x⟩⋔E⇒e⟨y⟩` |
| `async with aiohttp.ClientSession() as session:` | `⊢⊣⊡η·S()⇒s⟨` |
| `await asyncio.gather(*tasks)` | `⊡γ·G(◇t)` |
| `'.'.join(x for x in X)` | `·⊕(X)` |
| `x.strip().lower()` | `x·⌿·↓` |
| `math.floor(x/y)` | `⌊x/y⌋` |
| `math.ceil(x/y)` | `⌈x/y⌉` |
| `abs(x-y)` | `∥x-y∥` |
| `math.sqrt(x)` | `√x` |
| `with open(X, 'r') as f:` | `⊢⊣⊗(X,'r')⇒f⟨` |
| `collections.defaultdict(list)` | `Γ·∂(ℓ)` |
| `assert x == y` | `⊪x≡y` |
| `raise ValueError(X)` | `↑V(X)` |
| `datetime.datetime.now()` | `Θ·N()` |

### 2.7. Compression Levels

Phiton supports different compression levels:

1. **Level 1**: Basic conversion with readable symbols and preserved structure
2. **Level 2**: More symbol substitutions but maintain readability
3. **Level 3**: Full symbol substitution with some structure preservation
4. **Level 4**: Aggressive symbol substitution and minimal structure
5. **Level 5**: Maximum compression with shortest possible representation

### 2.8. Conversion Process

#### 2.8.1. 6.1 Python to Phiton (`phitonize`)

1. Parse Python code into AST
2. Traverse AST and convert each node to Phiton notation
3. Apply pattern replacements for common idioms
4. Apply compression optimizations based on level
5. Generate symbol table for frequently used expressions
6. Optimize imports and structure

#### 2.8.2. 6.2 Phiton to Python (`dephitonize`)

1. Apply symbol replacements to convert Phiton to Python
2. Replace numeric and string literals
3. Fix function definitions and calls
4. Process blocks and indentation
5. Validate the decompressed Python code

### 2.9. Examples

#### 2.9.1. 7.1 Factorial Function

**Python:**
```python
def factorial(n):
    if n <= 1:
        return 1
    else:
        return n * factorial(n - 1)
```

**Phiton (Level 3):**
```
ƒfactorialn⟨⋔n≤#1⟨⇐#1⟩⋮⇐n*factorialn-#1⟩
```

#### 2.9.2. 7.2 List Comprehension

**Python:**
```python
[x * 2 for x in range(10) if x % 2 == 0]
```

**Phiton (Level 3):**
```
[x*#2∀x∈ℜ(#10)⋔x%#2≡#0]
```

#### 2.9.3. 7.3 Class Definition

**Python:**
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    def greet(self):
        return f"Hello, my name is {self.name}"
```

**Phiton (Level 3):**
```
ΣPerson⟨ƒ__init__self,name,age⟨self·name≔name→self·age≔age⟩→ƒgreetself⟨⇐「Hello, my name is {self·name}」⟩⟩
```

### 2.10. Implementation Notes

1. **AST-based Conversion**: Both phitonize and dephitonize use Python's AST for reliable code transformation
2. **Pattern Priority**: More specific patterns take precedence over general ones
3. **Symbol Table**: Frequently used expressions are cached in a symbol table
4. **Scope Awareness**: Symbol substitutions respect Python scoping rules
5. **Validation**: Generated code is validated through AST parsing
6. **Error Handling**: Conversion errors provide detailed feedback
7. **Compression Optimization**: Advanced compression uses frequency analysis

### 2.11. Best Practices

1. Use compression level 1-2 for code that needs to be read frequently
2. Use level 3 for a balance of readability and compression
3. Reserve levels 4-5 for maximum compression when readability is less important
4. Document the compression level used in project metadata
5. Maintain a style guide for consistent Phiton usage in projects
6. Consider using syntax highlighting for Phiton code
7. Include original Python code in comments for complex transformations
