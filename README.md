## Dune multichain decoding helper functions

This repository offers helper functions to identify all Safe supported deployments of:

- Proxy factories
- Safe contracts
- Safe L2 contracts

The list of supported blockchains get compared to blockchains that are supported in the decoding process by Dune.
We finally print a list of blockains for which we need to add decoding requests.

### Example usage

```python
> python main.py --fname <file_path> --deployments "canonical" "eip155" "zksync"
```

This prints the given deployments for the given file path, if they are present in this file.
