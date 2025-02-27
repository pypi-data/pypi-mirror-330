from .solidipes_buttons import SolidipesButtons as SPB
from .solidipes_logo_widget import SolidipesLogoWidget as SPLW

################################################################


class FrontPage(SPLW):
    def __init__(self, **kwargs):
        from solidipes.utils import get_completed_stages

        super().__init__(
            title="""
        <center>

# Welcome to the Solidipes Curation Tool!
        """,
            width="15%",
            **kwargs,
        )

        steps = [
            {
                "name": "acquisition",
                "description": (
                    "Upload any files relevant to your paper, and browse them like you would in a file browser."
                ),
            },
            {
                "name": "curation",
                "description": (
                    "Automatically verify the correct formatting of your files, review their contents, and discuss"
                    " potential issues."
                ),
            },
            {
                "name": "metadata",
                "description": (
                    "Easily edit any metadata relevant to your paper such as authors, keywords, description, and more."
                ),
            },
            {
                "name": "export",
                "description": (
                    "Once all previous steps are complete, review your work and export it to databases such as Zenodo."
                ),
            },
        ]
        completed_stages = get_completed_stages()
        incomplete_stages = set(range(len(steps))) - set(completed_stages)
        last_stage = min(incomplete_stages)

        buttons_custom_style = {
            "grid-column": 1,
            "width": "100%",
        }

        html = """
<style>
    .steps-container {
        align-items: center;
        gap: 1rem;
        grid-template-columns: 9rem 1fr;
        max-width: 55rem;
    }

    .steps-text {
        grid-column: 2;
        margin-bottom: 1rem;
        text-align: left;
    }

    @media all and (min-width: 680px) {
        .steps-container {
            display: grid;
        }

        .steps-text {
            margin-bottom: 0;
        }
    }
</style>
<center>
    <h3 style="margin-bottom: 1rem;">Here, you can prepare your paper’s data for publication in four steps:</h3>

    <div class="steps-container">
        """

        for i, step in enumerate(steps):
            name = step["name"].capitalize()
            if i in completed_stages:
                name = f"✔️ {name} &nbsp;"

            html += SPB()._html_link_button(
                name,
                f"?page={step['name']}",
                type="primary" if i == last_stage else "secondary",
                custom_style=buttons_custom_style,
            )
            html += f'<div class="steps-text">{step["description"]}</div>'

        html += """
    </div>
</center>
        """

        self.layout.html(html)
