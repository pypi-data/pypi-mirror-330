// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @custom:security-contact contract_security@leealabs.com
contract AgentRegistry is Ownable {
    event Registered(address pub, string name);
    event Deleted(address pub);
    event FeeUpdated(address pub, string name, uint256 newFee);

    struct AgentScore {
        uint256 activity;
        uint256 accuracy;
    }

    struct Agent {
        string name;
        uint256 fee;
        AgentScore score;
        uint index;
    }

    mapping(address => Agent) private _agentStructs;
    address[] private _agentIndex;
    address private _dao;

    constructor(address initialOwner, address dao) Ownable(initialOwner) {
        _dao = dao;
    }

    function isAgent(address agentAddress) public view returns (bool isIndeed) {
        if (_agentIndex.length == 0) return false;
        return (_agentIndex[_agentStructs[agentAddress].index] == agentAddress);
    }

    function registerAgent(
        address agentAddress,
        uint256 agentFee,
        string memory name
    ) public returns (uint index) {
        require(!isAgent(agentAddress));
        _agentIndex.push(agentAddress);
        _agentStructs[agentAddress].fee = agentFee;
        _agentStructs[agentAddress].name = name;
        _agentStructs[agentAddress].index = _agentIndex.length - 1;
        emit Registered(agentAddress, name);
        return _agentIndex.length - 1;
    }

    function deleteAgent(
        address agentAddress
    ) public onlyOwner returns (uint index) {
        require(isAgent(agentAddress));
        uint rowToDelete = _agentStructs[agentAddress].index;
        address keyToMove = _agentIndex[_agentIndex.length - 1];
        _agentIndex[rowToDelete] = keyToMove;
        _agentStructs[keyToMove].index = rowToDelete;
        _agentIndex.pop();
        emit Deleted(agentAddress);
        return rowToDelete;
    }

    function getAgent(
        address agentAddress
    )
        public
        view
        returns (
            string memory name,
            uint256 fee,
            uint256 activityScore,
            uint256 accuracyScore,
            uint index
        )
    {
        require(isAgent(agentAddress) == true);
        return (
            _agentStructs[agentAddress].name,
            _agentStructs[agentAddress].fee,
            _agentStructs[agentAddress].score.activity,
            _agentStructs[agentAddress].score.accuracy,
            _agentStructs[agentAddress].index
        );
    }

    function updateAgentFee(
        address agentAddress,
        uint256 newFee
    ) public onlyOwner returns (bool success) {
        require(isAgent(agentAddress));
        _agentStructs[agentAddress].fee = newFee;
        emit FeeUpdated(agentAddress, _agentStructs[agentAddress].name,  _agentStructs[agentAddress].fee);
        return true;
    }

    function updateAgentActivityScore(
        address agentAddress,
        uint256 newActivityScore
    ) public onlyOwner returns (bool success) {
        require(isAgent(agentAddress));
        _agentStructs[agentAddress].score.activity = newActivityScore;
        return true;
    }

    function updateAgentAccuracyScore(
        address agentAddress,
        uint256 newAccuracyScore
    ) public onlyOwner returns (bool success) {
        require(isAgent(agentAddress));
        _agentStructs[agentAddress].score.accuracy = newAccuracyScore;
        return true;
    }

    function getAgentActivityScore(
        address agentAddress
    ) public view returns (uint256 fee) {
        require(isAgent(agentAddress));
        return (_agentStructs[agentAddress].score.activity);
    }

    function getAgentAccuracyScore(
        address agentAddress
    ) public view returns (uint256 fee) {
        require(isAgent(agentAddress));
        return (_agentStructs[agentAddress].score.accuracy);
    }

    function getAgentFee(
        address agentAddress
    ) public view returns (uint256 fee) {
        require(isAgent(agentAddress));
        return (_agentStructs[agentAddress].fee);
    }

    function getAgentCount() public view returns (uint count) {
        return _agentIndex.length;
    }

    function getAgentAtIndex(
        uint index
    ) public view returns (address agentAddress) {
        return _agentIndex[index];
    }
}
