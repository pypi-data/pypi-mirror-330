from dataclasses import dataclass

from sponsored_ads_service.protobuf import sponsored_ads_service_pb2 as pb


@dataclass(frozen=True)
class TextNotice:
    key: str
    text: str
    description: str

    def to_pb(self) -> pb.Notice:
        return pb.Notice(
            text_notice=pb.TextNotice(
                key=self.key,
                text=self.text,
                description=self.description,
            )
        )


@dataclass(frozen=True)
class ImageNotice:
    key: str
    image_url: str
    alt_text: str
    description: str

    def to_pb(self) -> pb.Notice:
        return pb.Notice(
            image_notice=pb.ImageNotice(
                key=self.key,
                image_url=self.image_url,
                alt_text=self.alt_text,
                description=self.description,
            )
        )


Notice = TextNotice | ImageNotice
