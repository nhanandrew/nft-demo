// SPDX-License-Identifier: MIT
pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    uint256 public tokenCounter;
    bytes32 public keyhash;
    uint256 public fee;
    enum Flavor {
        SEVERE,
        NIGHTTIME,
        MSPAINT
    }
    mapping(uint256 => Flavor) public tokenIdToFlavor;
    mapping(bytes32 => address) public requestIdToSender;
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event flavorAssigned(uint256 indexed tokenId, Flavor flavor);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyhash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("ProfilePic", "PP")
    {
        tokenCounter = 0;
        keyhash = _keyhash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyhash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Flavor flavor = Flavor(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToFlavor[newTokenId] = flavor;
        emit flavorAssigned(newTokenId, flavor);
        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);
        //_setTokenURI(newTokenId, tokenURI); //for more decentralization, use fulfillRandomness to get
        tokenCounter += 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // 3 token URIs for each flavor
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
