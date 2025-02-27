// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import {ERC20} from "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import {Ownable} from "@openzeppelin/contracts/access/Ownable.sol";
import {Math} from "@openzeppelin/contracts/utils/math/Math.sol";
import {ReentrancyGuard} from "@openzeppelin/contracts/utils/ReentrancyGuard.sol";
import {AgentRegistry} from "./AgentRegistry.sol";
import {LeeaGlobalParams} from "./GlobalParameters.sol";
import {ValidatorStaking} from "./ValidatorStaking.sol";

/// @custom:security-contact contract_security@leealabs.com
contract Escrow is Ownable, ReentrancyGuard {
    event Deposited(
        address user,
        address indexed escrow,
        address indexed token,
        uint256 amount
    );
    event Withdrawn(
        address user,
        address indexed escrow,
        address indexed token,
        uint256 amount
    );
    event FeePaid(
        address user,
        address agent,
        address indexed escrow,
        address indexed token,
        uint256 amount
    );

    mapping(address => uint256) private escrowBalance;

    ERC20 private _token;
    AgentRegistry private _agentRegistry;
    LeeaGlobalParams private _globalParams;
    ValidatorStaking private _validatorStaking;

    constructor(
        LeeaGlobalParams globalParams,
        ERC20 leeaToken,
        AgentRegistry agentRegistry,
        ValidatorStaking validatorStaking,
        address initialOwner
    ) Ownable(initialOwner) {
        _token = leeaToken;
        _agentRegistry = agentRegistry;
        _globalParams = globalParams;
        _validatorStaking = validatorStaking;
    }

    function deposit(uint256 _amount) public {
        require(_amount > 0, "You need to deposit at least some tokens");
        require(
            _token.balanceOf(msg.sender) > _amount,
            "You need to have at least amount of tokens"
        );
        require(
            _token.approve(address(this), _amount),
            "Cant approve tokens to escrow"
        );
        require(
            _token.transferFrom(msg.sender, address(this), _amount),
            "Cant transfer tokens to escrow"
        );
        escrowBalance[msg.sender] += _amount;
        emit Deposited(msg.sender, address(this), address(_token), _amount);
    }

    function withdrawFullAmount(address _user) public nonReentrant {
        require(msg.sender == owner(), "Only owner is allowed");
        require(escrowBalance[_user] > 0, "Balance is zero");
        uint256 _currentBalance = escrowBalance[_user];
        require(
            _token.transferFrom(address(this), _user, _currentBalance),
            "Cant transfer tokens to user"
        );
        emit Withdrawn(_user, address(this), address(_token), _currentBalance);
    }

    function payFee(address user, address agent) public nonReentrant onlyOwner {
        require(_agentRegistry.isAgent(agent), "Agent is not registered");
        uint256 agentFee = _agentRegistry.getAgentFee(agent);
        (uint256 systemFeeNom, uint256 systemFeeDen) = _globalParams
            .getSystemFeeRate();
        // TODO pay attention to calculation here
        uint256 systemFee = Math.mulDiv(agentFee, systemFeeNom, systemFeeDen);
        uint256 totalFee = agentFee + systemFee;
        require(escrowBalance[user] >= totalFee, "Balance less than fee");
        require(
            _token.balanceOf(address(this)) > totalFee,
            "Not enough escrow balance"
        );
        // send fee to agent
        require(
            _token.transferFrom(address(this), agent, agentFee),
            "Cant transfer tokens to escrow"
        );
        // send fee to validator staking
        require(
            _token.transferFrom(
                address(this),
                address(_validatorStaking),
                systemFee
            ),
            "Cant transfer tokens to escrow"
        );
        escrowBalance[msg.sender] -= totalFee;
        emit FeePaid(user, agent, address(this), address(_token), totalFee);
    }
}
