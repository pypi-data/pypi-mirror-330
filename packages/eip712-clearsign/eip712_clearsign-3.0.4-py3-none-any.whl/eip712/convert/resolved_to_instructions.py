from eip712.model.instruction import (
    DEFAULT_FIELD_PREFIX,
    EIP712DappInstructions,
    EIP712FieldInstruction,
    EIP712Instruction,
    EIP712InstructionType,
    EIP712MessageInstruction,
)
from eip712.model.resolved.descriptor import ResolvedEIP712DAppDescriptor
from eip712.model.types import EIP712Format
from eip712.utils import get_schema_hash


class EIP712ResolvedToInstructionsConverter:
    def convert(self, descriptor: ResolvedEIP712DAppDescriptor) -> EIP712DappInstructions:
        """
        Convert a resolved EIP712 descriptor to a dictionary of EIP712 instructions.
        """
        instructions: EIP712DappInstructions = {}
        for contract in descriptor.contracts:
            instructions[contract.address] = {}
            for message in contract.messages:
                schema_hash = get_schema_hash(message.schema_)
                instructions_list: list[EIP712Instruction] = []
                for field in message.mapper.fields:
                    match field.format:
                        case EIP712Format.AMOUNT:
                            # special case: if assetPath is None, the token referenced is EIP712Domain.verifyingContract
                            # we generate only one instruction with coin_ref=0xFF
                            if field.assetPath is None:
                                instructions_list.append(
                                    EIP712FieldInstruction(
                                        type_prefix=22,
                                        display_name=field.label,
                                        chain_id=descriptor.chainId,
                                        contract_address=contract.address,
                                        schema_hash=schema_hash,
                                        field_path=field.path,
                                        format=EIP712InstructionType.AMOUNT,
                                        coin_ref=255,
                                    )
                                )
                            else:
                                # General case: amount format generates two instructions:
                                # - in v1, this will result in 2 screens (raw token contract address, then raw amount)
                                # - in v2, this will result in 1 screen (amount with token)

                                if field.coinRef is None:
                                    raise ValueError(f"EIP712 amount value should have coin_ref: {self}")

                                instructions_list.extend(
                                    [
                                        EIP712FieldInstruction(
                                            type_prefix=11,
                                            display_name=field.label,
                                            chain_id=descriptor.chainId,
                                            contract_address=contract.address,
                                            schema_hash=schema_hash,
                                            field_path=field.assetPath,
                                            format=EIP712InstructionType.TOKEN,
                                            coin_ref=field.coinRef,
                                        ),
                                        EIP712FieldInstruction(
                                            type_prefix=22,
                                            display_name=field.label,
                                            chain_id=descriptor.chainId,
                                            contract_address=contract.address,
                                            schema_hash=schema_hash,
                                            field_path=field.path,
                                            format=EIP712InstructionType.AMOUNT,
                                            coin_ref=field.coinRef,
                                        ),
                                    ]
                                )
                        case EIP712Format.DATETIME:
                            instructions_list.append(
                                EIP712FieldInstruction(
                                    type_prefix=33,
                                    display_name=field.label,
                                    chain_id=descriptor.chainId,
                                    contract_address=contract.address,
                                    schema_hash=schema_hash,
                                    field_path=field.path,
                                    format=EIP712InstructionType.DATETIME,
                                    coin_ref=None,
                                )
                            )
                        case _:
                            instructions_list.append(
                                EIP712FieldInstruction(
                                    type_prefix=DEFAULT_FIELD_PREFIX,
                                    display_name=field.label,
                                    chain_id=descriptor.chainId,
                                    contract_address=contract.address,
                                    schema_hash=schema_hash,
                                    field_path=field.path,
                                    format=EIP712InstructionType.RAW,
                                    coin_ref=None,
                                )
                            )

                # Insert MessageInstruction at the beginning of the list
                # This is done after because it requires the length of the field instructions
                # computed above
                instructions_list.insert(
                    0,
                    EIP712MessageInstruction(
                        type_prefix=183,
                        display_name=message.mapper.label,
                        chain_id=descriptor.chainId,
                        contract_address=contract.address,
                        schema_hash=schema_hash,
                        field_mappers_count=len(instructions_list),
                    ),
                )
                instructions[contract.address][schema_hash] = instructions_list

        return instructions
