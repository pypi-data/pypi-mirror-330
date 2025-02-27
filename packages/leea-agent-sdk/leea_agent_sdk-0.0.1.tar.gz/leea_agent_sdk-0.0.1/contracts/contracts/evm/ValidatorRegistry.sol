// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";

/// @custom:security-contact contract_security@leealabs.com
contract ValidatorRegistry is Ownable {
    event Registered(address pub, string name);

    struct Validator {
        string name;
        string url;
        uint index;
    }

    mapping(address => Validator) private _validatorStructs;
    address[] private _validatorIndex;

    constructor(address initialOwner) Ownable(initialOwner) {}

    function isValidator(
        address agentAddress
    ) public view returns (bool isIndeed) {
        if (_validatorIndex.length == 0) return false;
        return (_validatorIndex[_validatorStructs[agentAddress].index] ==
            agentAddress);
    }

    function registerValidator(
        address agentAddress
    ) public onlyOwner returns (uint index) {
        require(!isValidator(agentAddress));
        _validatorIndex.push(agentAddress);
        _validatorStructs[agentAddress].index = _validatorIndex.length - 1;
        return _validatorIndex.length - 1;
    }

    function deleteValidator(
        address validatorAddress
    ) public onlyOwner returns (uint index) {
        require(isValidator(validatorAddress));
        uint rowToDelete = _validatorStructs[validatorAddress].index;
        address keyToMove = _validatorIndex[_validatorIndex.length - 1];
        _validatorIndex[rowToDelete] = keyToMove;
        _validatorStructs[keyToMove].index = rowToDelete;
        _validatorIndex.pop();
        return rowToDelete;
    }

    function getValidator(
        address validatorAddress
    ) public view returns (string memory name, string memory url, uint index) {
        require(isValidator(validatorAddress) == true);
        return (
            _validatorStructs[validatorAddress].name,
            _validatorStructs[validatorAddress].url,
            _validatorStructs[validatorAddress].index
        );
    }

    function updateValidatorURL(
        address validatorAddress,
        string memory newURL
    ) public onlyOwner returns (bool success) {
        require(isValidator(validatorAddress));
        _validatorStructs[validatorAddress].url = newURL;
        return true;
    }

    function getValidatorCount() public view returns (uint count) {
        return _validatorIndex.length;
    }

    function getValidatorAtIndex(
        uint index
    ) public view returns (address validatorAddress) {
        return _validatorIndex[index];
    }
}
