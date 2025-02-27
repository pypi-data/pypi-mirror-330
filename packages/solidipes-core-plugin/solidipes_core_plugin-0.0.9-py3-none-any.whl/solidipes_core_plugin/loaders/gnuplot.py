from .code_snippet import CodeSnippet


class GnuPlot(CodeSnippet):
    supported_mime_types = {"drawing/gnuplot": ["gp", "gpu", "gih"]}

    def __init__(self, **kwargs):
        from ..viewers.image_source import ImageSource as ImageSourceViewer

        super().__init__(**kwargs)
        self.compatible_viewers[:0] = [ImageSourceViewer]

    @CodeSnippet.loadable
    def image(self):
        import os

        cur_dir = os.getcwd()
        text = self.text
        images = []
        try:
            import tempfile

            import pygnuplot.gnuplot as gnuplot
            from PIL import Image as PILImage

            path = os.path.dirname(self.file_info.path)
            os.chdir(path)
            g = gnuplot.Gnuplot(log=True)
            import streamlit as st

            for line in text.split("\n"):
                if line.startswith("set terminal"):
                    continue
                if line.startswith("set output"):
                    continue
                if line.startswith("plot"):
                    with tempfile.NamedTemporaryFile() as fp:
                        fp.close()
                        g.cmd("set terminal pngcairo")
                        g.cmd(f'set output "{fp.name}.png"')
                        g.cmd(line)
                        g.plot(line[4:])
                        import time

                        time.sleep(0.2)
                        images.append(PILImage.open(f"{fp.name}.png"))
                        os.remove(f"{fp.name}.png")
                        continue
                g.cmd(line)
            os.chdir(cur_dir)
        except Exception as e:
            import streamlit as st

            st.exception(e)

        os.chdir(cur_dir)
        return images
