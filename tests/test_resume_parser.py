from src.resume.resume_manager import discover_resumes


def test_discover_resumes_ignores_non_pdf_files(tmp_path):
	(tmp_path / "resume.pdf").write_bytes(b"pdf")
	(tmp_path / "notes.txt").write_text("not a resume")

	assert [path.name for path in discover_resumes(tmp_path)] == ["resume.pdf"]
