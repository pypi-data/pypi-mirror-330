from crawler_utils.social_media.items import UserProfile, GroupProfile, Message, SocialConnection
from crawler_utils.test.crawler_tests.func.test_parser.parser_info import ParserInfo
from crawler_utils.test.crawler_tests.func.spider_utils import spiders_specification


parsers = spiders_specification.get("spiders").get("parsers", [])

parsers_to_check = [
    ParserInfo(
        parser_name=parser.get("parser_name"),
        path_to_test_results=parser.get("path_to_test_results"),
        output_itemtypes=parser.get("output_itemtypes")
    ) for parser in parsers
]