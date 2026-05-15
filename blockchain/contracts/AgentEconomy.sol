// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract AgentEconomyToken is ERC20, Ownable {
    uint256 public constant TOTAL_SUPPLY = 1_000_000_000 * 10**18; // 1B tokens
    
    constructor() ERC20("AgentEconomyToken", "AET") Ownable(msg.sender) {
        _mint(msg.sender, TOTAL_SUPPLY);
    }
}

contract AgentMarketplace is Ownable {
    struct AgentOffer {
        address agent;
        string capabilities;
        uint256 pricePerTask;
        uint256 reputationScore;
        uint256 tasksCompleted;
        bool active;
    }
    
    struct Bounty {
        uint256 id;
        address creator;
        string taskDescription;
        uint256 reward;
        address winner;
        bool completed;
        uint256 deadline;
    }
    
    AgentEconomyToken public token;
    mapping(address => AgentOffer) public agentOffers;
    mapping(uint256 => Bounty) public bounties;
    uint256 public bountyCounter;
    
    event TaskCompleted(address indexed agent, uint256 payment);
    event BountyCreated(uint256 indexed bountyId, uint256 reward);
    event BountyAwarded(uint256 indexed bountyId, address winner);
    
    constructor(address _token) Ownable(msg.sender) {
        token = AgentEconomyToken(_token);
    }
    
    function registerAgent(string memory _capabilities, uint256 _pricePerTask) external {
        agentOffers[msg.sender] = AgentOffer({
            agent: msg.sender,
            capabilities: _capabilities,
            pricePerTask: _pricePerTask,
            reputationScore: 1000, // Start at 1000
            tasksCompleted: 0,
            active: true
        });
    }
    
    function hireAgent(address _agent, uint256 _taskComplexity) external {
        AgentOffer storage offer = agentOffers[_agent];
        require(offer.active, "Agent not active");
        
        uint256 payment = offer.pricePerTask * _taskComplexity;
        token.transferFrom(msg.sender, _agent, payment);
        
        emit TaskCompleted(_agent, payment);
        offer.tasksCompleted++;
        offer.reputationScore = (offer.reputationScore * 99 + 1000) / 100; // Update rep
    }
    
    function createBounty(string memory _description, uint256 _reward, uint256 _deadline) external {
        require(token.transferFrom(msg.sender, address(this), _reward), "Payment failed");
        
        bounties[bountyCounter] = Bounty({
            id: bountyCounter,
            creator: msg.sender,
            taskDescription: _description,
            reward: _reward,
            winner: address(0),
            completed: false,
            deadline: block.timestamp + _deadline
        });
        
        emit BountyCreated(bountyCounter, _reward);
        bountyCounter++;
    }
}
