# Mercado Radar - SDK

The Mercado Radar SDK library provides convenient access to the Mercado Radar API from applications written in the
Python language. It includes a pre-defined set of classes for API resources that initialize themselves dynamically from
API responses.

For more information visit the [API Documentation](https://mercadoradar.readme.io/).

## Installation

You don't need the source code unless you want to modify the package for contribution. If you just want to use the
package, just run:

```shell
pip install mercadoradar
```

## Usage

### Authentication

The library needs to be configured with your users's API Token which you can get it through
suporte@mercadoradar.com.br

1. Set it as the `MERCADORADAR_TOKEN` environment variable before using the library:

```shell
export MERCADORADAR_TOKEN='YOUR_API_TOKEN'
```

2. Or set directly on initialization:

```python
from src.mercadoradar import MercadoRadar

mercadoradar = MercadoRadar(token='YOUR_API_TOKEN')
```

### Resources

All resources have the methods:

* create
* retrieve
* update
* delete
* list

| Resource                | Module                  |
|-------------------------|-------------------------|
| Account                 | account                 |
| Attribute Type          | attribute_type          |
| Attribute Value         | attribute_value         |
| Brand                   | brand                   |      
| Category                | category                |
| Filter                  | filter                  |
| Product                 | product                 |
| Product Attribute Value | product_attribute_value |
| Product History         | product_history         |
| Search                  | search                  |
| Seller                  | seller                  |
| Site                    | site                    |
| User                    | user                    |


### Examples
```python
from mercadoradar import MercadoRadar

mercadoradar = MercadoRadar(token="YOUR_TOKEN")

products = mercadoradar.product.list()
out_of_stock_products = mercadoradar.product.list(status=["OUT_OF_STOCK"])
my_product = mercadoradar.product.retrieve(id=1)

sellers = mercadoradar.seller.list()
my_seller = mercadoradar.seller.retrieve(id=1)

brazil_sites = mercadoradar.site.list(country="BRAZIL")

my_product_history = mercadoradar.product_history.list(product_id=1)
```

## Requirements

Python 3.10.*

## Development

1. Install dependencies

```shell
poetry env use python3.10
poetry config virtualenvs.in-project true
poetry install
```

## Publish
```shell
poetry config pypi-token.pypi <TOKEN>
poetry build
poetry publish --build
```


## Licence

MIT License

Copyright (c) 2025 Mercado Radar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.