from floweaver_path.lib.utils import extract_files
from floweaver_path.lib.utils import load_file


def test_extract_template_csv():
    files = extract_files('./src/template/data')
    df = load_file(files[0])
    assert df.shape == (400, 4), 'the shape of template data should be (400, 4)'
