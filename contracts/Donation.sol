// SPDX-License-Identifier: MIT
pragma solidity 0.8.29;

contract Donation {
    address public owner; // Владелец контракта (ты)
    uint public totalDonations; // Общая сумма пожертвований
    mapping(address => uint) public donations; // Кто сколько пожертвовал

    event Donated(address indexed donor, uint amount);

    constructor() {
        owner = msg.sender; // Тот, кто развернул контракт
    }

    function donate() public payable {
        require(msg.value > 0, "Donation must be greater than 0");
        donations[msg.sender] += msg.value;
        totalDonations += msg.value;
        emit Donated(msg.sender, msg.value);
    }

    function getBalance() public view returns (uint) {
        return address(this).balance;
    }

    function withdraw() public {
        require(msg.sender == owner, "Only owner can withdraw");
        payable(owner).transfer(address(this).balance);
    }
}