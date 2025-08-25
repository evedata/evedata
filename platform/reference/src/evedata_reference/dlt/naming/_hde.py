from typing import override

from dlt.common.normalizers.naming import snake_case


class NamingConvention(snake_case.NamingConvention):
    @override
    def normalize_identifier(self, identifier: str) -> str:
        match identifier:
            case "attributeIDs":
                return "attribute_ids"
            case "categoryIDs":
                return "category_ids"
            case "groupIDs":
                return "group_ids"
            case _:
                return super().normalize_identifier(identifier)
