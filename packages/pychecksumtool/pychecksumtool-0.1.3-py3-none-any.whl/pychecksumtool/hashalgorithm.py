import hashlib
import enum
from typing import Dict, Set


class HashAlgorithm(str, enum.Enum):
    """Enum of hash algorithms supported by hashlib.

    This enum inherits from str to allow string-like behavior while providing
    type safety and auto-completion in IDEs.
    """
    # Core algorithms
    MD5 = 'md5'
    SHA1 = 'sha1'
    SHA224 = 'sha224'
    SHA256 = 'sha256'
    SHA384 = 'sha384'
    SHA512 = 'sha512'

    # Modern algorithms (may not be available on all platforms)
    BLAKE2B = 'blake2b'
    BLAKE2S = 'blake2s'
    SHA3_224 = 'sha3_224'
    SHA3_256 = 'sha3_256'
    SHA3_384 = 'sha3_384'
    SHA3_512 = 'sha3_512'

    @classmethod
    def from_string(cls, algorithm: str) -> 'HashAlgorithm':
        """Convert a string to a HashAlgorithm enum value.

        Args:
            algorithm: String representation of the algorithm

        Returns:
            The corresponding HashAlgorithm enum value

        Raises:
            ValueError: If the algorithm is not supported
        """
        try:
            return cls(algorithm.lower())
        except ValueError:
            available = ", ".join(sorted([a.value for a in cls]))
            raise ValueError(
                f"Hash algorithm '{algorithm}' is not supported. "
                f"Supported algorithms: {available}"
            )

    @classmethod
    def is_available(cls, algorithm: 'HashAlgorithm') -> bool:
        """Check if the algorithm is available in the current hashlib installation.

        Args:
            algorithm: The HashAlgorithm to check

        Returns:
            True if the algorithm is available, False otherwise
        """
        return algorithm.value in hashlib.algorithms_available

    @classmethod
    def get_available(cls) -> Set['HashAlgorithm']:
        """Get a set of all available hash algorithms in the current installation.

        Returns:
            Set of available HashAlgorithm values
        """
        return {algo for algo in cls if algo.value in hashlib.algorithms_available}

    @classmethod
    def get_empty_hash(cls, algorithm: 'HashAlgorithm') -> str:
        """Get the hash of an empty string for the given algorithm.

        Args:
            algorithm: The HashAlgorithm to use

        Returns:
            The hash of an empty string
        """
        if algorithm in EMPTY_HASHES:
            return EMPTY_HASHES[algorithm]
        else:
            raise ValueError(f"Empty hash not available for algorithm '{algorithm}'")


# Pre-computed empty hashes for all supported algorithms
EMPTY_HASHES: Dict[HashAlgorithm, str] = {
    HashAlgorithm.MD5: 'd41d8cd98f00b204e9800998ecf8427e',
    HashAlgorithm.SHA1: 'da39a3ee5e6b4b0d3255bfef95601890afd80709',
    HashAlgorithm.SHA224: 'd14a028c2a3a2bc9476102bb288234c415a2b01f828ea62ac5b3e42f',
    HashAlgorithm.SHA256: 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855',
    HashAlgorithm.SHA384: '38b060a751ac96384cd9327eb1b1e36a21fdb71114be07434c0cc7bf63f6e1da274edebfe76f65fbd51ad2f14898b95b',
    HashAlgorithm.SHA512: 'cf83e1357eefb8bdf1542850d66d8007d620e4050b5715dc83f4a921d36ce9ce47d0d13c5d85f2b0ff8318d2877eec2f63b931bd47417a81a538327af927da3e',
    HashAlgorithm.BLAKE2B: '786a02f742015903c6c6fd852552d272912f4740e15847618a86e217f71f5419d25e1031afee585313896444934eb04b903a685b1448b755d56f701afe9be2ce',
    HashAlgorithm.BLAKE2S: '69217a3079908094e11121d042354a7c1f55b6482ca1a51e1b250dfd1ed0eef9',
    HashAlgorithm.SHA3_224: '6b4e03423667dbb73b6e15454f0eb1abd4597f9a1b078e3f5b5a6bc7',
    HashAlgorithm.SHA3_256: 'a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a',
    HashAlgorithm.SHA3_384: '0c63a75b845e4f7d01107d852e4c2485c51a50aaaa94fc61995e71bbee983a2ac3713831264adb47fb6bd1e058d5f004',
    HashAlgorithm.SHA3_512: 'a69f73cca23a9ac5c8b567dc185a756e97c982164fe25859e0d1dcc1475c80a615b2123af1f5f94c11e3e9402c3ac558f500199d95b6d3e301758586281dcd26',
}