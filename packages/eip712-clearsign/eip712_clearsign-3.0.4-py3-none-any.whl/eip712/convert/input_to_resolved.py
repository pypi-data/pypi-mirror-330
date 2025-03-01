from eip712.model.input.contract import InputEIP712Contract
from eip712.model.input.descriptor import InputEIP712DAppDescriptor
from eip712.model.input.message import InputEIP712Mapper, InputEIP712MapperField, InputEIP712Message
from eip712.model.resolved.contract import ResolvedEIP712Contract
from eip712.model.resolved.descriptor import ResolvedEIP712DAppDescriptor
from eip712.model.resolved.message import ResolvedEIP712Mapper, ResolvedEIP712MapperField, ResolvedEIP712Message
from eip712.model.types import EIP712Format


class EIP712InputToResolvedConverter:
    def convert(
        self,
        descriptor: InputEIP712DAppDescriptor,
    ) -> ResolvedEIP712DAppDescriptor:
        """
        Convert an input EIP712 descriptor to a resolved EIP712 descriptor.
        """
        return ResolvedEIP712DAppDescriptor(
            blockchainName=descriptor.blockchainName,
            chainId=descriptor.chainId,
            name=descriptor.name,
            contracts=[self._convert_contract(contract) for contract in descriptor.contracts],
        )

    @classmethod
    def _convert_contract(cls, contract: InputEIP712Contract) -> ResolvedEIP712Contract:
        return ResolvedEIP712Contract(
            address=contract.address,
            contractName=contract.contractName,
            messages=[cls._convert_message(message) for message in contract.messages],
        )

    @classmethod
    def _convert_message(cls, message: InputEIP712Message) -> ResolvedEIP712Message:
        return ResolvedEIP712Message(
            schema=message.schema_,
            mapper=cls._convert_mapper(message.mapper),
        )

    @classmethod
    def _convert_mapper(cls, mapper: InputEIP712Mapper) -> ResolvedEIP712Mapper:
        coin_refs: dict[str, int] = {}
        return ResolvedEIP712Mapper(
            label=mapper.label,
            fields=[cls._convert_field(field, coin_refs) for field in mapper.fields],
        )

    @classmethod
    def _convert_field(cls, field: InputEIP712MapperField, coin_refs: dict[str, int]) -> ResolvedEIP712MapperField:
        coin_ref: int | None = None
        if field.format == EIP712Format.AMOUNT and (path := field.assetPath) is not None:
            if path not in coin_refs:
                coin_refs[path] = len(coin_refs)
            coin_ref = coin_refs[path]

        return ResolvedEIP712MapperField(
            path=field.path,
            label=field.label,
            assetPath=field.assetPath,
            format=field.format,
            coinRef=coin_ref,
        )
