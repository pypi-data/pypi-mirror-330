package contracts

import (
	"context"
	"math/big"
	"testing"

	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	"github.com/ethereum/go-ethereum/crypto"
	"github.com/stretchr/testify/require"

	token_contract "github.com/Leea-Labs/leea-contracts/contracts/artifacts/token"
)

func TestTokenContract(t *testing.T) {
	ctx := context.Background()
	key, err := crypto.GenerateKey()
	keyAddr := crypto.PubkeyToAddress(key.PublicKey)
	sim, auth, err := SetupBackend()
	require.NoError(t, err)
	_, _, token, err := token_contract.DeployLeeaToken(auth, sim.Client(), auth.From)
	require.NoError(t, err)
	sim.Commit()
	_, err = token.Transfer(auth, keyAddr, big.NewInt(100))
	require.NoError(t, err)
	sim.Commit()
	val, err := token.BalanceOf(&bind.CallOpts{Context: ctx}, keyAddr)
	require.Equal(t, big.NewInt(100).Uint64(), val.Uint64())
}
