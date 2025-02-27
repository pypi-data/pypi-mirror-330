#!/bin/bash

#### Governance
solc --optimize --base-path . --include-path node_modules/ --evm-version paris --abi LeeaGovernance.sol -o artifacts/governance/ --overwrite
solc --optimize --base-path . --include-path node_modules/ --evm-version paris --bin LeeaGovernance.sol -o artifacts/governance/ --overwrite
abigen --abi artifacts/governance/LeeaGovernance.abi --bin artifacts/governance/LeeaGovernance.bin --pkg governance --type LeeaGovernance --out artifacts/governance/LeeaGovernance.go

#### Token
solc --optimize --base-path . --include-path node_modules/ --evm-version paris --abi LeeaToken.sol -o artifacts/token/ --overwrite
solc --optimize --base-path . --include-path node_modules/ --evm-version paris --bin LeeaToken.sol -o artifacts/token/ --overwrite
abigen --abi artifacts/token/LeeaToken.abi --bin artifacts/token/LeeaToken.bin --pkg token --type LeeaToken --out artifacts/token/LeeaToken.go

#### Escrow
solc --optimize --base-path . --include-path node_modules/ --evm-version paris --abi Escrow.sol -o artifacts/escrow/ --overwrite
solc --optimize --base-path . --include-path node_modules/ --evm-version paris --bin Escrow.sol -o artifacts/escrow/ --overwrite
abigen --abi artifacts/escrow/Escrow.abi --bin artifacts/escrow/Escrow.bin --pkg escrow --type Escrow --out artifacts/escrow/Escrow.go

#### Agent Registry
solc --optimize --base-path . --include-path node_modules/ --evm-version paris --abi AgentRegistry.sol -o artifacts/aregistry/ --overwrite
solc --optimize --base-path . --include-path node_modules/ --evm-version paris --bin AgentRegistry.sol -o artifacts/aregistry/ --overwrite
abigen --abi artifacts/aregistry/AgentRegistry.abi --bin artifacts/aregistry/AgentRegistry.bin --pkg aregistry --type AgentRegistry --out artifacts/aregistry/AgentRegistry.go
