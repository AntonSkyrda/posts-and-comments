import bleach
from lxml import etree, html


def clean_and_validate_html(content):
    allowed_tags = {"a", "code", "i", "strong"}
    allowed_attrs = {
        "a": ["href", "title"],
    }

    cleaned_content = bleach.clean(
        content, tags=allowed_tags, attributes=allowed_attrs, strip=True
    )

    try:
        document = html.fromstring(
            cleaned_content, parser=html.HTMLParser(recover=False)
        )

        xhtml = etree.tostring(
            document, pretty_print=True, encoding="unicode", method="xml"
        )
        return xhtml
    except (etree.XMLSyntaxError, etree.DocumentInvalid) as e:

        print(f"Validation Error: {e}")
        return ""
