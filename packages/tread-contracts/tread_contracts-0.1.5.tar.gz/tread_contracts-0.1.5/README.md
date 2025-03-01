# Python client for Tread contracts

## Getting started

This project is using the following tools:
* [`pipx`](https://pipx.pypa.io/stable/installation/)
* [`poetry`](https://python-poetry.org/docs/)

You can install these as follows:

```shell
> brew install pipx
> pipx ensurepath
> pipx install poetry
> poetry completions bash >> ~/.bash_completion
```

With `poetry`, you can install dependencies as follows. Note that if you do not have a virtual env active, `poetry` will automatically create and manage one for you, specific to this project.

```
> poetry install
```

## Run tests

You can run simple tests as follows. These will run on the Sepolia Base testnet by default.

```shell
# Note: Make sure the poetry virtualenv is active, e.g. `source .venv/bin/activate`.
#
# Run with Gelato meta-transactions (enabled by default).
> python -m test_client.main auto
# Run with meta-transactions disabled.
> python -m test_client.main auto false
```

## Publish to PyPI

Make sure the `version` field in `pyproject.toml` is updated as needed.

```shell
poetry publish --build
```

## Example transactions

### Trader ID

Reading a record or writing an attestations requires a trader ID. We are using 0xABCD as a mock trader ID for these examples.

### Contract read example

```shell
> python -m test_client.main read-info

Attestations contract 0xB4f9A1f1347b7D8eb97dC70672576BB96E0510e0:
  data group members: 0x64D8672534A169B0340fA10F6340CE45aE36d0e7
  epoch length: 600 seconds
  epoch zero start: 0 (1969-12-31 19:00:00 local)
  Current epoch number: 2880124
  Current epoch 2880124 starts at 1728074400 (2024-10-04 16:40:00 local) and ends at 1728075000 (2024-10-04 16:50:00 local)
```

### Data attestation write example

```shell
> python -m test_client.main write-data 0xABCD 0 0x1234 mock-cid

Submitted transaction 0x2280079a88ae3af1923feeb40e0938862d7f141c1c87d31d5da0ca189c1010c7. Waiting for confirmation...
Transaction confirmed in block 16153093
```

### Data attestation read example

```shell
> python -m test_client.main read-data 0xABCD 0

Consensus for epoch 0:
  Merkle root: 0x0000000000000000000000000000000000000000000000000000000000001234
```

### Risk end-to-end example

```shell
>  python -m test_client.main create-group 0x64D8672534A169B0340fA10F6340CE45aE36d0e7 1

Submitting and waiting for transaction...
Created risk group 1

> python -m test_client.main read-group 1

Risk group 1:
  members: ['0x64D8672534A169B0340fA10F6340CE45aE36d0e7']
  threshold: 1

> python -m test_client.main create-parameter mock-name mock-desc

Submitting and waiting for transaction...
Created risk parameter 0

> python -m test_client.main read-parameter 0

Risk parameter 0:
  name: mock-name
  description: mock-desc

> python -m test_client.main write-risk 0xABCD 0 0 1 123

Submitted transaction 0xb9d1ae7fd71d43a456a62fcffba7aae0542671e66eef410136be547d803c7205. Waiting for confirmation...
Transaction confirmed in block 16153127

> python -m test_client.main read-risk 0xABCD 0 0 1

Consensus for epoch 0:
  Risk value: 1234
```
