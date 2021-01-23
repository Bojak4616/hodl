pragma solidity = 0.4.25;

contract DynamicStretching {
    bool public locked;
    
    constructor() public payable {
        locked = true;
    }
    
    function unlock() public payable {
        require(msg.value == 0.01337 ether);
        locked = false;
    }
    
    function withdraw() public payable {
        require(!locked);
        msg.sender.call.value(address(this).balance)();
    }
}




