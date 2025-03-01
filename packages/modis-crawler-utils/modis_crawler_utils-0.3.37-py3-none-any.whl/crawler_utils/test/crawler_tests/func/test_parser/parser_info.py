import itertools
from typing import Optional, List, Type
from crawler_utils.social_media.items import SocialMediaItem
from pydantic_core import PydanticUndefined
from crawler_utils.social_media.items import MessageType
from crawler_utils.social_media.items import UserProfile, GroupProfile, Message, SocialConnection
from crawler_utils.test.crawler_tests.func.spider_utils import get_itemtype_mapping


class ParserInfo:
    """
    Class for storing and managing information about the parser, including its name, path to test results,
    and the types of social media items it produces.

    Attributes:
        parser_name (str): Name of the parser.
        path_to_test_results (str): Path to the directory where test results are stored.
        _output_itemtypes (set[Type[SocialMediaItem]]): Set of output item types associated with this parser.
    """
    parser_name: str
    path_to_test_results: str
    _output_itemtypes: set[Type[SocialMediaItem]]

    def __init__(self, parser_name: str, path_to_test_results: str, output_itemtypes: List[str]):
        self.parser_name = parser_name
        self.path_to_test_results = path_to_test_results

        itemtype_mapping = get_itemtype_mapping()
        self._output_itemtypes = {itemtype_mapping[itemtype] for itemtype in output_itemtypes if
                                  itemtype in itemtype_mapping}

    def __str__(self):
        return self.parser_name


    @property
    def output_itemtypes(self) -> List[Optional[str]]:
        default_itemtypes = [itemtype.model_fields['type'].default for itemtype in self._output_itemtypes]

        if 'message' in default_itemtypes:
            default_itemtypes.remove('message')
            default_itemtypes += [e.name.lower() for e in MessageType]
        return [item for item in default_itemtypes if item is not PydanticUndefined]

    def get_itemtype_cls(self, itemtype_name: str) -> Type[SocialMediaItem]:
        for itemtype, cls in zip(self.output_itemtypes, self._output_itemtypes):
            if itemtype == itemtype_name:
                return cls
        raise ValueError(f"Item type '{itemtype_name}' not found.")
