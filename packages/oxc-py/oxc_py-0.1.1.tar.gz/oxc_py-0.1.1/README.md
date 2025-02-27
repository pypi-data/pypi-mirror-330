# oxc-py

Python bindings to the [oxc](https://github.com/oxc-project/oxc) [transformer](https://github.com/oxc-project/oxc/tree/main/crates/oxc_transformer).

## Usage

```py
from oxc_py import transform

jsx = """
import * as React from 'react'
import * as ReactDOM from 'react-dom'

ReactDOM.render(
    <h1>Hello, world!</h1>,
    document.getElementById('root')
);
"""

print(transform(jsx))
```

## Development

### Setup

```sh
uv venv
source .venv/bin/activate
uv sync --extra dev
```

### Test

```sh
uv run pytest
```

## Resources
- https://github.com/keller-mark/esbuild-py
- https://github.com/oxc-project/oxc/blob/71155cf575b6947bb0e85376d18375c2f3c50c73/crates/oxc_transformer/examples/transformer.rs
- https://docs.rs/oxc_transformer/0.53.0/oxc_transformer/
- https://www.maturin.rs/tutorial.html