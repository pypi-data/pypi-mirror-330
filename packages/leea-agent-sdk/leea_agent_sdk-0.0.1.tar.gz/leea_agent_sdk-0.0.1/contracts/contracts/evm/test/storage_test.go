package contracts

import (
	"fmt"
	"math/big"
	"testing"

	"github.com/stretchr/testify/require"

	storage_contract "github.com/Leea-Labs/leea-contracts/contracts/artifacts/storage"
)

func TestStorageContract(t *testing.T) {
	sim, auth, err := SetupBackend()
	require.NoError(t, err)
	_, tx, store, err := storage_contract.DeployStorage(auth, sim.Client())
	require.NoError(t, err)
	sim.Commit()
	tx, err = store.Store(auth, big.NewInt(420))
	require.NoError(t, err)
	fmt.Printf("State update pending: 0x%x\n", tx.Hash())
	sim.Commit()
	val, err := store.Retrieve(nil)
	require.Equal(t, big.NewInt(420).Uint64(), val.Uint64())
}
