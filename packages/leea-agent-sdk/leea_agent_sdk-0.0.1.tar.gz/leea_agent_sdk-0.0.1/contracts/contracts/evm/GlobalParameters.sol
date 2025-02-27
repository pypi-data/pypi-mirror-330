// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {Math} from "@openzeppelin/contracts/utils/math/Math.sol";

/// @custom:security-contact contract_security@leealabs.com
contract LeeaGlobalParams is Ownable {
    event MinimStakeUpdated(uint256 newStake);
    event SystemFeeRateUpdated(
        uint256 newSystemFeeNominator,
        uint256 newSystemFeeDenominator
    );
    event MinimAgentScoreUpdated(uint256 newAgentScore);

    // Minimum validator stake
    uint256 private _minValidatorStake;

    // Slashing validator amount
    uint256 private _slashValidator;

    // System fee rate
    uint256 private _systemFeeNominator;
    uint256 private _systemFeeDenominator;

    // Minimum agent score to block agent
    uint256 private _minimumAgentScore;

    constructor(
        address dao,
        uint256 initialMinValidatorStake,
        uint256 initialSystemFeeNominator,
        uint256 initialsSystemFeeDenominator,
        uint256 initialMinimumAgentScore,
        uint256 initialSlashingValidator
    ) Ownable(dao) {
        _minValidatorStake = initialMinValidatorStake;
        _systemFeeNominator = initialSystemFeeNominator;
        _systemFeeDenominator = initialsSystemFeeDenominator;
        _minimumAgentScore = initialMinimumAgentScore;
        _slashValidator = initialSlashingValidator;
    }

    function updateStake(uint256 newStake) public onlyOwner {
        require(newStake > 0, "New stake should be greater than zero");
        _minValidatorStake = newStake;
        emit MinimStakeUpdated(newStake);
    }

    function updateSystemFeeRate(
        uint256 nominator,
        uint256 denominator
    ) public onlyOwner {
        require(
            nominator > 0 && nominator <= 100,
            "nominator should be in range 0 < x <= 100"
        );
        require(
            denominator > 0 && denominator <= 100,
            "denominator should be in range 0 < x <= 100"
        );
        require(
            nominator < denominator,
            "nominator should be less than denominator"
        );
        _systemFeeNominator = nominator;
        _systemFeeDenominator = denominator;
        emit SystemFeeRateUpdated(nominator, denominator);
    }

    function updateMinimumAgentScore(uint256 minAgentScore) public onlyOwner {
        require(
            minAgentScore > 0,
            "New minimum agent score should be greater than zero"
        );
        _minimumAgentScore = minAgentScore;
        emit MinimAgentScoreUpdated(minAgentScore);
    }

    function getStake() public view returns (uint256) {
        return _minValidatorStake;
    }

    function getSystemFeeRate() public view returns (uint256, uint256) {
        return (_systemFeeNominator, _systemFeeDenominator);
    }

    function getMinimumAgentScore() public view returns (uint256) {
        return _minimumAgentScore;
    }

    function getSlashingAmount() public view returns (uint256) {
        return _slashValidator;
    }
}
