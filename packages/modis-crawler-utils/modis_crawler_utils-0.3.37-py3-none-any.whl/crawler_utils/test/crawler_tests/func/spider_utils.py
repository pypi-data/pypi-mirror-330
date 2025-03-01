from pathlib import Path
import sys
from crawler_utils.social_media.items import UserProfile, GroupProfile, Message, SocialConnection,SocialMediaItem
from typing import Type, Dict,List

from crawler_utils.test.crawler_tests.func.settings import spiders_specification


def get_limits2type() -> Dict[str, str]:
    return spiders_specification.get("limits2type", {})

def get_itemtype2id() -> Dict[str, List[str]]:
    return spiders_specification.get("itemtype2id", {})

def get_itemtype_mapping() -> Dict[str, Type[SocialMediaItem]]:
    return {
        'GroupProfile': GroupProfile,
        'Message': Message,
        'UserProfile': UserProfile,
        'SocialConnection': SocialConnection,
    }

