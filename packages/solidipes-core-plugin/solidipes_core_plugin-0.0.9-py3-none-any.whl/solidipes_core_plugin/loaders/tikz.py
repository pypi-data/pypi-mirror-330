from solidipes.utils import solidipes_logging as logging

from .code_snippet import CodeSnippet

logger = logging.getLogger()


class TIKZ(CodeSnippet):
    supported_mime_types = {"latex/tikz": "tikz"}

    def __init__(self, **kwargs):
        from ..viewers.image_source import ImageSource as ImageSourceViewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [ImageSourceViewer]

    @CodeSnippet.loadable
    def pdf(self):
        text = self.text
        if r"\begin{document}" not in text:
            header = r"""
            \documentclass[tikz,convert={outfile=\jobname.svg}]{standalone}
\usetikzlibrary{calc,patterns,snakes}
% \usetikzlibrary{...}% tikz package already loaded by 'tikz' option
            """
            if "gnuplot" in text:
                header += r"""
                \usepackage{gnuplot-lua-tikz}
                """
            header += r"""
            \begin{document}
            """

            text = header + text + r"\end{document}"

        import tempfile

        with tempfile.NamedTemporaryFile(delete=False) as fp:
            fp.write(text.encode())
            fp.close()
            import subprocess

            try:
                p = subprocess.Popen(f"rubber -d {fp.name}", shell=True, stderr=subprocess.PIPE)
                p.wait()
                if p.returncode:
                    error = p.stderr.read().decode()
                    logger.error(error)
                    raise RuntimeError(error)

                import os

                from .pdf import PDF

                pdf_file = os.path.split(fp.name)[-1]
                pdf = PDF(path=pdf_file + ".pdf").pdf
                for ext in ["pdf", "aux", "log", "rubbercache"]:
                    os.remove(pdf_file + "." + ext)
                return pdf
            except Exception as e:
                logger.error(e)
                raise RuntimeError(str(e))
