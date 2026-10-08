from __future__ import annotations

import json
from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent
SONGS_DIR = ROOT / 'utwory'
OUTPUT = ROOT / 'songs.json'


def text_of_first(root: ET.Element, local_name: str) -> str:
    for elem in root.iter():
        if elem.tag.rsplit('}', 1)[-1] == local_name:
            text = (elem.text or '').strip()
            if text:
                return text
    return ''


def sanitize_id(title: str) -> str:
    value = ''.join(ch.lower() if ch.isalnum() else '-' for ch in title)
    while '--' in value:
        value = value.replace('--', '-')
    return value.strip('-') or 'song'


def main() -> None:
    songs = []
    for xml_path in sorted(SONGS_DIR.glob('*.xml')):
        try:
            root = ET.parse(xml_path).getroot()
        except ET.ParseError:
            continue

        title = text_of_first(root, 'title') or xml_path.stem
        author = text_of_first(root, 'author') or 'Nieznany'
        theme = text_of_first(root, 'theme') or 'worship'

        songs.append({
            'id': sanitize_id(title),
            'title': title,
            'author': author,
            'theme': theme,
            'path': xml_path.relative_to(ROOT).as_posix(),
        })

    OUTPUT.write_text(json.dumps(songs, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Zapisano {len(songs)} utworów do {OUTPUT.name}')


if __name__ == '__main__':
    main()
