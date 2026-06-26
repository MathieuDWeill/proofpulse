// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title ProofPulseAnchor
/// @notice Minimal evidence-hash anchoring contract for the hackathon demo.
/// @dev This stores proof hashes, not private evidence. Evidence can live in S3/IPFS/customer vaults.
contract ProofPulseAnchor {
    enum Severity { Low, Medium, High, Critical }

    struct EvidenceRecord {
        bytes32 bundleHash;
        string bundleURI;
        string targetId;
        Severity severity;
        address reporter;
        uint256 timestamp;
    }

    mapping(bytes32 => EvidenceRecord) public records;
    event EvidenceAnchored(bytes32 indexed bundleHash, string targetId, Severity severity, address indexed reporter, string bundleURI);

    function anchorEvidence(bytes32 bundleHash, string calldata bundleURI, string calldata targetId, Severity severity) external {
        require(bundleHash != bytes32(0), "empty hash");
        require(records[bundleHash].timestamp == 0, "already anchored");
        records[bundleHash] = EvidenceRecord({
            bundleHash: bundleHash,
            bundleURI: bundleURI,
            targetId: targetId,
            severity: severity,
            reporter: msg.sender,
            timestamp: block.timestamp
        });
        emit EvidenceAnchored(bundleHash, targetId, severity, msg.sender, bundleURI);
    }

    function isAnchored(bytes32 bundleHash) external view returns (bool) {
        return records[bundleHash].timestamp != 0;
    }
}
