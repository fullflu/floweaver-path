from floweaver_path.lib.utils import extract_files


def test_extract_template_csv():
    files = extract_files('./src/template/data')
    assert len(files) == 1, 'file number should be 1'
    assert files[0] == './src/template/data/template.csv', 'file name should be `./template/data/template.csv`'
