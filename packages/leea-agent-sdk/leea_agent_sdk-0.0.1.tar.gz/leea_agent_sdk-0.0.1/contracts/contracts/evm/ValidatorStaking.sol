// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {LeeaGlobalParams} from "./GlobalParameters.sol";
import {ValidatorRegistry} from "./ValidatorRegistry.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";

/// @custom:security-contact contract_security@leealabs.com
contract ValidatorStaking is Ownable, ReentrancyGuard {
    /**
     * @dev The account is not registered as validator.
     */
    error NotRegisteredValidator(address);

    event StakeSuccess(address validator, uint256 amount);

    event ValidatorSlashed(address validator, uint256 amount, uint256 left);

    mapping(address => uint256) private _stakes;

    ERC20 private _token;
    LeeaGlobalParams private _globalParams;
    ValidatorRegistry private _valRegistry;

    constructor(
        address initialOwner,
        ERC20 leeaToken,
        LeeaGlobalParams globalParams,
        ValidatorRegistry validatorReg
    ) Ownable(initialOwner) {
        _token = leeaToken;
        _globalParams = globalParams;
        _valRegistry = validatorReg;
    }

    function stake() public validatorRegistered(msg.sender) nonReentrant {
        uint256 minStake = _globalParams.getStake();
        require(
            _token.balanceOf(msg.sender) >= minStake,
            "Your token balance should be greater or equal to required stake amount"
        );
        require(
            _token.approve(address(this), minStake),
            "Cant approve tokens to stake"
        );
        require(
            _token.transferFrom(msg.sender, address(this), minStake),
            "Cant transfer tokens to stake"
        );
        _stakes[msg.sender] += minStake;
        emit StakeSuccess(msg.sender, minStake);
    }

    function slash(
        address validator
    ) public onlyOwner validatorRegistered(validator) nonReentrant {
        uint256 slashingAmount = _globalParams.getSlashingAmount();
        require(
            getStake(validator) >= slashingAmount,
            "Validator stake is zero"
        );
        require(
            _token.balanceOf(address(this)) >= slashingAmount,
            "Balance of staking contract should be greater or equal to required slashing"
        );
        _stakes[validator] -= slashingAmount;
        emit ValidatorSlashed(validator, slashingAmount, getStake(validator));
    }

    function payStakingRewards(address validator) public onlyOwner validatorRegistered(validator) nonReentrant {}

    function getStake(
        address validator
    ) public view validatorRegistered(validator) returns (uint256) {
        return _stakes[validator];
    }

    modifier validatorRegistered(address validator) {
        if (_valRegistry.isValidator(validator)) {
            revert NotRegisteredValidator(validator);
        }
        _;
    }
}
