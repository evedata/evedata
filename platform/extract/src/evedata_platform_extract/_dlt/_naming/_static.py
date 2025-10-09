from typing import override

from dlt.common.normalizers.naming import snake_case


class NamingConvention(snake_case.NamingConvention):
    @override
    def normalize_identifier(self, identifier: str) -> str:
        result = super().normalize_identifier(identifier)
        return result.replace("i_ds", "ids")
