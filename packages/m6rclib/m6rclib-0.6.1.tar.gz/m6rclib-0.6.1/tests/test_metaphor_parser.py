import os
import stat
from pathlib import Path

import pytest

from m6rclib import (
    MetaphorASTNodeType,
    MetaphorParser,
    MetaphorParserError,
    format_ast,
)


@pytest.fixture
def parser():
    """Provide a parser instance for tests."""
    return MetaphorParser()


@pytest.fixture
def setup_files(tmp_path):
    """Create sample files for testing."""
    # Python file
    py_file = tmp_path / "test.py"
    py_file.write_text("def hello():\n    print('Hello, World!')")

    # Text file
    txt_file = tmp_path / "test.txt"
    txt_file.write_text("Plain text content")

    # JavaScript file
    js_file = tmp_path / "test.js"
    js_file.write_text("function hello() { console.log('Hello'); }")

    # Multiple extension file
    multi_file = tmp_path / "test.spec.js"
    multi_file.write_text("describe('test', () => { it('works', () => {}); });")

    return tmp_path


@pytest.fixture
def temp_test_files(tmp_path):
    """Create a set of temporary test files"""
    d = tmp_path / "test_files"
    d.mkdir()

    # Create main file
    main = d / "main.m6r"
    main.write_text(
        "Role:\n" \
        "    Description\n" \
        "\n" \
        "Context:\n" \
        "    Some context\n" \
        "\n" \
        "Action:\n" \
        "    Do something\n"
    )

    # Create include file
    include = d / "include.m6r"
    include.write_text(
        "Context: Include\n" \
        "    Included content\n"
    )

    return str(d)


@pytest.fixture
def create_read_only_file(tmp_path):
    """Create a read-only file for testing permission errors"""
    p = tmp_path / "readonly.m6r"
    p.write_text(
        "Role: Test\n" \
        "    Description\n"
    )

    # Remove read permissions
    os.chmod(p, stat.S_IWRITE)
    yield p

    # Restore permissions for cleanup
    os.chmod(p, stat.S_IWRITE | stat.S_IREAD)


def test_basic_parsing(parser, temp_test_files):
    """Test basic parsing of a valid file"""
    main_file = Path(temp_test_files) / "main.m6r"
    result = parser.parse_file(str(main_file), [])
    assert len(result.get_children_of_type(MetaphorASTNodeType.TEXT)) > 1
    assert len(result.get_children_of_type(MetaphorASTNodeType.ROLE)) == 1
    assert len(result.get_children_of_type(MetaphorASTNodeType.CONTEXT)) == 1
    assert len(result.get_children_of_type(MetaphorASTNodeType.ACTION)) == 1


def test_invalid_structure(parser, tmp_path):
    """Test handling of invalid document structure"""
    p = tmp_path / "invalid.m6r"
    p.write_text(
        "InvalidKeyword: Test\n" \
        "    Description\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Unexpected token" in str(exc_info.value.errors[0].message)


def test_valid_keyword_parsing(parser):
    """Test that valid keywords are parsed correctly."""
    input_text = (
        "Role: Test\n"
        "    Description\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    roles = result.get_children_of_type(MetaphorASTNodeType.ROLE)
    assert len(roles) == 1
    assert roles[0].value == "Test"


def test_invalid_keyword_error(parser):
    """Test that invalid keywords raise appropriate error."""
    input_text = "InvalidKeyword: Test\n    Text\n"

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "Unexpected token" in error.message


def test_error_location_tracking(parser):
    """Test that error location is correctly tracked."""
    input_text = (
        "Role: Test\n"
        "    Description\n"
        "  BadIndent: Wrong\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert error.line == 3
    assert "test.txt" == error.filename


def test_keyword_empty_value(parser):
    """Test parsing keyword with no value."""
    input_text = (
        "Role:\n"
        "    Description\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    assert role.value == ""


def test_keyword_whitespace_value(parser):
    """Test parsing keyword with whitespace value."""
    input_text = (
        "Role:     \n"
        "    Description\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    assert role.value == ""


def test_duplicate_role_error(parser):
    """Test that duplicate Role keywords raise error."""
    input_text = (
        "Role: First\n"
        "    Description\n"
        "Role: Second\n"
        "    Text\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "'Role' already defined" in error.message


def test_duplicate_context_error(parser):
    """Test that duplicate Context keywords raise error."""
    input_text = (
        "Context: First\n"
        "    Description\n"
        "Context: Second\n"
        "    Text\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "'Context' already defined" in error.message


def test_duplicate_action_error(parser):
    """Test that duplicate Action keywords raise error."""
    input_text = (
        "Action: First\n"
        "    Description\n"
        "Action: Second\n"
        "    Text\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "'Action' already defined" in error.message


def test_keyword_text_preservation(parser):
    """Test that text following keywords is preserved."""
    input_text = (
        "Role: Test Role Description\n"
        "    Text\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    assert role.value == "Test Role Description"


def test_text_content_preservation(parser):
    """Test that indented text content is preserved."""
    input_text = (
        "Role: Test\n"
        "    First line\n"
        "    Second line\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    texts = role.get_children_of_type(MetaphorASTNodeType.TEXT)
    assert len(texts) == 2
    assert texts[0].value == "First line"
    assert texts[1].value == "Second line"


def test_empty_input(parser):
    """Test handling of empty input."""
    result = parser.parse("", "test.txt", [])

    # Preamble will still be generated
    assert len(result.children) > 0

    # But no user content
    assert len(result.get_children_of_type(MetaphorASTNodeType.ROLE)) == 0
    assert len(result.get_children_of_type(MetaphorASTNodeType.CONTEXT)) == 0
    assert len(result.get_children_of_type(MetaphorASTNodeType.ACTION)) == 0


def test_indentation_handling(parser):
    """Test handling of indentation through parser."""
    input_text = (
        "Context: Test\n"
        "    Description\n"
        "    Context: Nested\n"
        "        Nested content\n"
    )
    result = parser.parse(input_text, "test.txt", [])
    context_node = result.get_children_of_type(MetaphorASTNodeType.CONTEXT)[0]
    nested_contexts = context_node.get_children_of_type(MetaphorASTNodeType.CONTEXT)
    assert len(nested_contexts) == 1
    assert len(nested_contexts[0].get_children_of_type(MetaphorASTNodeType.TEXT)) == 1


def test_incorrect_indentation(parser):
    """Test handling of incorrect indentation."""
    input_text = (
        "Role: Test\n"
        "   Bad indent\n"  # 3 spaces instead of 4
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "indent" in error.message.lower()


def test_keyword_handling(parser):
    """Test keyword handling through parser."""
    input_text = (
        "Role: Test\n"
        "    Description\n"
        "Context: Setup\n"
        "    Details\n"
        "Action: Do\n"
        "    Steps\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    assert len(result.get_children_of_type(MetaphorASTNodeType.ROLE)) == 1
    assert len(result.get_children_of_type(MetaphorASTNodeType.CONTEXT)) == 1
    assert len(result.get_children_of_type(MetaphorASTNodeType.ACTION)) == 1


def test_fenced_code_blocks(parser):
    """Test handling of fenced code blocks."""
    input_text = (
        "Context: Test\n"
        "    Before code\n"
        "    ```python\n"
        "    def hello():\n"
        "        print('Hello')\n"
        "\n"
        "        print('World')\n"
        "    ```\n"
        "    After code\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    context = result.get_children_of_type(MetaphorASTNodeType.CONTEXT)[0]
    text_nodes = context.get_children_of_type(MetaphorASTNodeType.TEXT)

    # Convert text nodes to list of values for easier testing
    text_values = [node.value for node in text_nodes]
    assert "Before code" in text_values
    assert "```python" in text_values
    assert "def hello():" in text_values
    assert "    print('Hello')" in text_values
    assert "" in text_values
    assert "    print('World')" in text_values
    assert "```" in text_values
    assert "After code" in text_values


def test_fenced_code_blocks_with_blanks(parser):
    """Test handling of fenced code blocks with blank lines."""
    input_text = (
        "Context: Test\n"
        "    Before code\n"
        "    ```python\n"
        "    def hello():\n"
        "        print('Hello')\n"
        "    ```\n"
        "    After code\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    context = result.get_children_of_type(MetaphorASTNodeType.CONTEXT)[0]
    text_nodes = context.get_children_of_type(MetaphorASTNodeType.TEXT)

    # Convert text nodes to list of values for easier testing
    text_values = [node.value for node in text_nodes]
    assert "Before code" in text_values
    assert "```python" in text_values
    assert "def hello():" in text_values
    assert "    print('Hello')" in text_values
    assert "```" in text_values
    assert "After code" in text_values


def test_empty_lines(parser):
    """Test handling of empty lines."""
    input_text = (
        "Role: Test\n"
        "\n"
        "    Description\n"
        "\n"
        "    More text\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    text_nodes = role.get_children_of_type(MetaphorASTNodeType.TEXT)
    assert len(text_nodes) == 2
    assert text_nodes[0].value == "Description"
    assert text_nodes[1].value == "More text"


def test_tab_characters(parser):
    """Test handling of tab characters in input."""
    input_text = (
        "Role: Test\n"
        "    Description\n"  # Proper indentation after Role
        "\tTabbed line\n"  # Line starting with tab
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "[Tab]" in error.message


def test_comment_lines(parser):
    """Test handling of comment lines."""
    input_text = (
        "Role: Test\n"
        "    # This is a comment\n"
        "    Actual content\n"
        "# Another comment\n"
        "    More content\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role_node = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    text_nodes = role_node.get_children_of_type(MetaphorASTNodeType.TEXT)

    # Comments should be ignored
    assert len(text_nodes) == 2
    assert text_nodes[0].value == "Actual content"
    assert text_nodes[1].value == "More content"


def test_mixed_spaces_and_tab(parser):
    """Test handling of mixed tabs and spaces."""
    input_text = (
        "Role: Test\n"
        "    First line\n"  # Proper indentation after Role
        "    \t\n"  # Tab preceded by spaces
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])

    error = exc_info.value.errors[0]
    assert "[Tab]" in error.message


def test_tab_in_content_block(parser):
    """Test handling of tabs appearing within a content block."""
    input_text = (
        "Role: Test\n"
        "    Normal line\n"
        "    Line with\ttab\n"  # Tab in middle of content
        "    Another normal line\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    role_node = result.get_children_of_type(MetaphorASTNodeType.ROLE)[0]
    text_nodes = role_node.get_children_of_type(MetaphorASTNodeType.TEXT)
    assert len(text_nodes) == 3
    assert "\t" in text_nodes[1].value  # Tab preserved in content


def test_commented_keywords(parser):
    """Test that commented keywords are ignored."""
    input_text = (
        "Role: Test\n"
        "    First line\n"
        "# Role: Commented\n"
        "    Second line\n"
        "    # Context: Still commented\n"
        "    Third line\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    # Should only have one Role node since others are commented
    roles = result.get_children_of_type(MetaphorASTNodeType.ROLE)
    assert len(roles) == 1

    # Should have three text lines
    text_nodes = roles[0].get_children_of_type(MetaphorASTNodeType.TEXT)
    assert len(text_nodes) == 3
    assert text_nodes[0].value == "First line"
    assert text_nodes[1].value == "Second line"
    assert text_nodes[2].value == "Third line"


def test_python_embedding(parser, setup_files):
    """Test embedding of Python files with syntax highlighting."""
    input_text = (
        "Context: Code\n"
        "    Some context\n"
        f"    Embed: {setup_files}/test.py\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    context = result.get_children_of_type(MetaphorASTNodeType.CONTEXT)[0]
    text_nodes = context.get_children_of_type(MetaphorASTNodeType.TEXT)

    # Find the code block
    code_text = "\n".join(node.value for node in text_nodes)
    assert "```python" in code_text
    assert "def hello():" in code_text
    assert "print('Hello, World!')" in code_text


def test_multiple_file_embedding(parser, setup_files):
    """Test embedding multiple files using wildcards."""
    input_text = (
        "Context: JavaScript\n"
        f"    Embed: {setup_files}/*.js\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    formatted = format_ast(result)

    assert "```javascript" in formatted
    assert "function hello()" in formatted
    assert "describe('test'" in formatted


def test_missing_file_handling(parser, setup_files):
    """Test handling of missing files."""
    input_text = (
        "Context: Missing\n"
        f"    Embed: {setup_files}/nonexistent.txt\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse(input_text, "test.txt", [])
    error = exc_info.value.errors[0]
    assert "does not match any files" in error.message


def test_language_detection(parser, setup_files):
    """Test correct language detection for different file types."""
    for filename, expected_lang in [
        ("test.py", "python"),
        ("test.txt", "plaintext"),
        ("test.js", "javascript"),
        ("test.spec.js", "javascript")
    ]:
        input_text = (
            "Context: Test\n"
            f"    Embed: {setup_files}/{filename}\n"
        )

        result = parser.parse(input_text, "test.txt", [])
        formatted = format_ast(result)
        assert f"```{expected_lang}" in formatted


def test_recursive_embedding(tmp_path):
    """Test recursive file embedding with **/ pattern."""
    # Create nested directory structure
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    subsubdir = subdir / "deeper"
    subsubdir.mkdir()

    # Create files at different levels
    (tmp_path / "root.txt").write_text("Root content")
    (subdir / "level1.txt").write_text("Level 1 content")
    (subsubdir / "level2.txt").write_text("Level 2 content")

    parser = MetaphorParser()
    input_text = (
        "Context: Files\n"
        f"    Embed: {tmp_path}/**/*.txt\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    formatted = format_ast(result)

    assert "Root content" in formatted
    assert "Level 1 content" in formatted
    assert "Level 2 content" in formatted


def test_file_without_extension(parser, tmp_path):
    """Test embedding file with no extension."""
    # Create a file without extension
    no_ext_file = tmp_path / "noextension"
    no_ext_file.write_text("Content without extension")

    input_text = (
        "Context: Test\n"
        f"    Embed: {no_ext_file}\n"
    )

    result = parser.parse(input_text, "test.txt", [])
    formatted = format_ast(result)

    # Should use plaintext for files without extension
    assert "```plaintext" in formatted
    assert "Content without extension" in formatted


def test_missing_indent_after_keyword(parser, tmp_path):
    """Test handling of missing indent after keyword text"""
    p = tmp_path / "missing_indent.m6r"
    p.write_text(
        "Role: Test\n" \
        "No indent here\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Expected indent after keyword description" in str(exc_info.value.errors[0].message)


def test_file_not_found(parser):
    """Test handling of non-existent file"""
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file("nonexistent.m6r", [])

    assert any("File not found" in str(error.message) for error in exc_info.value.errors)


def test_action_unexpected_token(tmp_path):
    """Test handling of unexpected tokens in Action blocks"""
    p = tmp_path / "action_bad_token.m6r"
    p.write_text(
        "Action: DoSomething\n" \
        "    First text\n" \
        "    Context: Invalid\n" \
        "        This shouldn't be here\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Unexpected token: Context: in 'Action' block" in str(exc_info.value.errors[0].message)


def test_action_bad_outdent(tmp_path):
    """Test handling of incorrect indentation in Action blocks"""
    p = tmp_path / "action_bad_outdent.m6r"

    # 4, 3, 4 spaces.
    p.write_text(
        "Action: DoSomething\n" \
        "    First line correct\n" \
        "   Bad outdent level\n" \
        "    Back to correct\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "[Bad Outdent]" in str(exc_info.value.errors[0].message)


def test_action_missing_indent(tmp_path):
    """Test handling of missing indentation in Action blocks"""
    p = tmp_path / "action_no_indent.m6r"
    p.write_text(
        "Action: DoSomething\n" \
        "No indent here"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Expected indent after keyword description for 'Action' block" in str(exc_info.value.errors[0].message)


def test_action_missing_description_and_indent(tmp_path):
    """Test handling of Action block with neither description nor indent"""
    p = tmp_path / "action_invalid.m6r"
    p.write_text(
        "Action:\n" \
        "Text without indent\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Expected description or indent for 'Action' block" in str(exc_info.value.errors[0].message)


def test_action_inner_unexpected(tmp_path):
    """Test handling of unexpected tokens in Action blocks"""
    p = tmp_path / "action_bad_token.m6r"
    p.write_text(
        "Action: TestAction\n" \
        "    First text\n" \
        "    Role: Invalid\n" \
        "        This shouldn't be here\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Unexpected token: Role: in 'Action' block" in str(exc_info.value.errors[0].message)


def test_action_late_text(tmp_path):
    """Test handling of text after inner Action in Action blocks"""
    p = tmp_path / "action_late_text.m6r"
    p.write_text(
        "Action: TestAction\n" \
        "    First text\n" \
        "    Action: Inner\n" \
        "        Inner action\n" \
        "    Late text is wrong here\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Text must come first in an 'Action' block" in str(exc_info.value.errors[0].message)


def test_action_duplicate_sections(parser, tmp_path):
    """Test handling of duplicate sections"""
    p = tmp_path / "duplicate.m6r"
    p.write_text(
        "Action: Test1\n" \
        "    Description\n" \
        "Action: Test2\n" \
        "    Description\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "'Action' already defined" in str(exc_info.value.errors[0].message)


def test_context_missing_indent(tmp_path):
    """Test handling of missing indentation in Context blocks"""
    p = tmp_path / "context_no_indent.m6r"
    p.write_text(
        "Context: TestContext\n" \
        "No indent here\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Expected indent after keyword description for 'Context' block" in str(exc_info.value.errors[0].message)


def test_context_missing_description_and_indent(tmp_path):
    """Test handling of Context block with neither description nor indent"""
    p = tmp_path / "context_invalid.m6r"
    p.write_text(
        "Context:\n" \
        "Text without indent\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Expected description or indent for 'Context' block" in str(exc_info.value.errors[0].message)


def test_context_inner_unexpected(tmp_path):
    """Test handling of unexpected tokens in Context blocks"""
    p = tmp_path / "context_bad_token.m6r"
    p.write_text(
        "Context: TestContext\n" \
        "    First text\n" \
        "    Action: Invalid\n" \
        "        This shouldn't be here\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Unexpected token: Action: in 'Context' block" in str(exc_info.value.errors[0].message)


def test_context_late_text(tmp_path):
    """Test handling of text after inner Context in Context blocks"""
    p = tmp_path / "context_late_text.m6r"
    p.write_text(
        "Context: TestContext\n" \
        "    First text\n" \
        "    Context: Inner\n" \
        "        Inner content\n" \
        "    Late text is wrong here\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Text must come first in a 'Context' block" in str(exc_info.value.errors[0].message)


def test_context_duplicate_sections(parser, tmp_path):
    """Test handling of duplicate sections"""
    p = tmp_path / "duplicate.m6r"
    p.write_text(
        "Context: Test1\n" \
        "    Description\n" \
        "Context: Test2\n" \
        "    Description\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "'Context' already defined" in str(exc_info.value.errors[0].message)


def test_role_unexpected_token(tmp_path):
    """Test handling of unexpected tokens in Role blocks"""
    p = tmp_path / "role_bad_token.m6r"
    p.write_text(
        "Role: TestRole\n" \
        "    First text\n" \
        "    Action: Invalid\n" \
        "        This shouldn't be here\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Unexpected token: Action: in 'Role' block" in str(exc_info.value.errors[0].message)


def test_role_missing_indent(tmp_path):
    """Test handling of missing indentation in Role blocks"""
    p = tmp_path / "role_no_indent.m6r"
    p.write_text(
        "Role: TestRole\n" \
        "No indent here\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Expected indent after keyword description for 'Role' block" in str(exc_info.value.errors[0].message)


def test_role_missing_description_and_indent(tmp_path):
    """Test handling of Role block with neither description nor indent"""
    p = tmp_path / "role_invalid.m6r"
    p.write_text(
        "Role:\n" \
        "Text without indent\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Expected description or indent for 'Role' block" in str(exc_info.value.errors[0].message)


def test_role_inner_unexpected(tmp_path):
    """Test handling of unexpected tokens in Role blocks"""
    p = tmp_path / "role_bad_token.m6r"
    p.write_text(
        "Role: TestRole\n" \
        "    First text\n" \
        "    Action: Invalid\n" \
        "        This shouldn't be here\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Unexpected token: Action: in 'Role' block" in str(exc_info.value.errors[0].message)


def test_role_late_text(tmp_path):
    """Test handling of text after inner Role in Role blocks"""
    p = tmp_path / "role_late_text.m6r"
    p.write_text(
        "Role: TestRole\n" \
        "    First text\n" \
        "    Role: Inner\n" \
        "        Inner role\n" \
        "    Late text is wrong here\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Text must come first in a 'Role' block" in str(exc_info.value.errors[0].message)


def test_role_duplicate_sections(parser, tmp_path):
    """Test handling of duplicate sections"""
    p = tmp_path / "duplicate.m6r"
    p.write_text(
        "Role: Test1\n" \
        "    Description\n" \
        "Role: Test2\n" \
        "    Description\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "'Role' already defined" in str(exc_info.value.errors[0].message)


def test_include_rel_path(parser, tmp_path):
    """Test handling of Include directive"""
    # Create main file - fixed indentation
    main_file = tmp_path / "main.m6r"
    include_file = tmp_path / "include.m6r"

    main_file.write_text(
        "Role: Test\n" \
        "    Description\n" \
        "Include: include.m6r\n"
    )

    include_file.write_text(
        "Context: Included\n" \
        "    Content\n"
    )

    result = parser.parse_file(str(main_file), [str(tmp_path)])
    assert len(result.get_children_of_type(MetaphorASTNodeType.ROLE)) == 1
    context_nodes = result.get_children_of_type(MetaphorASTNodeType.CONTEXT)
    assert len(context_nodes) == 1

    # The first child node should be the keyword text "Included"
    assert any(node.value == "Content" for node in context_nodes[0].children)


def test_include_abs_path(parser, tmp_path):
    """Test handling of Include directive"""
    # Create main file - fixed indentation
    main_file = tmp_path / "main.m6r"
    include_file = tmp_path / "include.m6r"

    main_file.write_text(
        f"Role: Test\n" \
        f"    Description\n" \
        f"Include: {include_file}\n"
    )

    include_file.write_text(
        "Context: Included\n" \
        "    Content\n"
    )

    result = parser.parse_file(str(main_file), [str(tmp_path)])
    assert len(result.get_children_of_type(MetaphorASTNodeType.ROLE)) == 1
    context_nodes = result.get_children_of_type(MetaphorASTNodeType.CONTEXT)
    assert len(context_nodes) == 1

    # The first child node should be the keyword text "Included"
    assert any(node.value == "Content" for node in context_nodes[0].children)


def test_recursive_includes(parser, tmp_path):
    """Test handling of recursive includes"""
    file1 = tmp_path / "file1.m6r"
    file2 = tmp_path / "file2.m6r"

    # No indent on Include directives
    file1.write_text(
        "Role: Test1\n" \
        "    Description\n" \
        "Include: file2.m6r\n"
    )

    file2.write_text(
        "Context: Test2\n" \
        "    Description\n" \
        "Include: file1.m6r\n"
    )

    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(file1), [str(tmp_path)])

        # Check the actual error messages in the errors list
        errors = exc_info.value.errors
        assert any("has already been used" in error.message for error in errors)


def test_include_search_paths(parser, tmp_path):
    """Test handling of search paths for includes"""
    empty_include_dir = tmp_path / "empty_includes"
    empty_include_dir.mkdir()

    include_dir = tmp_path / "includes"
    include_dir.mkdir()

    main_file = tmp_path / "main.m6r"
    include_file = include_dir / "included.m6r"

    main_file.write_text(
        "Role: Test\n" \
        "    Description\n" \
        "Include: included.m6r\n"
    )

    include_file.write_text(
        "Context: Included\n" \
        "    Content\n"
    )

    result = parser.parse_file(str(main_file), [str(empty_include_dir), str(include_dir)])
    assert len(result.get_children_of_type(MetaphorASTNodeType.ROLE)) == 1
    assert len(result.get_children_of_type(MetaphorASTNodeType.CONTEXT)) == 1


def test_include_missing_filename(tmp_path):
    """Test handling of missing filename in Include directives"""
    p = tmp_path / "include_no_file.m6r"
    p.write_text(
        "Role: Test\n" \
        "    First text\n" \
        "    Include:\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Expected file name for 'Include'" in str(exc_info.value.errors[0].message)


def test_file_permission_error(create_read_only_file):
    """Test handling of permission errors when reading files"""
    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(create_read_only_file), [])

    assert "You do not have permission to access" in str(exc_info.value.errors[0].message)


def test_directory_error(tmp_path):
    """Test handling of IsADirectoryError"""
    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(tmp_path), [])

    assert "Is a directory" in str(exc_info.value.errors[0].message)


def test_os_error(tmp_path, monkeypatch):
    """Test handling of general OS errors"""
    def mock_open(*args, **kwargs):
        raise OSError("Simulated OS error")

    monkeypatch.setattr("builtins.open", mock_open)

    p = tmp_path / "test.m6r"
    p.write_text("Role: Test")

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "OS error" in str(exc_info.value.errors[0].message)


def test_include_file_not_found(parser, tmp_path):
    """Test parse_file() error handling with existing token context"""
    # Create a main file that includes a non-existent file
    main_file = tmp_path / "main.m6r"
    main_file.write_text(
        "Role: Test\n" \
        "    Description\n" \
        "    Include: nonexistent.m6r\n"
    )

    # This should trigger the error handling with a current_token
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(main_file), [])

    # Verify the error has the correct token context
    error = exc_info.value.errors[0]
    assert "File not found" in error.message
    assert error.filename == str(main_file)  # Should have the main file as context
    assert error.line > 0  # Should have a valid line number
    assert error.column > 0  # Should have a valid column number
    assert "Include: nonexistent.m6r" in error.input_text  # Should have the failing line


def test_include_abs_file_not_found(parser, tmp_path):
    """Test parse_file() error handling with existing token context"""
    # Create a main file that includes a non-existent file
    main_file = tmp_path / "main.m6r"
    nonexist_file = tmp_path / "nonexistent.m6r"
    main_file.write_text(
        f"Role: Test\n" \
        f"    Description\n" \
        f"    Include: {nonexist_file}\n"
    )

    # This should trigger the error handling with a current_token
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(main_file), [])

    # Verify the error has the correct token context
    error = exc_info.value.errors[0]
    assert "File not found" in error.message
    assert error.filename == str(main_file)  # Should have the main file as context
    assert error.line > 0  # Should have a valid line number
    assert error.column > 0  # Should have a valid column number
    assert f"Include: {nonexist_file}" in error.input_text  # Should have the failing line


def test_embed_directive(parser, tmp_path):
    """Test handling of Embed directive"""
    main_file = tmp_path / "main.m6r"
    # Embed needs to be within a Context block
    main_file.write_text(
        "Role: Test\n" \
        "    Description\n" \
        "Context: Files\n" \
        "    Context text\n" \
        "    Embed: test.txt\n"
    )

    # Create embed file
    embed_file = tmp_path / "test.txt"
    embed_file.write_text("This is just plain text")

    current_dir = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = parser.parse_file(str(main_file), [])
        assert len(result.get_children_of_type(MetaphorASTNodeType.ROLE)) == 1
        context_nodes = result.get_children_of_type(MetaphorASTNodeType.CONTEXT)
        assert len(context_nodes) == 1

        # The embedded content should be part of the Context block's content
        context = context_nodes[0]
        embedded_text = [
            node for node in context.children
            if node.node_type == MetaphorASTNodeType.TEXT and
            ("test.txt" in node.value or "plaintext" in node.value)
        ]
        assert len(embedded_text) > 0
    finally:
        os.chdir(current_dir)


def test_wildcard_embed(parser, tmp_path):
    """Test handling of wildcard patterns in Embed directive"""
    # Create multiple test files
    (tmp_path / "test1.txt").write_text("Content 1")
    (tmp_path / "test2.txt").write_text("Content 2")

    main_file = tmp_path / "main.m6r"

    # Embed within Context block
    main_file.write_text(
        "Role: Test\n" \
        "    Description\n" \
        "Context: Files\n" \
        "    Context text\n" \
        "    Embed: test*.txt\n"
    )

    current_dir = os.getcwd()
    os.chdir(tmp_path)
    try:
        result = parser.parse_file(str(main_file), [])
        assert len(result.get_children_of_type(MetaphorASTNodeType.ROLE)) == 1
        context_nodes = result.get_children_of_type(MetaphorASTNodeType.CONTEXT)
        assert len(context_nodes) == 1

        # Check for content from both embedded files
        context = context_nodes[0]
        embedded_text = [
            node for node in context.children if node.node_type == MetaphorASTNodeType.TEXT
        ]

        # Should find both filenames
        assert any("test1.txt" in node.value for node in embedded_text)
        assert any("test2.txt" in node.value for node in embedded_text)

        # Should find both contents
        assert any("Content 1" in node.value for node in embedded_text)
        assert any("Content 2" in node.value for node in embedded_text)
    finally:
        os.chdir(current_dir)


def test_embed_missing_filename(tmp_path):
    """Test handling of missing filename in Embed directives"""
    p = tmp_path / "embed_no_file.m6r"
    p.write_text(
        "Context: Test\n" \
        "    First text\n" \
        "    Embed:\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "Expected file name or wildcard match for 'Embed'" in str(exc_info.value.errors[0].message)


def test_embed_no_matches(tmp_path):
    """Test handling of no matching files for Embed directives"""
    p = tmp_path / "embed_no_matches.m6r"
    p.write_text(
        "Context: Test\n" \
        "    First text\n" \
        "    Embed: nonexistent*.txt\n"
    )

    parser = MetaphorParser()
    with pytest.raises(MetaphorParserError) as exc_info:
        parser.parse_file(str(p), [])

    assert "nonexistent*.txt does not match any files for 'Embed'" in str(exc_info.value.errors[0].message)


def test_recursive_embed(tmp_path):
    """Test handling of recursive Embed with **/ pattern"""
    # Create a nested directory structure
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    subsubdir = subdir / "deeper"
    subsubdir.mkdir()

    # Create test files at different levels
    (tmp_path / "root.txt").write_text("Root content")
    (subdir / "level1.txt").write_text("Level 1 content")
    (subsubdir / "level2.txt").write_text("Level 2 content")

    main_file = tmp_path / "main.m6r"

    # Use **/ pattern to recursively match files, with proper 4-space indentation.
    # Note the ./ prefix to ensure we look in current directory.
    main_file.write_text(
        "Role: Test\n" \
        "    Description\n" \
        "Context: Files\n" \
        "    Context text\n" \
        "    Embed: ./**/*.txt\n"
    )

    current_dir = os.getcwd()
    os.chdir(tmp_path)
    try:
        parser = MetaphorParser()
        result = parser.parse_file(str(main_file), [])

        # Check for content from all embedded files
        context_nodes = result.get_children_of_type(MetaphorASTNodeType.CONTEXT)
        context = context_nodes[0]
        embedded_text = [
            node for node in context.children if node.node_type == MetaphorASTNodeType.TEXT
        ]

        # Should find all filenames
        assert any("root.txt" in node.value for node in embedded_text)
        assert any("level1.txt" in node.value for node in embedded_text)
        assert any("level2.txt" in node.value for node in embedded_text)

        # Should find all contents
        assert any("Root content" in node.value for node in embedded_text)
        assert any("Level 1 content" in node.value for node in embedded_text)
        assert any("Level 2 content" in node.value for node in embedded_text)
    finally:
        os.chdir(current_dir)
