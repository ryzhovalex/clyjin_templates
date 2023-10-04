from clyjin_templates.conversion import TemplateGroupConversionUtils
from clyjin_templates.filesystem.models import FileNode
from clyjin_templates.template.group import TemplateGroup, TemplateGroupInternal


def test_convert():
    group: TemplateGroup = TemplateGroup.model_validate({
        "name": "test",
        "tree": {
            "main.py": {
                "$content": "print(${a})"
            },
            "service.py": {
                "$content": "&service.py"
            },
            "readme": {
                "$content": "hello!"
            }
        },
        "templates": {
            "service.py": None
        },
        "description": "Test template!",
        "vars": {
            "a": {
                "default": 1
            }
        }
    })

    internal: TemplateGroupInternal = \
        TemplateGroupConversionUtils.convert_to_internal(
            group,
            {
                "a": 5
            }
        )

    print(internal)
    assert 0
