# blockchainpy

A very minimal implementation of a blockchain in Python. Please note that this is by no means intended to be use in a real scenario, the code used here is for educational purposes only.

## Feature Roadmap:

- [X] Possibility to add blocks to the chain
- [X] Simple Proof of Work (PoW) algorithm
- [X] Possibility to add transactions
- [X] Possibility to mine new blocks
- [X] Possibility to replace the chain with a new one
- [ ] Wallet management
- [ ] Sign transactions
- [ ] Peer to Peer communication

## Set Up

1. Check out the code
2. Install requirements
    ```
    pipenv install
    ```
3. Start the server with:
    ```
   pipenv run python -m flask run
    ```

4. Visit http://localhost/api-docs
   
## Tests

The code is covered by tests, to run the tests please execute

```
pipenv run python -m unittest
```