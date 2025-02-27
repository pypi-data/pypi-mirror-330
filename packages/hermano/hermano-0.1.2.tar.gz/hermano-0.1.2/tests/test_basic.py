
def test_import():
    """Test that the package can be imported."""
    import hermano
    assert hermano.__version__ is not None

def test_cli_import():
    """Test that the CLI module can be imported."""
    from hermano import cli
    assert cli.cli is not None 