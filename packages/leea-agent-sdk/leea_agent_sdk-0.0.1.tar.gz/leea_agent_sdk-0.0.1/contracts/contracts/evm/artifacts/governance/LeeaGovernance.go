// Code generated - DO NOT EDIT.
// This file is a generated binding and any manual changes will be lost.

package governance

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

// LeeaGovernanceMetaData contains all meta data concerning the LeeaGovernance contract.
var LeeaGovernanceMetaData = &bind.MetaData{
	ABI: "[{\"inputs\":[{\"internalType\":\"contractIVotes\",\"name\":\"_token\",\"type\":\"address\"}],\"stateMutability\":\"nonpayable\",\"type\":\"constructor\"},{\"inputs\":[],\"name\":\"CheckpointUnorderedInsertion\",\"type\":\"error\"},{\"inputs\":[],\"name\":\"FailedCall\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"voter\",\"type\":\"address\"}],\"name\":\"GovernorAlreadyCastVote\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"GovernorAlreadyQueuedProposal\",\"type\":\"error\"},{\"inputs\":[],\"name\":\"GovernorDisabledDeposit\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"proposer\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"votes\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"threshold\",\"type\":\"uint256\"}],\"name\":\"GovernorInsufficientProposerVotes\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"targets\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"calldatas\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"values\",\"type\":\"uint256\"}],\"name\":\"GovernorInvalidProposalLength\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"quorumNumerator\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"quorumDenominator\",\"type\":\"uint256\"}],\"name\":\"GovernorInvalidQuorumFraction\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"voter\",\"type\":\"address\"}],\"name\":\"GovernorInvalidSignature\",\"type\":\"error\"},{\"inputs\":[],\"name\":\"GovernorInvalidVoteParams\",\"type\":\"error\"},{\"inputs\":[],\"name\":\"GovernorInvalidVoteType\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"votingPeriod\",\"type\":\"uint256\"}],\"name\":\"GovernorInvalidVotingPeriod\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"GovernorNonexistentProposal\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"GovernorNotQueuedProposal\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"account\",\"type\":\"address\"}],\"name\":\"GovernorOnlyExecutor\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"account\",\"type\":\"address\"}],\"name\":\"GovernorOnlyProposer\",\"type\":\"error\"},{\"inputs\":[],\"name\":\"GovernorQueueNotImplemented\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"proposer\",\"type\":\"address\"}],\"name\":\"GovernorRestrictedProposer\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"},{\"internalType\":\"enumIGovernor.ProposalState\",\"name\":\"current\",\"type\":\"uint8\"},{\"internalType\":\"bytes32\",\"name\":\"expectedStates\",\"type\":\"bytes32\"}],\"name\":\"GovernorUnexpectedProposalState\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"account\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"currentNonce\",\"type\":\"uint256\"}],\"name\":\"InvalidAccountNonce\",\"type\":\"error\"},{\"inputs\":[],\"name\":\"InvalidShortString\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"uint8\",\"name\":\"bits\",\"type\":\"uint8\"},{\"internalType\":\"uint256\",\"name\":\"value\",\"type\":\"uint256\"}],\"name\":\"SafeCastOverflowedUintDowncast\",\"type\":\"error\"},{\"inputs\":[{\"internalType\":\"string\",\"name\":\"str\",\"type\":\"string\"}],\"name\":\"StringTooLong\",\"type\":\"error\"},{\"anonymous\":false,\"inputs\":[],\"name\":\"EIP712DomainChanged\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"ProposalCanceled\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"address\",\"name\":\"proposer\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"address[]\",\"name\":\"targets\",\"type\":\"address[]\"},{\"indexed\":false,\"internalType\":\"uint256[]\",\"name\":\"values\",\"type\":\"uint256[]\"},{\"indexed\":false,\"internalType\":\"string[]\",\"name\":\"signatures\",\"type\":\"string[]\"},{\"indexed\":false,\"internalType\":\"bytes[]\",\"name\":\"calldatas\",\"type\":\"bytes[]\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"voteStart\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"voteEnd\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"string\",\"name\":\"description\",\"type\":\"string\"}],\"name\":\"ProposalCreated\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"ProposalExecuted\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"etaSeconds\",\"type\":\"uint256\"}],\"name\":\"ProposalQueued\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"oldProposalThreshold\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"newProposalThreshold\",\"type\":\"uint256\"}],\"name\":\"ProposalThresholdSet\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"oldQuorumNumerator\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"newQuorumNumerator\",\"type\":\"uint256\"}],\"name\":\"QuorumNumeratorUpdated\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"internalType\":\"address\",\"name\":\"voter\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint8\",\"name\":\"support\",\"type\":\"uint8\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"weight\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"string\",\"name\":\"reason\",\"type\":\"string\"}],\"name\":\"VoteCast\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":true,\"internalType\":\"address\",\"name\":\"voter\",\"type\":\"address\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint8\",\"name\":\"support\",\"type\":\"uint8\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"weight\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"string\",\"name\":\"reason\",\"type\":\"string\"},{\"indexed\":false,\"internalType\":\"bytes\",\"name\":\"params\",\"type\":\"bytes\"}],\"name\":\"VoteCastWithParams\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"oldVotingDelay\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"newVotingDelay\",\"type\":\"uint256\"}],\"name\":\"VotingDelaySet\",\"type\":\"event\"},{\"anonymous\":false,\"inputs\":[{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"oldVotingPeriod\",\"type\":\"uint256\"},{\"indexed\":false,\"internalType\":\"uint256\",\"name\":\"newVotingPeriod\",\"type\":\"uint256\"}],\"name\":\"VotingPeriodSet\",\"type\":\"event\"},{\"inputs\":[],\"name\":\"BALLOT_TYPEHASH\",\"outputs\":[{\"internalType\":\"bytes32\",\"name\":\"\",\"type\":\"bytes32\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"CLOCK_MODE\",\"outputs\":[{\"internalType\":\"string\",\"name\":\"\",\"type\":\"string\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"COUNTING_MODE\",\"outputs\":[{\"internalType\":\"string\",\"name\":\"\",\"type\":\"string\"}],\"stateMutability\":\"pure\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"EXTENDED_BALLOT_TYPEHASH\",\"outputs\":[{\"internalType\":\"bytes32\",\"name\":\"\",\"type\":\"bytes32\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"cancel\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address[]\",\"name\":\"targets\",\"type\":\"address[]\"},{\"internalType\":\"uint256[]\",\"name\":\"values\",\"type\":\"uint256[]\"},{\"internalType\":\"bytes[]\",\"name\":\"calldatas\",\"type\":\"bytes[]\"},{\"internalType\":\"bytes32\",\"name\":\"descriptionHash\",\"type\":\"bytes32\"}],\"name\":\"cancel\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"},{\"internalType\":\"uint8\",\"name\":\"support\",\"type\":\"uint8\"}],\"name\":\"castVote\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"},{\"internalType\":\"uint8\",\"name\":\"support\",\"type\":\"uint8\"},{\"internalType\":\"address\",\"name\":\"voter\",\"type\":\"address\"},{\"internalType\":\"bytes\",\"name\":\"signature\",\"type\":\"bytes\"}],\"name\":\"castVoteBySig\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"},{\"internalType\":\"uint8\",\"name\":\"support\",\"type\":\"uint8\"},{\"internalType\":\"string\",\"name\":\"reason\",\"type\":\"string\"}],\"name\":\"castVoteWithReason\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"},{\"internalType\":\"uint8\",\"name\":\"support\",\"type\":\"uint8\"},{\"internalType\":\"string\",\"name\":\"reason\",\"type\":\"string\"},{\"internalType\":\"bytes\",\"name\":\"params\",\"type\":\"bytes\"}],\"name\":\"castVoteWithReasonAndParams\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"},{\"internalType\":\"uint8\",\"name\":\"support\",\"type\":\"uint8\"},{\"internalType\":\"address\",\"name\":\"voter\",\"type\":\"address\"},{\"internalType\":\"string\",\"name\":\"reason\",\"type\":\"string\"},{\"internalType\":\"bytes\",\"name\":\"params\",\"type\":\"bytes\"},{\"internalType\":\"bytes\",\"name\":\"signature\",\"type\":\"bytes\"}],\"name\":\"castVoteWithReasonAndParamsBySig\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"clock\",\"outputs\":[{\"internalType\":\"uint48\",\"name\":\"\",\"type\":\"uint48\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"eip712Domain\",\"outputs\":[{\"internalType\":\"bytes1\",\"name\":\"fields\",\"type\":\"bytes1\"},{\"internalType\":\"string\",\"name\":\"name\",\"type\":\"string\"},{\"internalType\":\"string\",\"name\":\"version\",\"type\":\"string\"},{\"internalType\":\"uint256\",\"name\":\"chainId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"verifyingContract\",\"type\":\"address\"},{\"internalType\":\"bytes32\",\"name\":\"salt\",\"type\":\"bytes32\"},{\"internalType\":\"uint256[]\",\"name\":\"extensions\",\"type\":\"uint256[]\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address[]\",\"name\":\"targets\",\"type\":\"address[]\"},{\"internalType\":\"uint256[]\",\"name\":\"values\",\"type\":\"uint256[]\"},{\"internalType\":\"bytes[]\",\"name\":\"calldatas\",\"type\":\"bytes[]\"},{\"internalType\":\"bytes32\",\"name\":\"descriptionHash\",\"type\":\"bytes32\"}],\"name\":\"execute\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"payable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"execute\",\"outputs\":[],\"stateMutability\":\"payable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"account\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"timepoint\",\"type\":\"uint256\"}],\"name\":\"getVotes\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"account\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"timepoint\",\"type\":\"uint256\"},{\"internalType\":\"bytes\",\"name\":\"params\",\"type\":\"bytes\"}],\"name\":\"getVotesWithParams\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"},{\"internalType\":\"address\",\"name\":\"account\",\"type\":\"address\"}],\"name\":\"hasVoted\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address[]\",\"name\":\"targets\",\"type\":\"address[]\"},{\"internalType\":\"uint256[]\",\"name\":\"values\",\"type\":\"uint256[]\"},{\"internalType\":\"bytes[]\",\"name\":\"calldatas\",\"type\":\"bytes[]\"},{\"internalType\":\"bytes32\",\"name\":\"descriptionHash\",\"type\":\"bytes32\"}],\"name\":\"hashProposal\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"pure\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"name\",\"outputs\":[{\"internalType\":\"string\",\"name\":\"\",\"type\":\"string\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"owner\",\"type\":\"address\"}],\"name\":\"nonces\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"},{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"},{\"internalType\":\"uint256[]\",\"name\":\"\",\"type\":\"uint256[]\"},{\"internalType\":\"uint256[]\",\"name\":\"\",\"type\":\"uint256[]\"},{\"internalType\":\"bytes\",\"name\":\"\",\"type\":\"bytes\"}],\"name\":\"onERC1155BatchReceived\",\"outputs\":[{\"internalType\":\"bytes4\",\"name\":\"\",\"type\":\"bytes4\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"},{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"},{\"internalType\":\"bytes\",\"name\":\"\",\"type\":\"bytes\"}],\"name\":\"onERC1155Received\",\"outputs\":[{\"internalType\":\"bytes4\",\"name\":\"\",\"type\":\"bytes4\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"},{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"},{\"internalType\":\"bytes\",\"name\":\"\",\"type\":\"bytes\"}],\"name\":\"onERC721Received\",\"outputs\":[{\"internalType\":\"bytes4\",\"name\":\"\",\"type\":\"bytes4\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"proposalCount\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"proposalDeadline\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"proposalDetails\",\"outputs\":[{\"internalType\":\"address[]\",\"name\":\"targets\",\"type\":\"address[]\"},{\"internalType\":\"uint256[]\",\"name\":\"values\",\"type\":\"uint256[]\"},{\"internalType\":\"bytes[]\",\"name\":\"calldatas\",\"type\":\"bytes[]\"},{\"internalType\":\"bytes32\",\"name\":\"descriptionHash\",\"type\":\"bytes32\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"index\",\"type\":\"uint256\"}],\"name\":\"proposalDetailsAt\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"},{\"internalType\":\"address[]\",\"name\":\"targets\",\"type\":\"address[]\"},{\"internalType\":\"uint256[]\",\"name\":\"values\",\"type\":\"uint256[]\"},{\"internalType\":\"bytes[]\",\"name\":\"calldatas\",\"type\":\"bytes[]\"},{\"internalType\":\"bytes32\",\"name\":\"descriptionHash\",\"type\":\"bytes32\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"proposalEta\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"name\":\"proposalNeedsQueuing\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"proposalProposer\",\"outputs\":[{\"internalType\":\"address\",\"name\":\"\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"proposalSnapshot\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"proposalThreshold\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"proposalVotes\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"againstVotes\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"forVotes\",\"type\":\"uint256\"},{\"internalType\":\"uint256\",\"name\":\"abstainVotes\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address[]\",\"name\":\"targets\",\"type\":\"address[]\"},{\"internalType\":\"uint256[]\",\"name\":\"values\",\"type\":\"uint256[]\"},{\"internalType\":\"bytes[]\",\"name\":\"calldatas\",\"type\":\"bytes[]\"},{\"internalType\":\"string\",\"name\":\"description\",\"type\":\"string\"}],\"name\":\"propose\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address[]\",\"name\":\"targets\",\"type\":\"address[]\"},{\"internalType\":\"uint256[]\",\"name\":\"values\",\"type\":\"uint256[]\"},{\"internalType\":\"bytes[]\",\"name\":\"calldatas\",\"type\":\"bytes[]\"},{\"internalType\":\"bytes32\",\"name\":\"descriptionHash\",\"type\":\"bytes32\"}],\"name\":\"queue\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"queue\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"blockNumber\",\"type\":\"uint256\"}],\"name\":\"quorum\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"quorumDenominator\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"timepoint\",\"type\":\"uint256\"}],\"name\":\"quorumNumerator\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"quorumNumerator\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"address\",\"name\":\"target\",\"type\":\"address\"},{\"internalType\":\"uint256\",\"name\":\"value\",\"type\":\"uint256\"},{\"internalType\":\"bytes\",\"name\":\"data\",\"type\":\"bytes\"}],\"name\":\"relay\",\"outputs\":[],\"stateMutability\":\"payable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"newProposalThreshold\",\"type\":\"uint256\"}],\"name\":\"setProposalThreshold\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint48\",\"name\":\"newVotingDelay\",\"type\":\"uint48\"}],\"name\":\"setVotingDelay\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint32\",\"name\":\"newVotingPeriod\",\"type\":\"uint32\"}],\"name\":\"setVotingPeriod\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"proposalId\",\"type\":\"uint256\"}],\"name\":\"state\",\"outputs\":[{\"internalType\":\"enumIGovernor.ProposalState\",\"name\":\"\",\"type\":\"uint8\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"bytes4\",\"name\":\"interfaceId\",\"type\":\"bytes4\"}],\"name\":\"supportsInterface\",\"outputs\":[{\"internalType\":\"bool\",\"name\":\"\",\"type\":\"bool\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"token\",\"outputs\":[{\"internalType\":\"contractIERC5805\",\"name\":\"\",\"type\":\"address\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[{\"internalType\":\"uint256\",\"name\":\"newQuorumNumerator\",\"type\":\"uint256\"}],\"name\":\"updateQuorumNumerator\",\"outputs\":[],\"stateMutability\":\"nonpayable\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"version\",\"outputs\":[{\"internalType\":\"string\",\"name\":\"\",\"type\":\"string\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"votingDelay\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"inputs\":[],\"name\":\"votingPeriod\",\"outputs\":[{\"internalType\":\"uint256\",\"name\":\"\",\"type\":\"uint256\"}],\"stateMutability\":\"view\",\"type\":\"function\"},{\"stateMutability\":\"payable\",\"type\":\"receive\"}]",
	Bin: "0x61018060405234801561001157600080fd5b50604051615216380380615216833981016040819052610030916106ad565b60048162015180620d2f0060006040518060400160405280600e81526020016d4c656561476f7665726e616e636560901b8152508061007361016d60201b60201c565b61007e826000610188565b6101205261008d816001610188565b61014052815160208084019190912060e052815190820120610100524660a05261011a60e05161010051604080517f8b73c3c69bb8fe3d512ecc4cf759cc79239f7b179b0ffacaa9a75d522b39400f60208201529081019290925260608201524660808201523060a082015260009060c00160405160208183030381529060405280519060200120905090565b60805250503060c052600361012f8282610775565b5061013b9050836101bb565b61014482610221565b61014d816102c7565b5050506001600160a01b03166101605261016681610308565b50506108ee565b6040805180820190915260018152603160f81b602082015290565b60006020835110156101a45761019d8361039e565b90506101b5565b816101af8482610775565b5060ff90505b92915050565b6008546040805165ffffffffffff928316815291831660208301527fc565b045403dc03c2eea82b81a0465edad9e2e7fc4d97e11421c209da93d7a93910160405180910390a16008805465ffffffffffff191665ffffffffffff92909216919091179055565b8063ffffffff166000036102505760405163f1cfbf0560e01b8152600060048201526024015b60405180910390fd5b6008546040805163ffffffff66010000000000009093048316815291831660208301527f7e3f7f0708a84de9203036abaa450dccc85ad5ff52f78c170f3edb55cf5e8828910160405180910390a16008805463ffffffff90921666010000000000000263ffffffff60301b19909216919091179055565b60075460408051918252602082018390527fccb45da8d5717e6c4544694297c4ba5cf151d455c9bb0ed4fc7a38411bc05461910160405180910390a1600755565b6064808211156103355760405163243e544560e01b81526004810183905260248101829052604401610247565b600061033f6103dc565b905061035e61034c6103f6565b61035585610471565b600c91906104a9565b505060408051828152602081018590527f0553476bf02ef2726e8ce5ced78d63e26e602e4a2257b1f559418e24b4633997910160405180910390a1505050565b600080829050601f815111156103c9578260405163305a27a960e01b81526004016102479190610833565b80516103d482610881565b179392505050565b60006103e8600c6104c4565b6001600160d01b0316905090565b60006104026101605190565b6001600160a01b03166391ddadf46040518163ffffffff1660e01b8152600401602060405180830381865afa92505050801561045b575060408051601f3d908101601f19168201909252610458918101906108a5565b60015b61046c5761046761050f565b905090565b919050565b60006001600160d01b038211156104a5576040516306dfcc6560e41b815260d0600482015260248101839052604401610247565b5090565b6000806104b785858561051a565b915091505b935093915050565b80546000908015610505576104ec836104de6001846108cd565b600091825260209091200190565b54660100000000000090046001600160d01b0316610508565b60005b9392505050565b60006104674361067a565b82546000908190801561061c576000610538876104de6001856108cd565b805490915065ffffffffffff80821691660100000000000090046001600160d01b031690881682111561057e57604051632520601d60e01b815260040160405180910390fd5b8765ffffffffffff168265ffffffffffff16036105ba57825465ffffffffffff1666010000000000006001600160d01b0389160217835561060e565b6040805180820190915265ffffffffffff808a1682526001600160d01b03808a1660208085019182528d54600181018f5560008f815291909120945191519092166601000000000000029216919091179101555b94508593506104bc92505050565b50506040805180820190915265ffffffffffff80851682526001600160d01b0380851660208085019182528854600181018a5560008a81529182209551925190931666010000000000000291909316179201919091559050816104bc565b600065ffffffffffff8211156104a5576040516306dfcc6560e41b81526030600482015260248101839052604401610247565b6000602082840312156106bf57600080fd5b81516001600160a01b038116811461050857600080fd5b634e487b7160e01b600052604160045260246000fd5b600181811c9082168061070057607f821691505b60208210810361072057634e487b7160e01b600052602260045260246000fd5b50919050565b601f82111561077057806000526020600020601f840160051c8101602085101561074d5750805b601f840160051c820191505b8181101561076d5760008155600101610759565b50505b505050565b81516001600160401b0381111561078e5761078e6106d6565b6107a28161079c84546106ec565b84610726565b6020601f8211600181146107d657600083156107be5750848201515b600019600385901b1c1916600184901b17845561076d565b600084815260208120601f198516915b8281101561080657878501518255602094850194600190920191016107e6565b50848210156108245786840151600019600387901b60f8161c191681555b50505050600190811b01905550565b602081526000825180602084015260005b818110156108615760208186018101516040868401015201610844565b506000604082850101526040601f19601f83011684010191505092915050565b805160208083015191908110156107205760001960209190910360031b1b16919050565b6000602082840312156108b757600080fd5b815165ffffffffffff8116811461050857600080fd5b818103818111156101b557634e487b7160e01b600052601160045260246000fd5b60805160a05160c05160e051610100516101205161014051610160516148a761096f60003960008181610ab70152818161132f015281816118860152818161251c015261270d015260006124e7015260006124ba015260006129360152600061290e0152600061286901526000612893015260006128bd01526148a76000f3fe6080604052600436106103035760003560e01c80637d5e81e211610190578063c28bc2fa116100dc578063e540d01d11610095578063f23a6e611161006f578063f23a6e6114610a5c578063f8ce560a14610a88578063fc0c546a14610aa8578063fe0d94c114610adb57600080fd5b8063e540d01d146109fc578063eb9019d414610a1c578063ece40cc114610a3c57600080fd5b8063c28bc2fa1461091a578063c59057e41461092d578063da35c6641461094d578063dd4e2ba514610962578063ddf0b009146109a8578063deaaa7cc146109c857600080fd5b80639a802a6d11610149578063ab58fb8e11610123578063ab58fb8e14610881578063b58131b0146108b9578063bc197c81146108ce578063c01f9e37146108fa57600080fd5b80639a802a6d1461082b578063a7713a701461084b578063a9a952941461086057600080fd5b80637d5e81e21461074d5780637ecebe001461076d57806384b0196e146107a35780638ff262e3146107cb57806391ddadf4146107eb57806397c3d3341461081757600080fd5b80633e4f49e61161024f57806354fd4d50116102085780635f398a14116101e25780635f398a14146106cd57806360c4247f146106ed578063790518871461070d5780637b3c71d31461072d57600080fd5b806354fd4d5014610663578063567813881461068d5780635b8d0e0d146106ad57600080fd5b80633e4f49e61461054257806340e58ee51461056f578063438596321461058f578063452115d6146105d95780634bf5d7e9146105f9578063544ffc9c1461060e57600080fd5b8063160cbed7116102bc5780632d63f693116102965780632d63f693146104a85780632e82db94146104c85780632fe3e261146104f95780633932abb11461052d57600080fd5b8063160cbed71461044557806316e9eaec146104655780632656227d1461049557600080fd5b806301ffc9a71461031057806302a251a31461034557806306f3f9e61461037157806306fdde0314610391578063143489d0146103b3578063150b7a021461040157600080fd5b3661030b575b005b600080fd5b34801561031c57600080fd5b5061033061032b36600461375a565b610aee565b60405190151581526020015b60405180910390f35b34801561035157600080fd5b50600854600160301b900463ffffffff165b60405190815260200161033c565b34801561037d57600080fd5b5061030961038c366004613784565b610b45565b34801561039d57600080fd5b506103a6610b59565b60405161033c91906137ed565b3480156103bf57600080fd5b506103e96103ce366004613784565b6000908152600460205260409020546001600160a01b031690565b6040516001600160a01b03909116815260200161033c565b34801561040d57600080fd5b5061042c61041c3660046138e2565b630a85bd0160e11b949350505050565b6040516001600160e01b0319909116815260200161033c565b34801561045157600080fd5b50610363610460366004613ab1565b610beb565b34801561047157600080fd5b50610485610480366004613784565b610c35565b60405161033c9493929190613c1d565b6103636104a3366004613ab1565b610e3f565b3480156104b457600080fd5b506103636104c3366004613784565b610f6a565b3480156104d457600080fd5b506104e86104e3366004613784565b610f8b565b60405161033c959493929190613c68565b34801561050557600080fd5b506103637f3e83946653575f9a39005e1545185629e92736b7528ab20ca3816f315424a81181565b34801561053957600080fd5b50610363610fce565b34801561054e57600080fd5b5061056261055d366004613784565b610fe1565b60405161033c9190613cf2565b34801561057b57600080fd5b5061030961058a366004613784565b61111b565b34801561059b57600080fd5b506103306105aa366004613d00565b60008281526009602090815260408083206001600160a01b038516845260030190915290205460ff1692915050565b3480156105e557600080fd5b506103636105f4366004613ab1565b6112bc565b34801561060557600080fd5b506103a661132b565b34801561061a57600080fd5b50610648610629366004613784565b6000908152600960205260409020805460018201546002909201549092565b6040805193845260208401929092529082015260600161033c565b34801561066f57600080fd5b506040805180820190915260018152603160f81b60208201526103a6565b34801561069957600080fd5b506103636106a8366004613d3d565b6113ed565b3480156106b957600080fd5b506103636106c8366004613da8565b611416565b3480156106d957600080fd5b506103636106e8366004613e6a565b611575565b3480156106f957600080fd5b50610363610708366004613784565b6115ca565b34801561071957600080fd5b50610309610728366004613f05565b611658565b34801561073957600080fd5b50610363610748366004613f22565b611669565b34801561075957600080fd5b50610363610768366004613f7b565b6116b1565b34801561077957600080fd5b5061036361078836600461403f565b6001600160a01b031660009081526002602052604090205490565b3480156107af57600080fd5b506107b861176a565b60405161033c979695949392919061405a565b3480156107d757600080fd5b506103636107e63660046140ca565b6117b0565b3480156107f757600080fd5b50610800611882565b60405165ffffffffffff909116815260200161033c565b34801561082357600080fd5b506064610363565b34801561083757600080fd5b50610363610846366004614119565b61190a565b34801561085757600080fd5b50610363611921565b34801561086c57600080fd5b5061033061087b366004613784565b50600090565b34801561088d57600080fd5b5061036361089c366004613784565b60009081526004602052604090206001015465ffffffffffff1690565b3480156108c557600080fd5b5061036361193b565b3480156108da57600080fd5b5061042c6108e936600461416f565b63bc197c8160e01b95945050505050565b34801561090657600080fd5b50610363610915366004613784565b611946565b610309610928366004614209565b611989565b34801561093957600080fd5b50610363610948366004613ab1565b611a09565b34801561095957600080fd5b50600a54610363565b34801561096e57600080fd5b506040805180820190915260208082527f737570706f72743d627261766f2671756f72756d3d666f722c6162737461696e908201526103a6565b3480156109b457600080fd5b506103096109c3366004613784565b611a43565b3480156109d457600080fd5b506103637ff2aad550cf55f045cb27e9c559f9889fdfb6e6cdaa032301d6ea397784ae51d781565b348015610a0857600080fd5b50610309610a1736600461424a565b611bdf565b348015610a2857600080fd5b50610363610a37366004614270565b611bf0565b348015610a4857600080fd5b50610309610a57366004613784565b611c11565b348015610a6857600080fd5b5061042c610a7736600461429a565b63f23a6e6160e01b95945050505050565b348015610a9457600080fd5b50610363610aa3366004613784565b611c22565b348015610ab457600080fd5b507f00000000000000000000000000000000000000000000000000000000000000006103e9565b610309610ae9366004613784565b611c2d565b60006001600160e01b031982166332a2ad4360e11b1480610b1f57506001600160e01b03198216630271189760e51b145b80610b3a57506301ffc9a760e01b6001600160e01b03198316145b92915050565b905090565b610b4d611dc9565b610b5681611e00565b50565b606060038054610b68906142f2565b80601f0160208091040260200160405190810160405280929190818152602001828054610b94906142f2565b8015610be15780601f10610bb657610100808354040283529160200191610be1565b820191906000526020600020905b815481529060010190602001808311610bc457829003601f168201915b5050505050905090565b600080610bfa86868686611a09565b9050610c0f81610c0a6004611e96565b611eb9565b506000604051634844252360e11b815260040160405180910390fd5b5095945050505050565b6000818152600b602090815260408083208151815460a0948102820185019093526080810183815260609586958695919485949390928492849190840182828015610ca957602002820191906000526020600020905b81546001600160a01b03168152600190910190602001808311610c8b575b5050505050815260200160018201805480602002602001604051908101604052809291908181526020018280548015610d0157602002820191906000526020600020905b815481526020019060010190808311610ced575b5050505050815260200160028201805480602002602001604051908101604052809291908181526020016000905b82821015610ddb578382906000526020600020018054610d4e906142f2565b80601f0160208091040260200160405190810160405280929190818152602001828054610d7a906142f2565b8015610dc75780601f10610d9c57610100808354040283529160200191610dc7565b820191906000526020600020905b815481529060010190602001808311610daa57829003601f168201915b505050505081526020019060010190610d2f565b505050508152602001600382015481525050905080606001516000801b03610e1e57604051636ad0607560e01b8152600481018790526024015b60405180910390fd5b80516020820151604083015160609093015191989097509195509350915050565b600080610e4e86868686611a09565b9050610e6e81610e5e6005611e96565b610e686004611e96565b17611eb9565b506000818152600460205260409020805460ff60f01b1916600160f01b17905530610e963090565b6001600160a01b031614610f205760005b8651811015610f1e57306001600160a01b0316878281518110610ecc57610ecc61432c565b60200260200101516001600160a01b031603610f1657610f16858281518110610ef757610ef761432c565b6020026020010151805190602001206005611ef890919063ffffffff16565b600101610ea7565b505b610f2d8187878787611f5a565b6040518181527f712ae1383f79ac853f8d882153778e0260ef8f03b504e2866e0593e04d2b291f906020015b60405180910390a195945050505050565b600090815260046020526040902054600160a01b900465ffffffffffff1690565b600060608060606000600a8681548110610fa757610fa761432c565b90600052602060002001549450610fbd85610c35565b979992985090969095509350915050565b6000610b4060085465ffffffffffff1690565b6000818152600460205260408120805460ff600160f01b8204811691600160f81b900416811561101657506007949350505050565b801561102757506002949350505050565b600061103286610f6a565b90508060000361105857604051636ad0607560e01b815260048101879052602401610e15565b6000611062611882565b65ffffffffffff169050808210611080575060009695505050505050565b600061108b88611946565b90508181106110a257506001979650505050505050565b6110ab88612034565b15806110cb57506000888152600960205260409020805460019091015411155b156110de57506003979650505050505050565b60008881526004602052604090206001015465ffffffffffff1660000361110d57506004979650505050505050565b506005979650505050505050565b6000818152600b6020908152604091829020805483518184028101840190945280845290926112b7929091849183018282801561118157602002820191906000526020600020905b81546001600160a01b03168152600190910190602001808311611163575b5050505050826001018054806020026020016040519081016040528092919081815260200182805480156111d457602002820191906000526020600020905b8154815260200190600101908083116111c0575b505050505083600201805480602002602001604051908101604052809291908181526020016000905b828210156112a957838290600052602060002001805461121c906142f2565b80601f0160208091040260200160405190810160405280929190818152602001828054611248906142f2565b80156112955780601f1061126a57610100808354040283529160200191611295565b820191906000526020600020905b81548152906001019060200180831161127857829003601f168201915b5050505050815260200190600101906111fd565b5050505084600301546112bc565b505050565b6000806112cb86868686611a09565b90506112db81610c0a6000611e96565b506000818152600460205260409020546001600160a01b031633146113155760405163233d98e360e01b8152336004820152602401610e15565b6113218686868661206b565b9695505050505050565b60607f00000000000000000000000000000000000000000000000000000000000000006001600160a01b0316634bf5d7e96040518163ffffffff1660e01b8152600401600060405180830381865afa9250505080156113ac57506040513d6000823e601f3d908101601f191682016040526113a99190810190614342565b60015b6113e8575060408051808201909152601d81527f6d6f64653d626c6f636b6e756d6265722666726f6d3d64656661756c74000000602082015290565b919050565b60008033905061140e8482856040518060200160405280600081525061211c565b949350505050565b6000806114f9876114f37f3e83946653575f9a39005e1545185629e92736b7528ab20ca3816f315424a8118c8c8c61146b8e6001600160a01b0316600090815260026020526040902080546001810190915590565b8d8d60405161147b9291906143af565b60405180910390208c805190602001206040516020016114d89796959493929190968752602087019590955260ff9390931660408601526001600160a01b03919091166060850152608084015260a083015260c082015260e00190565b60405160208183030381529060405280519060200120612148565b85612175565b905080611524576040516394ab6c0760e01b81526001600160a01b0388166004820152602401610e15565b61156889888a89898080601f0160208091040260200160405190810160405280939291908181526020018383808284376000920191909152508b92506121e9915050565b9998505050505050505050565b6000803390506115bf87828888888080601f0160208091040260200160405190810160405280939291908181526020018383808284376000920191909152508a92506121e9915050565b979650505050505050565b600c805460009182906115de6001846143d5565b815481106115ee576115ee61432c565b6000918252602090912001805490915065ffffffffffff811690600160301b90046001600160d01b0316858211611631576001600160d01b031695945050505050565b61164561163d876122cb565b600c90612302565b6001600160d01b03169695505050505050565b611660611dc9565b610b56816123b7565b60008033905061132186828787878080601f01602080910402602001604051908101604052809392919081815260200183838082843760009201919091525061211c92505050565b6000336116be818461241d565b6116e65760405163d9b3955760e01b81526001600160a01b0382166004820152602401610e15565b60006116f061193b565b9050801561175d57600061171f836001611708611882565b61171291906143e8565b65ffffffffffff16611bf0565b90508181101561175b57604051636121770b60e11b81526001600160a01b03841660048201526024810182905260448101839052606401610e15565b505b6115bf87878787866124a4565b60006060806000806000606061177e6124b3565b6117866124e0565b60408051600080825260208201909252600f60f81b9b939a50919850469750309650945092509050565b60008061183c846114f37ff2aad550cf55f045cb27e9c559f9889fdfb6e6cdaa032301d6ea397784ae51d78989896118058b6001600160a01b0316600090815260026020526040902080546001810190915590565b60408051602081019690965285019390935260ff90911660608401526001600160a01b0316608083015260a082015260c0016114d8565b905080611867576040516394ab6c0760e01b81526001600160a01b0385166004820152602401610e15565b6113218685876040518060200160405280600081525061211c565b60007f00000000000000000000000000000000000000000000000000000000000000006001600160a01b03166391ddadf46040518163ffffffff1660e01b8152600401602060405180830381865afa9250505080156118fe575060408051601f3d908101601f191682019092526118fb91810190614406565b60015b6113e857610b4061250d565b6000611917848484612518565b90505b9392505050565b600061192d600c6125ae565b6001600160d01b0316905090565b6000610b4060075490565b60008181526004602052604081205461197b90600160d01b810463ffffffff1690600160a01b900465ffffffffffff16614423565b65ffffffffffff1692915050565b611991611dc9565b600080856001600160a01b03168585856040516119af9291906143af565b60006040518083038185875af1925050503d80600081146119ec576040519150601f19603f3d011682016040523d82523d6000602084013e6119f1565b606091505b5091509150611a0082826125e7565b50505050505050565b600084848484604051602001611a229493929190613c1d565b60408051601f19818403018152919052805160209091012095945050505050565b6000818152600b6020908152604091829020805483518184028101840190945280845290926112b79290918491830182828015611aa957602002820191906000526020600020905b81546001600160a01b03168152600190910190602001808311611a8b575b505050505082600101805480602002602001604051908101604052809291908181526020018280548015611afc57602002820191906000526020600020905b815481526020019060010190808311611ae8575b505050505083600201805480602002602001604051908101604052809291908181526020016000905b82821015611bd1578382906000526020600020018054611b44906142f2565b80601f0160208091040260200160405190810160405280929190818152602001828054611b70906142f2565b8015611bbd5780601f10611b9257610100808354040283529160200191611bbd565b820191906000526020600020905b815481529060010190602001808311611ba057829003601f168201915b505050505081526020019060010190611b25565b505050508460030154610beb565b611be7611dc9565b610b5681612603565b600061191a8383611c0c60408051602081019091526000815290565b612518565b611c19611dc9565b610b56816126a1565b6000610b3a826126e2565b6000818152600b6020908152604091829020805483518184028101840190945280845290926112b79290918491830182828015611c9357602002820191906000526020600020905b81546001600160a01b03168152600190910190602001808311611c75575b505050505082600101805480602002602001604051908101604052809291908181526020018280548015611ce657602002820191906000526020600020905b815481526020019060010190808311611cd2575b505050505083600201805480602002602001604051908101604052809291908181526020016000905b82821015611dbb578382906000526020600020018054611d2e906142f2565b80601f0160208091040260200160405190810160405280929190818152602001828054611d5a906142f2565b8015611da75780601f10611d7c57610100808354040283529160200191611da7565b820191906000526020600020905b815481529060010190602001808311611d8a57829003601f168201915b505050505081526020019060010190611d0f565b505050508460030154610e3f565b303314611deb576040516347096e4760e01b8152336004820152602401610e15565b565b80611df8600561278c565b03611ded5750565b606480821115611e2d5760405163243e544560e01b81526004810183905260248101829052604401610e15565b6000611e37611921565b9050611e56611e44611882565b611e4d856127fb565b600c919061282f565b505060408051828152602081018590527f0553476bf02ef2726e8ce5ced78d63e26e602e4a2257b1f559418e24b4633997910160405180910390a1505050565b6000816007811115611eaa57611eaa613cba565b600160ff919091161b92915050565b600080611ec584610fe1565b9050600083611ed383611e96565b160361191a578381846040516331b75e4d60e01b8152600401610e1593929190614441565b81546001600160801b03600160801b820481169181166001830190911603611f2457611f24604161284a565b6001600160801b03808216600090815260018086016020526040909120939093558354919092018216600160801b029116179055565b60005b845181101561202c57600080868381518110611f7b57611f7b61432c565b60200260200101516001600160a01b0316868481518110611f9e57611f9e61432c565b6020026020010151868581518110611fb857611fb861432c565b6020026020010151604051611fcd9190614463565b60006040518083038185875af1925050503d806000811461200a576040519150601f19603f3d011682016040523d82523d6000602084013e61200f565b606091505b509150915061201e82826125e7565b505050806001019050611f5d565b505050505050565b600081815260096020526040812060028101546001820154612056919061447f565b612062610aa385610f6a565b11159392505050565b60008061207a86868686611a09565b90506120c88161208a6007611e96565b6120946006611e96565b61209e6002611e96565b60016120ab600782614492565b6120b690600261458a565b6120c091906143d5565b181818611eb9565b506000818152600460205260409081902080546001600160f81b0316600160f81b179055517f789cf55be980739dad1d0699b93b58e806b51c9d96619bfa8fe0a28abaa7b30c90610f599083815260200190565b600061213f8585858561213a60408051602081019091526000815290565b6121e9565b95945050505050565b6000610b3a61215561285c565b8360405161190160f01b8152600281019290925260228201526042902090565b6000836001600160a01b03163b6000036121d7576000806121968585612987565b50909250905060008160038111156121b0576121b0613cba565b1480156121ce5750856001600160a01b0316826001600160a01b0316145b9250505061191a565b6121e28484846129d4565b905061191a565b60006121f986610c0a6001611e96565b50600061220f8661220989610f6a565b85612518565b905060006122208888888588612aaf565b9050835160000361227757866001600160a01b03167fb8e138887d0aa13bab447e82de9d5c1777041ecd21ca36ba824ff1e6c07ddda48988848960405161226a9493929190614599565b60405180910390a26115bf565b866001600160a01b03167fe2babfbac5889a709b63bb7f598b324e08bc5a4fb9ec647fb3cbc9ec07eb871289888489896040516122b89594939291906145c1565b60405180910390a2979650505050505050565b600065ffffffffffff8211156122fe576040516306dfcc6560e41b81526030600482015260248101839052604401610e15565b5090565b81546000908181600581111561236157600061231d84612bb2565b61232790856143d5565b60008881526020902090915081015465ffffffffffff90811690871610156123515780915061235f565b61235c81600161447f565b92505b505b600061236f87878585612d0b565b905080156123aa57612394876123866001846143d5565b600091825260209091200190565b54600160301b90046001600160d01b03166115bf565b6000979650505050505050565b6008546040805165ffffffffffff928316815291831660208301527fc565b045403dc03c2eea82b81a0465edad9e2e7fc4d97e11421c209da93d7a93910160405180910390a16008805465ffffffffffff191665ffffffffffff92909216919091179055565b80516000906034811015612435576001915050610b3a565b60131981840101516001600160b01b03198116692370726f706f7365723d60b01b1461246657600192505050610b3a565b60008061247786602a860386612d6d565b915091508115806115bf5750866001600160a01b0316816001600160a01b03161494505050505092915050565b60006113218686868686612e1c565b6060610b407f00000000000000000000000000000000000000000000000000000000000000006000612ef7565b6060610b407f00000000000000000000000000000000000000000000000000000000000000006001612ef7565b6000610b40436122cb565b60007f0000000000000000000000000000000000000000000000000000000000000000604051630748d63560e31b81526001600160a01b038681166004830152602482018690529190911690633a46b1a890604401602060405180830381865afa15801561258a573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906119179190614607565b805460009080156125de576125c8836123866001846143d5565b54600160301b90046001600160d01b031661191a565b60009392505050565b6060826125fc576125f782612fa2565b610b3a565b5080610b3a565b8063ffffffff1660000361262d5760405163f1cfbf0560e01b815260006004820152602401610e15565b6008546040805163ffffffff600160301b9093048316815291831660208301527f7e3f7f0708a84de9203036abaa450dccc85ad5ff52f78c170f3edb55cf5e8828910160405180910390a16008805463ffffffff909216600160301b0269ffffffff00000000000019909216919091179055565b60075460408051918252602082018390527fccb45da8d5717e6c4544694297c4ba5cf151d455c9bb0ed4fc7a38411bc05461910160405180910390a1600755565b600060646126ef836115ca565b604051632394e7a360e21b8152600481018590526001600160a01b037f00000000000000000000000000000000000000000000000000000000000000001690638e539e8c90602401602060405180830381865afa158015612754573d6000803e3d6000fd5b505050506040513d601f19601f820116820180604052508101906127789190614607565b6127829190614620565b610b3a919061464d565b80546000906001600160801b0380821691600160801b90041681036127b5576127b5603161284a565b6001600160801b038181166000908152600185810160205260408220805492905585546fffffffffffffffffffffffffffffffff19169301909116919091179092555090565b60006001600160d01b038211156122fe576040516306dfcc6560e41b815260d0600482015260248101839052604401610e15565b60008061283d858585612fcb565b915091505b935093915050565b634e487b71600052806020526024601cfd5b6000306001600160a01b037f0000000000000000000000000000000000000000000000000000000000000000161480156128b557507f000000000000000000000000000000000000000000000000000000000000000046145b156128df57507f000000000000000000000000000000000000000000000000000000000000000090565b610b40604080517f8b73c3c69bb8fe3d512ecc4cf759cc79239f7b179b0ffacaa9a75d522b39400f60208201527f0000000000000000000000000000000000000000000000000000000000000000918101919091527f000000000000000000000000000000000000000000000000000000000000000060608201524660808201523060a082015260009060c00160405160208183030381529060405280519060200120905090565b600080600083516041036129c15760208401516040850151606086015160001a6129b38882858561311f565b9550955095505050506129cd565b50508151600091506002905b9250925092565b6000806000856001600160a01b031685856040516024016129f692919061466f565b60408051601f198184030181529181526020820180516001600160e01b0316630b135d3f60e11b17905251612a2b9190614463565b600060405180830381855afa9150503d8060008114612a66576040519150601f19603f3d011682016040523d82523d6000602084013e612a6b565b606091505b5091509150818015612a7f57506020815110155b801561132157508051630b135d3f60e11b90612aa49083016020908101908401614607565b149695505050505050565b60008581526009602090815260408083206001600160a01b03881684526003810190925282205460ff1615612b02576040516371c6af4960e01b81526001600160a01b0387166004820152602401610e15565b6001600160a01b03861660009081526003820160205260409020805460ff1916600117905560ff8516612b4e5783816000016000828254612b43919061447f565b90915550612ba79050565b60001960ff861601612b6e5783816001016000828254612b43919061447f565b60011960ff861601612b8e5783816002016000828254612b43919061447f565b6040516303599be160e11b815260040160405180910390fd5b509195945050505050565b600060018211612bc0575090565b816001600160801b8210612bd95760809190911c9060401b5b680100000000000000008210612bf45760409190911c9060201b5b6401000000008210612c0b5760209190911c9060101b5b620100008210612c205760109190911c9060081b5b6101008210612c345760089190911c9060041b5b60108210612c475760049190911c9060021b5b60048210612c535760011b5b600302600190811c90818581612c6b57612c6b614637565b048201901c90506001818581612c8357612c83614637565b048201901c90506001818581612c9b57612c9b614637565b048201901c90506001818581612cb357612cb3614637565b048201901c90506001818581612ccb57612ccb614637565b048201901c90506001818581612ce357612ce3614637565b048201901c9050612d02818581612cfc57612cfc614637565b04821190565b90039392505050565b60005b81831015612d65576000612d2284846131ee565b60008781526020902090915065ffffffffffff86169082015465ffffffffffff161115612d5157809250612d5f565b612d5c81600161447f565b93505b50612d0e565b509392505050565b6000808451831180612d7e57508284115b15612d8e57506000905080612842565b6000612d9b85600161447f565b84118015612dc3575061060f60f31b612db78787016020015190565b6001600160f01b031916145b90506000612dd48215156002614620565b612ddf90602861447f565b905080612dec87876143d5565b03612e0e57600080612dff898989613209565b90965094506128429350505050565b600080935093505050612842565b600080612e2c87878787876132cf565b600a805460018101825560009182527fc65a7bb8d6351c1cf70c95a316cc6a92839c986682d98bc35f958f4883f9d2a801829055604080516080810182528a815260208181018b90528183018a90528851898201206060830152848452600b8152919092208251805194955092939092612eaa928492910190613600565b506020828101518051612ec39260018501920190613661565b5060408201518051612edf91600284019160209091019061369c565b50606091909101516003909101559695505050505050565b606060ff8314612f1157612f0a836134ef565b9050610b3a565b818054612f1d906142f2565b80601f0160208091040260200160405190810160405280929190818152602001828054612f49906142f2565b8015612f965780601f10612f6b57610100808354040283529160200191612f96565b820191906000526020600020905b815481529060010190602001808311612f7957829003601f168201915b50505050509050610b3a565b805115612fb25780518082602001fd5b60405163d6bda27560e01b815260040160405180910390fd5b8254600090819080156130c4576000612fe9876123866001856143d5565b805490915065ffffffffffff80821691600160301b90046001600160d01b031690881682111561302c57604051632520601d60e01b815260040160405180910390fd5b8765ffffffffffff168265ffffffffffff160361306557825465ffffffffffff16600160301b6001600160d01b038916021783556130b6565b6040805180820190915265ffffffffffff808a1682526001600160d01b03808a1660208085019182528d54600181018f5560008f81529190912094519151909216600160301b029216919091179101555b945085935061284292505050565b50506040805180820190915265ffffffffffff80851682526001600160d01b0380851660208085019182528854600181018a5560008a815291822095519251909316600160301b029190931617920191909155905081612842565b600080807f7fffffffffffffffffffffffffffffff5d576e7357a4501ddfe92f46681b20a084111561315a57506000915060039050826131e4565b604080516000808252602082018084528a905260ff891692820192909252606081018790526080810186905260019060a0016020604051602081039080840390855afa1580156131ae573d6000803e3d6000fd5b5050604051601f1901519150506001600160a01b0381166131da575060009250600191508290506131e4565b9250600091508190505b9450945094915050565b60006131fd600284841861464d565b61191a9084841661447f565b600080848161321986600161447f565b85118015613241575061060f60f31b6132358388016020015190565b6001600160f01b031916145b905060006132528215156002614620565b9050600080613261838a61447f565b90505b878110156132be57600061328361327e8784016020015190565b61352e565b9050600f8160ff1611156132a35760008097509750505050505050612842565b6132ae601084614620565b60ff909116019150600101613264565b506001999098509650505050505050565b60006132e48686868680519060200120611a09565b9050845186511415806132f957508351865114155b8061330357508551155b1561333857855184518651604051630447b05d60e41b8152600481019390935260248301919091526044820152606401610e15565b600081815260046020526040902054600160a01b900465ffffffffffff1615613383578061336582610fe1565b6040516331b75e4d60e01b8152610e15929190600090600401614441565b600061338d610fce565b613395611882565b65ffffffffffff166133a7919061447f565b905060006133c260085463ffffffff600160301b9091041690565b600084815260046020526040902080546001600160a01b0319166001600160a01b0387161781559091506133f5836122cb565b815465ffffffffffff91909116600160a01b0265ffffffffffff60a01b19909116178155613422826135a7565b815463ffffffff91909116600160d01b0263ffffffff60d01b1990911617815588517f7d84a6263ae0d98d3329bd7b46bb4e8d6f98cd35a7adb45c274c8b7fd5ebd5e090859087908c908c906001600160401b0381111561348557613485613817565b6040519080825280602002602001820160405280156134b857816020015b60608152602001906001900390816134a35790505b508c896134c58a8261447f565b8e6040516134db99989796959493929190614688565b60405180910390a150505095945050505050565b606060006134fc836135d8565b604080516020808252818301909252919250600091906020820181803683375050509182525060208101929092525090565b600060f882901c602f811180156135485750603a8160ff16105b1561355657602f1901610b3a565b60608160ff1611801561356c575060678160ff16105b1561357a5760561901610b3a565b60408160ff16118015613590575060478160ff16105b1561359e5760361901610b3a565b5060ff92915050565b600063ffffffff8211156122fe576040516306dfcc6560e41b81526020600482015260248101839052604401610e15565b600060ff8216601f811115610b3a57604051632cd44ac360e21b815260040160405180910390fd5b828054828255906000526020600020908101928215613655579160200282015b8281111561365557825182546001600160a01b0319166001600160a01b03909116178255602090920191600190910190613620565b506122fe9291506136ee565b828054828255906000526020600020908101928215613655579160200282015b82811115613655578251825591602001919060010190613681565b8280548282559060005260206000209081019282156136e2579160200282015b828111156136e257825182906136d290826147b3565b50916020019190600101906136bc565b506122fe929150613703565b5b808211156122fe57600081556001016136ef565b808211156122fe5760006137178282613720565b50600101613703565b50805461372c906142f2565b6000825580601f1061373c575050565b601f016020900490600052602060002090810190610b5691906136ee565b60006020828403121561376c57600080fd5b81356001600160e01b03198116811461191a57600080fd5b60006020828403121561379657600080fd5b5035919050565b60005b838110156137b85781810151838201526020016137a0565b50506000910152565b600081518084526137d981602086016020860161379d565b601f01601f19169290920160200192915050565b60208152600061191a60208301846137c1565b80356001600160a01b03811681146113e857600080fd5b634e487b7160e01b600052604160045260246000fd5b604051601f8201601f191681016001600160401b038111828210171561385557613855613817565b604052919050565b60006001600160401b0382111561387657613876613817565b50601f01601f191660200190565b60006138976138928461385d565b61382d565b90508281528383830111156138ab57600080fd5b828260208301376000602084830101529392505050565b600082601f8301126138d357600080fd5b61191a83833560208501613884565b600080600080608085870312156138f857600080fd5b61390185613800565b935061390f60208601613800565b92506040850135915060608501356001600160401b0381111561393157600080fd5b61393d878288016138c2565b91505092959194509250565b60006001600160401b0382111561396257613962613817565b5060051b60200190565b600082601f83011261397d57600080fd5b813561398b61389282613949565b8082825260208201915060208360051b8601019250858311156139ad57600080fd5b602085015b83811015610c2b576139c381613800565b8352602092830192016139b2565b600082601f8301126139e257600080fd5b81356139f061389282613949565b8082825260208201915060208360051b860101925085831115613a1257600080fd5b602085015b83811015610c2b578035835260209283019201613a17565b600082601f830112613a4057600080fd5b8135613a4e61389282613949565b8082825260208201915060208360051b860101925085831115613a7057600080fd5b602085015b83811015610c2b5780356001600160401b03811115613a9357600080fd5b613aa2886020838a01016138c2565b84525060209283019201613a75565b60008060008060808587031215613ac757600080fd5b84356001600160401b03811115613add57600080fd5b613ae98782880161396c565b94505060208501356001600160401b03811115613b0557600080fd5b613b11878288016139d1565b93505060408501356001600160401b03811115613b2d57600080fd5b613b3987828801613a2f565b949793965093946060013593505050565b600081518084526020840193506020830160005b82811015613b855781516001600160a01b0316865260209586019590910190600101613b5e565b5093949350505050565b600081518084526020840193506020830160005b82811015613b85578151865260209586019590910190600101613ba3565b600082825180855260208501945060208160051b8301016020850160005b83811015613c1157601f19858403018852613bfb8383516137c1565b6020988901989093509190910190600101613bdf565b50909695505050505050565b608081526000613c306080830187613b4a565b8281036020840152613c428187613b8f565b90508281036040840152613c568186613bc1565b91505082606083015295945050505050565b85815260a060208201526000613c8160a0830187613b4a565b8281036040840152613c938187613b8f565b90508281036060840152613ca78186613bc1565b9150508260808301529695505050505050565b634e487b7160e01b600052602160045260246000fd5b60088110613cee57634e487b7160e01b600052602160045260246000fd5b9052565b60208101610b3a8284613cd0565b60008060408385031215613d1357600080fd5b82359150613d2360208401613800565b90509250929050565b803560ff811681146113e857600080fd5b60008060408385031215613d5057600080fd5b82359150613d2360208401613d2c565b60008083601f840112613d7257600080fd5b5081356001600160401b03811115613d8957600080fd5b602083019150836020828501011115613da157600080fd5b9250929050565b600080600080600080600060c0888a031215613dc357600080fd5b87359650613dd360208901613d2c565b9550613de160408901613800565b945060608801356001600160401b03811115613dfc57600080fd5b613e088a828b01613d60565b90955093505060808801356001600160401b03811115613e2757600080fd5b613e338a828b016138c2565b92505060a08801356001600160401b03811115613e4f57600080fd5b613e5b8a828b016138c2565b91505092959891949750929550565b600080600080600060808688031215613e8257600080fd5b85359450613e9260208701613d2c565b935060408601356001600160401b03811115613ead57600080fd5b613eb988828901613d60565b90945092505060608601356001600160401b03811115613ed857600080fd5b613ee4888289016138c2565b9150509295509295909350565b65ffffffffffff81168114610b5657600080fd5b600060208284031215613f1757600080fd5b813561191a81613ef1565b60008060008060608587031215613f3857600080fd5b84359350613f4860208601613d2c565b925060408501356001600160401b03811115613f6357600080fd5b613f6f87828801613d60565b95989497509550505050565b60008060008060808587031215613f9157600080fd5b84356001600160401b03811115613fa757600080fd5b613fb38782880161396c565b94505060208501356001600160401b03811115613fcf57600080fd5b613fdb878288016139d1565b93505060408501356001600160401b03811115613ff757600080fd5b61400387828801613a2f565b92505060608501356001600160401b0381111561401f57600080fd5b8501601f8101871361403057600080fd5b61393d87823560208401613884565b60006020828403121561405157600080fd5b61191a82613800565b60ff60f81b8816815260e06020820152600061407960e08301896137c1565b828103604084015261408b81896137c1565b606084018890526001600160a01b038716608085015260a0840186905283810360c085015290506140bc8185613b8f565b9a9950505050505050505050565b600080600080608085870312156140e057600080fd5b843593506140f060208601613d2c565b92506140fe60408601613800565b915060608501356001600160401b0381111561393157600080fd5b60008060006060848603121561412e57600080fd5b61413784613800565b92506020840135915060408401356001600160401b0381111561415957600080fd5b614165868287016138c2565b9150509250925092565b600080600080600060a0868803121561418757600080fd5b61419086613800565b945061419e60208701613800565b935060408601356001600160401b038111156141b957600080fd5b6141c5888289016139d1565b93505060608601356001600160401b038111156141e157600080fd5b6141ed888289016139d1565b92505060808601356001600160401b03811115613ed857600080fd5b6000806000806060858703121561421f57600080fd5b61422885613800565b93506020850135925060408501356001600160401b03811115613f6357600080fd5b60006020828403121561425c57600080fd5b813563ffffffff8116811461191a57600080fd5b6000806040838503121561428357600080fd5b61428c83613800565b946020939093013593505050565b600080600080600060a086880312156142b257600080fd5b6142bb86613800565b94506142c960208701613800565b9350604086013592506060860135915060808601356001600160401b03811115613ed857600080fd5b600181811c9082168061430657607f821691505b60208210810361432657634e487b7160e01b600052602260045260246000fd5b50919050565b634e487b7160e01b600052603260045260246000fd5b60006020828403121561435457600080fd5b81516001600160401b0381111561436a57600080fd5b8201601f8101841361437b57600080fd5b80516143896138928261385d565b81815285602083850101111561439e57600080fd5b61213f82602083016020860161379d565b8183823760009101908152919050565b634e487b7160e01b600052601160045260246000fd5b81810381811115610b3a57610b3a6143bf565b65ffffffffffff8281168282160390811115610b3a57610b3a6143bf565b60006020828403121561441857600080fd5b815161191a81613ef1565b65ffffffffffff8181168382160190811115610b3a57610b3a6143bf565b838152606081016144556020830185613cd0565b826040830152949350505050565b6000825161447581846020870161379d565b9190910192915050565b80820180821115610b3a57610b3a6143bf565b60ff8181168382160190811115610b3a57610b3a6143bf565b6001815b6001841115612842578085048111156144ca576144ca6143bf565b60018416156144d857908102905b60019390931c9280026144af565b6000826144f557506001610b3a565b8161450257506000610b3a565b816001811461451857600281146145225761453e565b6001915050610b3a565b60ff841115614533576145336143bf565b50506001821b610b3a565b5060208310610133831016604e8410600b8410161715614561575081810a610b3a565b61456e60001984846144ab565b8060001904821115614582576145826143bf565b029392505050565b600061191a60ff8416836144e6565b84815260ff8416602082015282604082015260806060820152600061132160808301846137c1565b85815260ff8516602082015283604082015260a0606082015260006145e960a08301856137c1565b82810360808401526145fb81856137c1565b98975050505050505050565b60006020828403121561461957600080fd5b5051919050565b8082028115828204841417610b3a57610b3a6143bf565b634e487b7160e01b600052601260045260246000fd5b60008261466a57634e487b7160e01b600052601260045260246000fd5b500490565b82815260406020820152600061191760408301846137c1565b8981526001600160a01b0389166020820152610120604082018190526000906146b39083018a613b4a565b82810360608401526146c5818a613b8f565b9050828103608084015280885180835260208301915060208160051b84010160208b0160005b8381101561471d57601f198684030185526147078383516137c1565b60209586019590935091909101906001016146eb565b505085810360a0870152614731818b613bc1565b93505050508560c08401528460e084015282810361010084015261475581856137c1565b9c9b505050505050505050505050565b601f8211156112b757806000526020600020601f840160051c8101602085101561478c5750805b601f840160051c820191505b818110156147ac5760008155600101614798565b5050505050565b81516001600160401b038111156147cc576147cc613817565b6147e0816147da84546142f2565b84614765565b6020601f82116001811461481457600083156147fc5750848201515b600019600385901b1c1916600184901b1784556147ac565b600084815260208120601f198516915b828110156148445787850151825560209485019460019092019101614824565b50848210156148625786840151600019600387901b60f8161c191681555b50505050600190811b0190555056fea26469706673582212205f19cf713bd5faa520072a41cded7070205d4ab2c4d2e8cb3d2c1ca48cf11ffd64736f6c634300081c0033",
}

// LeeaGovernanceABI is the input ABI used to generate the binding from.
// Deprecated: Use LeeaGovernanceMetaData.ABI instead.
var LeeaGovernanceABI = LeeaGovernanceMetaData.ABI

// LeeaGovernanceBin is the compiled bytecode used for deploying new contracts.
// Deprecated: Use LeeaGovernanceMetaData.Bin instead.
var LeeaGovernanceBin = LeeaGovernanceMetaData.Bin

// DeployLeeaGovernance deploys a new Ethereum contract, binding an instance of LeeaGovernance to it.
func DeployLeeaGovernance(auth *bind.TransactOpts, backend bind.ContractBackend, _token common.Address) (common.Address, *types.Transaction, *LeeaGovernance, error) {
	parsed, err := LeeaGovernanceMetaData.GetAbi()
	if err != nil {
		return common.Address{}, nil, nil, err
	}
	if parsed == nil {
		return common.Address{}, nil, nil, errors.New("GetABI returned nil")
	}

	address, tx, contract, err := bind.DeployContract(auth, *parsed, common.FromHex(LeeaGovernanceBin), backend, _token)
	if err != nil {
		return common.Address{}, nil, nil, err
	}
	return address, tx, &LeeaGovernance{LeeaGovernanceCaller: LeeaGovernanceCaller{contract: contract}, LeeaGovernanceTransactor: LeeaGovernanceTransactor{contract: contract}, LeeaGovernanceFilterer: LeeaGovernanceFilterer{contract: contract}}, nil
}

// LeeaGovernance is an auto generated Go binding around an Ethereum contract.
type LeeaGovernance struct {
	LeeaGovernanceCaller     // Read-only binding to the contract
	LeeaGovernanceTransactor // Write-only binding to the contract
	LeeaGovernanceFilterer   // Log filterer for contract events
}

// LeeaGovernanceCaller is an auto generated read-only Go binding around an Ethereum contract.
type LeeaGovernanceCaller struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// LeeaGovernanceTransactor is an auto generated write-only Go binding around an Ethereum contract.
type LeeaGovernanceTransactor struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// LeeaGovernanceFilterer is an auto generated log filtering Go binding around an Ethereum contract events.
type LeeaGovernanceFilterer struct {
	contract *bind.BoundContract // Generic contract wrapper for the low level calls
}

// LeeaGovernanceSession is an auto generated Go binding around an Ethereum contract,
// with pre-set call and transact options.
type LeeaGovernanceSession struct {
	Contract     *LeeaGovernance   // Generic contract binding to set the session for
	CallOpts     bind.CallOpts     // Call options to use throughout this session
	TransactOpts bind.TransactOpts // Transaction auth options to use throughout this session
}

// LeeaGovernanceCallerSession is an auto generated read-only Go binding around an Ethereum contract,
// with pre-set call options.
type LeeaGovernanceCallerSession struct {
	Contract *LeeaGovernanceCaller // Generic contract caller binding to set the session for
	CallOpts bind.CallOpts         // Call options to use throughout this session
}

// LeeaGovernanceTransactorSession is an auto generated write-only Go binding around an Ethereum contract,
// with pre-set transact options.
type LeeaGovernanceTransactorSession struct {
	Contract     *LeeaGovernanceTransactor // Generic contract transactor binding to set the session for
	TransactOpts bind.TransactOpts         // Transaction auth options to use throughout this session
}

// LeeaGovernanceRaw is an auto generated low-level Go binding around an Ethereum contract.
type LeeaGovernanceRaw struct {
	Contract *LeeaGovernance // Generic contract binding to access the raw methods on
}

// LeeaGovernanceCallerRaw is an auto generated low-level read-only Go binding around an Ethereum contract.
type LeeaGovernanceCallerRaw struct {
	Contract *LeeaGovernanceCaller // Generic read-only contract binding to access the raw methods on
}

// LeeaGovernanceTransactorRaw is an auto generated low-level write-only Go binding around an Ethereum contract.
type LeeaGovernanceTransactorRaw struct {
	Contract *LeeaGovernanceTransactor // Generic write-only contract binding to access the raw methods on
}

// NewLeeaGovernance creates a new instance of LeeaGovernance, bound to a specific deployed contract.
func NewLeeaGovernance(address common.Address, backend bind.ContractBackend) (*LeeaGovernance, error) {
	contract, err := bindLeeaGovernance(address, backend, backend, backend)
	if err != nil {
		return nil, err
	}
	return &LeeaGovernance{LeeaGovernanceCaller: LeeaGovernanceCaller{contract: contract}, LeeaGovernanceTransactor: LeeaGovernanceTransactor{contract: contract}, LeeaGovernanceFilterer: LeeaGovernanceFilterer{contract: contract}}, nil
}

// NewLeeaGovernanceCaller creates a new read-only instance of LeeaGovernance, bound to a specific deployed contract.
func NewLeeaGovernanceCaller(address common.Address, caller bind.ContractCaller) (*LeeaGovernanceCaller, error) {
	contract, err := bindLeeaGovernance(address, caller, nil, nil)
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceCaller{contract: contract}, nil
}

// NewLeeaGovernanceTransactor creates a new write-only instance of LeeaGovernance, bound to a specific deployed contract.
func NewLeeaGovernanceTransactor(address common.Address, transactor bind.ContractTransactor) (*LeeaGovernanceTransactor, error) {
	contract, err := bindLeeaGovernance(address, nil, transactor, nil)
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceTransactor{contract: contract}, nil
}

// NewLeeaGovernanceFilterer creates a new log filterer instance of LeeaGovernance, bound to a specific deployed contract.
func NewLeeaGovernanceFilterer(address common.Address, filterer bind.ContractFilterer) (*LeeaGovernanceFilterer, error) {
	contract, err := bindLeeaGovernance(address, nil, nil, filterer)
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceFilterer{contract: contract}, nil
}

// bindLeeaGovernance binds a generic wrapper to an already deployed contract.
func bindLeeaGovernance(address common.Address, caller bind.ContractCaller, transactor bind.ContractTransactor, filterer bind.ContractFilterer) (*bind.BoundContract, error) {
	parsed, err := LeeaGovernanceMetaData.GetAbi()
	if err != nil {
		return nil, err
	}
	return bind.NewBoundContract(address, *parsed, caller, transactor, filterer), nil
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_LeeaGovernance *LeeaGovernanceRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _LeeaGovernance.Contract.LeeaGovernanceCaller.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_LeeaGovernance *LeeaGovernanceRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.LeeaGovernanceTransactor.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_LeeaGovernance *LeeaGovernanceRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.LeeaGovernanceTransactor.contract.Transact(opts, method, params...)
}

// Call invokes the (constant) contract method with params as input values and
// sets the output to result. The result type might be a single field for simple
// returns, a slice of interfaces for anonymous returns and a struct for named
// returns.
func (_LeeaGovernance *LeeaGovernanceCallerRaw) Call(opts *bind.CallOpts, result *[]interface{}, method string, params ...interface{}) error {
	return _LeeaGovernance.Contract.contract.Call(opts, result, method, params...)
}

// Transfer initiates a plain transaction to move funds to the contract, calling
// its default method if one is available.
func (_LeeaGovernance *LeeaGovernanceTransactorRaw) Transfer(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.contract.Transfer(opts)
}

// Transact invokes the (paid) contract method with params as input values.
func (_LeeaGovernance *LeeaGovernanceTransactorRaw) Transact(opts *bind.TransactOpts, method string, params ...interface{}) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.contract.Transact(opts, method, params...)
}

// BALLOTTYPEHASH is a free data retrieval call binding the contract method 0xdeaaa7cc.
//
// Solidity: function BALLOT_TYPEHASH() view returns(bytes32)
func (_LeeaGovernance *LeeaGovernanceCaller) BALLOTTYPEHASH(opts *bind.CallOpts) ([32]byte, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "BALLOT_TYPEHASH")

	if err != nil {
		return *new([32]byte), err
	}

	out0 := *abi.ConvertType(out[0], new([32]byte)).(*[32]byte)

	return out0, err

}

// BALLOTTYPEHASH is a free data retrieval call binding the contract method 0xdeaaa7cc.
//
// Solidity: function BALLOT_TYPEHASH() view returns(bytes32)
func (_LeeaGovernance *LeeaGovernanceSession) BALLOTTYPEHASH() ([32]byte, error) {
	return _LeeaGovernance.Contract.BALLOTTYPEHASH(&_LeeaGovernance.CallOpts)
}

// BALLOTTYPEHASH is a free data retrieval call binding the contract method 0xdeaaa7cc.
//
// Solidity: function BALLOT_TYPEHASH() view returns(bytes32)
func (_LeeaGovernance *LeeaGovernanceCallerSession) BALLOTTYPEHASH() ([32]byte, error) {
	return _LeeaGovernance.Contract.BALLOTTYPEHASH(&_LeeaGovernance.CallOpts)
}

// CLOCKMODE is a free data retrieval call binding the contract method 0x4bf5d7e9.
//
// Solidity: function CLOCK_MODE() view returns(string)
func (_LeeaGovernance *LeeaGovernanceCaller) CLOCKMODE(opts *bind.CallOpts) (string, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "CLOCK_MODE")

	if err != nil {
		return *new(string), err
	}

	out0 := *abi.ConvertType(out[0], new(string)).(*string)

	return out0, err

}

// CLOCKMODE is a free data retrieval call binding the contract method 0x4bf5d7e9.
//
// Solidity: function CLOCK_MODE() view returns(string)
func (_LeeaGovernance *LeeaGovernanceSession) CLOCKMODE() (string, error) {
	return _LeeaGovernance.Contract.CLOCKMODE(&_LeeaGovernance.CallOpts)
}

// CLOCKMODE is a free data retrieval call binding the contract method 0x4bf5d7e9.
//
// Solidity: function CLOCK_MODE() view returns(string)
func (_LeeaGovernance *LeeaGovernanceCallerSession) CLOCKMODE() (string, error) {
	return _LeeaGovernance.Contract.CLOCKMODE(&_LeeaGovernance.CallOpts)
}

// COUNTINGMODE is a free data retrieval call binding the contract method 0xdd4e2ba5.
//
// Solidity: function COUNTING_MODE() pure returns(string)
func (_LeeaGovernance *LeeaGovernanceCaller) COUNTINGMODE(opts *bind.CallOpts) (string, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "COUNTING_MODE")

	if err != nil {
		return *new(string), err
	}

	out0 := *abi.ConvertType(out[0], new(string)).(*string)

	return out0, err

}

// COUNTINGMODE is a free data retrieval call binding the contract method 0xdd4e2ba5.
//
// Solidity: function COUNTING_MODE() pure returns(string)
func (_LeeaGovernance *LeeaGovernanceSession) COUNTINGMODE() (string, error) {
	return _LeeaGovernance.Contract.COUNTINGMODE(&_LeeaGovernance.CallOpts)
}

// COUNTINGMODE is a free data retrieval call binding the contract method 0xdd4e2ba5.
//
// Solidity: function COUNTING_MODE() pure returns(string)
func (_LeeaGovernance *LeeaGovernanceCallerSession) COUNTINGMODE() (string, error) {
	return _LeeaGovernance.Contract.COUNTINGMODE(&_LeeaGovernance.CallOpts)
}

// EXTENDEDBALLOTTYPEHASH is a free data retrieval call binding the contract method 0x2fe3e261.
//
// Solidity: function EXTENDED_BALLOT_TYPEHASH() view returns(bytes32)
func (_LeeaGovernance *LeeaGovernanceCaller) EXTENDEDBALLOTTYPEHASH(opts *bind.CallOpts) ([32]byte, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "EXTENDED_BALLOT_TYPEHASH")

	if err != nil {
		return *new([32]byte), err
	}

	out0 := *abi.ConvertType(out[0], new([32]byte)).(*[32]byte)

	return out0, err

}

// EXTENDEDBALLOTTYPEHASH is a free data retrieval call binding the contract method 0x2fe3e261.
//
// Solidity: function EXTENDED_BALLOT_TYPEHASH() view returns(bytes32)
func (_LeeaGovernance *LeeaGovernanceSession) EXTENDEDBALLOTTYPEHASH() ([32]byte, error) {
	return _LeeaGovernance.Contract.EXTENDEDBALLOTTYPEHASH(&_LeeaGovernance.CallOpts)
}

// EXTENDEDBALLOTTYPEHASH is a free data retrieval call binding the contract method 0x2fe3e261.
//
// Solidity: function EXTENDED_BALLOT_TYPEHASH() view returns(bytes32)
func (_LeeaGovernance *LeeaGovernanceCallerSession) EXTENDEDBALLOTTYPEHASH() ([32]byte, error) {
	return _LeeaGovernance.Contract.EXTENDEDBALLOTTYPEHASH(&_LeeaGovernance.CallOpts)
}

// Clock is a free data retrieval call binding the contract method 0x91ddadf4.
//
// Solidity: function clock() view returns(uint48)
func (_LeeaGovernance *LeeaGovernanceCaller) Clock(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "clock")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// Clock is a free data retrieval call binding the contract method 0x91ddadf4.
//
// Solidity: function clock() view returns(uint48)
func (_LeeaGovernance *LeeaGovernanceSession) Clock() (*big.Int, error) {
	return _LeeaGovernance.Contract.Clock(&_LeeaGovernance.CallOpts)
}

// Clock is a free data retrieval call binding the contract method 0x91ddadf4.
//
// Solidity: function clock() view returns(uint48)
func (_LeeaGovernance *LeeaGovernanceCallerSession) Clock() (*big.Int, error) {
	return _LeeaGovernance.Contract.Clock(&_LeeaGovernance.CallOpts)
}

// Eip712Domain is a free data retrieval call binding the contract method 0x84b0196e.
//
// Solidity: function eip712Domain() view returns(bytes1 fields, string name, string version, uint256 chainId, address verifyingContract, bytes32 salt, uint256[] extensions)
func (_LeeaGovernance *LeeaGovernanceCaller) Eip712Domain(opts *bind.CallOpts) (struct {
	Fields            [1]byte
	Name              string
	Version           string
	ChainId           *big.Int
	VerifyingContract common.Address
	Salt              [32]byte
	Extensions        []*big.Int
}, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "eip712Domain")

	outstruct := new(struct {
		Fields            [1]byte
		Name              string
		Version           string
		ChainId           *big.Int
		VerifyingContract common.Address
		Salt              [32]byte
		Extensions        []*big.Int
	})
	if err != nil {
		return *outstruct, err
	}

	outstruct.Fields = *abi.ConvertType(out[0], new([1]byte)).(*[1]byte)
	outstruct.Name = *abi.ConvertType(out[1], new(string)).(*string)
	outstruct.Version = *abi.ConvertType(out[2], new(string)).(*string)
	outstruct.ChainId = *abi.ConvertType(out[3], new(*big.Int)).(**big.Int)
	outstruct.VerifyingContract = *abi.ConvertType(out[4], new(common.Address)).(*common.Address)
	outstruct.Salt = *abi.ConvertType(out[5], new([32]byte)).(*[32]byte)
	outstruct.Extensions = *abi.ConvertType(out[6], new([]*big.Int)).(*[]*big.Int)

	return *outstruct, err

}

// Eip712Domain is a free data retrieval call binding the contract method 0x84b0196e.
//
// Solidity: function eip712Domain() view returns(bytes1 fields, string name, string version, uint256 chainId, address verifyingContract, bytes32 salt, uint256[] extensions)
func (_LeeaGovernance *LeeaGovernanceSession) Eip712Domain() (struct {
	Fields            [1]byte
	Name              string
	Version           string
	ChainId           *big.Int
	VerifyingContract common.Address
	Salt              [32]byte
	Extensions        []*big.Int
}, error) {
	return _LeeaGovernance.Contract.Eip712Domain(&_LeeaGovernance.CallOpts)
}

// Eip712Domain is a free data retrieval call binding the contract method 0x84b0196e.
//
// Solidity: function eip712Domain() view returns(bytes1 fields, string name, string version, uint256 chainId, address verifyingContract, bytes32 salt, uint256[] extensions)
func (_LeeaGovernance *LeeaGovernanceCallerSession) Eip712Domain() (struct {
	Fields            [1]byte
	Name              string
	Version           string
	ChainId           *big.Int
	VerifyingContract common.Address
	Salt              [32]byte
	Extensions        []*big.Int
}, error) {
	return _LeeaGovernance.Contract.Eip712Domain(&_LeeaGovernance.CallOpts)
}

// GetVotes is a free data retrieval call binding the contract method 0xeb9019d4.
//
// Solidity: function getVotes(address account, uint256 timepoint) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) GetVotes(opts *bind.CallOpts, account common.Address, timepoint *big.Int) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "getVotes", account, timepoint)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetVotes is a free data retrieval call binding the contract method 0xeb9019d4.
//
// Solidity: function getVotes(address account, uint256 timepoint) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) GetVotes(account common.Address, timepoint *big.Int) (*big.Int, error) {
	return _LeeaGovernance.Contract.GetVotes(&_LeeaGovernance.CallOpts, account, timepoint)
}

// GetVotes is a free data retrieval call binding the contract method 0xeb9019d4.
//
// Solidity: function getVotes(address account, uint256 timepoint) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) GetVotes(account common.Address, timepoint *big.Int) (*big.Int, error) {
	return _LeeaGovernance.Contract.GetVotes(&_LeeaGovernance.CallOpts, account, timepoint)
}

// GetVotesWithParams is a free data retrieval call binding the contract method 0x9a802a6d.
//
// Solidity: function getVotesWithParams(address account, uint256 timepoint, bytes params) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) GetVotesWithParams(opts *bind.CallOpts, account common.Address, timepoint *big.Int, params []byte) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "getVotesWithParams", account, timepoint, params)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// GetVotesWithParams is a free data retrieval call binding the contract method 0x9a802a6d.
//
// Solidity: function getVotesWithParams(address account, uint256 timepoint, bytes params) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) GetVotesWithParams(account common.Address, timepoint *big.Int, params []byte) (*big.Int, error) {
	return _LeeaGovernance.Contract.GetVotesWithParams(&_LeeaGovernance.CallOpts, account, timepoint, params)
}

// GetVotesWithParams is a free data retrieval call binding the contract method 0x9a802a6d.
//
// Solidity: function getVotesWithParams(address account, uint256 timepoint, bytes params) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) GetVotesWithParams(account common.Address, timepoint *big.Int, params []byte) (*big.Int, error) {
	return _LeeaGovernance.Contract.GetVotesWithParams(&_LeeaGovernance.CallOpts, account, timepoint, params)
}

// HasVoted is a free data retrieval call binding the contract method 0x43859632.
//
// Solidity: function hasVoted(uint256 proposalId, address account) view returns(bool)
func (_LeeaGovernance *LeeaGovernanceCaller) HasVoted(opts *bind.CallOpts, proposalId *big.Int, account common.Address) (bool, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "hasVoted", proposalId, account)

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// HasVoted is a free data retrieval call binding the contract method 0x43859632.
//
// Solidity: function hasVoted(uint256 proposalId, address account) view returns(bool)
func (_LeeaGovernance *LeeaGovernanceSession) HasVoted(proposalId *big.Int, account common.Address) (bool, error) {
	return _LeeaGovernance.Contract.HasVoted(&_LeeaGovernance.CallOpts, proposalId, account)
}

// HasVoted is a free data retrieval call binding the contract method 0x43859632.
//
// Solidity: function hasVoted(uint256 proposalId, address account) view returns(bool)
func (_LeeaGovernance *LeeaGovernanceCallerSession) HasVoted(proposalId *big.Int, account common.Address) (bool, error) {
	return _LeeaGovernance.Contract.HasVoted(&_LeeaGovernance.CallOpts, proposalId, account)
}

// HashProposal is a free data retrieval call binding the contract method 0xc59057e4.
//
// Solidity: function hashProposal(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash) pure returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) HashProposal(opts *bind.CallOpts, targets []common.Address, values []*big.Int, calldatas [][]byte, descriptionHash [32]byte) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "hashProposal", targets, values, calldatas, descriptionHash)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// HashProposal is a free data retrieval call binding the contract method 0xc59057e4.
//
// Solidity: function hashProposal(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash) pure returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) HashProposal(targets []common.Address, values []*big.Int, calldatas [][]byte, descriptionHash [32]byte) (*big.Int, error) {
	return _LeeaGovernance.Contract.HashProposal(&_LeeaGovernance.CallOpts, targets, values, calldatas, descriptionHash)
}

// HashProposal is a free data retrieval call binding the contract method 0xc59057e4.
//
// Solidity: function hashProposal(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash) pure returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) HashProposal(targets []common.Address, values []*big.Int, calldatas [][]byte, descriptionHash [32]byte) (*big.Int, error) {
	return _LeeaGovernance.Contract.HashProposal(&_LeeaGovernance.CallOpts, targets, values, calldatas, descriptionHash)
}

// Name is a free data retrieval call binding the contract method 0x06fdde03.
//
// Solidity: function name() view returns(string)
func (_LeeaGovernance *LeeaGovernanceCaller) Name(opts *bind.CallOpts) (string, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "name")

	if err != nil {
		return *new(string), err
	}

	out0 := *abi.ConvertType(out[0], new(string)).(*string)

	return out0, err

}

// Name is a free data retrieval call binding the contract method 0x06fdde03.
//
// Solidity: function name() view returns(string)
func (_LeeaGovernance *LeeaGovernanceSession) Name() (string, error) {
	return _LeeaGovernance.Contract.Name(&_LeeaGovernance.CallOpts)
}

// Name is a free data retrieval call binding the contract method 0x06fdde03.
//
// Solidity: function name() view returns(string)
func (_LeeaGovernance *LeeaGovernanceCallerSession) Name() (string, error) {
	return _LeeaGovernance.Contract.Name(&_LeeaGovernance.CallOpts)
}

// Nonces is a free data retrieval call binding the contract method 0x7ecebe00.
//
// Solidity: function nonces(address owner) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) Nonces(opts *bind.CallOpts, owner common.Address) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "nonces", owner)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// Nonces is a free data retrieval call binding the contract method 0x7ecebe00.
//
// Solidity: function nonces(address owner) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) Nonces(owner common.Address) (*big.Int, error) {
	return _LeeaGovernance.Contract.Nonces(&_LeeaGovernance.CallOpts, owner)
}

// Nonces is a free data retrieval call binding the contract method 0x7ecebe00.
//
// Solidity: function nonces(address owner) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) Nonces(owner common.Address) (*big.Int, error) {
	return _LeeaGovernance.Contract.Nonces(&_LeeaGovernance.CallOpts, owner)
}

// ProposalCount is a free data retrieval call binding the contract method 0xda35c664.
//
// Solidity: function proposalCount() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) ProposalCount(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "proposalCount")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// ProposalCount is a free data retrieval call binding the contract method 0xda35c664.
//
// Solidity: function proposalCount() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) ProposalCount() (*big.Int, error) {
	return _LeeaGovernance.Contract.ProposalCount(&_LeeaGovernance.CallOpts)
}

// ProposalCount is a free data retrieval call binding the contract method 0xda35c664.
//
// Solidity: function proposalCount() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) ProposalCount() (*big.Int, error) {
	return _LeeaGovernance.Contract.ProposalCount(&_LeeaGovernance.CallOpts)
}

// ProposalDeadline is a free data retrieval call binding the contract method 0xc01f9e37.
//
// Solidity: function proposalDeadline(uint256 proposalId) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) ProposalDeadline(opts *bind.CallOpts, proposalId *big.Int) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "proposalDeadline", proposalId)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// ProposalDeadline is a free data retrieval call binding the contract method 0xc01f9e37.
//
// Solidity: function proposalDeadline(uint256 proposalId) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) ProposalDeadline(proposalId *big.Int) (*big.Int, error) {
	return _LeeaGovernance.Contract.ProposalDeadline(&_LeeaGovernance.CallOpts, proposalId)
}

// ProposalDeadline is a free data retrieval call binding the contract method 0xc01f9e37.
//
// Solidity: function proposalDeadline(uint256 proposalId) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) ProposalDeadline(proposalId *big.Int) (*big.Int, error) {
	return _LeeaGovernance.Contract.ProposalDeadline(&_LeeaGovernance.CallOpts, proposalId)
}

// ProposalDetails is a free data retrieval call binding the contract method 0x16e9eaec.
//
// Solidity: function proposalDetails(uint256 proposalId) view returns(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash)
func (_LeeaGovernance *LeeaGovernanceCaller) ProposalDetails(opts *bind.CallOpts, proposalId *big.Int) (struct {
	Targets         []common.Address
	Values          []*big.Int
	Calldatas       [][]byte
	DescriptionHash [32]byte
}, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "proposalDetails", proposalId)

	outstruct := new(struct {
		Targets         []common.Address
		Values          []*big.Int
		Calldatas       [][]byte
		DescriptionHash [32]byte
	})
	if err != nil {
		return *outstruct, err
	}

	outstruct.Targets = *abi.ConvertType(out[0], new([]common.Address)).(*[]common.Address)
	outstruct.Values = *abi.ConvertType(out[1], new([]*big.Int)).(*[]*big.Int)
	outstruct.Calldatas = *abi.ConvertType(out[2], new([][]byte)).(*[][]byte)
	outstruct.DescriptionHash = *abi.ConvertType(out[3], new([32]byte)).(*[32]byte)

	return *outstruct, err

}

// ProposalDetails is a free data retrieval call binding the contract method 0x16e9eaec.
//
// Solidity: function proposalDetails(uint256 proposalId) view returns(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash)
func (_LeeaGovernance *LeeaGovernanceSession) ProposalDetails(proposalId *big.Int) (struct {
	Targets         []common.Address
	Values          []*big.Int
	Calldatas       [][]byte
	DescriptionHash [32]byte
}, error) {
	return _LeeaGovernance.Contract.ProposalDetails(&_LeeaGovernance.CallOpts, proposalId)
}

// ProposalDetails is a free data retrieval call binding the contract method 0x16e9eaec.
//
// Solidity: function proposalDetails(uint256 proposalId) view returns(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash)
func (_LeeaGovernance *LeeaGovernanceCallerSession) ProposalDetails(proposalId *big.Int) (struct {
	Targets         []common.Address
	Values          []*big.Int
	Calldatas       [][]byte
	DescriptionHash [32]byte
}, error) {
	return _LeeaGovernance.Contract.ProposalDetails(&_LeeaGovernance.CallOpts, proposalId)
}

// ProposalDetailsAt is a free data retrieval call binding the contract method 0x2e82db94.
//
// Solidity: function proposalDetailsAt(uint256 index) view returns(uint256 proposalId, address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash)
func (_LeeaGovernance *LeeaGovernanceCaller) ProposalDetailsAt(opts *bind.CallOpts, index *big.Int) (struct {
	ProposalId      *big.Int
	Targets         []common.Address
	Values          []*big.Int
	Calldatas       [][]byte
	DescriptionHash [32]byte
}, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "proposalDetailsAt", index)

	outstruct := new(struct {
		ProposalId      *big.Int
		Targets         []common.Address
		Values          []*big.Int
		Calldatas       [][]byte
		DescriptionHash [32]byte
	})
	if err != nil {
		return *outstruct, err
	}

	outstruct.ProposalId = *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)
	outstruct.Targets = *abi.ConvertType(out[1], new([]common.Address)).(*[]common.Address)
	outstruct.Values = *abi.ConvertType(out[2], new([]*big.Int)).(*[]*big.Int)
	outstruct.Calldatas = *abi.ConvertType(out[3], new([][]byte)).(*[][]byte)
	outstruct.DescriptionHash = *abi.ConvertType(out[4], new([32]byte)).(*[32]byte)

	return *outstruct, err

}

// ProposalDetailsAt is a free data retrieval call binding the contract method 0x2e82db94.
//
// Solidity: function proposalDetailsAt(uint256 index) view returns(uint256 proposalId, address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash)
func (_LeeaGovernance *LeeaGovernanceSession) ProposalDetailsAt(index *big.Int) (struct {
	ProposalId      *big.Int
	Targets         []common.Address
	Values          []*big.Int
	Calldatas       [][]byte
	DescriptionHash [32]byte
}, error) {
	return _LeeaGovernance.Contract.ProposalDetailsAt(&_LeeaGovernance.CallOpts, index)
}

// ProposalDetailsAt is a free data retrieval call binding the contract method 0x2e82db94.
//
// Solidity: function proposalDetailsAt(uint256 index) view returns(uint256 proposalId, address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash)
func (_LeeaGovernance *LeeaGovernanceCallerSession) ProposalDetailsAt(index *big.Int) (struct {
	ProposalId      *big.Int
	Targets         []common.Address
	Values          []*big.Int
	Calldatas       [][]byte
	DescriptionHash [32]byte
}, error) {
	return _LeeaGovernance.Contract.ProposalDetailsAt(&_LeeaGovernance.CallOpts, index)
}

// ProposalEta is a free data retrieval call binding the contract method 0xab58fb8e.
//
// Solidity: function proposalEta(uint256 proposalId) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) ProposalEta(opts *bind.CallOpts, proposalId *big.Int) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "proposalEta", proposalId)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// ProposalEta is a free data retrieval call binding the contract method 0xab58fb8e.
//
// Solidity: function proposalEta(uint256 proposalId) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) ProposalEta(proposalId *big.Int) (*big.Int, error) {
	return _LeeaGovernance.Contract.ProposalEta(&_LeeaGovernance.CallOpts, proposalId)
}

// ProposalEta is a free data retrieval call binding the contract method 0xab58fb8e.
//
// Solidity: function proposalEta(uint256 proposalId) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) ProposalEta(proposalId *big.Int) (*big.Int, error) {
	return _LeeaGovernance.Contract.ProposalEta(&_LeeaGovernance.CallOpts, proposalId)
}

// ProposalNeedsQueuing is a free data retrieval call binding the contract method 0xa9a95294.
//
// Solidity: function proposalNeedsQueuing(uint256 ) view returns(bool)
func (_LeeaGovernance *LeeaGovernanceCaller) ProposalNeedsQueuing(opts *bind.CallOpts, arg0 *big.Int) (bool, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "proposalNeedsQueuing", arg0)

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// ProposalNeedsQueuing is a free data retrieval call binding the contract method 0xa9a95294.
//
// Solidity: function proposalNeedsQueuing(uint256 ) view returns(bool)
func (_LeeaGovernance *LeeaGovernanceSession) ProposalNeedsQueuing(arg0 *big.Int) (bool, error) {
	return _LeeaGovernance.Contract.ProposalNeedsQueuing(&_LeeaGovernance.CallOpts, arg0)
}

// ProposalNeedsQueuing is a free data retrieval call binding the contract method 0xa9a95294.
//
// Solidity: function proposalNeedsQueuing(uint256 ) view returns(bool)
func (_LeeaGovernance *LeeaGovernanceCallerSession) ProposalNeedsQueuing(arg0 *big.Int) (bool, error) {
	return _LeeaGovernance.Contract.ProposalNeedsQueuing(&_LeeaGovernance.CallOpts, arg0)
}

// ProposalProposer is a free data retrieval call binding the contract method 0x143489d0.
//
// Solidity: function proposalProposer(uint256 proposalId) view returns(address)
func (_LeeaGovernance *LeeaGovernanceCaller) ProposalProposer(opts *bind.CallOpts, proposalId *big.Int) (common.Address, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "proposalProposer", proposalId)

	if err != nil {
		return *new(common.Address), err
	}

	out0 := *abi.ConvertType(out[0], new(common.Address)).(*common.Address)

	return out0, err

}

// ProposalProposer is a free data retrieval call binding the contract method 0x143489d0.
//
// Solidity: function proposalProposer(uint256 proposalId) view returns(address)
func (_LeeaGovernance *LeeaGovernanceSession) ProposalProposer(proposalId *big.Int) (common.Address, error) {
	return _LeeaGovernance.Contract.ProposalProposer(&_LeeaGovernance.CallOpts, proposalId)
}

// ProposalProposer is a free data retrieval call binding the contract method 0x143489d0.
//
// Solidity: function proposalProposer(uint256 proposalId) view returns(address)
func (_LeeaGovernance *LeeaGovernanceCallerSession) ProposalProposer(proposalId *big.Int) (common.Address, error) {
	return _LeeaGovernance.Contract.ProposalProposer(&_LeeaGovernance.CallOpts, proposalId)
}

// ProposalSnapshot is a free data retrieval call binding the contract method 0x2d63f693.
//
// Solidity: function proposalSnapshot(uint256 proposalId) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) ProposalSnapshot(opts *bind.CallOpts, proposalId *big.Int) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "proposalSnapshot", proposalId)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// ProposalSnapshot is a free data retrieval call binding the contract method 0x2d63f693.
//
// Solidity: function proposalSnapshot(uint256 proposalId) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) ProposalSnapshot(proposalId *big.Int) (*big.Int, error) {
	return _LeeaGovernance.Contract.ProposalSnapshot(&_LeeaGovernance.CallOpts, proposalId)
}

// ProposalSnapshot is a free data retrieval call binding the contract method 0x2d63f693.
//
// Solidity: function proposalSnapshot(uint256 proposalId) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) ProposalSnapshot(proposalId *big.Int) (*big.Int, error) {
	return _LeeaGovernance.Contract.ProposalSnapshot(&_LeeaGovernance.CallOpts, proposalId)
}

// ProposalThreshold is a free data retrieval call binding the contract method 0xb58131b0.
//
// Solidity: function proposalThreshold() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) ProposalThreshold(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "proposalThreshold")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// ProposalThreshold is a free data retrieval call binding the contract method 0xb58131b0.
//
// Solidity: function proposalThreshold() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) ProposalThreshold() (*big.Int, error) {
	return _LeeaGovernance.Contract.ProposalThreshold(&_LeeaGovernance.CallOpts)
}

// ProposalThreshold is a free data retrieval call binding the contract method 0xb58131b0.
//
// Solidity: function proposalThreshold() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) ProposalThreshold() (*big.Int, error) {
	return _LeeaGovernance.Contract.ProposalThreshold(&_LeeaGovernance.CallOpts)
}

// ProposalVotes is a free data retrieval call binding the contract method 0x544ffc9c.
//
// Solidity: function proposalVotes(uint256 proposalId) view returns(uint256 againstVotes, uint256 forVotes, uint256 abstainVotes)
func (_LeeaGovernance *LeeaGovernanceCaller) ProposalVotes(opts *bind.CallOpts, proposalId *big.Int) (struct {
	AgainstVotes *big.Int
	ForVotes     *big.Int
	AbstainVotes *big.Int
}, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "proposalVotes", proposalId)

	outstruct := new(struct {
		AgainstVotes *big.Int
		ForVotes     *big.Int
		AbstainVotes *big.Int
	})
	if err != nil {
		return *outstruct, err
	}

	outstruct.AgainstVotes = *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)
	outstruct.ForVotes = *abi.ConvertType(out[1], new(*big.Int)).(**big.Int)
	outstruct.AbstainVotes = *abi.ConvertType(out[2], new(*big.Int)).(**big.Int)

	return *outstruct, err

}

// ProposalVotes is a free data retrieval call binding the contract method 0x544ffc9c.
//
// Solidity: function proposalVotes(uint256 proposalId) view returns(uint256 againstVotes, uint256 forVotes, uint256 abstainVotes)
func (_LeeaGovernance *LeeaGovernanceSession) ProposalVotes(proposalId *big.Int) (struct {
	AgainstVotes *big.Int
	ForVotes     *big.Int
	AbstainVotes *big.Int
}, error) {
	return _LeeaGovernance.Contract.ProposalVotes(&_LeeaGovernance.CallOpts, proposalId)
}

// ProposalVotes is a free data retrieval call binding the contract method 0x544ffc9c.
//
// Solidity: function proposalVotes(uint256 proposalId) view returns(uint256 againstVotes, uint256 forVotes, uint256 abstainVotes)
func (_LeeaGovernance *LeeaGovernanceCallerSession) ProposalVotes(proposalId *big.Int) (struct {
	AgainstVotes *big.Int
	ForVotes     *big.Int
	AbstainVotes *big.Int
}, error) {
	return _LeeaGovernance.Contract.ProposalVotes(&_LeeaGovernance.CallOpts, proposalId)
}

// Quorum is a free data retrieval call binding the contract method 0xf8ce560a.
//
// Solidity: function quorum(uint256 blockNumber) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) Quorum(opts *bind.CallOpts, blockNumber *big.Int) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "quorum", blockNumber)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// Quorum is a free data retrieval call binding the contract method 0xf8ce560a.
//
// Solidity: function quorum(uint256 blockNumber) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) Quorum(blockNumber *big.Int) (*big.Int, error) {
	return _LeeaGovernance.Contract.Quorum(&_LeeaGovernance.CallOpts, blockNumber)
}

// Quorum is a free data retrieval call binding the contract method 0xf8ce560a.
//
// Solidity: function quorum(uint256 blockNumber) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) Quorum(blockNumber *big.Int) (*big.Int, error) {
	return _LeeaGovernance.Contract.Quorum(&_LeeaGovernance.CallOpts, blockNumber)
}

// QuorumDenominator is a free data retrieval call binding the contract method 0x97c3d334.
//
// Solidity: function quorumDenominator() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) QuorumDenominator(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "quorumDenominator")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// QuorumDenominator is a free data retrieval call binding the contract method 0x97c3d334.
//
// Solidity: function quorumDenominator() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) QuorumDenominator() (*big.Int, error) {
	return _LeeaGovernance.Contract.QuorumDenominator(&_LeeaGovernance.CallOpts)
}

// QuorumDenominator is a free data retrieval call binding the contract method 0x97c3d334.
//
// Solidity: function quorumDenominator() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) QuorumDenominator() (*big.Int, error) {
	return _LeeaGovernance.Contract.QuorumDenominator(&_LeeaGovernance.CallOpts)
}

// QuorumNumerator is a free data retrieval call binding the contract method 0x60c4247f.
//
// Solidity: function quorumNumerator(uint256 timepoint) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) QuorumNumerator(opts *bind.CallOpts, timepoint *big.Int) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "quorumNumerator", timepoint)

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// QuorumNumerator is a free data retrieval call binding the contract method 0x60c4247f.
//
// Solidity: function quorumNumerator(uint256 timepoint) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) QuorumNumerator(timepoint *big.Int) (*big.Int, error) {
	return _LeeaGovernance.Contract.QuorumNumerator(&_LeeaGovernance.CallOpts, timepoint)
}

// QuorumNumerator is a free data retrieval call binding the contract method 0x60c4247f.
//
// Solidity: function quorumNumerator(uint256 timepoint) view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) QuorumNumerator(timepoint *big.Int) (*big.Int, error) {
	return _LeeaGovernance.Contract.QuorumNumerator(&_LeeaGovernance.CallOpts, timepoint)
}

// QuorumNumerator0 is a free data retrieval call binding the contract method 0xa7713a70.
//
// Solidity: function quorumNumerator() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) QuorumNumerator0(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "quorumNumerator0")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// QuorumNumerator0 is a free data retrieval call binding the contract method 0xa7713a70.
//
// Solidity: function quorumNumerator() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) QuorumNumerator0() (*big.Int, error) {
	return _LeeaGovernance.Contract.QuorumNumerator0(&_LeeaGovernance.CallOpts)
}

// QuorumNumerator0 is a free data retrieval call binding the contract method 0xa7713a70.
//
// Solidity: function quorumNumerator() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) QuorumNumerator0() (*big.Int, error) {
	return _LeeaGovernance.Contract.QuorumNumerator0(&_LeeaGovernance.CallOpts)
}

// State is a free data retrieval call binding the contract method 0x3e4f49e6.
//
// Solidity: function state(uint256 proposalId) view returns(uint8)
func (_LeeaGovernance *LeeaGovernanceCaller) State(opts *bind.CallOpts, proposalId *big.Int) (uint8, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "state", proposalId)

	if err != nil {
		return *new(uint8), err
	}

	out0 := *abi.ConvertType(out[0], new(uint8)).(*uint8)

	return out0, err

}

// State is a free data retrieval call binding the contract method 0x3e4f49e6.
//
// Solidity: function state(uint256 proposalId) view returns(uint8)
func (_LeeaGovernance *LeeaGovernanceSession) State(proposalId *big.Int) (uint8, error) {
	return _LeeaGovernance.Contract.State(&_LeeaGovernance.CallOpts, proposalId)
}

// State is a free data retrieval call binding the contract method 0x3e4f49e6.
//
// Solidity: function state(uint256 proposalId) view returns(uint8)
func (_LeeaGovernance *LeeaGovernanceCallerSession) State(proposalId *big.Int) (uint8, error) {
	return _LeeaGovernance.Contract.State(&_LeeaGovernance.CallOpts, proposalId)
}

// SupportsInterface is a free data retrieval call binding the contract method 0x01ffc9a7.
//
// Solidity: function supportsInterface(bytes4 interfaceId) view returns(bool)
func (_LeeaGovernance *LeeaGovernanceCaller) SupportsInterface(opts *bind.CallOpts, interfaceId [4]byte) (bool, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "supportsInterface", interfaceId)

	if err != nil {
		return *new(bool), err
	}

	out0 := *abi.ConvertType(out[0], new(bool)).(*bool)

	return out0, err

}

// SupportsInterface is a free data retrieval call binding the contract method 0x01ffc9a7.
//
// Solidity: function supportsInterface(bytes4 interfaceId) view returns(bool)
func (_LeeaGovernance *LeeaGovernanceSession) SupportsInterface(interfaceId [4]byte) (bool, error) {
	return _LeeaGovernance.Contract.SupportsInterface(&_LeeaGovernance.CallOpts, interfaceId)
}

// SupportsInterface is a free data retrieval call binding the contract method 0x01ffc9a7.
//
// Solidity: function supportsInterface(bytes4 interfaceId) view returns(bool)
func (_LeeaGovernance *LeeaGovernanceCallerSession) SupportsInterface(interfaceId [4]byte) (bool, error) {
	return _LeeaGovernance.Contract.SupportsInterface(&_LeeaGovernance.CallOpts, interfaceId)
}

// Token is a free data retrieval call binding the contract method 0xfc0c546a.
//
// Solidity: function token() view returns(address)
func (_LeeaGovernance *LeeaGovernanceCaller) Token(opts *bind.CallOpts) (common.Address, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "token")

	if err != nil {
		return *new(common.Address), err
	}

	out0 := *abi.ConvertType(out[0], new(common.Address)).(*common.Address)

	return out0, err

}

// Token is a free data retrieval call binding the contract method 0xfc0c546a.
//
// Solidity: function token() view returns(address)
func (_LeeaGovernance *LeeaGovernanceSession) Token() (common.Address, error) {
	return _LeeaGovernance.Contract.Token(&_LeeaGovernance.CallOpts)
}

// Token is a free data retrieval call binding the contract method 0xfc0c546a.
//
// Solidity: function token() view returns(address)
func (_LeeaGovernance *LeeaGovernanceCallerSession) Token() (common.Address, error) {
	return _LeeaGovernance.Contract.Token(&_LeeaGovernance.CallOpts)
}

// Version is a free data retrieval call binding the contract method 0x54fd4d50.
//
// Solidity: function version() view returns(string)
func (_LeeaGovernance *LeeaGovernanceCaller) Version(opts *bind.CallOpts) (string, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "version")

	if err != nil {
		return *new(string), err
	}

	out0 := *abi.ConvertType(out[0], new(string)).(*string)

	return out0, err

}

// Version is a free data retrieval call binding the contract method 0x54fd4d50.
//
// Solidity: function version() view returns(string)
func (_LeeaGovernance *LeeaGovernanceSession) Version() (string, error) {
	return _LeeaGovernance.Contract.Version(&_LeeaGovernance.CallOpts)
}

// Version is a free data retrieval call binding the contract method 0x54fd4d50.
//
// Solidity: function version() view returns(string)
func (_LeeaGovernance *LeeaGovernanceCallerSession) Version() (string, error) {
	return _LeeaGovernance.Contract.Version(&_LeeaGovernance.CallOpts)
}

// VotingDelay is a free data retrieval call binding the contract method 0x3932abb1.
//
// Solidity: function votingDelay() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) VotingDelay(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "votingDelay")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// VotingDelay is a free data retrieval call binding the contract method 0x3932abb1.
//
// Solidity: function votingDelay() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) VotingDelay() (*big.Int, error) {
	return _LeeaGovernance.Contract.VotingDelay(&_LeeaGovernance.CallOpts)
}

// VotingDelay is a free data retrieval call binding the contract method 0x3932abb1.
//
// Solidity: function votingDelay() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) VotingDelay() (*big.Int, error) {
	return _LeeaGovernance.Contract.VotingDelay(&_LeeaGovernance.CallOpts)
}

// VotingPeriod is a free data retrieval call binding the contract method 0x02a251a3.
//
// Solidity: function votingPeriod() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCaller) VotingPeriod(opts *bind.CallOpts) (*big.Int, error) {
	var out []interface{}
	err := _LeeaGovernance.contract.Call(opts, &out, "votingPeriod")

	if err != nil {
		return *new(*big.Int), err
	}

	out0 := *abi.ConvertType(out[0], new(*big.Int)).(**big.Int)

	return out0, err

}

// VotingPeriod is a free data retrieval call binding the contract method 0x02a251a3.
//
// Solidity: function votingPeriod() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) VotingPeriod() (*big.Int, error) {
	return _LeeaGovernance.Contract.VotingPeriod(&_LeeaGovernance.CallOpts)
}

// VotingPeriod is a free data retrieval call binding the contract method 0x02a251a3.
//
// Solidity: function votingPeriod() view returns(uint256)
func (_LeeaGovernance *LeeaGovernanceCallerSession) VotingPeriod() (*big.Int, error) {
	return _LeeaGovernance.Contract.VotingPeriod(&_LeeaGovernance.CallOpts)
}

// Cancel is a paid mutator transaction binding the contract method 0x40e58ee5.
//
// Solidity: function cancel(uint256 proposalId) returns()
func (_LeeaGovernance *LeeaGovernanceTransactor) Cancel(opts *bind.TransactOpts, proposalId *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "cancel", proposalId)
}

// Cancel is a paid mutator transaction binding the contract method 0x40e58ee5.
//
// Solidity: function cancel(uint256 proposalId) returns()
func (_LeeaGovernance *LeeaGovernanceSession) Cancel(proposalId *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Cancel(&_LeeaGovernance.TransactOpts, proposalId)
}

// Cancel is a paid mutator transaction binding the contract method 0x40e58ee5.
//
// Solidity: function cancel(uint256 proposalId) returns()
func (_LeeaGovernance *LeeaGovernanceTransactorSession) Cancel(proposalId *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Cancel(&_LeeaGovernance.TransactOpts, proposalId)
}

// Cancel0 is a paid mutator transaction binding the contract method 0x452115d6.
//
// Solidity: function cancel(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactor) Cancel0(opts *bind.TransactOpts, targets []common.Address, values []*big.Int, calldatas [][]byte, descriptionHash [32]byte) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "cancel0", targets, values, calldatas, descriptionHash)
}

// Cancel0 is a paid mutator transaction binding the contract method 0x452115d6.
//
// Solidity: function cancel(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) Cancel0(targets []common.Address, values []*big.Int, calldatas [][]byte, descriptionHash [32]byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Cancel0(&_LeeaGovernance.TransactOpts, targets, values, calldatas, descriptionHash)
}

// Cancel0 is a paid mutator transaction binding the contract method 0x452115d6.
//
// Solidity: function cancel(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactorSession) Cancel0(targets []common.Address, values []*big.Int, calldatas [][]byte, descriptionHash [32]byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Cancel0(&_LeeaGovernance.TransactOpts, targets, values, calldatas, descriptionHash)
}

// CastVote is a paid mutator transaction binding the contract method 0x56781388.
//
// Solidity: function castVote(uint256 proposalId, uint8 support) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactor) CastVote(opts *bind.TransactOpts, proposalId *big.Int, support uint8) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "castVote", proposalId, support)
}

// CastVote is a paid mutator transaction binding the contract method 0x56781388.
//
// Solidity: function castVote(uint256 proposalId, uint8 support) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) CastVote(proposalId *big.Int, support uint8) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.CastVote(&_LeeaGovernance.TransactOpts, proposalId, support)
}

// CastVote is a paid mutator transaction binding the contract method 0x56781388.
//
// Solidity: function castVote(uint256 proposalId, uint8 support) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactorSession) CastVote(proposalId *big.Int, support uint8) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.CastVote(&_LeeaGovernance.TransactOpts, proposalId, support)
}

// CastVoteBySig is a paid mutator transaction binding the contract method 0x8ff262e3.
//
// Solidity: function castVoteBySig(uint256 proposalId, uint8 support, address voter, bytes signature) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactor) CastVoteBySig(opts *bind.TransactOpts, proposalId *big.Int, support uint8, voter common.Address, signature []byte) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "castVoteBySig", proposalId, support, voter, signature)
}

// CastVoteBySig is a paid mutator transaction binding the contract method 0x8ff262e3.
//
// Solidity: function castVoteBySig(uint256 proposalId, uint8 support, address voter, bytes signature) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) CastVoteBySig(proposalId *big.Int, support uint8, voter common.Address, signature []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.CastVoteBySig(&_LeeaGovernance.TransactOpts, proposalId, support, voter, signature)
}

// CastVoteBySig is a paid mutator transaction binding the contract method 0x8ff262e3.
//
// Solidity: function castVoteBySig(uint256 proposalId, uint8 support, address voter, bytes signature) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactorSession) CastVoteBySig(proposalId *big.Int, support uint8, voter common.Address, signature []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.CastVoteBySig(&_LeeaGovernance.TransactOpts, proposalId, support, voter, signature)
}

// CastVoteWithReason is a paid mutator transaction binding the contract method 0x7b3c71d3.
//
// Solidity: function castVoteWithReason(uint256 proposalId, uint8 support, string reason) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactor) CastVoteWithReason(opts *bind.TransactOpts, proposalId *big.Int, support uint8, reason string) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "castVoteWithReason", proposalId, support, reason)
}

// CastVoteWithReason is a paid mutator transaction binding the contract method 0x7b3c71d3.
//
// Solidity: function castVoteWithReason(uint256 proposalId, uint8 support, string reason) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) CastVoteWithReason(proposalId *big.Int, support uint8, reason string) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.CastVoteWithReason(&_LeeaGovernance.TransactOpts, proposalId, support, reason)
}

// CastVoteWithReason is a paid mutator transaction binding the contract method 0x7b3c71d3.
//
// Solidity: function castVoteWithReason(uint256 proposalId, uint8 support, string reason) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactorSession) CastVoteWithReason(proposalId *big.Int, support uint8, reason string) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.CastVoteWithReason(&_LeeaGovernance.TransactOpts, proposalId, support, reason)
}

// CastVoteWithReasonAndParams is a paid mutator transaction binding the contract method 0x5f398a14.
//
// Solidity: function castVoteWithReasonAndParams(uint256 proposalId, uint8 support, string reason, bytes params) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactor) CastVoteWithReasonAndParams(opts *bind.TransactOpts, proposalId *big.Int, support uint8, reason string, params []byte) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "castVoteWithReasonAndParams", proposalId, support, reason, params)
}

// CastVoteWithReasonAndParams is a paid mutator transaction binding the contract method 0x5f398a14.
//
// Solidity: function castVoteWithReasonAndParams(uint256 proposalId, uint8 support, string reason, bytes params) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) CastVoteWithReasonAndParams(proposalId *big.Int, support uint8, reason string, params []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.CastVoteWithReasonAndParams(&_LeeaGovernance.TransactOpts, proposalId, support, reason, params)
}

// CastVoteWithReasonAndParams is a paid mutator transaction binding the contract method 0x5f398a14.
//
// Solidity: function castVoteWithReasonAndParams(uint256 proposalId, uint8 support, string reason, bytes params) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactorSession) CastVoteWithReasonAndParams(proposalId *big.Int, support uint8, reason string, params []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.CastVoteWithReasonAndParams(&_LeeaGovernance.TransactOpts, proposalId, support, reason, params)
}

// CastVoteWithReasonAndParamsBySig is a paid mutator transaction binding the contract method 0x5b8d0e0d.
//
// Solidity: function castVoteWithReasonAndParamsBySig(uint256 proposalId, uint8 support, address voter, string reason, bytes params, bytes signature) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactor) CastVoteWithReasonAndParamsBySig(opts *bind.TransactOpts, proposalId *big.Int, support uint8, voter common.Address, reason string, params []byte, signature []byte) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "castVoteWithReasonAndParamsBySig", proposalId, support, voter, reason, params, signature)
}

// CastVoteWithReasonAndParamsBySig is a paid mutator transaction binding the contract method 0x5b8d0e0d.
//
// Solidity: function castVoteWithReasonAndParamsBySig(uint256 proposalId, uint8 support, address voter, string reason, bytes params, bytes signature) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) CastVoteWithReasonAndParamsBySig(proposalId *big.Int, support uint8, voter common.Address, reason string, params []byte, signature []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.CastVoteWithReasonAndParamsBySig(&_LeeaGovernance.TransactOpts, proposalId, support, voter, reason, params, signature)
}

// CastVoteWithReasonAndParamsBySig is a paid mutator transaction binding the contract method 0x5b8d0e0d.
//
// Solidity: function castVoteWithReasonAndParamsBySig(uint256 proposalId, uint8 support, address voter, string reason, bytes params, bytes signature) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactorSession) CastVoteWithReasonAndParamsBySig(proposalId *big.Int, support uint8, voter common.Address, reason string, params []byte, signature []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.CastVoteWithReasonAndParamsBySig(&_LeeaGovernance.TransactOpts, proposalId, support, voter, reason, params, signature)
}

// Execute is a paid mutator transaction binding the contract method 0x2656227d.
//
// Solidity: function execute(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash) payable returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactor) Execute(opts *bind.TransactOpts, targets []common.Address, values []*big.Int, calldatas [][]byte, descriptionHash [32]byte) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "execute", targets, values, calldatas, descriptionHash)
}

// Execute is a paid mutator transaction binding the contract method 0x2656227d.
//
// Solidity: function execute(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash) payable returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) Execute(targets []common.Address, values []*big.Int, calldatas [][]byte, descriptionHash [32]byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Execute(&_LeeaGovernance.TransactOpts, targets, values, calldatas, descriptionHash)
}

// Execute is a paid mutator transaction binding the contract method 0x2656227d.
//
// Solidity: function execute(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash) payable returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactorSession) Execute(targets []common.Address, values []*big.Int, calldatas [][]byte, descriptionHash [32]byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Execute(&_LeeaGovernance.TransactOpts, targets, values, calldatas, descriptionHash)
}

// Execute0 is a paid mutator transaction binding the contract method 0xfe0d94c1.
//
// Solidity: function execute(uint256 proposalId) payable returns()
func (_LeeaGovernance *LeeaGovernanceTransactor) Execute0(opts *bind.TransactOpts, proposalId *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "execute0", proposalId)
}

// Execute0 is a paid mutator transaction binding the contract method 0xfe0d94c1.
//
// Solidity: function execute(uint256 proposalId) payable returns()
func (_LeeaGovernance *LeeaGovernanceSession) Execute0(proposalId *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Execute0(&_LeeaGovernance.TransactOpts, proposalId)
}

// Execute0 is a paid mutator transaction binding the contract method 0xfe0d94c1.
//
// Solidity: function execute(uint256 proposalId) payable returns()
func (_LeeaGovernance *LeeaGovernanceTransactorSession) Execute0(proposalId *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Execute0(&_LeeaGovernance.TransactOpts, proposalId)
}

// OnERC1155BatchReceived is a paid mutator transaction binding the contract method 0xbc197c81.
//
// Solidity: function onERC1155BatchReceived(address , address , uint256[] , uint256[] , bytes ) returns(bytes4)
func (_LeeaGovernance *LeeaGovernanceTransactor) OnERC1155BatchReceived(opts *bind.TransactOpts, arg0 common.Address, arg1 common.Address, arg2 []*big.Int, arg3 []*big.Int, arg4 []byte) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "onERC1155BatchReceived", arg0, arg1, arg2, arg3, arg4)
}

// OnERC1155BatchReceived is a paid mutator transaction binding the contract method 0xbc197c81.
//
// Solidity: function onERC1155BatchReceived(address , address , uint256[] , uint256[] , bytes ) returns(bytes4)
func (_LeeaGovernance *LeeaGovernanceSession) OnERC1155BatchReceived(arg0 common.Address, arg1 common.Address, arg2 []*big.Int, arg3 []*big.Int, arg4 []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.OnERC1155BatchReceived(&_LeeaGovernance.TransactOpts, arg0, arg1, arg2, arg3, arg4)
}

// OnERC1155BatchReceived is a paid mutator transaction binding the contract method 0xbc197c81.
//
// Solidity: function onERC1155BatchReceived(address , address , uint256[] , uint256[] , bytes ) returns(bytes4)
func (_LeeaGovernance *LeeaGovernanceTransactorSession) OnERC1155BatchReceived(arg0 common.Address, arg1 common.Address, arg2 []*big.Int, arg3 []*big.Int, arg4 []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.OnERC1155BatchReceived(&_LeeaGovernance.TransactOpts, arg0, arg1, arg2, arg3, arg4)
}

// OnERC1155Received is a paid mutator transaction binding the contract method 0xf23a6e61.
//
// Solidity: function onERC1155Received(address , address , uint256 , uint256 , bytes ) returns(bytes4)
func (_LeeaGovernance *LeeaGovernanceTransactor) OnERC1155Received(opts *bind.TransactOpts, arg0 common.Address, arg1 common.Address, arg2 *big.Int, arg3 *big.Int, arg4 []byte) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "onERC1155Received", arg0, arg1, arg2, arg3, arg4)
}

// OnERC1155Received is a paid mutator transaction binding the contract method 0xf23a6e61.
//
// Solidity: function onERC1155Received(address , address , uint256 , uint256 , bytes ) returns(bytes4)
func (_LeeaGovernance *LeeaGovernanceSession) OnERC1155Received(arg0 common.Address, arg1 common.Address, arg2 *big.Int, arg3 *big.Int, arg4 []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.OnERC1155Received(&_LeeaGovernance.TransactOpts, arg0, arg1, arg2, arg3, arg4)
}

// OnERC1155Received is a paid mutator transaction binding the contract method 0xf23a6e61.
//
// Solidity: function onERC1155Received(address , address , uint256 , uint256 , bytes ) returns(bytes4)
func (_LeeaGovernance *LeeaGovernanceTransactorSession) OnERC1155Received(arg0 common.Address, arg1 common.Address, arg2 *big.Int, arg3 *big.Int, arg4 []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.OnERC1155Received(&_LeeaGovernance.TransactOpts, arg0, arg1, arg2, arg3, arg4)
}

// OnERC721Received is a paid mutator transaction binding the contract method 0x150b7a02.
//
// Solidity: function onERC721Received(address , address , uint256 , bytes ) returns(bytes4)
func (_LeeaGovernance *LeeaGovernanceTransactor) OnERC721Received(opts *bind.TransactOpts, arg0 common.Address, arg1 common.Address, arg2 *big.Int, arg3 []byte) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "onERC721Received", arg0, arg1, arg2, arg3)
}

// OnERC721Received is a paid mutator transaction binding the contract method 0x150b7a02.
//
// Solidity: function onERC721Received(address , address , uint256 , bytes ) returns(bytes4)
func (_LeeaGovernance *LeeaGovernanceSession) OnERC721Received(arg0 common.Address, arg1 common.Address, arg2 *big.Int, arg3 []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.OnERC721Received(&_LeeaGovernance.TransactOpts, arg0, arg1, arg2, arg3)
}

// OnERC721Received is a paid mutator transaction binding the contract method 0x150b7a02.
//
// Solidity: function onERC721Received(address , address , uint256 , bytes ) returns(bytes4)
func (_LeeaGovernance *LeeaGovernanceTransactorSession) OnERC721Received(arg0 common.Address, arg1 common.Address, arg2 *big.Int, arg3 []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.OnERC721Received(&_LeeaGovernance.TransactOpts, arg0, arg1, arg2, arg3)
}

// Propose is a paid mutator transaction binding the contract method 0x7d5e81e2.
//
// Solidity: function propose(address[] targets, uint256[] values, bytes[] calldatas, string description) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactor) Propose(opts *bind.TransactOpts, targets []common.Address, values []*big.Int, calldatas [][]byte, description string) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "propose", targets, values, calldatas, description)
}

// Propose is a paid mutator transaction binding the contract method 0x7d5e81e2.
//
// Solidity: function propose(address[] targets, uint256[] values, bytes[] calldatas, string description) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) Propose(targets []common.Address, values []*big.Int, calldatas [][]byte, description string) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Propose(&_LeeaGovernance.TransactOpts, targets, values, calldatas, description)
}

// Propose is a paid mutator transaction binding the contract method 0x7d5e81e2.
//
// Solidity: function propose(address[] targets, uint256[] values, bytes[] calldatas, string description) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactorSession) Propose(targets []common.Address, values []*big.Int, calldatas [][]byte, description string) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Propose(&_LeeaGovernance.TransactOpts, targets, values, calldatas, description)
}

// Queue is a paid mutator transaction binding the contract method 0x160cbed7.
//
// Solidity: function queue(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactor) Queue(opts *bind.TransactOpts, targets []common.Address, values []*big.Int, calldatas [][]byte, descriptionHash [32]byte) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "queue", targets, values, calldatas, descriptionHash)
}

// Queue is a paid mutator transaction binding the contract method 0x160cbed7.
//
// Solidity: function queue(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceSession) Queue(targets []common.Address, values []*big.Int, calldatas [][]byte, descriptionHash [32]byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Queue(&_LeeaGovernance.TransactOpts, targets, values, calldatas, descriptionHash)
}

// Queue is a paid mutator transaction binding the contract method 0x160cbed7.
//
// Solidity: function queue(address[] targets, uint256[] values, bytes[] calldatas, bytes32 descriptionHash) returns(uint256)
func (_LeeaGovernance *LeeaGovernanceTransactorSession) Queue(targets []common.Address, values []*big.Int, calldatas [][]byte, descriptionHash [32]byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Queue(&_LeeaGovernance.TransactOpts, targets, values, calldatas, descriptionHash)
}

// Queue0 is a paid mutator transaction binding the contract method 0xddf0b009.
//
// Solidity: function queue(uint256 proposalId) returns()
func (_LeeaGovernance *LeeaGovernanceTransactor) Queue0(opts *bind.TransactOpts, proposalId *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "queue0", proposalId)
}

// Queue0 is a paid mutator transaction binding the contract method 0xddf0b009.
//
// Solidity: function queue(uint256 proposalId) returns()
func (_LeeaGovernance *LeeaGovernanceSession) Queue0(proposalId *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Queue0(&_LeeaGovernance.TransactOpts, proposalId)
}

// Queue0 is a paid mutator transaction binding the contract method 0xddf0b009.
//
// Solidity: function queue(uint256 proposalId) returns()
func (_LeeaGovernance *LeeaGovernanceTransactorSession) Queue0(proposalId *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Queue0(&_LeeaGovernance.TransactOpts, proposalId)
}

// Relay is a paid mutator transaction binding the contract method 0xc28bc2fa.
//
// Solidity: function relay(address target, uint256 value, bytes data) payable returns()
func (_LeeaGovernance *LeeaGovernanceTransactor) Relay(opts *bind.TransactOpts, target common.Address, value *big.Int, data []byte) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "relay", target, value, data)
}

// Relay is a paid mutator transaction binding the contract method 0xc28bc2fa.
//
// Solidity: function relay(address target, uint256 value, bytes data) payable returns()
func (_LeeaGovernance *LeeaGovernanceSession) Relay(target common.Address, value *big.Int, data []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Relay(&_LeeaGovernance.TransactOpts, target, value, data)
}

// Relay is a paid mutator transaction binding the contract method 0xc28bc2fa.
//
// Solidity: function relay(address target, uint256 value, bytes data) payable returns()
func (_LeeaGovernance *LeeaGovernanceTransactorSession) Relay(target common.Address, value *big.Int, data []byte) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Relay(&_LeeaGovernance.TransactOpts, target, value, data)
}

// SetProposalThreshold is a paid mutator transaction binding the contract method 0xece40cc1.
//
// Solidity: function setProposalThreshold(uint256 newProposalThreshold) returns()
func (_LeeaGovernance *LeeaGovernanceTransactor) SetProposalThreshold(opts *bind.TransactOpts, newProposalThreshold *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "setProposalThreshold", newProposalThreshold)
}

// SetProposalThreshold is a paid mutator transaction binding the contract method 0xece40cc1.
//
// Solidity: function setProposalThreshold(uint256 newProposalThreshold) returns()
func (_LeeaGovernance *LeeaGovernanceSession) SetProposalThreshold(newProposalThreshold *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.SetProposalThreshold(&_LeeaGovernance.TransactOpts, newProposalThreshold)
}

// SetProposalThreshold is a paid mutator transaction binding the contract method 0xece40cc1.
//
// Solidity: function setProposalThreshold(uint256 newProposalThreshold) returns()
func (_LeeaGovernance *LeeaGovernanceTransactorSession) SetProposalThreshold(newProposalThreshold *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.SetProposalThreshold(&_LeeaGovernance.TransactOpts, newProposalThreshold)
}

// SetVotingDelay is a paid mutator transaction binding the contract method 0x79051887.
//
// Solidity: function setVotingDelay(uint48 newVotingDelay) returns()
func (_LeeaGovernance *LeeaGovernanceTransactor) SetVotingDelay(opts *bind.TransactOpts, newVotingDelay *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "setVotingDelay", newVotingDelay)
}

// SetVotingDelay is a paid mutator transaction binding the contract method 0x79051887.
//
// Solidity: function setVotingDelay(uint48 newVotingDelay) returns()
func (_LeeaGovernance *LeeaGovernanceSession) SetVotingDelay(newVotingDelay *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.SetVotingDelay(&_LeeaGovernance.TransactOpts, newVotingDelay)
}

// SetVotingDelay is a paid mutator transaction binding the contract method 0x79051887.
//
// Solidity: function setVotingDelay(uint48 newVotingDelay) returns()
func (_LeeaGovernance *LeeaGovernanceTransactorSession) SetVotingDelay(newVotingDelay *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.SetVotingDelay(&_LeeaGovernance.TransactOpts, newVotingDelay)
}

// SetVotingPeriod is a paid mutator transaction binding the contract method 0xe540d01d.
//
// Solidity: function setVotingPeriod(uint32 newVotingPeriod) returns()
func (_LeeaGovernance *LeeaGovernanceTransactor) SetVotingPeriod(opts *bind.TransactOpts, newVotingPeriod uint32) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "setVotingPeriod", newVotingPeriod)
}

// SetVotingPeriod is a paid mutator transaction binding the contract method 0xe540d01d.
//
// Solidity: function setVotingPeriod(uint32 newVotingPeriod) returns()
func (_LeeaGovernance *LeeaGovernanceSession) SetVotingPeriod(newVotingPeriod uint32) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.SetVotingPeriod(&_LeeaGovernance.TransactOpts, newVotingPeriod)
}

// SetVotingPeriod is a paid mutator transaction binding the contract method 0xe540d01d.
//
// Solidity: function setVotingPeriod(uint32 newVotingPeriod) returns()
func (_LeeaGovernance *LeeaGovernanceTransactorSession) SetVotingPeriod(newVotingPeriod uint32) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.SetVotingPeriod(&_LeeaGovernance.TransactOpts, newVotingPeriod)
}

// UpdateQuorumNumerator is a paid mutator transaction binding the contract method 0x06f3f9e6.
//
// Solidity: function updateQuorumNumerator(uint256 newQuorumNumerator) returns()
func (_LeeaGovernance *LeeaGovernanceTransactor) UpdateQuorumNumerator(opts *bind.TransactOpts, newQuorumNumerator *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.contract.Transact(opts, "updateQuorumNumerator", newQuorumNumerator)
}

// UpdateQuorumNumerator is a paid mutator transaction binding the contract method 0x06f3f9e6.
//
// Solidity: function updateQuorumNumerator(uint256 newQuorumNumerator) returns()
func (_LeeaGovernance *LeeaGovernanceSession) UpdateQuorumNumerator(newQuorumNumerator *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.UpdateQuorumNumerator(&_LeeaGovernance.TransactOpts, newQuorumNumerator)
}

// UpdateQuorumNumerator is a paid mutator transaction binding the contract method 0x06f3f9e6.
//
// Solidity: function updateQuorumNumerator(uint256 newQuorumNumerator) returns()
func (_LeeaGovernance *LeeaGovernanceTransactorSession) UpdateQuorumNumerator(newQuorumNumerator *big.Int) (*types.Transaction, error) {
	return _LeeaGovernance.Contract.UpdateQuorumNumerator(&_LeeaGovernance.TransactOpts, newQuorumNumerator)
}

// Receive is a paid mutator transaction binding the contract receive function.
//
// Solidity: receive() payable returns()
func (_LeeaGovernance *LeeaGovernanceTransactor) Receive(opts *bind.TransactOpts) (*types.Transaction, error) {
	return _LeeaGovernance.contract.RawTransact(opts, nil) // calldata is disallowed for receive function
}

// Receive is a paid mutator transaction binding the contract receive function.
//
// Solidity: receive() payable returns()
func (_LeeaGovernance *LeeaGovernanceSession) Receive() (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Receive(&_LeeaGovernance.TransactOpts)
}

// Receive is a paid mutator transaction binding the contract receive function.
//
// Solidity: receive() payable returns()
func (_LeeaGovernance *LeeaGovernanceTransactorSession) Receive() (*types.Transaction, error) {
	return _LeeaGovernance.Contract.Receive(&_LeeaGovernance.TransactOpts)
}

// LeeaGovernanceEIP712DomainChangedIterator is returned from FilterEIP712DomainChanged and is used to iterate over the raw logs and unpacked data for EIP712DomainChanged events raised by the LeeaGovernance contract.
type LeeaGovernanceEIP712DomainChangedIterator struct {
	Event *LeeaGovernanceEIP712DomainChanged // Event containing the contract specifics and raw log

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
func (it *LeeaGovernanceEIP712DomainChangedIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(LeeaGovernanceEIP712DomainChanged)
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
		it.Event = new(LeeaGovernanceEIP712DomainChanged)
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
func (it *LeeaGovernanceEIP712DomainChangedIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *LeeaGovernanceEIP712DomainChangedIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// LeeaGovernanceEIP712DomainChanged represents a EIP712DomainChanged event raised by the LeeaGovernance contract.
type LeeaGovernanceEIP712DomainChanged struct {
	Raw types.Log // Blockchain specific contextual infos
}

// FilterEIP712DomainChanged is a free log retrieval operation binding the contract event 0x0a6387c9ea3628b88a633bb4f3b151770f70085117a15f9bf3787cda53f13d31.
//
// Solidity: event EIP712DomainChanged()
func (_LeeaGovernance *LeeaGovernanceFilterer) FilterEIP712DomainChanged(opts *bind.FilterOpts) (*LeeaGovernanceEIP712DomainChangedIterator, error) {

	logs, sub, err := _LeeaGovernance.contract.FilterLogs(opts, "EIP712DomainChanged")
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceEIP712DomainChangedIterator{contract: _LeeaGovernance.contract, event: "EIP712DomainChanged", logs: logs, sub: sub}, nil
}

// WatchEIP712DomainChanged is a free log subscription operation binding the contract event 0x0a6387c9ea3628b88a633bb4f3b151770f70085117a15f9bf3787cda53f13d31.
//
// Solidity: event EIP712DomainChanged()
func (_LeeaGovernance *LeeaGovernanceFilterer) WatchEIP712DomainChanged(opts *bind.WatchOpts, sink chan<- *LeeaGovernanceEIP712DomainChanged) (event.Subscription, error) {

	logs, sub, err := _LeeaGovernance.contract.WatchLogs(opts, "EIP712DomainChanged")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(LeeaGovernanceEIP712DomainChanged)
				if err := _LeeaGovernance.contract.UnpackLog(event, "EIP712DomainChanged", log); err != nil {
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

// ParseEIP712DomainChanged is a log parse operation binding the contract event 0x0a6387c9ea3628b88a633bb4f3b151770f70085117a15f9bf3787cda53f13d31.
//
// Solidity: event EIP712DomainChanged()
func (_LeeaGovernance *LeeaGovernanceFilterer) ParseEIP712DomainChanged(log types.Log) (*LeeaGovernanceEIP712DomainChanged, error) {
	event := new(LeeaGovernanceEIP712DomainChanged)
	if err := _LeeaGovernance.contract.UnpackLog(event, "EIP712DomainChanged", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// LeeaGovernanceProposalCanceledIterator is returned from FilterProposalCanceled and is used to iterate over the raw logs and unpacked data for ProposalCanceled events raised by the LeeaGovernance contract.
type LeeaGovernanceProposalCanceledIterator struct {
	Event *LeeaGovernanceProposalCanceled // Event containing the contract specifics and raw log

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
func (it *LeeaGovernanceProposalCanceledIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(LeeaGovernanceProposalCanceled)
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
		it.Event = new(LeeaGovernanceProposalCanceled)
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
func (it *LeeaGovernanceProposalCanceledIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *LeeaGovernanceProposalCanceledIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// LeeaGovernanceProposalCanceled represents a ProposalCanceled event raised by the LeeaGovernance contract.
type LeeaGovernanceProposalCanceled struct {
	ProposalId *big.Int
	Raw        types.Log // Blockchain specific contextual infos
}

// FilterProposalCanceled is a free log retrieval operation binding the contract event 0x789cf55be980739dad1d0699b93b58e806b51c9d96619bfa8fe0a28abaa7b30c.
//
// Solidity: event ProposalCanceled(uint256 proposalId)
func (_LeeaGovernance *LeeaGovernanceFilterer) FilterProposalCanceled(opts *bind.FilterOpts) (*LeeaGovernanceProposalCanceledIterator, error) {

	logs, sub, err := _LeeaGovernance.contract.FilterLogs(opts, "ProposalCanceled")
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceProposalCanceledIterator{contract: _LeeaGovernance.contract, event: "ProposalCanceled", logs: logs, sub: sub}, nil
}

// WatchProposalCanceled is a free log subscription operation binding the contract event 0x789cf55be980739dad1d0699b93b58e806b51c9d96619bfa8fe0a28abaa7b30c.
//
// Solidity: event ProposalCanceled(uint256 proposalId)
func (_LeeaGovernance *LeeaGovernanceFilterer) WatchProposalCanceled(opts *bind.WatchOpts, sink chan<- *LeeaGovernanceProposalCanceled) (event.Subscription, error) {

	logs, sub, err := _LeeaGovernance.contract.WatchLogs(opts, "ProposalCanceled")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(LeeaGovernanceProposalCanceled)
				if err := _LeeaGovernance.contract.UnpackLog(event, "ProposalCanceled", log); err != nil {
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

// ParseProposalCanceled is a log parse operation binding the contract event 0x789cf55be980739dad1d0699b93b58e806b51c9d96619bfa8fe0a28abaa7b30c.
//
// Solidity: event ProposalCanceled(uint256 proposalId)
func (_LeeaGovernance *LeeaGovernanceFilterer) ParseProposalCanceled(log types.Log) (*LeeaGovernanceProposalCanceled, error) {
	event := new(LeeaGovernanceProposalCanceled)
	if err := _LeeaGovernance.contract.UnpackLog(event, "ProposalCanceled", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// LeeaGovernanceProposalCreatedIterator is returned from FilterProposalCreated and is used to iterate over the raw logs and unpacked data for ProposalCreated events raised by the LeeaGovernance contract.
type LeeaGovernanceProposalCreatedIterator struct {
	Event *LeeaGovernanceProposalCreated // Event containing the contract specifics and raw log

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
func (it *LeeaGovernanceProposalCreatedIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(LeeaGovernanceProposalCreated)
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
		it.Event = new(LeeaGovernanceProposalCreated)
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
func (it *LeeaGovernanceProposalCreatedIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *LeeaGovernanceProposalCreatedIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// LeeaGovernanceProposalCreated represents a ProposalCreated event raised by the LeeaGovernance contract.
type LeeaGovernanceProposalCreated struct {
	ProposalId  *big.Int
	Proposer    common.Address
	Targets     []common.Address
	Values      []*big.Int
	Signatures  []string
	Calldatas   [][]byte
	VoteStart   *big.Int
	VoteEnd     *big.Int
	Description string
	Raw         types.Log // Blockchain specific contextual infos
}

// FilterProposalCreated is a free log retrieval operation binding the contract event 0x7d84a6263ae0d98d3329bd7b46bb4e8d6f98cd35a7adb45c274c8b7fd5ebd5e0.
//
// Solidity: event ProposalCreated(uint256 proposalId, address proposer, address[] targets, uint256[] values, string[] signatures, bytes[] calldatas, uint256 voteStart, uint256 voteEnd, string description)
func (_LeeaGovernance *LeeaGovernanceFilterer) FilterProposalCreated(opts *bind.FilterOpts) (*LeeaGovernanceProposalCreatedIterator, error) {

	logs, sub, err := _LeeaGovernance.contract.FilterLogs(opts, "ProposalCreated")
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceProposalCreatedIterator{contract: _LeeaGovernance.contract, event: "ProposalCreated", logs: logs, sub: sub}, nil
}

// WatchProposalCreated is a free log subscription operation binding the contract event 0x7d84a6263ae0d98d3329bd7b46bb4e8d6f98cd35a7adb45c274c8b7fd5ebd5e0.
//
// Solidity: event ProposalCreated(uint256 proposalId, address proposer, address[] targets, uint256[] values, string[] signatures, bytes[] calldatas, uint256 voteStart, uint256 voteEnd, string description)
func (_LeeaGovernance *LeeaGovernanceFilterer) WatchProposalCreated(opts *bind.WatchOpts, sink chan<- *LeeaGovernanceProposalCreated) (event.Subscription, error) {

	logs, sub, err := _LeeaGovernance.contract.WatchLogs(opts, "ProposalCreated")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(LeeaGovernanceProposalCreated)
				if err := _LeeaGovernance.contract.UnpackLog(event, "ProposalCreated", log); err != nil {
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

// ParseProposalCreated is a log parse operation binding the contract event 0x7d84a6263ae0d98d3329bd7b46bb4e8d6f98cd35a7adb45c274c8b7fd5ebd5e0.
//
// Solidity: event ProposalCreated(uint256 proposalId, address proposer, address[] targets, uint256[] values, string[] signatures, bytes[] calldatas, uint256 voteStart, uint256 voteEnd, string description)
func (_LeeaGovernance *LeeaGovernanceFilterer) ParseProposalCreated(log types.Log) (*LeeaGovernanceProposalCreated, error) {
	event := new(LeeaGovernanceProposalCreated)
	if err := _LeeaGovernance.contract.UnpackLog(event, "ProposalCreated", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// LeeaGovernanceProposalExecutedIterator is returned from FilterProposalExecuted and is used to iterate over the raw logs and unpacked data for ProposalExecuted events raised by the LeeaGovernance contract.
type LeeaGovernanceProposalExecutedIterator struct {
	Event *LeeaGovernanceProposalExecuted // Event containing the contract specifics and raw log

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
func (it *LeeaGovernanceProposalExecutedIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(LeeaGovernanceProposalExecuted)
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
		it.Event = new(LeeaGovernanceProposalExecuted)
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
func (it *LeeaGovernanceProposalExecutedIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *LeeaGovernanceProposalExecutedIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// LeeaGovernanceProposalExecuted represents a ProposalExecuted event raised by the LeeaGovernance contract.
type LeeaGovernanceProposalExecuted struct {
	ProposalId *big.Int
	Raw        types.Log // Blockchain specific contextual infos
}

// FilterProposalExecuted is a free log retrieval operation binding the contract event 0x712ae1383f79ac853f8d882153778e0260ef8f03b504e2866e0593e04d2b291f.
//
// Solidity: event ProposalExecuted(uint256 proposalId)
func (_LeeaGovernance *LeeaGovernanceFilterer) FilterProposalExecuted(opts *bind.FilterOpts) (*LeeaGovernanceProposalExecutedIterator, error) {

	logs, sub, err := _LeeaGovernance.contract.FilterLogs(opts, "ProposalExecuted")
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceProposalExecutedIterator{contract: _LeeaGovernance.contract, event: "ProposalExecuted", logs: logs, sub: sub}, nil
}

// WatchProposalExecuted is a free log subscription operation binding the contract event 0x712ae1383f79ac853f8d882153778e0260ef8f03b504e2866e0593e04d2b291f.
//
// Solidity: event ProposalExecuted(uint256 proposalId)
func (_LeeaGovernance *LeeaGovernanceFilterer) WatchProposalExecuted(opts *bind.WatchOpts, sink chan<- *LeeaGovernanceProposalExecuted) (event.Subscription, error) {

	logs, sub, err := _LeeaGovernance.contract.WatchLogs(opts, "ProposalExecuted")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(LeeaGovernanceProposalExecuted)
				if err := _LeeaGovernance.contract.UnpackLog(event, "ProposalExecuted", log); err != nil {
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

// ParseProposalExecuted is a log parse operation binding the contract event 0x712ae1383f79ac853f8d882153778e0260ef8f03b504e2866e0593e04d2b291f.
//
// Solidity: event ProposalExecuted(uint256 proposalId)
func (_LeeaGovernance *LeeaGovernanceFilterer) ParseProposalExecuted(log types.Log) (*LeeaGovernanceProposalExecuted, error) {
	event := new(LeeaGovernanceProposalExecuted)
	if err := _LeeaGovernance.contract.UnpackLog(event, "ProposalExecuted", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// LeeaGovernanceProposalQueuedIterator is returned from FilterProposalQueued and is used to iterate over the raw logs and unpacked data for ProposalQueued events raised by the LeeaGovernance contract.
type LeeaGovernanceProposalQueuedIterator struct {
	Event *LeeaGovernanceProposalQueued // Event containing the contract specifics and raw log

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
func (it *LeeaGovernanceProposalQueuedIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(LeeaGovernanceProposalQueued)
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
		it.Event = new(LeeaGovernanceProposalQueued)
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
func (it *LeeaGovernanceProposalQueuedIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *LeeaGovernanceProposalQueuedIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// LeeaGovernanceProposalQueued represents a ProposalQueued event raised by the LeeaGovernance contract.
type LeeaGovernanceProposalQueued struct {
	ProposalId *big.Int
	EtaSeconds *big.Int
	Raw        types.Log // Blockchain specific contextual infos
}

// FilterProposalQueued is a free log retrieval operation binding the contract event 0x9a2e42fd6722813d69113e7d0079d3d940171428df7373df9c7f7617cfda2892.
//
// Solidity: event ProposalQueued(uint256 proposalId, uint256 etaSeconds)
func (_LeeaGovernance *LeeaGovernanceFilterer) FilterProposalQueued(opts *bind.FilterOpts) (*LeeaGovernanceProposalQueuedIterator, error) {

	logs, sub, err := _LeeaGovernance.contract.FilterLogs(opts, "ProposalQueued")
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceProposalQueuedIterator{contract: _LeeaGovernance.contract, event: "ProposalQueued", logs: logs, sub: sub}, nil
}

// WatchProposalQueued is a free log subscription operation binding the contract event 0x9a2e42fd6722813d69113e7d0079d3d940171428df7373df9c7f7617cfda2892.
//
// Solidity: event ProposalQueued(uint256 proposalId, uint256 etaSeconds)
func (_LeeaGovernance *LeeaGovernanceFilterer) WatchProposalQueued(opts *bind.WatchOpts, sink chan<- *LeeaGovernanceProposalQueued) (event.Subscription, error) {

	logs, sub, err := _LeeaGovernance.contract.WatchLogs(opts, "ProposalQueued")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(LeeaGovernanceProposalQueued)
				if err := _LeeaGovernance.contract.UnpackLog(event, "ProposalQueued", log); err != nil {
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

// ParseProposalQueued is a log parse operation binding the contract event 0x9a2e42fd6722813d69113e7d0079d3d940171428df7373df9c7f7617cfda2892.
//
// Solidity: event ProposalQueued(uint256 proposalId, uint256 etaSeconds)
func (_LeeaGovernance *LeeaGovernanceFilterer) ParseProposalQueued(log types.Log) (*LeeaGovernanceProposalQueued, error) {
	event := new(LeeaGovernanceProposalQueued)
	if err := _LeeaGovernance.contract.UnpackLog(event, "ProposalQueued", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// LeeaGovernanceProposalThresholdSetIterator is returned from FilterProposalThresholdSet and is used to iterate over the raw logs and unpacked data for ProposalThresholdSet events raised by the LeeaGovernance contract.
type LeeaGovernanceProposalThresholdSetIterator struct {
	Event *LeeaGovernanceProposalThresholdSet // Event containing the contract specifics and raw log

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
func (it *LeeaGovernanceProposalThresholdSetIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(LeeaGovernanceProposalThresholdSet)
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
		it.Event = new(LeeaGovernanceProposalThresholdSet)
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
func (it *LeeaGovernanceProposalThresholdSetIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *LeeaGovernanceProposalThresholdSetIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// LeeaGovernanceProposalThresholdSet represents a ProposalThresholdSet event raised by the LeeaGovernance contract.
type LeeaGovernanceProposalThresholdSet struct {
	OldProposalThreshold *big.Int
	NewProposalThreshold *big.Int
	Raw                  types.Log // Blockchain specific contextual infos
}

// FilterProposalThresholdSet is a free log retrieval operation binding the contract event 0xccb45da8d5717e6c4544694297c4ba5cf151d455c9bb0ed4fc7a38411bc05461.
//
// Solidity: event ProposalThresholdSet(uint256 oldProposalThreshold, uint256 newProposalThreshold)
func (_LeeaGovernance *LeeaGovernanceFilterer) FilterProposalThresholdSet(opts *bind.FilterOpts) (*LeeaGovernanceProposalThresholdSetIterator, error) {

	logs, sub, err := _LeeaGovernance.contract.FilterLogs(opts, "ProposalThresholdSet")
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceProposalThresholdSetIterator{contract: _LeeaGovernance.contract, event: "ProposalThresholdSet", logs: logs, sub: sub}, nil
}

// WatchProposalThresholdSet is a free log subscription operation binding the contract event 0xccb45da8d5717e6c4544694297c4ba5cf151d455c9bb0ed4fc7a38411bc05461.
//
// Solidity: event ProposalThresholdSet(uint256 oldProposalThreshold, uint256 newProposalThreshold)
func (_LeeaGovernance *LeeaGovernanceFilterer) WatchProposalThresholdSet(opts *bind.WatchOpts, sink chan<- *LeeaGovernanceProposalThresholdSet) (event.Subscription, error) {

	logs, sub, err := _LeeaGovernance.contract.WatchLogs(opts, "ProposalThresholdSet")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(LeeaGovernanceProposalThresholdSet)
				if err := _LeeaGovernance.contract.UnpackLog(event, "ProposalThresholdSet", log); err != nil {
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

// ParseProposalThresholdSet is a log parse operation binding the contract event 0xccb45da8d5717e6c4544694297c4ba5cf151d455c9bb0ed4fc7a38411bc05461.
//
// Solidity: event ProposalThresholdSet(uint256 oldProposalThreshold, uint256 newProposalThreshold)
func (_LeeaGovernance *LeeaGovernanceFilterer) ParseProposalThresholdSet(log types.Log) (*LeeaGovernanceProposalThresholdSet, error) {
	event := new(LeeaGovernanceProposalThresholdSet)
	if err := _LeeaGovernance.contract.UnpackLog(event, "ProposalThresholdSet", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// LeeaGovernanceQuorumNumeratorUpdatedIterator is returned from FilterQuorumNumeratorUpdated and is used to iterate over the raw logs and unpacked data for QuorumNumeratorUpdated events raised by the LeeaGovernance contract.
type LeeaGovernanceQuorumNumeratorUpdatedIterator struct {
	Event *LeeaGovernanceQuorumNumeratorUpdated // Event containing the contract specifics and raw log

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
func (it *LeeaGovernanceQuorumNumeratorUpdatedIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(LeeaGovernanceQuorumNumeratorUpdated)
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
		it.Event = new(LeeaGovernanceQuorumNumeratorUpdated)
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
func (it *LeeaGovernanceQuorumNumeratorUpdatedIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *LeeaGovernanceQuorumNumeratorUpdatedIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// LeeaGovernanceQuorumNumeratorUpdated represents a QuorumNumeratorUpdated event raised by the LeeaGovernance contract.
type LeeaGovernanceQuorumNumeratorUpdated struct {
	OldQuorumNumerator *big.Int
	NewQuorumNumerator *big.Int
	Raw                types.Log // Blockchain specific contextual infos
}

// FilterQuorumNumeratorUpdated is a free log retrieval operation binding the contract event 0x0553476bf02ef2726e8ce5ced78d63e26e602e4a2257b1f559418e24b4633997.
//
// Solidity: event QuorumNumeratorUpdated(uint256 oldQuorumNumerator, uint256 newQuorumNumerator)
func (_LeeaGovernance *LeeaGovernanceFilterer) FilterQuorumNumeratorUpdated(opts *bind.FilterOpts) (*LeeaGovernanceQuorumNumeratorUpdatedIterator, error) {

	logs, sub, err := _LeeaGovernance.contract.FilterLogs(opts, "QuorumNumeratorUpdated")
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceQuorumNumeratorUpdatedIterator{contract: _LeeaGovernance.contract, event: "QuorumNumeratorUpdated", logs: logs, sub: sub}, nil
}

// WatchQuorumNumeratorUpdated is a free log subscription operation binding the contract event 0x0553476bf02ef2726e8ce5ced78d63e26e602e4a2257b1f559418e24b4633997.
//
// Solidity: event QuorumNumeratorUpdated(uint256 oldQuorumNumerator, uint256 newQuorumNumerator)
func (_LeeaGovernance *LeeaGovernanceFilterer) WatchQuorumNumeratorUpdated(opts *bind.WatchOpts, sink chan<- *LeeaGovernanceQuorumNumeratorUpdated) (event.Subscription, error) {

	logs, sub, err := _LeeaGovernance.contract.WatchLogs(opts, "QuorumNumeratorUpdated")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(LeeaGovernanceQuorumNumeratorUpdated)
				if err := _LeeaGovernance.contract.UnpackLog(event, "QuorumNumeratorUpdated", log); err != nil {
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

// ParseQuorumNumeratorUpdated is a log parse operation binding the contract event 0x0553476bf02ef2726e8ce5ced78d63e26e602e4a2257b1f559418e24b4633997.
//
// Solidity: event QuorumNumeratorUpdated(uint256 oldQuorumNumerator, uint256 newQuorumNumerator)
func (_LeeaGovernance *LeeaGovernanceFilterer) ParseQuorumNumeratorUpdated(log types.Log) (*LeeaGovernanceQuorumNumeratorUpdated, error) {
	event := new(LeeaGovernanceQuorumNumeratorUpdated)
	if err := _LeeaGovernance.contract.UnpackLog(event, "QuorumNumeratorUpdated", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// LeeaGovernanceVoteCastIterator is returned from FilterVoteCast and is used to iterate over the raw logs and unpacked data for VoteCast events raised by the LeeaGovernance contract.
type LeeaGovernanceVoteCastIterator struct {
	Event *LeeaGovernanceVoteCast // Event containing the contract specifics and raw log

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
func (it *LeeaGovernanceVoteCastIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(LeeaGovernanceVoteCast)
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
		it.Event = new(LeeaGovernanceVoteCast)
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
func (it *LeeaGovernanceVoteCastIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *LeeaGovernanceVoteCastIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// LeeaGovernanceVoteCast represents a VoteCast event raised by the LeeaGovernance contract.
type LeeaGovernanceVoteCast struct {
	Voter      common.Address
	ProposalId *big.Int
	Support    uint8
	Weight     *big.Int
	Reason     string
	Raw        types.Log // Blockchain specific contextual infos
}

// FilterVoteCast is a free log retrieval operation binding the contract event 0xb8e138887d0aa13bab447e82de9d5c1777041ecd21ca36ba824ff1e6c07ddda4.
//
// Solidity: event VoteCast(address indexed voter, uint256 proposalId, uint8 support, uint256 weight, string reason)
func (_LeeaGovernance *LeeaGovernanceFilterer) FilterVoteCast(opts *bind.FilterOpts, voter []common.Address) (*LeeaGovernanceVoteCastIterator, error) {

	var voterRule []interface{}
	for _, voterItem := range voter {
		voterRule = append(voterRule, voterItem)
	}

	logs, sub, err := _LeeaGovernance.contract.FilterLogs(opts, "VoteCast", voterRule)
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceVoteCastIterator{contract: _LeeaGovernance.contract, event: "VoteCast", logs: logs, sub: sub}, nil
}

// WatchVoteCast is a free log subscription operation binding the contract event 0xb8e138887d0aa13bab447e82de9d5c1777041ecd21ca36ba824ff1e6c07ddda4.
//
// Solidity: event VoteCast(address indexed voter, uint256 proposalId, uint8 support, uint256 weight, string reason)
func (_LeeaGovernance *LeeaGovernanceFilterer) WatchVoteCast(opts *bind.WatchOpts, sink chan<- *LeeaGovernanceVoteCast, voter []common.Address) (event.Subscription, error) {

	var voterRule []interface{}
	for _, voterItem := range voter {
		voterRule = append(voterRule, voterItem)
	}

	logs, sub, err := _LeeaGovernance.contract.WatchLogs(opts, "VoteCast", voterRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(LeeaGovernanceVoteCast)
				if err := _LeeaGovernance.contract.UnpackLog(event, "VoteCast", log); err != nil {
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

// ParseVoteCast is a log parse operation binding the contract event 0xb8e138887d0aa13bab447e82de9d5c1777041ecd21ca36ba824ff1e6c07ddda4.
//
// Solidity: event VoteCast(address indexed voter, uint256 proposalId, uint8 support, uint256 weight, string reason)
func (_LeeaGovernance *LeeaGovernanceFilterer) ParseVoteCast(log types.Log) (*LeeaGovernanceVoteCast, error) {
	event := new(LeeaGovernanceVoteCast)
	if err := _LeeaGovernance.contract.UnpackLog(event, "VoteCast", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// LeeaGovernanceVoteCastWithParamsIterator is returned from FilterVoteCastWithParams and is used to iterate over the raw logs and unpacked data for VoteCastWithParams events raised by the LeeaGovernance contract.
type LeeaGovernanceVoteCastWithParamsIterator struct {
	Event *LeeaGovernanceVoteCastWithParams // Event containing the contract specifics and raw log

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
func (it *LeeaGovernanceVoteCastWithParamsIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(LeeaGovernanceVoteCastWithParams)
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
		it.Event = new(LeeaGovernanceVoteCastWithParams)
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
func (it *LeeaGovernanceVoteCastWithParamsIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *LeeaGovernanceVoteCastWithParamsIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// LeeaGovernanceVoteCastWithParams represents a VoteCastWithParams event raised by the LeeaGovernance contract.
type LeeaGovernanceVoteCastWithParams struct {
	Voter      common.Address
	ProposalId *big.Int
	Support    uint8
	Weight     *big.Int
	Reason     string
	Params     []byte
	Raw        types.Log // Blockchain specific contextual infos
}

// FilterVoteCastWithParams is a free log retrieval operation binding the contract event 0xe2babfbac5889a709b63bb7f598b324e08bc5a4fb9ec647fb3cbc9ec07eb8712.
//
// Solidity: event VoteCastWithParams(address indexed voter, uint256 proposalId, uint8 support, uint256 weight, string reason, bytes params)
func (_LeeaGovernance *LeeaGovernanceFilterer) FilterVoteCastWithParams(opts *bind.FilterOpts, voter []common.Address) (*LeeaGovernanceVoteCastWithParamsIterator, error) {

	var voterRule []interface{}
	for _, voterItem := range voter {
		voterRule = append(voterRule, voterItem)
	}

	logs, sub, err := _LeeaGovernance.contract.FilterLogs(opts, "VoteCastWithParams", voterRule)
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceVoteCastWithParamsIterator{contract: _LeeaGovernance.contract, event: "VoteCastWithParams", logs: logs, sub: sub}, nil
}

// WatchVoteCastWithParams is a free log subscription operation binding the contract event 0xe2babfbac5889a709b63bb7f598b324e08bc5a4fb9ec647fb3cbc9ec07eb8712.
//
// Solidity: event VoteCastWithParams(address indexed voter, uint256 proposalId, uint8 support, uint256 weight, string reason, bytes params)
func (_LeeaGovernance *LeeaGovernanceFilterer) WatchVoteCastWithParams(opts *bind.WatchOpts, sink chan<- *LeeaGovernanceVoteCastWithParams, voter []common.Address) (event.Subscription, error) {

	var voterRule []interface{}
	for _, voterItem := range voter {
		voterRule = append(voterRule, voterItem)
	}

	logs, sub, err := _LeeaGovernance.contract.WatchLogs(opts, "VoteCastWithParams", voterRule)
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(LeeaGovernanceVoteCastWithParams)
				if err := _LeeaGovernance.contract.UnpackLog(event, "VoteCastWithParams", log); err != nil {
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

// ParseVoteCastWithParams is a log parse operation binding the contract event 0xe2babfbac5889a709b63bb7f598b324e08bc5a4fb9ec647fb3cbc9ec07eb8712.
//
// Solidity: event VoteCastWithParams(address indexed voter, uint256 proposalId, uint8 support, uint256 weight, string reason, bytes params)
func (_LeeaGovernance *LeeaGovernanceFilterer) ParseVoteCastWithParams(log types.Log) (*LeeaGovernanceVoteCastWithParams, error) {
	event := new(LeeaGovernanceVoteCastWithParams)
	if err := _LeeaGovernance.contract.UnpackLog(event, "VoteCastWithParams", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// LeeaGovernanceVotingDelaySetIterator is returned from FilterVotingDelaySet and is used to iterate over the raw logs and unpacked data for VotingDelaySet events raised by the LeeaGovernance contract.
type LeeaGovernanceVotingDelaySetIterator struct {
	Event *LeeaGovernanceVotingDelaySet // Event containing the contract specifics and raw log

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
func (it *LeeaGovernanceVotingDelaySetIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(LeeaGovernanceVotingDelaySet)
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
		it.Event = new(LeeaGovernanceVotingDelaySet)
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
func (it *LeeaGovernanceVotingDelaySetIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *LeeaGovernanceVotingDelaySetIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// LeeaGovernanceVotingDelaySet represents a VotingDelaySet event raised by the LeeaGovernance contract.
type LeeaGovernanceVotingDelaySet struct {
	OldVotingDelay *big.Int
	NewVotingDelay *big.Int
	Raw            types.Log // Blockchain specific contextual infos
}

// FilterVotingDelaySet is a free log retrieval operation binding the contract event 0xc565b045403dc03c2eea82b81a0465edad9e2e7fc4d97e11421c209da93d7a93.
//
// Solidity: event VotingDelaySet(uint256 oldVotingDelay, uint256 newVotingDelay)
func (_LeeaGovernance *LeeaGovernanceFilterer) FilterVotingDelaySet(opts *bind.FilterOpts) (*LeeaGovernanceVotingDelaySetIterator, error) {

	logs, sub, err := _LeeaGovernance.contract.FilterLogs(opts, "VotingDelaySet")
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceVotingDelaySetIterator{contract: _LeeaGovernance.contract, event: "VotingDelaySet", logs: logs, sub: sub}, nil
}

// WatchVotingDelaySet is a free log subscription operation binding the contract event 0xc565b045403dc03c2eea82b81a0465edad9e2e7fc4d97e11421c209da93d7a93.
//
// Solidity: event VotingDelaySet(uint256 oldVotingDelay, uint256 newVotingDelay)
func (_LeeaGovernance *LeeaGovernanceFilterer) WatchVotingDelaySet(opts *bind.WatchOpts, sink chan<- *LeeaGovernanceVotingDelaySet) (event.Subscription, error) {

	logs, sub, err := _LeeaGovernance.contract.WatchLogs(opts, "VotingDelaySet")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(LeeaGovernanceVotingDelaySet)
				if err := _LeeaGovernance.contract.UnpackLog(event, "VotingDelaySet", log); err != nil {
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

// ParseVotingDelaySet is a log parse operation binding the contract event 0xc565b045403dc03c2eea82b81a0465edad9e2e7fc4d97e11421c209da93d7a93.
//
// Solidity: event VotingDelaySet(uint256 oldVotingDelay, uint256 newVotingDelay)
func (_LeeaGovernance *LeeaGovernanceFilterer) ParseVotingDelaySet(log types.Log) (*LeeaGovernanceVotingDelaySet, error) {
	event := new(LeeaGovernanceVotingDelaySet)
	if err := _LeeaGovernance.contract.UnpackLog(event, "VotingDelaySet", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}

// LeeaGovernanceVotingPeriodSetIterator is returned from FilterVotingPeriodSet and is used to iterate over the raw logs and unpacked data for VotingPeriodSet events raised by the LeeaGovernance contract.
type LeeaGovernanceVotingPeriodSetIterator struct {
	Event *LeeaGovernanceVotingPeriodSet // Event containing the contract specifics and raw log

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
func (it *LeeaGovernanceVotingPeriodSetIterator) Next() bool {
	// If the iterator failed, stop iterating
	if it.fail != nil {
		return false
	}
	// If the iterator completed, deliver directly whatever's available
	if it.done {
		select {
		case log := <-it.logs:
			it.Event = new(LeeaGovernanceVotingPeriodSet)
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
		it.Event = new(LeeaGovernanceVotingPeriodSet)
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
func (it *LeeaGovernanceVotingPeriodSetIterator) Error() error {
	return it.fail
}

// Close terminates the iteration process, releasing any pending underlying
// resources.
func (it *LeeaGovernanceVotingPeriodSetIterator) Close() error {
	it.sub.Unsubscribe()
	return nil
}

// LeeaGovernanceVotingPeriodSet represents a VotingPeriodSet event raised by the LeeaGovernance contract.
type LeeaGovernanceVotingPeriodSet struct {
	OldVotingPeriod *big.Int
	NewVotingPeriod *big.Int
	Raw             types.Log // Blockchain specific contextual infos
}

// FilterVotingPeriodSet is a free log retrieval operation binding the contract event 0x7e3f7f0708a84de9203036abaa450dccc85ad5ff52f78c170f3edb55cf5e8828.
//
// Solidity: event VotingPeriodSet(uint256 oldVotingPeriod, uint256 newVotingPeriod)
func (_LeeaGovernance *LeeaGovernanceFilterer) FilterVotingPeriodSet(opts *bind.FilterOpts) (*LeeaGovernanceVotingPeriodSetIterator, error) {

	logs, sub, err := _LeeaGovernance.contract.FilterLogs(opts, "VotingPeriodSet")
	if err != nil {
		return nil, err
	}
	return &LeeaGovernanceVotingPeriodSetIterator{contract: _LeeaGovernance.contract, event: "VotingPeriodSet", logs: logs, sub: sub}, nil
}

// WatchVotingPeriodSet is a free log subscription operation binding the contract event 0x7e3f7f0708a84de9203036abaa450dccc85ad5ff52f78c170f3edb55cf5e8828.
//
// Solidity: event VotingPeriodSet(uint256 oldVotingPeriod, uint256 newVotingPeriod)
func (_LeeaGovernance *LeeaGovernanceFilterer) WatchVotingPeriodSet(opts *bind.WatchOpts, sink chan<- *LeeaGovernanceVotingPeriodSet) (event.Subscription, error) {

	logs, sub, err := _LeeaGovernance.contract.WatchLogs(opts, "VotingPeriodSet")
	if err != nil {
		return nil, err
	}
	return event.NewSubscription(func(quit <-chan struct{}) error {
		defer sub.Unsubscribe()
		for {
			select {
			case log := <-logs:
				// New log arrived, parse the event and forward to the user
				event := new(LeeaGovernanceVotingPeriodSet)
				if err := _LeeaGovernance.contract.UnpackLog(event, "VotingPeriodSet", log); err != nil {
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

// ParseVotingPeriodSet is a log parse operation binding the contract event 0x7e3f7f0708a84de9203036abaa450dccc85ad5ff52f78c170f3edb55cf5e8828.
//
// Solidity: event VotingPeriodSet(uint256 oldVotingPeriod, uint256 newVotingPeriod)
func (_LeeaGovernance *LeeaGovernanceFilterer) ParseVotingPeriodSet(log types.Log) (*LeeaGovernanceVotingPeriodSet, error) {
	event := new(LeeaGovernanceVotingPeriodSet)
	if err := _LeeaGovernance.contract.UnpackLog(event, "VotingPeriodSet", log); err != nil {
		return nil, err
	}
	event.Raw = log
	return event, nil
}
