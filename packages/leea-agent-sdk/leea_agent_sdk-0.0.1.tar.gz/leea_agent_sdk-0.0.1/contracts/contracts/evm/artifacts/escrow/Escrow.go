// Code generated - DO NOT EDIT.
// This file is a generated binding and any manual changes will be lost.

package escrow

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

// EscrowMetaData contains all meta data concerning the Escrow contract.
var EscrowMetaData = &bind.MetaData{
	ABI: "[{\"inputs\":[{\"internalType\":\"contractLeeaGlobalParams\",\"name\":\"globalParams\",\"type\":\"address\"},{\"internalType\":\"contractERC20\",\"name\":\"leeaToken\",\"type\":\"address\"},{\"internalType\":\"contractAgentRegistry\",\"name\":\"agentRegistry\",\"type\":\"address\"},{\"internalType\":\"contractValidatorStaking\",\"name\":\"validatorStaking\",\"type\":\"address\"},{\"internalType\":\"address\",\"name\":\"initialOwner\",\"type\":\"address\"}],\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"owner\",\"type\":\"address\"}],\"name\":\"OwnableInvalidOwner\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"account\",\"type\":\"address\"}],\"name\":\"OwnableUnauthorizedAccount\",\"type\":\"error\"},{\"inputs\":[],\"name\":\"ReentrancyGuardReentrantCall\",\"type\":\"error\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"address\",\"name\":\"user\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"escrow\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"token\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"amount\",\"type\":\"uint256\"}],\"name\":\"Deposited\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"address\",\"name\":\"user\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"address\",\"name\":\"agent\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"escrow\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"token\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"amount\",\"type\":\"uint256\"}],\"name\":\"FeePaid\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"internalType\":\"address\",\"name\":\"previousOwner\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"newOwner\",\"type\":\"address\"}],\"name\":\"OwnershipTransferred\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"address\",\"name\":\"user\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"escrow\",\"type\":\"address\"},{\"indexed\":true,\"internalType\":\"address\",\"name\":\"token\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"amount\",\"type\":\"uint256\"}],\"name\":\"Withdrawn\",\"type\":\"event\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"_amount\",\"type\":\"uint256\"}],\"name\":\"deposit\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"owner\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"user\",\"type\":\"address\"},{\"internalType\":\"address\",\"name\":\"agent\",\"type\":\"address\"}],\"name\":\"payFee\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"renounceOwnership\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"newOwner\",\"type\":\"address\"}],\"name\":\"transferOwnership\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"_user\",\"type\":\"address\"}],\"name\":\"withdrawFullAmount\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"}]",
	Bin: "0x608060405234801561001057600080fd5b50604051610f89380380610f8983398101604081905261002f9161012a565b806001600160a01b03811661005e57604051631e4fbdf760e01b81526000600482015260240160405180910390fd5b610067816100c2565b505060018055600380546001600160a01b03199081166001600160a01b03958616179091556004805482169385169390931790925560058054831694841694909417909355600680549091169290911691909117905561019f565b600080546001600160a01b038381166001600160a01b0319831681178455604051919092169283917f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e09190a35050565b6001600160a01b038116811461012757600080fd5b50565b600080600080600060a0868803121561014257600080fd5b855161014d81610112565b602087015190955061015e81610112565b604087015190945061016f81610112565b606087015190935061018081610112565b608087015190925061019181610112565b809150509295509295909350565b610ddb806101ae6000396000f3fe608060405234801561001057600080fd5b50600436106100625760003560e01c8063537dabd1146100675780635e0ac3801461007c578063715018a61461008f5780638da5cb5b14610097578063b6b55f25146100b6578063f2fde38b146100c9575b600080fd5b61007a610075366004610c2c565b6100dc565b005b61007a61008a366004610c5f565b610579565b61007a61075a565b600054604080516001600160a01b039092168252519081900360200190f35b61007a6100c4366004610c7a565b61076e565b61007a6100d7366004610c5f565b610a60565b6100e4610a9b565b6100ec610ac5565b600480546040516307feec1960e21b81526001600160a01b0384811693820193909352911690631ffbb06490602401602060405180830381865afa158015610138573d6000803e3d6000fd5b505050506040513d601f19601f8201168201806040525081019061015c9190610c93565b6101ad5760405162461bcd60e51b815260206004820152601760248201527f4167656e74206973206e6f74207265676973746572656400000000000000000060448201526064015b60405180910390fd5b60048054604051635e5a3f4d60e11b81526001600160a01b03848116938201939093526000929091169063bcb47e9a90602401602060405180830381865afa1580156101fd573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906102219190610cb5565b60055460408051631439842d60e21b8152815193945060009384936001600160a01b0316926350e610b492600480820193918290030181865afa15801561026c573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906102909190610cce565b9150915060006102a1848484610af2565b905060006102af8286610d08565b6001600160a01b0388166000908152600260205260409020549091508111156103125760405162461bcd60e51b815260206004820152601560248201527442616c616e6365206c657373207468616e2066656560581b60448201526064016101a4565b6003546040516370a0823160e01b815230600482015282916001600160a01b0316906370a0823190602401602060405180830381865afa15801561035a573d6000803e3d6000fd5b505050506040513d601f19601f8201168201806040525081019061037e9190610cb5565b116103cb5760405162461bcd60e51b815260206004820152601960248201527f4e6f7420656e6f75676820657363726f772062616c616e63650000000000000060448201526064016101a4565b6003546040516323b872dd60e01b81526001600160a01b03909116906323b872dd906103ff9030908a908a90600401610d21565b6020604051808303816000875af115801561041e573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906104429190610c93565b61045e5760405162461bcd60e51b81526004016101a490610d45565b6003546006546040516323b872dd60e01b81526001600160a01b03928316926323b872dd92610497923092909116908790600401610d21565b6020604051808303816000875af11580156104b6573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906104da9190610c93565b6104f65760405162461bcd60e51b81526004016101a490610d45565b3360009081526002602052604081208054839290610515908490610d7c565b90915550506003546040516001600160a01b039091169030907f4c62e1a244d85ca35db361def13d4f2a642285892bb639d4041b7efab0bd4c8e9061055f908b908b908790610d21565b60405180910390a3505050505061057560018055565b5050565b610581610a9b565b6000546001600160a01b031633146105d35760405162461bcd60e51b815260206004820152601560248201527413db9b1e481bdddb995c881a5cc8185b1b1bddd959605a1b60448201526064016101a4565b6001600160a01b03811660009081526002602052604090205461062a5760405162461bcd60e51b815260206004820152600f60248201526e42616c616e6365206973207a65726f60881b60448201526064016101a4565b6001600160a01b03808216600090815260026020526040908190205460035491516323b872dd60e01b8152909291909116906323b872dd9061067490309086908690600401610d21565b6020604051808303816000875af1158015610693573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906106b79190610c93565b6107035760405162461bcd60e51b815260206004820152601c60248201527f43616e74207472616e7366657220746f6b656e7320746f20757365720000000060448201526064016101a4565b600354604080516001600160a01b03858116825260208201859052825193169230927fa4195c37c2947bbe89165f03e320b6903116f0b10d8cfdb522330f7ce6f9fa24928290030190a35061075760018055565b50565b610762610ac5565b61076c6000610bae565b565b600081116107cf5760405162461bcd60e51b815260206004820152602860248201527f596f75206e65656420746f206465706f736974206174206c6561737420736f6d6044820152676520746f6b656e7360c01b60648201526084016101a4565b6003546040516370a0823160e01b815233600482015282916001600160a01b0316906370a0823190602401602060405180830381865afa158015610817573d6000803e3d6000fd5b505050506040513d601f19601f8201168201806040525081019061083b9190610cb5565b1161089b5760405162461bcd60e51b815260206004820152602a60248201527f596f75206e65656420746f2068617665206174206c6561737420616d6f756e74604482015269206f6620746f6b656e7360b01b60648201526084016101a4565b60035460405163095ea7b360e01b8152306004820152602481018390526001600160a01b039091169063095ea7b3906044016020604051808303816000875af11580156108ec573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906109109190610c93565b61095c5760405162461bcd60e51b815260206004820152601d60248201527f43616e7420617070726f766520746f6b656e7320746f20657363726f7700000060448201526064016101a4565b6003546040516323b872dd60e01b81526001600160a01b03909116906323b872dd9061099090339030908690600401610d21565b6020604051808303816000875af11580156109af573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906109d39190610c93565b6109ef5760405162461bcd60e51b81526004016101a490610d45565b3360009081526002602052604081208054839290610a0e908490610d08565b909155505060035460408051338152602081018490526001600160a01b039092169130917f4174a9435a04d04d274c76779cad136a41fde6937c56241c09ab9d3c7064a1a9910160405180910390a350565b610a68610ac5565b6001600160a01b038116610a9257604051631e4fbdf760e01b8152600060048201526024016101a4565b61075781610bae565b600260015403610abe57604051633ee5aeb560e01b815260040160405180910390fd5b6002600155565b6000546001600160a01b0316331461076c5760405163118cdaa760e01b81523360048201526024016101a4565b6000838302816000198587098281108382030391505080600003610b2957838281610b1f57610b1f610d8f565b0492505050610ba7565b808411610b4057610b406003851502601118610bfe565b6000848688096000868103871696879004966002600389028118808a02820302808a02820302808a02820302808a02820302808a02820302808a02909103029181900381900460010186841190950394909402919094039290920491909117919091029150505b9392505050565b600080546001600160a01b038381166001600160a01b0319831681178455604051919092169283917f8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e09190a35050565b634e487b71600052806020526024601cfd5b80356001600160a01b0381168114610c2757600080fd5b919050565b60008060408385031215610c3f57600080fd5b610c4883610c10565b9150610c5660208401610c10565b90509250929050565b600060208284031215610c7157600080fd5b610ba782610c10565b600060208284031215610c8c57600080fd5b5035919050565b600060208284031215610ca557600080fd5b81518015158114610ba757600080fd5b600060208284031215610cc757600080fd5b5051919050565b60008060408385031215610ce157600080fd5b505080516020909101519092909150565b634e487b7160e01b600052601160045260246000fd5b80820180821115610d1b57610d1b610cf2565b92915050565b6001600160a01b039384168152919092166020820152604081019190915260600190565b6020808252601e908201527f43616e74207472616e7366657220746f6b656e7320746f20657363726f770000604082015260600190565b81810381811115610d1b57610d1b610cf2565b634e487b7160e01b600052601260045260246000fdfea2646970667358221220fe58980aa3175e473dd018d61fe43b72ebf5fab385d3ee39c4ec08399004907264736f6c634300081c0033",
}

// EscrowABI is the input ABI used to generate the binding from.
// Deprecated: Use EscrowMetaData.ABI instead.
var EscrowABI = EscrowMetaData.ABI

// EscrowBin is the compiled bytecode used for deploying new contracts.
// Deprecated: Use EscrowMetaData.Bin instead.
var EscrowBin = EscrowMetaData.Bin

// DeployEscrow deploys a new Ethereum contract, binding an instance of Escrow to it.
func DeployEscrow(auth *bind.TransactOpts, backend bind.ContractBackend, globalParams common.Address, leeaToken common.Address, agentRegistry common.Address, validatorStaking common.Address, initialOwner common.Address) (common.Address, *types.Transaction, *Escrow, error) {
	parsed, err := EscrowMetaData.GetAbi()
	if err != nil {
		return common.Address{}, nil, nil, err
	}
	if parsed == nil {
		return common.Address{}, nil, nil, errors.New("GetABI returned nil")
	}

	address, tx, contract, err := bind.DeployContract(auth, *parsed, common.FromHex(EscrowBin), backend, globalParams, leeaToken, agentRegistry, validatorStaking, initialOwner)
	if err != nil {
		return common.Address{}, nil, nil, err
	}
	return address, tx, &Escrow{EscrowCaller: EscrowCaller{contract: contract}, EscrowTransactor: EscrowTransactor{contract: contract}, EscrowFilterer: EscrowFilterer{contract: contract}}, nil
}

// Escrow is an auto generated Go binding around an Ethereum contract.
type Escrow struct {
	EscrowCaller     // Read-only binding to the contract
	EscrowTransactor // Write-only binding to the contract
	EscrowFilterer   // Log filterer for contract events
}

// EscrowCaller is an auto generated read-only Go binding around an Ethereum contract.
type EscrowCaller struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// EscrowTransactor is an auto generated write-only Go binding around an Ethereum contract.
type EscrowTransactor struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// EscrowFilterer is an auto generated log filtering Go binding around an Ethereum contract events.
type EscrowFilterer struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// EscrowSession is an auto generated Go binding around an Ethereum contract,
// with pre-set call and transact options.
type EscrowSession struct {
	Contract     *Escrow           // Generic contract binding to set the session for
	CallOpts     bind.CallOpts     // Call options to use throughout this session
	TransactOpts bind.TransactOpts // Transaction auth options to use throughout this session
}

// EscrowCallerSession is an auto generated read-only Go binding around an Ethereum contract,
// with pre-set call options.
type EscrowCallerSession struct {
	Contract *EscrowCaller // Generic contract caller binding to set the session for
	CallOpts bind.CallOpts // Call options to use throughout this session
}

// EscrowTransactorSession is an auto generated write-only Go binding around an Ethereum contract,
// with pre-set transact options.
type EscrowTransactorSession struct {
	Contract     *EscrowTransactor // Generic contract transactor binding to set the session for
	TransactOpts bind.TransactOpts // Transaction auth options to use throughout this session
}

// EscrowRaw is an auto generated low-level Go binding around an Ethereum contract.
type EscrowRaw struct {
	Contract *Escrow // Generic contract binding to access the raw methods on
}

// EscrowCallerRaw is an auto generated low-level read-only Go binding around an Ethereum contract.
type EscrowCallerRaw struct {
	Contract *EscrowCaller // Generic read-only contract binding to access the raw methods on
}

// EscrowTransactorRaw is an auto generated low-level write-only Go binding around an Ethereum contract.
type EscrowTransactorRaw struct {
	Contract *EscrowTransactor // Generic write-only contract binding to access the raw methods on
}

// NewEscrow creates a new instance of Escrow, bound to a specific deployed contract.
func NewEscrow(address common.Address, backend bind.ContractBackend) (*Escrow, error) {
	contract, err := bindEscrow(address, backend, backend, backend)
	if err != nil {
		return nil, err
	}
	return &Escrow{EscrowCaller: EscrowCaller{contract: contract}, EscrowTransactor: EscrowTransactor{contract: contract}, EscrowFilterer: EscrowFilterer{contract: contract}}, nil
}

// NewEscrowCaller creates a new read-only instance of Escrow, bound to a specific deployed contract.
func NewEscrowCaller(address common.Address, caller bind.ContractCaller) (*EscrowCaller, error) {
	contract, err := bindEscrow(address, caller, nil, nil)
	if err != nil {
		return nil, err
	}
	return &EscrowCaller{contract: contract}, nil
}

// NewEscrowTransactor creates a new write-only instance of Escrow, bound to a specific deployed contract.
func NewEscrowTransactor(address common.Address, transactor bind.ContractTransactor) (*EscrowTransactor, error) {
	contract, err := bindEscrow(address, nil, transactor, nil)
	if err != nil {
		return nil, err
	}
	return &EscrowTransactor{contract: contract}, nil
}

// NewEscrowFilterer creates a new log filterer instance of Escrow, bound to a specific deployed contract.
func NewEscrowFilterer(address common.Address, filterer bind.ContractFilterer) (*EscrowFilterer, error) {
	contract, err := bindEscrow(address, nil, nil, filterer)
	if err != nil {
		return nil, err
	}
	return &EscrowFilterer{contract: contract}, nil
}

// bindEscrow binds a generic wrapper to an already deployed contract.
func bindEscrow(address common.Address, caller bind.ContractCaller, transactor bind.ContractTransactor, filterer bind.ContractFilterer) (*bind.BoundContract, error) {
	parsed, err := EscrowMetaData.GetAbi()
	if err != nil {
		return nil, err
	}
	return bind.NewBoundContract(address, *parsed, caller, transactor, filterer), nil
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_Escrow *EscrowRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _Escrow.Contract.EscrowCaller.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_Escrow *EscrowRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Escrow.Contract.EscrowTransactor.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_Escrow *EscrowRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _Escrow.Contract.EscrowTransactor.contract.Transact(opts, method, params...)
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_Escrow *EscrowCallerRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _Escrow.Contract.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_Escrow *EscrowTransactorRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Escrow.Contract.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_Escrow *EscrowTransactorRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _Escrow.Contract.contract.Transact(opts, method, params...)
}

// Owner is a free data retrieval call binding the contract method 0x8da5cb5b.
//
// Solidity: function owner() view returns(address)
func (_Escrow *EscrowCaller) Owner(opts *bind.CallOpts) (common.Address, error) {
	var out []interface{}
	err := _Escrow.contract.Call(opts, &out, "owner")

	if err != nil {
		return *new(common.Address), err
	}

	out0 := *abi.ConvertType(out[0], new(common.Address)).(*common.Address)

	return out0, err

}

// Owner is a free data retrieval call binding the contract method 0x8da5cb5b.
//
// Solidity: function owner() view returns(address)
func (_Escrow *EscrowSession) Owner() (common.Address, error) {
	return _Escrow.Contract.Owner(&_Escrow.CallOpts)
}

// Owner is a free data retrieval call binding the contract method 0x8da5cb5b.
//
// Solidity: function owner() view returns(address)
func (_Escrow *EscrowCallerSession) Owner() (common.Address, error) {
	return _Escrow.Contract.Owner(&_Escrow.CallOpts)
}

// Deposit is a paid mutator transaction binding the contract method 0xb6b55f25.
//
// Solidity: function deposit(uint256 _amount) returns()
func (_Escrow *EscrowTransactor) Deposit(opts *bind.TransactOpts, _amount *big.Int) (*types.Transaction, error) {
	return _Escrow.contract.Transact(opts, "deposit", _amount)
}

// Deposit is a paid mutator transaction binding the contract method 0xb6b55f25.
//
// Solidity: function deposit(uint256 _amount) returns()
func (_Escrow *EscrowSession) Deposit(_amount *big.Int) (*types.Transaction, error) {
	return _Escrow.Contract.Deposit(&_Escrow.TransactOpts, _amount)
}

// Deposit is a paid mutator transaction binding the contract method 0xb6b55f25.
//
// Solidity: function deposit(uint256 _amount) returns()
func (_Escrow *EscrowTransactorSession) Deposit(_amount *big.Int) (*types.Transaction, error) {
	return _Escrow.Contract.Deposit(&_Escrow.TransactOpts, _amount)
}

// PayFee is a paid mutator transaction binding the contract method 0x537dabd1.
//
// Solidity: function payFee(address user, address agent) returns()
func (_Escrow *EscrowTransactor) PayFee(opts *bind.TransactOpts, user common.Address, agent common.Address) (*types.Transaction, error) {
	return _Escrow.contract.Transact(opts, "payFee", user, agent)
}

// PayFee is a paid mutator transaction binding the contract method 0x537dabd1.
//
// Solidity: function payFee(address user, address agent) returns()
func (_Escrow *EscrowSession) PayFee(user common.Address, agent common.Address) (*types.Transaction, error) {
	return _Escrow.Contract.PayFee(&_Escrow.TransactOpts, user, agent)
}

// PayFee is a paid mutator transaction binding the contract method 0x537dabd1.
//
// Solidity: function payFee(address user, address agent) returns()
func (_Escrow *EscrowTransactorSession) PayFee(user common.Address, agent common.Address) (*types.Transaction, error) {
	return _Escrow.Contract.PayFee(&_Escrow.TransactOpts, user, agent)
}

// RenounceOwnership is a paid mutator transaction binding the contract method 0x715018a6.
//
// Solidity: function renounceOwnership() returns()
func (_Escrow *EscrowTransactor) RenounceOwnership(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _Escrow.contract.Transact(opts, "renounceOwnership")
}

// RenounceOwnership is a paid mutator transaction binding the contract method 0x715018a6.
//
// Solidity: function renounceOwnership() returns()
func (_Escrow *EscrowSession) RenounceOwnership() (*types.Transaction, error) {
	return _Escrow.Contract.RenounceOwnership(&_Escrow.TransactOpts)
}

// RenounceOwnership is a paid mutator transaction binding the contract method 0x715018a6.
//
// Solidity: function renounceOwnership() returns()
func (_Escrow *EscrowTransactorSession) RenounceOwnership() (*types.Transaction, error) {
	return _Escrow.Contract.RenounceOwnership(&_Escrow.TransactOpts)
}

// TransferOwnership is a paid mutator transaction binding the contract method 0xf2fde38b.
//
// Solidity: function transferOwnership(address newOwner) returns()
func (_Escrow *EscrowTransactor) TransferOwnership(opts *bind.TransactOpts, newOwner common.Address) (*types.Transaction, error) {
	return _Escrow.contract.Transact(opts, "transferOwnership", newOwner)
}

// TransferOwnership is a paid mutator transaction binding the contract method 0xf2fde38b.
//
// Solidity: function transferOwnership(address newOwner) returns()
func (_Escrow *EscrowSession) TransferOwnership(newOwner common.Address) (*types.Transaction, error) {
	return _Escrow.Contract.TransferOwnership(&_Escrow.TransactOpts, newOwner)
}

// TransferOwnership is a paid mutator transaction binding the contract method 0xf2fde38b.
//
// Solidity: function transferOwnership(address newOwner) returns()
func (_Escrow *EscrowTransactorSession) TransferOwnership(newOwner common.Address) (*types.Transaction, error) {
	return _Escrow.Contract.TransferOwnership(&_Escrow.TransactOpts, newOwner)
}

// WithdrawFullAmount is a paid mutator transaction binding the contract method 0x5e0ac380.
//
// Solidity: function withdrawFullAmount(address _user) returns()
func (_Escrow *EscrowTransactor) WithdrawFullAmount(opts *bind.TransactOpts, _user common.Address) (*types.Transaction, error) {
	return _Escrow.contract.Transact(opts, "withdrawFullAmount", _user)
}

// WithdrawFullAmount is a paid mutator transaction binding the contract method 0x5e0ac380.
//
// Solidity: function withdrawFullAmount(address _user) returns()
func (_Escrow *EscrowSession) WithdrawFullAmount(_user common.Address) (*types.Transaction, error) {
	return _Escrow.Contract.WithdrawFullAmount(&_Escrow.TransactOpts, _user)
}

// WithdrawFullAmount is a paid mutator transaction binding the contract method 0x5e0ac380.
//
// Solidity: function withdrawFullAmount(address _user) returns()
func (_Escrow *EscrowTransactorSession) WithdrawFullAmount(_user common.Address) (*types.Transaction, error) {
	return _Escrow.Contract.WithdrawFullAmount(&_Escrow.TransactOpts, _user)
}

// EscrowDepositedIterator is returned from FilterDeposited and is used to iterate over the raw logs and unpacked data for Deposited events raised by the Escrow contract.
type EscrowDepositedIterator struct {
	Event *EscrowDeposited // Event containing the contract specifics and raw log

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
func (it *EscrowDepositedIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(EscrowDeposited)
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
		it.Event = new(EscrowDeposited)
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
func (it *EscrowDepositedIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *EscrowDepositedIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// EscrowDeposited represents a Deposited event raised by the Escrow contract.
type EscrowDeposited struct {
	User   common.Address
	Escrow common.Address
	Token  common.Address
	Amount *big.Int
	Raw    types.Log // Blockchain specific contextual infos
}

// FilterDeposited is a free log retrieval operation binding the contract event 0x4174a9435a04d04d274c76779cad136a41fde6937c56241c09ab9d3c7064a1a9.
//
// Solidity: event Deposited(address user, address indexed escrow, address indexed token, uint256 amount)
func (_Escrow *EscrowFilterer) FilterDeposited(opts *bind.FilterOpts, escrow []common.Address, token []common.Address) (*EscrowDepositedIterator, error) {

	var escrowRule []interface{}
	for _, escrowItem := range escrow {
		escrowRule = append(escrowRule, escrowItem)
	}
	var tokenRule []interface{}
	for _, tokenItem := range token {
		tokenRule = append(tokenRule, tokenItem)
	}

	logs, sub, err := _Escrow.contract.FilterLogs(opts, "Deposited", escrowRule, tokenRule)
	if err != nil {
		return nil, err
	}
	return &EscrowDepositedIterator{contract: _Escrow.contract, event: "Deposited", logs: logs, sub: sub}, nil
}

// WatchDeposited is a free log subscription operation binding the contract event 0x4174a9435a04d04d274c76779cad136a41fde6937c56241c09ab9d3c7064a1a9.
//
// Solidity: event Deposited(address user, address indexed escrow, address indexed token, uint256 amount)
func (_Escrow *EscrowFilterer) WatchDeposited(opts *bind.WatchOpts, sink chan<- *EscrowDeposited, escrow []common.Address, token []common.Address) (event.Subscription, error) {

	var escrowRule []interface{}
	for _, escrowItem := range escrow {
		escrowRule = append(escrowRule, escrowItem)
	}
	var tokenRule []interface{}
	for _, tokenItem := range token {
		tokenRule = append(tokenRule, tokenItem)
	}

	logs, sub, err := _Escrow.contract.WatchLogs(opts, "Deposited", escrowRule, tokenRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(EscrowDeposited)
				if err := _Escrow.contract.UnpackLog(event, "Deposited", log); err != nil {
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

// ParseDeposited is a log parse operation binding the contract event 0x4174a9435a04d04d274c76779cad136a41fde6937c56241c09ab9d3c7064a1a9.
//
// Solidity: event Deposited(address user, address indexed escrow, address indexed token, uint256 amount)
func (_Escrow *EscrowFilterer) ParseDeposited(log types.Log) (*EscrowDeposited, error) {
	event := new(EscrowDeposited)
	if err := _Escrow.contract.UnpackLog(event, "Deposited", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// EscrowFeePaidIterator is returned from FilterFeePaid and is used to iterate over the raw logs and unpacked data for FeePaid events raised by the Escrow contract.
type EscrowFeePaidIterator struct {
	Event *EscrowFeePaid // Event containing the contract specifics and raw log

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
func (it *EscrowFeePaidIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(EscrowFeePaid)
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
		it.Event = new(EscrowFeePaid)
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
func (it *EscrowFeePaidIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *EscrowFeePaidIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// EscrowFeePaid represents a FeePaid event raised by the Escrow contract.
type EscrowFeePaid struct {
	User   common.Address
	Agent  common.Address
	Escrow common.Address
	Token  common.Address
	Amount *big.Int
	Raw    types.Log // Blockchain specific contextual infos
}

// FilterFeePaid is a free log retrieval operation binding the contract event 0x4c62e1a244d85ca35db361def13d4f2a642285892bb639d4041b7efab0bd4c8e.
//
// Solidity: event FeePaid(address user, address agent, address indexed escrow, address indexed token, uint256 amount)
func (_Escrow *EscrowFilterer) FilterFeePaid(opts *bind.FilterOpts, escrow []common.Address, token []common.Address) (*EscrowFeePaidIterator, error) {

	var escrowRule []interface{}
	for _, escrowItem := range escrow {
		escrowRule = append(escrowRule, escrowItem)
	}
	var tokenRule []interface{}
	for _, tokenItem := range token {
		tokenRule = append(tokenRule, tokenItem)
	}

	logs, sub, err := _Escrow.contract.FilterLogs(opts, "FeePaid", escrowRule, tokenRule)
	if err != nil {
		return nil, err
	}
	return &EscrowFeePaidIterator{contract: _Escrow.contract, event: "FeePaid", logs: logs, sub: sub}, nil
}

// WatchFeePaid is a free log subscription operation binding the contract event 0x4c62e1a244d85ca35db361def13d4f2a642285892bb639d4041b7efab0bd4c8e.
//
// Solidity: event FeePaid(address user, address agent, address indexed escrow, address indexed token, uint256 amount)
func (_Escrow *EscrowFilterer) WatchFeePaid(opts *bind.WatchOpts, sink chan<- *EscrowFeePaid, escrow []common.Address, token []common.Address) (event.Subscription, error) {

	var escrowRule []interface{}
	for _, escrowItem := range escrow {
		escrowRule = append(escrowRule, escrowItem)
	}
	var tokenRule []interface{}
	for _, tokenItem := range token {
		tokenRule = append(tokenRule, tokenItem)
	}

	logs, sub, err := _Escrow.contract.WatchLogs(opts, "FeePaid", escrowRule, tokenRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(EscrowFeePaid)
				if err := _Escrow.contract.UnpackLog(event, "FeePaid", log); err != nil {
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

// ParseFeePaid is a log parse operation binding the contract event 0x4c62e1a244d85ca35db361def13d4f2a642285892bb639d4041b7efab0bd4c8e.
//
// Solidity: event FeePaid(address user, address agent, address indexed escrow, address indexed token, uint256 amount)
func (_Escrow *EscrowFilterer) ParseFeePaid(log types.Log) (*EscrowFeePaid, error) {
	event := new(EscrowFeePaid)
	if err := _Escrow.contract.UnpackLog(event, "FeePaid", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// EscrowOwnershipTransferredIterator is returned from FilterOwnershipTransferred and is used to iterate over the raw logs and unpacked data for OwnershipTransferred events raised by the Escrow contract.
type EscrowOwnershipTransferredIterator struct {
	Event *EscrowOwnershipTransferred // Event containing the contract specifics and raw log

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
func (it *EscrowOwnershipTransferredIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(EscrowOwnershipTransferred)
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
		it.Event = new(EscrowOwnershipTransferred)
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
func (it *EscrowOwnershipTransferredIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *EscrowOwnershipTransferredIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// EscrowOwnershipTransferred represents a OwnershipTransferred event raised by the Escrow contract.
type EscrowOwnershipTransferred struct {
	PreviousOwner common.Address
	NewOwner      common.Address
	Raw           types.Log // Blockchain specific contextual infos
}

// FilterOwnershipTransferred is a free log retrieval operation binding the contract event 0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0.
//
// Solidity: event OwnershipTransferred(address indexed previousOwner, address indexed newOwner)
func (_Escrow *EscrowFilterer) FilterOwnershipTransferred(opts *bind.FilterOpts, previousOwner []common.Address, newOwner []common.Address) (*EscrowOwnershipTransferredIterator, error) {

	var previousOwnerRule []interface{}
	for _, previousOwnerItem := range previousOwner {
		previousOwnerRule = append(previousOwnerRule, previousOwnerItem)
	}
	var newOwnerRule []interface{}
	for _, newOwnerItem := range newOwner {
		newOwnerRule = append(newOwnerRule, newOwnerItem)
	}

	logs, sub, err := _Escrow.contract.FilterLogs(opts, "OwnershipTransferred", previousOwnerRule, newOwnerRule)
	if err != nil {
		return nil, err
	}
	return &EscrowOwnershipTransferredIterator{contract: _Escrow.contract, event: "OwnershipTransferred", logs: logs, sub: sub}, nil
}

// WatchOwnershipTransferred is a free log subscription operation binding the contract event 0x8be0079c531659141344cd1fd0a4f28419497f9722a3daafe3b4186f6b6457e0.
//
// Solidity: event OwnershipTransferred(address indexed previousOwner, address indexed newOwner)
func (_Escrow *EscrowFilterer) WatchOwnershipTransferred(opts *bind.WatchOpts, sink chan<- *EscrowOwnershipTransferred, previousOwner []common.Address, newOwner []common.Address) (event.Subscription, error) {

	var previousOwnerRule []interface{}
	for _, previousOwnerItem := range previousOwner {
		previousOwnerRule = append(previousOwnerRule, previousOwnerItem)
	}
	var newOwnerRule []interface{}
	for _, newOwnerItem := range newOwner {
		newOwnerRule = append(newOwnerRule, newOwnerItem)
	}

	logs, sub, err := _Escrow.contract.WatchLogs(opts, "OwnershipTransferred", previousOwnerRule, newOwnerRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(EscrowOwnershipTransferred)
				if err := _Escrow.contract.UnpackLog(event, "OwnershipTransferred", log); err != nil {
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
func (_Escrow *EscrowFilterer) ParseOwnershipTransferred(log types.Log) (*EscrowOwnershipTransferred, error) {
	event := new(EscrowOwnershipTransferred)
	if err := _Escrow.contract.UnpackLog(event, "OwnershipTransferred", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// EscrowWithdrawnIterator is returned from FilterWithdrawn and is used to iterate over the raw logs and unpacked data for Withdrawn events raised by the Escrow contract.
type EscrowWithdrawnIterator struct {
	Event *EscrowWithdrawn // Event containing the contract specifics and raw log

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
func (it *EscrowWithdrawnIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(EscrowWithdrawn)
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
		it.Event = new(EscrowWithdrawn)
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
func (it *EscrowWithdrawnIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *EscrowWithdrawnIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// EscrowWithdrawn represents a Withdrawn event raised by the Escrow contract.
type EscrowWithdrawn struct {
	User   common.Address
	Escrow common.Address
	Token  common.Address
	Amount *big.Int
	Raw    types.Log // Blockchain specific contextual infos
}

// FilterWithdrawn is a free log retrieval operation binding the contract event 0xa4195c37c2947bbe89165f03e320b6903116f0b10d8cfdb522330f7ce6f9fa24.
//
// Solidity: event Withdrawn(address user, address indexed escrow, address indexed token, uint256 amount)
func (_Escrow *EscrowFilterer) FilterWithdrawn(opts *bind.FilterOpts, escrow []common.Address, token []common.Address) (*EscrowWithdrawnIterator, error) {

	var escrowRule []interface{}
	for _, escrowItem := range escrow {
		escrowRule = append(escrowRule, escrowItem)
	}
	var tokenRule []interface{}
	for _, tokenItem := range token {
		tokenRule = append(tokenRule, tokenItem)
	}

	logs, sub, err := _Escrow.contract.FilterLogs(opts, "Withdrawn", escrowRule, tokenRule)
	if err != nil {
		return nil, err
	}
	return &EscrowWithdrawnIterator{contract: _Escrow.contract, event: "Withdrawn", logs: logs, sub: sub}, nil
}

// WatchWithdrawn is a free log subscription operation binding the contract event 0xa4195c37c2947bbe89165f03e320b6903116f0b10d8cfdb522330f7ce6f9fa24.
//
// Solidity: event Withdrawn(address user, address indexed escrow, address indexed token, uint256 amount)
func (_Escrow *EscrowFilterer) WatchWithdrawn(opts *bind.WatchOpts, sink chan<- *EscrowWithdrawn, escrow []common.Address, token []common.Address) (event.Subscription, error) {

	var escrowRule []interface{}
	for _, escrowItem := range escrow {
		escrowRule = append(escrowRule, escrowItem)
	}
	var tokenRule []interface{}
	for _, tokenItem := range token {
		tokenRule = append(tokenRule, tokenItem)
	}

	logs, sub, err := _Escrow.contract.WatchLogs(opts, "Withdrawn", escrowRule, tokenRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(EscrowWithdrawn)
				if err := _Escrow.contract.UnpackLog(event, "Withdrawn", log); err != nil {
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

// ParseWithdrawn is a log parse operation binding the contract event 0xa4195c37c2947bbe89165f03e320b6903116f0b10d8cfdb522330f7ce6f9fa24.
//
// Solidity: event Withdrawn(address user, address indexed escrow, address indexed token, uint256 amount)
func (_Escrow *EscrowFilterer) ParseWithdrawn(log types.Log) (*EscrowWithdrawn, error) {
	event := new(EscrowWithdrawn)
	if err := _Escrow.contract.UnpackLog(event, "Withdrawn", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}
