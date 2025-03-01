from pathlib import Path

import pytest

import eip712.model.types
from eip712 import (
    EIP712BaseMapper,
    EIP712ContractDescriptor,
    EIP712DAppDescriptor,
    EIP712FieldMapper,
    EIP712MessageNameMapper,
    EIP712Version,
)
from eip712.convert.input_to_resolved import EIP712InputToResolvedConverter
from eip712.convert.resolved_to_instructions import EIP712ResolvedToInstructionsConverter
from eip712.model.input.descriptor import InputEIP712DAppDescriptor
from eip712.serialize import serialize_instruction

TEST_FILE = Path(__file__).parent / "data" / "paraswap_eip712.json"
MESSAGE_INSTRUCTION = (
    "b7"  # identifier of a name mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "09"  # count of field mappers
    "4175677573747573524651204552433230206f72646572"  # name to display
)
MESSAGE_MAPPER = (
    EIP712MessageNameMapper,
    [MESSAGE_INSTRUCTION],
)

INSTRUCTIONS_V1 = [
    # nonceAndMeta
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "6e6f6e6365416e644d6574614e6f6e636520616e64206d65746164617461",  # field path and display name
    # expiry
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "65787069727945787069726174696f6e2074696d65",  # field path and display name
    # maker
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "6d616b65724d616b65722061646472657373",  # field path and display name
    # taker
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "74616b657254616b65722061646472657373",  # field path and display name
    # makerAsset
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "6d616b657241737365744d616b657220616d6f756e74",
    # makerAmount
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "6d616b6572416d6f756e744d616b657220616d6f756e74",  # field path and display name
    # takerAsset
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "74616b6572417373657454616b657220616d6f756e74",  # field path and display name
    # takerAmount
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "74616b6572416d6f756e7454616b657220616d6f756e74",  # field path and display name
    # verifyingContract amount
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "6d616b6572416d6f756e74416d6f756e7420666f726d61747465642066726f6d20766572696679696e67436f6e7472616374",
]

TEST_IDENTIFIERS_V1 = [
    MESSAGE_MAPPER,
    (
        EIP712FieldMapper,
        INSTRUCTIONS_V1,
    ),
]

INSTRUCTIONS_V2 = [
    # nonceAndMeta
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "6e6f6e6365416e644d6574614e6f6e636520616e64206d65746164617461",  # field path and display name
    # expiry
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "65787069727945787069726174696f6e2074696d65",  # field path and  display name
    # maker
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "6d616b65724d616b65722061646472657373",  # field path and display name
    # taker
    "48"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "74616b657254616b65722061646472657373",  # field path and display name
    # makerAsset
    "0b"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "6d616b6572417373657400",  # field path and token index
    # makerAmount
    "16"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "6d616b6572416d6f756e744d616b657220616d6f756e7400",  # field path, display name and token index
    # takerAsset
    "0b"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "74616b6572417373657401",  # field path and token index
    # takerAmount
    "16"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "74616b6572416d6f756e7454616b657220616d6f756e7401",  # field path, display name and token index
    # verifyingContract amount
    "16"  # identifier of a field mapper
    "0000000000000089"  # chain id
    "f3cd476c3c4d3ac5ca2724767f269070ca09a043"  # contract address
    "16c6594547c8c6af18ca0d8b500976bfb7f38764060cec3792c2aad3"  # message schema hash
    "6d616b6572416d6f756e74416d6f756e7420666f726d61747465642066726f6d20766572696679696e67436f6e7472616374ff",
]

TEST_IDENTIFIERS_V2 = [
    MESSAGE_MAPPER,
    (
        EIP712FieldMapper,
        INSTRUCTIONS_V2,
    ),
]


@pytest.mark.parametrize("expected_mapping_type, expected_mapping_identifiers", TEST_IDENTIFIERS_V1)
def test_identifiers_v1(
    expected_mapping_type: type[EIP712BaseMapper],
    expected_mapping_identifiers: list[str],
) -> None:
    with open(TEST_FILE, "rb") as f:
        eip712_descriptor = EIP712DAppDescriptor.model_validate_json(f.read())
        field_identifiers = [
            mapper.identifier(EIP712Version.V1)
            for mapper in eip712_descriptor.mappers()
            if isinstance(mapper, expected_mapping_type)
        ]
        assert field_identifiers == expected_mapping_identifiers


@pytest.mark.parametrize("expected_mapping_type, expected_mapping_identifiers", TEST_IDENTIFIERS_V2)
def test_identifiers_v2(
    expected_mapping_type: type[EIP712BaseMapper],
    expected_mapping_identifiers: list[str],
) -> None:
    with open(TEST_FILE, "rb") as f:
        eip712_descriptor = EIP712DAppDescriptor.model_validate_json(f.read())
        field_identifiers = [
            mapper.identifier(EIP712Version.V2)
            for mapper in eip712_descriptor.mappers()
            if isinstance(mapper, expected_mapping_type)
        ]
        assert field_identifiers == expected_mapping_identifiers


def test_serialize_instructions() -> None:
    input_model = InputEIP712DAppDescriptor.load(TEST_FILE)
    resolved_model = EIP712InputToResolvedConverter().convert(input_model)
    instructions = EIP712ResolvedToInstructionsConverter().convert(resolved_model)

    serialized_instructions_v1: list[str] = []
    serialized_instructions_v2: list[str] = []
    for _, per_address in instructions.items():
        for _, instructions_list in per_address.items():
            for instruction in instructions_list:
                serialized_instructions_v1.append(
                    serialize_instruction(instruction, eip712.model.types.EIP712Version.V1)
                )
                serialized_instructions_v2.append(
                    serialize_instruction(instruction, eip712.model.types.EIP712Version.V2)
                )

    assert serialized_instructions_v1[0] == MESSAGE_INSTRUCTION
    assert serialized_instructions_v1[1:] == INSTRUCTIONS_V1

    assert serialized_instructions_v2[0] == MESSAGE_INSTRUCTION
    assert serialized_instructions_v2[1:] == INSTRUCTIONS_V2


def test_add_message() -> None:
    target_contract = EIP712ContractDescriptor(
        address="0x9757f2d2b135150bbeb65308d4a91804107cd8d6",
        contractName="Rarible ExchangeV2",
        messages=[],
    )

    expected_eip712_dapp = EIP712DAppDescriptor.model_validate(
        {
            "blockchainName": "ethereum",
            "chainId": 1,
            "contracts": [
                {
                    "address": "0x9757f2d2b135150bbeb65308d4a91804107cd8d6",
                    "contractName": "Rarible ExchangeV2",
                    "messages": [
                        {
                            "mapper": {
                                "fields": [
                                    {"label": "Order maker", "path": "maker"},
                                    {
                                        "label": "Order makeAsset assetType assetClass",
                                        "path": "makeAsset.assetType.assetClass",
                                    },
                                    {
                                        "label": "Order makeAsset assetType data",
                                        "path": "makeAsset.assetType.data",
                                    },
                                    {
                                        "label": "Order makeAsset value",
                                        "path": "makeAsset.value",
                                    },
                                    {"label": "Order taker", "path": "taker"},
                                    {
                                        "label": "Order takeAsset assetType assetClass",
                                        "path": "takeAsset.assetType.assetClass",
                                    },
                                    {
                                        "label": "Order takeAsset assetType data",
                                        "path": "takeAsset.assetType.data",
                                    },
                                    {
                                        "label": "Order takeAsset value",
                                        "path": "takeAsset.value",
                                    },
                                    {"label": "Order salt", "path": "salt"},
                                    {"label": "Order start", "path": "start"},
                                    {"label": "Order end", "path": "end"},
                                    {"label": "Order dataType", "path": "dataType"},
                                    {"label": "Order data", "path": "data"},
                                ],
                                "label": "Order",
                            },
                            "schema": {
                                "Asset": [
                                    {"name": "assetType", "type": "AssetType"},
                                    {"name": "value", "type": "uint256"},
                                ],
                                "AssetType": [
                                    {"name": "assetClass", "type": "bytes4"},
                                    {"name": "data", "type": "bytes"},
                                ],
                                "EIP712Domain": [
                                    {"name": "name", "type": "string"},
                                    {"name": "version", "type": "string"},
                                    {"name": "chainId", "type": "uint256"},
                                    {"name": "verifyingContract", "type": "address"},
                                ],
                                "Order": [
                                    {"name": "maker", "type": "address"},
                                    {"name": "makeAsset", "type": "Asset"},
                                    {"name": "taker", "type": "address"},
                                    {"name": "takeAsset", "type": "Asset"},
                                    {"name": "salt", "type": "uint256"},
                                    {"name": "start", "type": "uint256"},
                                    {"name": "end", "type": "uint256"},
                                    {"name": "dataType", "type": "bytes4"},
                                    {"name": "data", "type": "bytes"},
                                ],
                            },
                        },
                        {
                            "mapper": {
                                "fields": [
                                    {"label": "Mail contents", "path": "contents"},
                                    {"label": "Mail from name", "path": "from.name"},
                                    {
                                        "label": "Mail from wallets [] name",
                                        "path": "from.wallets.[].name",
                                    },
                                    {
                                        "label": "Mail from wallets [] addr",
                                        "path": "from.wallets.[].addr",
                                    },
                                    {"label": "Mail to name", "path": "to.name"},
                                    {
                                        "label": "Mail to wallets [] name",
                                        "path": "to.wallets.[].name",
                                    },
                                    {
                                        "label": "Mail to wallets [] addr",
                                        "path": "to.wallets.[].addr",
                                    },
                                ],
                                "label": "Mail",
                            },
                            "schema": {
                                "EIP712Domain": [
                                    {"name": "chainId", "type": "uint256"},
                                    {"name": "name", "type": "string"},
                                    {"name": "verifyingContract", "type": "address"},
                                    {"name": "version", "type": "string"},
                                ],
                                "Mail": [
                                    {"name": "contents", "type": "string"},
                                    {"name": "from", "type": "Person"},
                                    {"name": "to", "type": "Person"},
                                ],
                                "Person": [
                                    {"name": "name", "type": "string"},
                                    {"name": "wallets", "type": "Wallet[]"},
                                ],
                                "Wallet": [
                                    {"name": "name", "type": "string"},
                                    {"name": "addr", "type": "address"},
                                ],
                            },
                        },
                    ],
                }
            ],
            "name": "Rarible",
        }
    )
    schemas = [m.schema_ for c in expected_eip712_dapp.contracts for m in c.messages]
    eip712_dapp = EIP712DAppDescriptor(blockchainName="ethereum", chainId=1, name="Rarible", contracts=[])
    assert expected_eip712_dapp != eip712_dapp
    for schema in schemas:
        eip712_dapp.add_message(target_contract=target_contract, schema=schema)
    assert expected_eip712_dapp == eip712_dapp
