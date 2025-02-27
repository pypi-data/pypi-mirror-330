from markdown_dom import MarkdownSection, MarkdownSectionTitle



def test_markdown_section() -> None:
    markdown_section = MarkdownSection("test")
    assert markdown_section.render(section_level=1) == "test"


def test_markdown_section_with_title() -> None:
    markdown_section = MarkdownSection(MarkdownSectionTitle("test"), "description")
    assert (
        markdown_section.render(section_level=1)
        == """# test
description"""
    )


def test_markdown_section_with_multiple_elements() -> None:
    markdown_section = MarkdownSection(
        MarkdownSectionTitle("test"),
        "description1",
        "description2",
    )
    assert (
        markdown_section.render(section_level=1)
        == """# test
description1
description2"""
    )


def test_markdown_section_with_none_elements() -> None:
    markdown_section = MarkdownSection(
        MarkdownSectionTitle("test"),
        None,
        "description",
    )
    assert (
        markdown_section.render(section_level=1)
        == """# test
description"""
    )


def test_markdown_section_nested() -> None:
    markdown_section = MarkdownSection(
        MarkdownSectionTitle("test"),
        MarkdownSection(
            MarkdownSectionTitle("nested"),
            "description",
        ),
        MarkdownSection(
            MarkdownSectionTitle("nested2"),
            "description2",
        ),
    )
    assert (
        markdown_section.render(section_level=2)
        == """## test
### nested
description

### nested2
description2"""
    )

