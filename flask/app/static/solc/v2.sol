pragma solidity = 0.4.25;

contract OneShotOneKill {
    address public owner;
    bool public locked;

    constructor() public payable {
        owner = msg.sender;
        locked = false;
    }

    function shootYourShot() public {
        require(msg.sender == owner && locked == false);
        uint256 total = address(this).balance;
        msg.sender.call.value(total / 20);
        locked = true;
    }

    function claimContract() public {
        owner = msg.sender;
    }

}
