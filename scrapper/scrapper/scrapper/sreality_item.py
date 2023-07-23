from dataclasses import dataclass


@dataclass
class SrealityItem:
    name: str
    image_url: str
    

def get_item(data: dict) -> SrealityItem:
    return SrealityItem(
            name=data['name'],
            image_url=data['_links']['image_middle2'][0]['href']
            )
