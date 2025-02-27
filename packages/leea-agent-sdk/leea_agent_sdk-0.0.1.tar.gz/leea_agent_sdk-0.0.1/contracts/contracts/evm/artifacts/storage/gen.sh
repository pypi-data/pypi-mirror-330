#!/bin/bash
solc --evm-version paris --abi Storage.sol -o build --overwrite
solc --evm-version paris --bin Storage.sol -o build --overwrite
abigen --abi ./build/Storage.abi --pkg storage --type Storage --out Storage.go --bin ./build/Storage.bin