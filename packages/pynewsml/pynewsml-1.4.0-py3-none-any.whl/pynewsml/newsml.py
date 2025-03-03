from datetime import datetime
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from lxml import etree


@dataclass
class Topic:
    topic_type: str
    formal_name: str
    descriptions: dict


@dataclass
class RevisionId:
    value: str
    update: str
    previous_revision: str

    def __init__(self, elem):
        self.value = elem.text
        self.update = elem.attrib.get("Update")
        self.previous_revision = elem.attrib.get("PreviousRevision")


@dataclass
class NewsIdentifier:
    provider_id: str
    date_id: str
    news_item_id: str
    revision_id: RevisionId
    public_identifier: str


@dataclass
class NewsLines:
    headline: str
    subheadline: str
    byline: str
    dateline: str
    creditline: str
    copyrightline: str
    keywords: List[str]


@dataclass
class ContentItem:
    media_type: str
    characteristics: Dict[str, str]
    href: Optional[str]
    data_content: Optional[str]


@dataclass
class Location:
    country: str
    country_name: str
    country_area: str
    sub_country_area: str
    city: str


@dataclass
class SubjectCode:
    formal_name: str
    scheme: str


@dataclass
class DescriptiveMetadata:
    language: str
    genre: str
    location: Location
    properties: dict
    subject_codes: List[SubjectCode]

    @classmethod
    def from_xml(cls, elem):
        language = elem.find("Language").get("FormalName")
        genre = elem.find("Genre").get("FormalName")

        subject_codes = [SubjectCode(e.get("FormalName"), e.get("Scheme"))
                         for e in elem.find("SubjectCode").iter() if e.tag != "SubjectCode"]

        properties = {
            prop.get("FormalName"): prop.get("Value")
            for prop in elem.findall("Property")
        }
        location_data = {
            prop.get("FormalName"): prop.get("Value")
            for prop in elem.find("Location").findall("Property")
        }
        location = Location(
            country=location_data.get("Country"),
            country_name=location_data.get("CountryName"),
            country_area=location_data.get("CountryArea"),
            sub_country_area=location_data.get("SubCountryArea"),
            city=location_data.get("City"),
        )

        return cls(language, genre, location, properties, subject_codes)


@dataclass
class NewsComponent:
    descriptive_metadata: DescriptiveMetadata


@dataclass
class NewsItem:
    identifier: NewsIdentifier
    date_label: datetime
    news_lines: NewsLines
    topics: List[Topic]
    content: List[ContentItem]
    news_component: NewsComponent


@dataclass
class NewsML:
    news_items: List[NewsItem] = field(default_factory=list)

    @classmethod
    def from_xml(cls, xml_string: str, encoding: str = 'iso-8859-1') -> "NewsML":
        root = etree.fromstring(xml_string.encode(encoding))
        news_items = []

        for news_item_elem in root.findall(".//NewsItem"):
            identifier = NewsIdentifier(
                provider_id=news_item_elem.findtext(".//ProviderId"),
                date_id=news_item_elem.findtext(".//DateId"),
                news_item_id=news_item_elem.findtext(".//NewsItemId"),
                revision_id=RevisionId(news_item_elem.find(".//RevisionId")),
                public_identifier=news_item_elem.findtext(
                    ".//PublicIdentifier"),
            )

            date_label = news_item_elem.findtext(".//DateLabel")
            date_label = datetime.strptime(date_label, "%d/%m/%Y %H:%M:%S")

            news_lines = NewsLines(
                headline=news_item_elem.findtext(".//HeadLine"),
                subheadline=news_item_elem.findtext(".//SubHeadLine"),
                byline=news_item_elem.findtext(".//ByLine"),
                dateline=news_item_elem.findtext(".//DateLine"),
                creditline=news_item_elem.findtext(".//CreditLine"),
                copyrightline=news_item_elem.findtext(".//CopyrightLine"),
                keywords=[kw.text for kw in news_item_elem.findall(
                    ".//KeywordLine")],
            )

            descriptive_metadata = news_item_elem.find(
                "NewsComponent").find("DescriptiveMetadata")
            news_component = NewsComponent(
                DescriptiveMetadata.from_xml(descriptive_metadata)
            )

            topics = cls._load_topics(news_item_elem)

            content_items = []
            for content_elem in news_item_elem.findall(".//ContentItem"):
                characteristics = content_elem.find(".//Characteristics")
                content = ContentItem(
                    media_type=content_elem.find(".//MediaType").get("FormalName"),
                    href=content_elem.get("Href"),
                    characteristics={c.get("FormalName"): c.get("Value")
                                     for c in characteristics.findall("Property")},
                    data_content=content_elem.findtext(".//DataContent"),
                )
                content_items.append(content)

            news_items.append(
                NewsItem(
                    identifier,
                    date_label,
                    news_lines,
                    topics,
                    content_items,
                    news_component
                )
            )

        return NewsML(news_items)

    @staticmethod
    def _load_topics(elem) -> List[Topic]:
        topics = []
        for topic_elem in elem.findall(".//Topic"):
            descriptions = {desc.attrib.get(
                "xml:lang"): desc.text for desc in topic_elem.findall("Description")}
            topics.append(
                Topic(
                    topic_type=topic_elem.find(
                        ".//TopicType").attrib.get("FormalName"),
                    formal_name=topic_elem.findtext(".//FormalName"),
                    descriptions=descriptions,
                )
            )
        return topics
