from bs4 import NavigableString, Tag
import pandas as pd

# A path to some content within a hyper structure
# e.g (div, 0, div, 2, p, text)
HYPER_PATH = tuple[str | int, ...]


def get_cleaned_attributes(tag: Tag) -> dict[str, str]:
    attributes = {}
    for attr, content in tag.attrs.items():
        if isinstance(content, list):
            # Beatiful soup turns class content into a list by splitting
            # at spaces. This turns it back into a single string.
            content = " ".join(content)
        attributes[attr] = content
    return attributes


def extract_content_from_tag(tag: Tag) -> dict[HYPER_PATH, str]:
    content_by_hyperpath: dict[HYPER_PATH, str] = {
        (tag.name, attr): content
        for attr, content in get_cleaned_attributes(tag).items()
    }

    for i, inner_element in enumerate(tag):
        if isinstance(inner_element, NavigableString):
            element_path: HYPER_PATH = (tag.name, i, "text")
            content_by_hyperpath[element_path] = str(inner_element).strip()

        if isinstance(inner_element, Tag):
            inner_content_by_path = extract_content_from_tag(inner_element)
            for inner_path, inner_content in inner_content_by_path.items():
                element_path = (tag.name, i, *inner_path)
                content_by_hyperpath[element_path] = inner_content

    return content_by_hyperpath


def tabulate_from_hyperpattern_tags(tags_with_structure: list[Tag]) -> pd.DataFrame:
    tag_contents = [extract_content_from_tag(tag) for tag in tags_with_structure]
    hyperframe = pd.DataFrame.from_records(tag_contents)

    # Drop columns in which all values are empty (None, Nan or empty string)
    is_column_empty = ~hyperframe.any(axis=0)
    empty_columns = hyperframe.columns[is_column_empty]
    hyperframe.drop(columns=empty_columns, inplace=True)

    return hyperframe
