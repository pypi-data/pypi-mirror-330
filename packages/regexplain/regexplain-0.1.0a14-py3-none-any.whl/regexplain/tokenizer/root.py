import re
from typing import Self
from . import grouped, non_grouped


class RegexTokenizer(grouped.MiscGroupRegexToken):
    """
    Every regex pattern must start as an object of this class, this is the
    most fundamental token. Every token in the input pattern is a sub-token of
    the root token. Since this is derived from group token, the full pattern
    is available in text form with the 'value' property.
    """

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        instance._parse_for_tokens.insert(  # NOQA
            0, non_grouped.UnpairedParenthesisRegexToken
        )
        return instance

    def __init__(self,
                 pattern: str,
                 flags: re.RegexFlag = re.NOFLAG):
        self._pattern = pattern

        self._ascii = re.ASCII in flags
        self._ignorecase = re.IGNORECASE in flags
        self._locale = re.LOCALE in flags
        self._multiline = re.MULTILINE in flags
        self._dotall = re.DOTALL in flags
        self._verbose = re.VERBOSE in flags
        self._debug = re.DEBUG in flags

        super().__init__(opening="", start_pos=0, super_token=None)

        self._closed = True  # root token is always considered closed

    def __getitem__(self, token_id):
        if not isinstance(token_id, int):
            raise ValueError("Token id/index must be integer")

        all_tokens_flat = self.sub_tokens_flat
        len_all_tokens_flat = len(all_tokens_flat)
        if token_id >= len_all_tokens_flat or token_id < 0:
            raise ValueError(f"Token id/index must be between "
                             f"0-{len_all_tokens_flat}")

        return all_tokens_flat[token_id]

    @property
    def id(self) -> bool | None:
        return None

    @property
    def index(self) -> int | None:
        return None

    @property
    def is_last_sibling(self) -> bool | None:
        return None

    @property
    def level(self) -> int:
        return 0

    @property
    def pattern(self) -> str:
        return self._pattern

    @property
    def root_token(self) -> type[Self]:
        return self

    @property
    def summary(self) -> str:
        return ""

    def explain(self,
                token_id: int | None = None,
                show_span: bool = True,
                show_group_pattern: bool = False,
                show_flags: bool = True,
                show_backreferences: bool = False,
                show_group_close_annotation: bool = True) -> None:
        explain = super().explain if token_id is None \
            else self.get_token_by_id(token_id)
        explain(
            show_span=show_span,
            show_group_pattern=show_group_pattern,
            show_flags=show_flags,
            show_backreferences=show_backreferences,
            show_group_close_annotation=show_group_close_annotation
        )

    def get_sibling(self, *args, **kwargs) -> type[Self] | None:
        raise NotImplementedError("Root token cannot have a sibling")
