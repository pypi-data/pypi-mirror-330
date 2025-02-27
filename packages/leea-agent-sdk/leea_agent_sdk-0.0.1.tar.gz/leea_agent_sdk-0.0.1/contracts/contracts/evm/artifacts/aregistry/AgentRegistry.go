// Code generated - DO NOT EDIT.
// This file is a generated binding and any manual changes will be lost.

package aregistry

import (
	"errors"
	"math/big"
	"strings"

	ethereum "github.com/ethereum/go-ethereum"
	"github.com/ethereum/go-ethereum/accounts/abi"
	"github.com/ethereum/go-ethereum/accounts/abi/bind"
	"github.com/ethereum/go-ethereum/common"
	"github.com/ethereum/go-ethereum/core/types"
	"github.com/ethereum/go-ethereum/event"
)

// Reference imports to suppress errors if they are not otherwise used.
var (
	_ = errors.New
	_ = big.NewInt
	_ = strings.NewReader
	_ = ethereum.NotFound
	_ = bind.Bind
	_ = common.Big1
	_ = types.BloomLookup
	_ = event.NewSubscription
	_ = abi.ConvertType
)

// AgentRegistryMetaData contains all meta data concerning the AgentRegistry contract.
var AgentRegistryMetaData = &bind.MetaData{
	ABI: "[{\"inputs\":[{\"internalType\":\"address\",\"name\":\"initialOwner\",\"type\":\"address\"},{\"internalType\":\"address\",\"name\":\"dao\",\"type\":\"address\"}],\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"owner\",\"type\":\"address\"}],\"name\":\"OwnableInvalidOwner\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"account\",\"type\":\"address\"}],\"name\":\"OwnableUnauthorizedAccount\",\"type\":\"error\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"address\",\"name\":\"pub\",\"type\":\"address\"}],\"name\":\"Deleted\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"address\",\"name\":\"pub\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"string\",\"name\":\"name\",\"type\":\"string\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"newFee\",\"type\":\"uint256\"}],\"name\":\"FeeUpdated\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"internalType\":\"address\",\"name\":\"previousOwner\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"newOwner\",\"type\":\"address\"}],\"name\":\"OwnershipTransferred\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"address\",\"name\":\"pub\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"string\",\"name\":\"name\",\"type\":\"string\"}],\"name\":\"Registered\",\"type\":\"event\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"agentAddress\",\"type\":\"address\"}],\"name\":\"deleteAgent\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"index\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"agentAddress\",\"type\":\"address\"}],\"name\":\"getAgent\",\"outputs\":[{\"internalType\":\"string\",\"name\":\"name\",\"type\":\"string\"},{\"internalType\":\"uint256\",\"name\":\"fee\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"activityScore\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"accuracyScore\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"index\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"agentAddress\",\"type\":\"address\"}],\"name\":\"getAgentAccuracyScore\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"fee\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"agentAddress\",\"type\":\"address\"}],\"name\":\"getAgentActivityScore\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"fee\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"index\",\"type\":\"uint256\"}],\"name\":\"getAgentAtIndex\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"agentAddress\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"getAgentCount\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"count\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"agentAddress\",\"type\":\"address\"}],\"name\":\"getAgentFee\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"fee\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"agentAddress\",\"type\":\"address\"}],\"name\":\"isAgent\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"isIndeed\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"owner\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"agentAddress\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"agentFee\",\"type\":\"uint256\"},{\"internalType\":\"string\",\"name\":\"name\",\"type\":\"string\"}],\"name\":\"registerAgent\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"index\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"renounceOwnership\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"newOwner\",\"type\":\"address\"}],\"name\":\"transferOwnership\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"agentAddress\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"newAccuracyScore\",\"type\":\"uint256\"}],\"name\":\"updateAgentAccuracyScore\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"success\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"agentAddress\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"newActivityScore\",\"type\":\"uint256\"}],\"name\":\"updateAgentActivityScore\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"success\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"agentAddress\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"newFee\",\"type\":\"uint256\"}],\"name\":\"updateAgentFee\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"success\",\"type\":\"bool\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"}]",
	Bin: "0x608060405234801561001057600080fd5b50604051610e36380380610e3683398101604081905261002f916100fa565b816001600160a01b03811661005e57604051631e4fbdf760e01b81526000600482015260240160405180910390fd5b6100678161008e565b50600380546001600160a01b0319166001600160a01b03929092169190911790555061012d565b600080546001600160a01b038381166001600160a01b0319831681178455604051919092169283917f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e09190a35050565b80516001600160a01b03811681146100f557600080fd5b919050565b6000806040838503121561010d57600080fd5b610116836100de565b9150610124602084016100de565b90509250929050565b610cfa8061013c6000396000f3fe608060405234801561001057600080fd5b50600436106100f55760003560e01c80638da5cb5b11610097578063eb24478211610066578063eb244782146101f0578063f2fde38b14610203578063fb3551ff14610216578063fdc344961461023a57600080fd5b80638da5cb5b146101b157806391cab63e146101c2578063bcb47e9a146101ca578063d1cdb9cc146101dd57600080fd5b80635bc085a4116100d35780635bc085a414610156578063715018a6146101695780637bcac9a5146101735780637ca454131461019e57600080fd5b80631ffbb064146100fa57806331f4e9d4146101225780635046fc1614610143575b600080fd5b61010d61010836600461089a565b61024d565b60405190151581526020015b60405180910390f35b61013561013036600461089a565b6102ae565b604051908152602001610119565b6101356101513660046108d2565b6102e1565b61010d6101643660046109a5565b6103de565b610171610423565b005b6101866101813660046109cf565b610437565b6040516001600160a01b039091168152602001610119565b61010d6101ac3660046109a5565b610467565b6000546001600160a01b0316610186565b600254610135565b6101356101d836600461089a565b6104e8565b6101356101eb36600461089a565b61051c565b61010d6101fe3660046109a5565b61054f565b61017161021136600461089a565b610593565b61022961022436600461089a565b6105d6565b604051610119959493929190610a2e565b61013561024836600461089a565b6106c3565b600254600090810361026157506000919050565b6001600160a01b03821660008181526001602052604090206004015460028054909190811061029257610292610a65565b6000918252602090912001546001600160a01b03161492915050565b60006102b98261024d565b6102c257600080fd5b506001600160a01b031660009081526001602052604090206002015490565b60006102ec8461024d565b156102f657600080fd5b6002805460018082019092557f405787fa12a823e0f2b7631cc41b3ba8828b3321ca811111fa75cd3aa3bb5ace0180546001600160a01b0319166001600160a01b038716908117909155600090815260208290526040902090810184905561035e8382610b04565b5060025461036e90600190610bc3565b6001600160a01b0385166000908152600160205260409081902060040191909155517fb3eccf73f39b1c07947c780b2b39df2a1bb058b4037b0a42d0881ca1a028a132906103bf9086908590610be4565b60405180910390a16002546103d690600190610bc3565b949350505050565b60006103e8610806565b6103f18361024d565b6103fa57600080fd5b506001600160a01b03821660009081526001602081905260409091206003018290555b92915050565b61042b610806565b6104356000610833565b565b60006002828154811061044c5761044c610a65565b6000918252602090912001546001600160a01b031692915050565b6000610471610806565b61047a8361024d565b61048357600080fd5b6001600160a01b03831660009081526001602081905260409182902090810184905590517fe65b1a0f0203c10a67161b92db1350d95cf4b2ba05ebf3df76c927f2402b9a93916104d7918691908690610c08565b60405180910390a150600192915050565b60006104f38261024d565b6104fc57600080fd5b506001600160a01b03166000908152600160208190526040909120015490565b60006105278261024d565b61053057600080fd5b506001600160a01b031660009081526001602052604090206003015490565b6000610559610806565b6105628361024d565b61056b57600080fd5b506001600160a01b038216600090815260016020819052604090912060020182905592915050565b61059b610806565b6001600160a01b0381166105ca57604051631e4fbdf760e01b8152600060048201526024015b60405180910390fd5b6105d381610833565b50565b60606000806000806105e78661024d565b15156001146105f557600080fd5b6001600160a01b0386166000908152600160208190526040909120908101546002820154600383015460048401548454859061063090610a7b565b80601f016020809104026020016040519081016040528092919081815260200182805461065c90610a7b565b80156106a95780601f1061067e576101008083540402835291602001916106a9565b820191906000526020600020905b81548152906001019060200180831161068c57829003601f168201915b505050505094509450945094509450945091939590929450565b60006106cd610806565b6106d68261024d565b6106df57600080fd5b6001600160a01b03821660009081526001602081905260408220600401546002805491939290916107109190610bc3565b8154811061072057610720610a65565b600091825260209091200154600280546001600160a01b03909216925082918490811061074f5761074f610a65565b600091825260208083209190910180546001600160a01b0319166001600160a01b039485161790559183168152600190915260409020600401829055600280548061079c5761079c610cae565b6000828152602090819020600019908301810180546001600160a01b03191690559091019091556040516001600160a01b03861681527f7fb2e49c6d2dcc748cced4be404df4b502a5091d84f32f62fa7821b5f9231f6b910160405180910390a15090505b919050565b6000546001600160a01b031633146104355760405163118cdaa760e01b81523360048201526024016105c1565b600080546001600160a01b038381166001600160a01b0319831681178455604051919092169283917f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e09190a35050565b80356001600160a01b038116811461080157600080fd5b6000602082840312156108ac57600080fd5b6108b582610883565b9392505050565b634e487b7160e01b600052604160045260246000fd5b6000806000606084860312156108e757600080fd5b6108f084610883565b925060208401359150604084013567ffffffffffffffff81111561091357600080fd5b8401601f8101861361092457600080fd5b803567ffffffffffffffff81111561093e5761093e6108bc565b604051601f8201601f19908116603f0116810167ffffffffffffffff8111828210171561096d5761096d6108bc565b60405281815282820160200188101561098557600080fd5b816020840160208301376000602083830101528093505050509250925092565b600080604083850312156109b857600080fd5b6109c183610883565b946020939093013593505050565b6000602082840312156109e157600080fd5b5035919050565b6000815180845260005b81811015610a0e576020818501810151868301820152016109f2565b506000602082860101526020601f19601f83011685010191505092915050565b60a081526000610a4160a08301886109e8565b90508560208301528460408301528360608301528260808301529695505050505050565b634e487b7160e01b600052603260045260246000fd5b600181811c90821680610a8f57607f821691505b602082108103610aaf57634e487b7160e01b600052602260045260246000fd5b50919050565b601f821115610aff57806000526020600020601f840160051c81016020851015610adc5750805b601f840160051c820191505b81811015610afc5760008155600101610ae8565b50505b505050565b815167ffffffffffffffff811115610b1e57610b1e6108bc565b610b3281610b2c8454610a7b565b84610ab5565b6020601f821160018114610b665760008315610b4e5750848201515b600019600385901b1c1916600184901b178455610afc565b600084815260208120601f198516915b82811015610b965787850151825560209485019460019092019101610b76565b5084821015610bb45786840151600019600387901b60f8161c191681555b50505050600190811b01905550565b8181038181111561041d57634e487b7160e01b600052601160045260246000fd5b6001600160a01b03831681526040602082018190526000906103d6908301846109e8565b6001600160a01b03841681526060602082015282546000908190610c2b81610a7b565b8060608601526001821660008114610c4a5760018114610c6657610c9a565b60ff1983166080870152608082151560051b8701019350610c9a565b87600052602060002060005b83811015610c9157815488820160800152600190910190602001610c72565b87016080019450505b505050604092909201929092529392505050565b634e487b7160e01b600052603160045260246000fdfea26469706673582212207a7da424a7f7bbbb6615bcd78d5906a7f18ca42189bb4af9abd512c82051875864736f6c634300081c0033",
}

// AgentRegistryABI is the input ABI used to generate the binding from.
// Deprecated: Use AgentRegistryMetaData.ABI instead.
var AgentRegistryABI = AgentRegistryMetaData.ABI

// AgentRegistryBin is the compiled bytecode used for deploying new contracts.
// Deprecated: Use AgentRegistryMetaData.Bin instead.
var AgentRegistryBin = AgentRegistryMetaData.Bin

// DeployAgentRegistry deploys a new Ethereum contract, binding an instance of AgentRegistry to it.
func DeployAgentRegistry(auth *bind.TransactOpts, backend bind.ContractBackend, initialOwner common.Address, dao common.Address) (common.Address, *types.Transaction, *AgentRegistry, error) {
	parsed, err := AgentRegistryMetaData.GetAbi()
	if err != nil {
		return common.Address{}, nil, nil, err
	}
	if parsed == nil {
		return common.Address{}, nil, nil, errors.New("GetABI returned nil")
	}

	address, tx, contract, err := bind.DeployContract(auth, *parsed, common.FromHex(AgentRegistryBin), backend, initialOwner, dao)
	if err != nil {
		return common.Address{}, nil, nil, err
	}
	return address, tx, &AgentRegistry{AgentRegistryCaller: AgentRegistryCaller{contract: contract}, AgentRegistryTransactor: AgentRegistryTransactor{contract: contract}, AgentRegistryFilterer: AgentRegistryFilterer{contract: contract}}, nil
}

// AgentRegistry is an auto generated Go binding around an Ethereum contract.
type AgentRegistry struct {
	AgentRegistryCaller     // Read-only binding to the contract
	AgentRegistryTransactor // Write-only binding to the contract
	AgentRegistryFilterer   // Log filterer for contract events
}

// AgentRegistryCaller is an auto generated read-only Go binding around an Ethereum contract.
type AgentRegistryCaller struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// AgentRegistryTransactor is an auto generated write-only Go binding around an Ethereum contract.
type AgentRegistryTransactor struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// AgentRegistryFilterer is an auto generated log filtering Go binding around an Ethereum contract events.
type AgentRegistryFilterer struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// AgentRegistrySession is an auto generated Go binding around an Ethereum contract,
// with pre-set call and transact options.
type AgentRegistrySession struct {
	Contract     *AgentRegistry    // Generic contract binding to set the session for
	CallOpts     bind.CallOpts     // Call options to use throughout this session
	TransactOpts bind.TransactOpts // Transaction auth options to use throughout this session
}

// AgentRegistryCallerSession is an auto generated read-only Go binding around an Ethereum contract,
// with pre-set call options.
type AgentRegistryCallerSession struct {
	Contract *AgentRegistryCaller // Generic contract caller binding to set the session for
	CallOpts bind.CallOpts        // Call options to use throughout this session
}

// AgentRegistryTransactorSession is an auto generated write-only Go binding around an Ethereum contract,
// with pre-set transact options.
type AgentRegistryTransactorSession struct {
	Contract     *AgentRegistryTransactor // Generic contract transactor binding to set the session for
	TransactOpts bind.TransactOpts        // Transaction auth options to use throughout this session
}

// AgentRegistryRaw is an auto generated low-level Go binding around an Ethereum contract.
type AgentRegistryRaw struct {
	Contract *AgentRegistry // Generic contract binding to access the raw methods on
}

// AgentRegistryCallerRaw is an auto generated low-level read-only Go binding around an Ethereum contract.
type AgentRegistryCallerRaw struct {
	Contract *AgentRegistryCaller // Generic read-only contract binding to access the raw methods on
}

// AgentRegistryTransactorRaw is an auto generated low-level write-only Go binding around an Ethereum contract.
type AgentRegistryTransactorRaw struct {
	Contract *AgentRegistryTransactor // Generic write-only contract binding to access the raw methods on
}

// NewAgentRegistry creates a new instance of AgentRegistry, bound to a specific deployed contract.
func NewAgentRegistry(address common.Address, backend bind.ContractBackend) (*AgentRegistry, error) {
	contract, err := bindAgentRegistry(address, backend, backend, backend)
	if err != nil {
		return nil, err
	}
	return &AgentRegistry{AgentRegistryCaller: AgentRegistryCaller{contract: contract}, AgentRegistryTransactor: AgentRegistryTransactor{contract: contract}, AgentRegistryFilterer: AgentRegistryFilterer{contract: contract}}, nil
}

// NewAgentRegistryCaller creates a new read-only instance of AgentRegistry, bound to a specific deployed contract.
func NewAgentRegistryCaller(address common.Address, caller bind.ContractCaller) (*AgentRegistryCaller, error) {
	contract, err := bindAgentRegistry(address, caller, nil, nil)
	if err != nil {
		return nil, err
	}
	return &AgentRegistryCaller{contract: contract}, nil
}

// NewAgentRegistryTransactor creates a new write-only instance of AgentRegistry, bound to a specific deployed contract.
func NewAgentRegistryTransactor(address common.Address, transactor bind.ContractTransactor) (*AgentRegistryTransactor, error) {
	contract, err := bindAgentRegistry(address, nil, transactor, nil)
	if err != nil {
		return nil, err
	}
	return &AgentRegistryTransactor{contract: contract}, nil
}

// NewAgentRegistryFilterer creates a new log filterer instance of AgentRegistry, bound to a specific deployed contract.
func NewAgentRegistryFilterer(address common.Address, filterer bind.ContractFilterer) (*AgentRegistryFilterer, error) {
	contract, err := bindAgentRegistry(address, nil, nil, filterer)
	if err != nil {
		return nil, err
	}
	return &AgentRegistryFilterer{contract: contract}, nil
}

// bindAgentRegistry binds a generic wrapper to an already deployed contract.
func bindAgentRegistry(address common.Address, caller bind.ContractCaller, transactor bind.ContractTransactor, filterer bind.ContractFilterer) (*bind.BoundContract, error) {
	parsed, err := AgentRegistryMetaData.GetAbi()
	if err != nil {
		return nil, err
	}
	return bind.NewBoundContract(address, *parsed, caller, transactor, filterer), nil
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_AgentRegistry *AgentRegistryRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _AgentRegistry.Contract.AgentRegistryCaller.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_AgentRegistry *AgentRegistryRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _AgentRegistry.Contract.AgentRegistryTransactor.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_AgentRegistry *AgentRegistryRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _AgentRegistry.Contract.AgentRegistryTransactor.contract.Transact(opts, method, params...)
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_AgentRegistry *AgentRegistryCallerRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _AgentRegistry.Contract.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_AgentRegistry *AgentRegistryTransactorRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _AgentRegistry.Contract.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_AgentRegistry *AgentRegistryTransactorRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _AgentRegistry.Contract.contract.Transact(opts, method, params...)
}

// GetAgent is a free data retrieval call binding the contract method 0xfb3551ff.
//
// Solidity: function getAgent(address agentAddress) view returns(string name, uint256 fee, uint256 activityScore, uint256 accuracyScore, uint256 index)
func (_AgentRegistry *AgentRegistryCaller) GetAgent(opts *bind.CallOpts, agentAddress common.Address) (struct {
	Name          string
	Fee           *big.Int
	ActivityScore *big.Int
	AccuracyScore *big.Int
	Index         *big.Int
}, error) {
	var out []interface{}
	err := _AgentRegistry.contract.Call(opts, &out, "getAgent", agentAddress)

	outstruct := new(struct {
		Name          string
		Fee           *big.Int
		ActivityScore *big.Int
		AccuracyScore *big.Int
		Index         *big.Int
	})
	if err != nil {
		return *outstruct, err
	}

	outstruct.Name = *abi.ConvertType(out[0], new(string)).(*string)
	outstruct.Fee = *abi.ConvertType(out[1], new(*big.Int)).(**big.Int)
	outstruct.ActivityScore = *abi.ConvertType(out[2], new(*big.Int)).(**big.Int)
	outstruct.AccuracyScore = *abi.ConvertType(out[3], new(*big.Int)).(**big.Int)
	outstruct.Index = *abi.ConvertType(out[4], new(*big.Int)).(**big.Int)

	return *outstruct, err

}

// GetAgent is a free data retrieval call binding the contract method 0xfb3551ff.
//
// Solidity: function getAgent(address agentAddress) view returns(string name, uint256 fee, uint256 activityScore, uint256 accuracyScore, uint256 index)
func (_AgentRegistry *AgentRegistrySession) GetAgent(agentAddress common.Address) (struct {
	Name          string
	Fee           *big.Int
	ActivityScore *big.Int
	AccuracyScore *big.Int
	Index         *big.Int
}, error) {
	return _AgentRegistry.Contract.GetAgent(&_AgentRegistry.CallOpts, agentAddress)
}

// GetAgent is a free data retrieval call binding the contract method 0xfb3551ff.
//
// Solidity: function getAgent(address agentAddress) view returns(string name, uint256 fee, uint256 activityScore, uint256 accuracyScore, uint256 index)
func (_AgentRegistry *AgentRegistryCallerSession) GetAgent(agentAddress common.Address) (struct {
	Name          string
	Fee           *big.Int
	ActivityScore *big.Int
	AccuracyScore *big.Int
	Index         *big.Int
}, error) {
	return _AgentRegistry.Contract.GetAgent(&_AgentRegistry.CallOpts, agentAddress)
}

// GetAgentAccuracyScore is a free data retrieval call binding the contract method 0xd1cdb9cc.
//
// Solidity: function getAgentAccuracyScore(address agentAddress) view returns(uint256 fee)
func (_AgentRegistry *AgentRegistryCaller) GetAgentAccuracyScore(opts *bind.CallOpts, agentAddress common.Address) (*big.Int, error) {
	var out []interface{}
	err := _AgentRegistry.contract.Call(opts, &out, "getAgentAccuracyScore", agentAddress)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetAgentAccuracyScore is a free data retrieval call binding the contract method 0xd1cdb9cc.
//
// Solidity: function getAgentAccuracyScore(address agentAddress) view returns(uint256 fee)
func (_AgentRegistry *AgentRegistrySession) GetAgentAccuracyScore(agentAddress common.Address) (*big.Int, error) {
	return _AgentRegistry.Contract.GetAgentAccuracyScore(&_AgentRegistry.CallOpts, agentAddress)
}

// GetAgentAccuracyScore is a free data retrieval call binding the contract method 0xd1cdb9cc.
//
// Solidity: function getAgentAccuracyScore(address agentAddress) view returns(uint256 fee)
func (_AgentRegistry *AgentRegistryCallerSession) GetAgentAccuracyScore(agentAddress common.Address) (*big.Int, error) {
	return _AgentRegistry.Contract.GetAgentAccuracyScore(&_AgentRegistry.CallOpts, agentAddress)
}

// GetAgentActivityScore is a free data retrieval call binding the contract method 0x31f4e9d4.
//
// Solidity: function getAgentActivityScore(address agentAddress) view returns(uint256 fee)
func (_AgentRegistry *AgentRegistryCaller) GetAgentActivityScore(opts *bind.CallOpts, agentAddress common.Address) (*big.Int, error) {
	var out []interface{}
	err := _AgentRegistry.contract.Call(opts, &out, "getAgentActivityScore", agentAddress)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetAgentActivityScore is a free data retrieval call binding the contract method 0x31f4e9d4.
//
// Solidity: function getAgentActivityScore(address agentAddress) view returns(uint256 fee)
func (_AgentRegistry *AgentRegistrySession) GetAgentActivityScore(agentAddress common.Address) (*big.Int, error) {
	return _AgentRegistry.Contract.GetAgentActivityScore(&_AgentRegistry.CallOpts, agentAddress)
}

// GetAgentActivityScore is a free data retrieval call binding the contract method 0x31f4e9d4.
//
// Solidity: function getAgentActivityScore(address agentAddress) view returns(uint256 fee)
func (_AgentRegistry *AgentRegistryCallerSession) GetAgentActivityScore(agentAddress common.Address) (*big.Int, error) {
	return _AgentRegistry.Contract.GetAgentActivityScore(&_AgentRegistry.CallOpts, agentAddress)
}

// GetAgentAtIndex is a free data retrieval call binding the contract method 0x7bcac9a5.
//
// Solidity: function getAgentAtIndex(uint256 index) view returns(address agentAddress)
func (_AgentRegistry *AgentRegistryCaller) GetAgentAtIndex(opts *bind.CallOpts, index *big.Int) (common.Address, error) {
	var out []interface{}
	err := _AgentRegistry.contract.Call(opts, &out, "getAgentAtIndex", index)

	if err != nil {
		return *new(common.Address), err
	}

	out0 := *abi.ConvertType(out[0], new(common.Address)).(*common.Address)

	return out0, err

}

// GetAgentAtIndex is a free data retrieval call binding the contract method 0x7bcac9a5.
//
// Solidity: function getAgentAtIndex(uint256 index) view returns(address agentAddress)
func (_AgentRegistry *AgentRegistrySession) GetAgentAtIndex(index *big.Int) (common.Address, error) {
	return _AgentRegistry.Contract.GetAgentAtIndex(&_AgentRegistry.CallOpts, index)
}

// GetAgentAtIndex is a free data retrieval call binding the contract method 0x7bcac9a5.
//
// Solidity: function getAgentAtIndex(uint256 index) view returns(address agentAddress)
func (_AgentRegistry *AgentRegistryCallerSession) GetAgentAtIndex(index *big.Int) (common.Address, error) {
	return _AgentRegistry.Contract.GetAgentAtIndex(&_AgentRegistry.CallOpts, index)
}

// GetAgentCount is a free data retrieval call binding the contract method 0x91cab63e.
//
// Solidity: function getAgentCount() view returns(uint256 count)
func (_AgentRegistry *AgentRegistryCaller) GetAgentCount(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _AgentRegistry.contract.Call(opts, &out, "getAgentCount")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetAgentCount is a free data retrieval call binding the contract method 0x91cab63e.
//
// Solidity: function getAgentCount() view returns(uint256 count)
func (_AgentRegistry *AgentRegistrySession) GetAgentCount() (*big.Int, error) {
	return _AgentRegistry.Contract.GetAgentCount(&_AgentRegistry.CallOpts)
}

// GetAgentCount is a free data retrieval call binding the contract method 0x91cab63e.
//
// Solidity: function getAgentCount() view returns(uint256 count)
func (_AgentRegistry *AgentRegistryCallerSession) GetAgentCount() (*big.Int, error) {
	return _AgentRegistry.Contract.GetAgentCount(&_AgentRegistry.CallOpts)
}

// GetAgentFee is a free data retrieval call binding the contract method 0xbcb47e9a.
//
// Solidity: function getAgentFee(address agentAddress) view returns(uint256 fee)
func (_AgentRegistry *AgentRegistryCaller) GetAgentFee(opts *bind.CallOpts, agentAddress common.Address) (*big.Int, error) {
	var out []interface{}
	err := _AgentRegistry.contract.Call(opts, &out, "getAgentFee", agentAddress)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetAgentFee is a free data retrieval call binding the contract method 0xbcb47e9a.
//
// Solidity: function getAgentFee(address agentAddress) view returns(uint256 fee)
func (_AgentRegistry *AgentRegistrySession) GetAgentFee(agentAddress common.Address) (*big.Int, error) {
	return _AgentRegistry.Contract.GetAgentFee(&_AgentRegistry.CallOpts, agentAddress)
}

// GetAgentFee is a free data retrieval call binding the contract method 0xbcb47e9a.
//
// Solidity: function getAgentFee(address agentAddress) view returns(uint256 fee)
func (_AgentRegistry *AgentRegistryCallerSession) GetAgentFee(agentAddress common.Address) (*big.Int, error) {
	return _AgentRegistry.Contract.GetAgentFee(&_AgentRegistry.CallOpts, agentAddress)
}

// IsAgent is a free data retrieval call binding the contract method 0x1ffbb064.
//
// Solidity: function isAgent(address agentAddress) view returns(bool isIndeed)
func (_AgentRegistry *AgentRegistryCaller) IsAgent(opts *bind.CallOpts, agentAddress common.Address) (bool, error) {
	var out []interface{}
	err := _AgentRegistry.contract.Call(opts, &out, "isAgent", agentAddress)

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// IsAgent is a free data retrieval call binding the contract method 0x1ffbb064.
//
// Solidity: function isAgent(address agentAddress) view returns(bool isIndeed)
func (_AgentRegistry *AgentRegistrySession) IsAgent(agentAddress common.Address) (bool, error) {
	return _AgentRegistry.Contract.IsAgent(&_AgentRegistry.CallOpts, agentAddress)
}

// IsAgent is a free data retrieval call binding the contract method 0x1ffbb064.
//
// Solidity: function isAgent(address agentAddress) view returns(bool isIndeed)
func (_AgentRegistry *AgentRegistryCallerSession) IsAgent(agentAddress common.Address) (bool, error) {
	return _AgentRegistry.Contract.IsAgent(&_AgentRegistry.CallOpts, agentAddress)
}

// Owner is a free data retrieval call binding the contract method 0x8da5cb5b.
//
// Solidity: function owner() view returns(address)
func (_AgentRegistry *AgentRegistryCaller) Owner(opts *bind.CallOpts) (common.Address, error) {
	var out []interface{}
	err := _AgentRegistry.contract.Call(opts, &out, "owner")

	if err != nil {
		return *new(common.Address), err
	}

	out0 := *abi.ConvertType(out[0], new(common.Address)).(*common.Address)

	return out0, err

}

// Owner is a free data retrieval call binding the contract method 0x8da5cb5b.
//
// Solidity: function owner() view returns(address)
func (_AgentRegistry *AgentRegistrySession) Owner() (common.Address, error) {
	return _AgentRegistry.Contract.Owner(&_AgentRegistry.CallOpts)
}

// Owner is a free data retrieval call binding the contract method 0x8da5cb5b.
//
// Solidity: function owner() view returns(address)
func (_AgentRegistry *AgentRegistryCallerSession) Owner() (common.Address, error) {
	return _AgentRegistry.Contract.Owner(&_AgentRegistry.CallOpts)
}

// DeleteAgent is a paid mutator transaction binding the contract method 0xfdc34496.
//
// Solidity: function deleteAgent(address agentAddress) returns(uint256 index)
func (_AgentRegistry *AgentRegistryTransactor) DeleteAgent(opts *bind.TransactOpts, agentAddress common.Address) (*types.Transaction, error) {
	return _AgentRegistry.contract.Transact(opts, "deleteAgent", agentAddress)
}

// DeleteAgent is a paid mutator transaction binding the contract method 0xfdc34496.
//
// Solidity: function deleteAgent(address agentAddress) returns(uint256 index)
func (_AgentRegistry *AgentRegistrySession) DeleteAgent(agentAddress common.Address) (*types.Transaction, error) {
	return _AgentRegistry.Contract.DeleteAgent(&_AgentRegistry.TransactOpts, agentAddress)
}

// DeleteAgent is a paid mutator transaction binding the contract method 0xfdc34496.
//
// Solidity: function deleteAgent(address agentAddress) returns(uint256 index)
func (_AgentRegistry *AgentRegistryTransactorSession) DeleteAgent(agentAddress common.Address) (*types.Transaction, error) {
	return _AgentRegistry.Contract.DeleteAgent(&_AgentRegistry.TransactOpts, agentAddress)
}

// RegisterAgent is a paid mutator transaction binding the contract method 0x5046fc16.
//
// Solidity: function registerAgent(address agentAddress, uint256 agentFee, string name) returns(uint256 index)
func (_AgentRegistry *AgentRegistryTransactor) RegisterAgent(opts *bind.TransactOpts, agentAddress common.Address, agentFee *big.Int, name string) (*types.Transaction, error) {
	return _AgentRegistry.contract.Transact(opts, "registerAgent", agentAddress, agentFee, name)
}

// RegisterAgent is a paid mutator transaction binding the contract method 0x5046fc16.
//
// Solidity: function registerAgent(address agentAddress, uint256 agentFee, string name) returns(uint256 index)
func (_AgentRegistry *AgentRegistrySession) RegisterAgent(agentAddress common.Address, agentFee *big.Int, name string) (*types.Transaction, error) {
	return _AgentRegistry.Contract.RegisterAgent(&_AgentRegistry.TransactOpts, agentAddress, agentFee, name)
}

// RegisterAgent is a paid mutator transaction binding the contract method 0x5046fc16.
//
// Solidity: function registerAgent(address agentAddress, uint256 agentFee, string name) returns(uint256 index)
func (_AgentRegistry *AgentRegistryTransactorSession) RegisterAgent(agentAddress common.Address, agentFee *big.Int, name string) (*types.Transaction, error) {
	return _AgentRegistry.Contract.RegisterAgent(&_AgentRegistry.TransactOpts, agentAddress, agentFee, name)
}

// RenounceOwnership is a paid mutator transaction binding the contract method 0x715018a6.
//
// Solidity: function renounceOwnership() returns()
func (_AgentRegistry *AgentRegistryTransactor) RenounceOwnership(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _AgentRegistry.contract.Transact(opts, "renounceOwnership")
}

// RenounceOwnership is a paid mutator transaction binding the contract method 0x715018a6.
//
// Solidity: function renounceOwnership() returns()
func (_AgentRegistry *AgentRegistrySession) RenounceOwnership() (*types.Transaction, error) {
	return _AgentRegistry.Contract.RenounceOwnership(&_AgentRegistry.TransactOpts)
}

// RenounceOwnership is a paid mutator transaction binding the contract method 0x715018a6.
//
// Solidity: function renounceOwnership() returns()
func (_AgentRegistry *AgentRegistryTransactorSession) RenounceOwnership() (*types.Transaction, error) {
	return _AgentRegistry.Contract.RenounceOwnership(&_AgentRegistry.TransactOpts)
}

// TransferOwnership is a paid mutator transaction binding the contract method 0xf2fde38b.
//
// Solidity: function transferOwnership(address newOwner) returns()
func (_AgentRegistry *AgentRegistryTransactor) TransferOwnership(opts *bind.TransactOpts, newOwner common.Address) (*types.Transaction, error) {
	return _AgentRegistry.contract.Transact(opts, "transferOwnership", newOwner)
}

// TransferOwnership is a paid mutator transaction binding the contract method 0xf2fde38b.
//
// Solidity: function transferOwnership(address newOwner) returns()
func (_AgentRegistry *AgentRegistrySession) TransferOwnership(newOwner common.Address) (*types.Transaction, error) {
	return _AgentRegistry.Contract.TransferOwnership(&_AgentRegistry.TransactOpts, newOwner)
}

// TransferOwnership is a paid mutator transaction binding the contract method 0xf2fde38b.
//
// Solidity: function transferOwnership(address newOwner) returns()
func (_AgentRegistry *AgentRegistryTransactorSession) TransferOwnership(newOwner common.Address) (*types.Transaction, error) {
	return _AgentRegistry.Contract.TransferOwnership(&_AgentRegistry.TransactOpts, newOwner)
}

// UpdateAgentAccuracyScore is a paid mutator transaction binding the contract method 0x5bc085a4.
//
// Solidity: function updateAgentAccuracyScore(address agentAddress, uint256 newAccuracyScore) returns(bool success)
func (_AgentRegistry *AgentRegistryTransactor) UpdateAgentAccuracyScore(opts *bind.TransactOpts, agentAddress common.Address, newAccuracyScore *big.Int) (*types.Transaction, error) {
	return _AgentRegistry.contract.Transact(opts, "updateAgentAccuracyScore", agentAddress, newAccuracyScore)
}

// UpdateAgentAccuracyScore is a paid mutator transaction binding the contract method 0x5bc085a4.
//
// Solidity: function updateAgentAccuracyScore(address agentAddress, uint256 newAccuracyScore) returns(bool success)
func (_AgentRegistry *AgentRegistrySession) UpdateAgentAccuracyScore(agentAddress common.Address, newAccuracyScore *big.Int) (*types.Transaction, error) {
	return _AgentRegistry.Contract.UpdateAgentAccuracyScore(&_AgentRegistry.TransactOpts, agentAddress, newAccuracyScore)
}

// UpdateAgentAccuracyScore is a paid mutator transaction binding the contract method 0x5bc085a4.
//
// Solidity: function updateAgentAccuracyScore(address agentAddress, uint256 newAccuracyScore) returns(bool success)
func (_AgentRegistry *AgentRegistryTransactorSession) UpdateAgentAccuracyScore(agentAddress common.Address, newAccuracyScore *big.Int) (*types.Transaction, error) {
	return _AgentRegistry.Contract.UpdateAgentAccuracyScore(&_AgentRegistry.TransactOpts, agentAddress, newAccuracyScore)
}

// UpdateAgentActivityScore is a paid mutator transaction binding the contract method 0xeb244782.
//
// Solidity: function updateAgentActivityScore(address agentAddress, uint256 newActivityScore) returns(bool success)
func (_AgentRegistry *AgentRegistryTransactor) UpdateAgentActivityScore(opts *bind.TransactOpts, agentAddress common.Address, newActivityScore *big.Int) (*types.Transaction, error) {
	return _AgentRegistry.contract.Transact(opts, "updateAgentActivityScore", agentAddress, newActivityScore)
}

// UpdateAgentActivityScore is a paid mutator transaction binding the contract method 0xeb244782.
//
// Solidity: function updateAgentActivityScore(address agentAddress, uint256 newActivityScore) returns(bool success)
func (_AgentRegistry *AgentRegistrySession) UpdateAgentActivityScore(agentAddress common.Address, newActivityScore *big.Int) (*types.Transaction, error) {
	return _AgentRegistry.Contract.UpdateAgentActivityScore(&_AgentRegistry.TransactOpts, agentAddress, newActivityScore)
}

// UpdateAgentActivityScore is a paid mutator transaction binding the contract method 0xeb244782.
//
// Solidity: function updateAgentActivityScore(address agentAddress, uint256 newActivityScore) returns(bool success)
func (_AgentRegistry *AgentRegistryTransactorSession) UpdateAgentActivityScore(agentAddress common.Address, newActivityScore *big.Int) (*types.Transaction, error) {
	return _AgentRegistry.Contract.UpdateAgentActivityScore(&_AgentRegistry.TransactOpts, agentAddress, newActivityScore)
}

// UpdateAgentFee is a paid mutator transaction binding the contract method 0x7ca45413.
//
// Solidity: function updateAgentFee(address agentAddress, uint256 newFee) returns(bool success)
func (_AgentRegistry *AgentRegistryTransactor) UpdateAgentFee(opts *bind.TransactOpts, agentAddress common.Address, newFee *big.Int) (*types.Transaction, error) {
	return _AgentRegistry.contract.Transact(opts, "updateAgentFee", agentAddress, newFee)
}

// UpdateAgentFee is a paid mutator transaction binding the contract method 0x7ca45413.
//
// Solidity: function updateAgentFee(address agentAddress, uint256 newFee) returns(bool success)
func (_AgentRegistry *AgentRegistrySession) UpdateAgentFee(agentAddress common.Address, newFee *big.Int) (*types.Transaction, error) {
	return _AgentRegistry.Contract.UpdateAgentFee(&_AgentRegistry.TransactOpts, agentAddress, newFee)
}

// UpdateAgentFee is a paid mutator transaction binding the contract method 0x7ca45413.
//
// Solidity: function updateAgentFee(address agentAddress, uint256 newFee) returns(bool success)
func (_AgentRegistry *AgentRegistryTransactorSession) UpdateAgentFee(agentAddress common.Address, newFee *big.Int) (*types.Transaction, error) {
	return _AgentRegistry.Contract.UpdateAgentFee(&_AgentRegistry.TransactOpts, agentAddress, newFee)
}

// AgentRegistryDeletedIterator is returned from FilterDeleted and is used to iterate over the raw logs and unpacked data for Deleted events raised by the AgentRegistry contract.
type AgentRegistryDeletedIterator struct {
	Event *AgentRegistryDeleted // Event containing the contract specifics and raw log

	contract *bind.BoundContract // Generic contract to use for unpacking event data
	event    string              // Event name to use for unpacking event data

	logs chan types.Log        // Log channel receiving the found contract events
	sub  ethereum.Subscription // Subscription for errors, completion and termination
	done bool                  // Whether the subscription completed delivering logs
	fail error                 // Occurred error to stop iteration
}

// Next advances the iterator to the subsequent event, returning whether there
// are any more events found. In case of a retrieval or parsing error, false is
// returned and Error() can be queried for the exact failure.
func (it *AgentRegistryDeletedIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(AgentRegistryDeleted)
			if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
				it.fail = err
				return false
			}
			it.Event.Raw = log
			return true

		default:
			return false
		}
	}
	// Iterator still in progress, wait for either a data or an error event
	select {
	case log := <-it.logs:
		it.Event = new(AgentRegistryDeleted)
		if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
			it.fail = err
			return false
		}
		it.Event.Raw = log
		return true

	case err := <-it.sub.Err():
		it.done = true
		it.fail = err
		return it.Next()
	}
}

// Error returns any retrieval or parsing error occurred during filtering.
func (it *AgentRegistryDeletedIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *AgentRegistryDeletedIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// AgentRegistryDeleted represents a Deleted event raised by the AgentRegistry contract.
type AgentRegistryDeleted struct {
	Pub common.Address
	Raw types.Log // Blockchain specific contextual infos
}

// FilterDeleted is a free log retrieval operation binding the contract event 0x7fb2e49c6d2dcc748cced4be404df4b502a5091d84f32f62fa7821b5f9231f6b.
//
// Solidity: event Deleted(address pub)
func (_AgentRegistry *AgentRegistryFilterer) FilterDeleted(opts *bind.FilterOpts) (*AgentRegistryDeletedIterator, error) {

	logs, sub, err := _AgentRegistry.contract.FilterLogs(opts, "Deleted")
	if err != nil {
		return nil, err
	}
	return &AgentRegistryDeletedIterator{contract: _AgentRegistry.contract, event: "Deleted", logs: logs, sub: sub}, nil
}

// WatchDeleted is a free log subscription operation binding the contract event 0x7fb2e49c6d2dcc748cced4be404df4b502a5091d84f32f62fa7821b5f9231f6b.
//
// Solidity: event Deleted(address pub)
func (_AgentRegistry *AgentRegistryFilterer) WatchDeleted(opts *bind.WatchOpts, sink chan<- *AgentRegistryDeleted) (event.Subscription, error) {

	logs, sub, err := _AgentRegistry.contract.WatchLogs(opts, "Deleted")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(AgentRegistryDeleted)
				if err := _AgentRegistry.contract.UnpackLog(event, "Deleted", log); err != nil {
					return err
				}
				event.Raw = log

				select {
				case sink <- event:
				case err := <-sub.Err():
					return err
				case <-quit:
					return nil
				}
			case err := <-sub.Err():
				return err
			case <-quit:
				return nil
			}
		}
	}), nil
}

// ParseDeleted is a log parse operation binding the contract event 0x7fb2e49c6d2dcc748cced4be404df4b502a5091d84f32f62fa7821b5f9231f6b.
//
// Solidity: event Deleted(address pub)
func (_AgentRegistry *AgentRegistryFilterer) ParseDeleted(log types.Log) (*AgentRegistryDeleted, error) {
	event := new(AgentRegistryDeleted)
	if err := _AgentRegistry.contract.UnpackLog(event, "Deleted", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// AgentRegistryFeeUpdatedIterator is returned from FilterFeeUpdated and is used to iterate over the raw logs and unpacked data for FeeUpdated events raised by the AgentRegistry contract.
type AgentRegistryFeeUpdatedIterator struct {
	Event *AgentRegistryFeeUpdated // Event containing the contract specifics and raw log

	contract *bind.BoundContract // Generic contract to use for unpacking event data
	event    string              // Event name to use for unpacking event data

	logs chan types.Log        // Log channel receiving the found contract events
	sub  ethereum.Subscription // Subscription for errors, completion and termination
	done bool                  // Whether the subscription completed delivering logs
	fail error                 // Occurred error to stop iteration
}

// Next advances the iterator to the subsequent event, returning whether there
// are any more events found. In case of a retrieval or parsing error, false is
// returned and Error() can be queried for the exact failure.
func (it *AgentRegistryFeeUpdatedIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(AgentRegistryFeeUpdated)
			if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
				it.fail = err
				return false
			}
			it.Event.Raw = log
			return true

		default:
			return false
		}
	}
	// Iterator still in progress, wait for either a data or an error event
	select {
	case log := <-it.logs:
		it.Event = new(AgentRegistryFeeUpdated)
		if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
			it.fail = err
			return false
		}
		it.Event.Raw = log
		return true

	case err := <-it.sub.Err():
		it.done = true
		it.fail = err
		return it.Next()
	}
}

// Error returns any retrieval or parsing error occurred during filtering.
func (it *AgentRegistryFeeUpdatedIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *AgentRegistryFeeUpdatedIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// AgentRegistryFeeUpdated represents a FeeUpdated event raised by the AgentRegistry contract.
type AgentRegistryFeeUpdated struct {
	Pub    common.Address
	Name   string
	NewFee *big.Int
	Raw    types.Log // Blockchain specific contextual infos
}

// FilterFeeUpdated is a free log retrieval operation binding the contract event 0xe65b1a0f0203c10a67161b92db1350d95cf4b2ba05ebf3df76c927f2402b9a93.
//
// Solidity: event FeeUpdated(address pub, string name, uint256 newFee)
func (_AgentRegistry *AgentRegistryFilterer) FilterFeeUpdated(opts *bind.FilterOpts) (*AgentRegistryFeeUpdatedIterator, error) {

	logs, sub, err := _AgentRegistry.contract.FilterLogs(opts, "FeeUpdated")
	if err != nil {
		return nil, err
	}
	return &AgentRegistryFeeUpdatedIterator{contract: _AgentRegistry.contract, event: "FeeUpdated", logs: logs, sub: sub}, nil
}

// WatchFeeUpdated is a free log subscription operation binding the contract event 0xe65b1a0f0203c10a67161b92db1350d95cf4b2ba05ebf3df76c927f2402b9a93.
//
// Solidity: event FeeUpdated(address pub, string name, uint256 newFee)
func (_AgentRegistry *AgentRegistryFilterer) WatchFeeUpdated(opts *bind.WatchOpts, sink chan<- *AgentRegistryFeeUpdated) (event.Subscription, error) {

	logs, sub, err := _AgentRegistry.contract.WatchLogs(opts, "FeeUpdated")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(AgentRegistryFeeUpdated)
				if err := _AgentRegistry.contract.UnpackLog(event, "FeeUpdated", log); err != nil {
					return err
				}
				event.Raw = log

				select {
				case sink <- event:
				case err := <-sub.Err():
					return err
				case <-quit:
					return nil
				}
			case err := <-sub.Err():
				return err
			case <-quit:
				return nil
			}
		}
	}), nil
}

// ParseFeeUpdated is a log parse operation binding the contract event 0xe65b1a0f0203c10a67161b92db1350d95cf4b2ba05ebf3df76c927f2402b9a93.
//
// Solidity: event FeeUpdated(address pub, string name, uint256 newFee)
func (_AgentRegistry *AgentRegistryFilterer) ParseFeeUpdated(log types.Log) (*AgentRegistryFeeUpdated, error) {
	event := new(AgentRegistryFeeUpdated)
	if err := _AgentRegistry.contract.UnpackLog(event, "FeeUpdated", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// AgentRegistryOwnershipTransferredIterator is returned from FilterOwnershipTransferred and is used to iterate over the raw logs and unpacked data for OwnershipTransferred events raised by the AgentRegistry contract.
type AgentRegistryOwnershipTransferredIterator struct {
	Event *AgentRegistryOwnershipTransferred // Event containing the contract specifics and raw log

	contract *bind.BoundContract // Generic contract to use for unpacking event data
	event    string              // Event name to use for unpacking event data

	logs chan types.Log        // Log channel receiving the found contract events
	sub  ethereum.Subscription // Subscription for errors, completion and termination
	done bool                  // Whether the subscription completed delivering logs
	fail error                 // Occurred error to stop iteration
}

// Next advances the iterator to the subsequent event, returning whether there
// are any more events found. In case of a retrieval or parsing error, false is
// returned and Error() can be queried for the exact failure.
func (it *AgentRegistryOwnershipTransferredIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(AgentRegistryOwnershipTransferred)
			if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
				it.fail = err
				return false
			}
			it.Event.Raw = log
			return true

		default:
			return false
		}
	}
	// Iterator still in progress, wait for either a data or an error event
	select {
	case log := <-it.logs:
		it.Event = new(AgentRegistryOwnershipTransferred)
		if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
			it.fail = err
			return false
		}
		it.Event.Raw = log
		return true

	case err := <-it.sub.Err():
		it.done = true
		it.fail = err
		return it.Next()
	}
}

// Error returns any retrieval or parsing error occurred during filtering.
func (it *AgentRegistryOwnershipTransferredIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *AgentRegistryOwnershipTransferredIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// AgentRegistryOwnershipTransferred represents a OwnershipTransferred event raised by the AgentRegistry contract.
type AgentRegistryOwnershipTransferred struct {
	PreviousOwner common.Address
	NewOwner      common.Address
	Raw           types.Log // Blockchain specific contextual infos
}

// FilterOwnershipTransferred is a free log retrieval operation binding the contract event 0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0.
//
// Solidity: event OwnershipTransferred(address indexed previousOwner, address indexed newOwner)
func (_AgentRegistry *AgentRegistryFilterer) FilterOwnershipTransferred(opts *bind.FilterOpts, previousOwner []common.Address, newOwner []common.Address) (*AgentRegistryOwnershipTransferredIterator, error) {

	var previousOwnerRule []interface{}
	for _, previousOwnerItem := range previousOwner {
		previousOwnerRule = append(previousOwnerRule, previousOwnerItem)
	}
	var newOwnerRule []interface{}
	for _, newOwnerItem := range newOwner {
		newOwnerRule = append(newOwnerRule, newOwnerItem)
	}

	logs, sub, err := _AgentRegistry.contract.FilterLogs(opts, "OwnershipTransferred", previousOwnerRule, newOwnerRule)
	if err != nil {
		return nil, err
	}
	return &AgentRegistryOwnershipTransferredIterator{contract: _AgentRegistry.contract, event: "OwnershipTransferred", logs: logs, sub: sub}, nil
}

// WatchOwnershipTransferred is a free log subscription operation binding the contract event 0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0.
//
// Solidity: event OwnershipTransferred(address indexed previousOwner, address indexed newOwner)
func (_AgentRegistry *AgentRegistryFilterer) WatchOwnershipTransferred(opts *bind.WatchOpts, sink chan<- *AgentRegistryOwnershipTransferred, previousOwner []common.Address, newOwner []common.Address) (event.Subscription, error) {

	var previousOwnerRule []interface{}
	for _, previousOwnerItem := range previousOwner {
		previousOwnerRule = append(previousOwnerRule, previousOwnerItem)
	}
	var newOwnerRule []interface{}
	for _, newOwnerItem := range newOwner {
		newOwnerRule = append(newOwnerRule, newOwnerItem)
	}

	logs, sub, err := _AgentRegistry.contract.WatchLogs(opts, "OwnershipTransferred", previousOwnerRule, newOwnerRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(AgentRegistryOwnershipTransferred)
				if err := _AgentRegistry.contract.UnpackLog(event, "OwnershipTransferred", log); err != nil {
					return err
				}
				event.Raw = log

				select {
				case sink <- event:
				case err := <-sub.Err():
					return err
				case <-quit:
					return nil
				}
			case err := <-sub.Err():
				return err
			case <-quit:
				return nil
			}
		}
	}), nil
}

// ParseOwnershipTransferred is a log parse operation binding the contract event 0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0.
//
// Solidity: event OwnershipTransferred(address indexed previousOwner, address indexed newOwner)
func (_AgentRegistry *AgentRegistryFilterer) ParseOwnershipTransferred(log types.Log) (*AgentRegistryOwnershipTransferred, error) {
	event := new(AgentRegistryOwnershipTransferred)
	if err := _AgentRegistry.contract.UnpackLog(event, "OwnershipTransferred", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// AgentRegistryRegisteredIterator is returned from FilterRegistered and is used to iterate over the raw logs and unpacked data for Registered events raised by the AgentRegistry contract.
type AgentRegistryRegisteredIterator struct {
	Event *AgentRegistryRegistered // Event containing the contract specifics and raw log

	contract *bind.BoundContract // Generic contract to use for unpacking event data
	event    string              // Event name to use for unpacking event data

	logs chan types.Log        // Log channel receiving the found contract events
	sub  ethereum.Subscription // Subscription for errors, completion and termination
	done bool                  // Whether the subscription completed delivering logs
	fail error                 // Occurred error to stop iteration
}

// Next advances the iterator to the subsequent event, returning whether there
// are any more events found. In case of a retrieval or parsing error, false is
// returned and Error() can be queried for the exact failure.
func (it *AgentRegistryRegisteredIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(AgentRegistryRegistered)
			if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
				it.fail = err
				return false
			}
			it.Event.Raw = log
			return true

		default:
			return false
		}
	}
	// Iterator still in progress, wait for either a data or an error event
	select {
	case log := <-it.logs:
		it.Event = new(AgentRegistryRegistered)
		if err := it.contract.UnpackLog(it.Event, it.event, log); err != nil {
			it.fail = err
			return false
		}
		it.Event.Raw = log
		return true

	case err := <-it.sub.Err():
		it.done = true
		it.fail = err
		return it.Next()
	}
}

// Error returns any retrieval or parsing error occurred during filtering.
func (it *AgentRegistryRegisteredIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *AgentRegistryRegisteredIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// AgentRegistryRegistered represents a Registered event raised by the AgentRegistry contract.
type AgentRegistryRegistered struct {
	Pub  common.Address
	Name string
	Raw  types.Log // Blockchain specific contextual infos
}

// FilterRegistered is a free log retrieval operation binding the contract event 0xb3eccf73f39b1c07947c780b2b39df2a1bb058b4037b0a42d0881ca1a028a132.
//
// Solidity: event Registered(address pub, string name)
func (_AgentRegistry *AgentRegistryFilterer) FilterRegistered(opts *bind.FilterOpts) (*AgentRegistryRegisteredIterator, error) {

	logs, sub, err := _AgentRegistry.contract.FilterLogs(opts, "Registered")
	if err != nil {
		return nil, err
	}
	return &AgentRegistryRegisteredIterator{contract: _AgentRegistry.contract, event: "Registered", logs: logs, sub: sub}, nil
}

// WatchRegistered is a free log subscription operation binding the contract event 0xb3eccf73f39b1c07947c780b2b39df2a1bb058b4037b0a42d0881ca1a028a132.
//
// Solidity: event Registered(address pub, string name)
func (_AgentRegistry *AgentRegistryFilterer) WatchRegistered(opts *bind.WatchOpts, sink chan<- *AgentRegistryRegistered) (event.Subscription, error) {

	logs, sub, err := _AgentRegistry.contract.WatchLogs(opts, "Registered")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(AgentRegistryRegistered)
				if err := _AgentRegistry.contract.UnpackLog(event, "Registered", log); err != nil {
					return err
				}
				event.Raw = log

				select {
				case sink <- event:
				case err := <-sub.Err():
					return err
				case <-quit:
					return nil
				}
			case err := <-sub.Err():
				return err
			case <-quit:
				return nil
			}
		}
	}), nil
}

// ParseRegistered is a log parse operation binding the contract event 0xb3eccf73f39b1c07947c780b2b39df2a1bb058b4037b0a42d0881ca1a028a132.
//
// Solidity: event Registered(address pub, string name)
func (_AgentRegistry *AgentRegistryFilterer) ParseRegistered(log types.Log) (*AgentRegistryRegistered, error) {
	event := new(AgentRegistryRegistered)
	if err := _AgentRegistry.contract.UnpackLog(event, "Registered", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}
