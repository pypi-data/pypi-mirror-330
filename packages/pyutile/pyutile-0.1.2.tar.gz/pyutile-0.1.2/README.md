# PyUtil
Collection of essential utilities across development and deployment

## Installation
```bash
  pip install pyutile
```

## Usage

```python
  from pyutile import *
```

## Utilities

### 1. Config
```python
  config = Config()
  config.load('config.json')
  config.get('key')
  config.set('key', 'value')
  config.save()
```