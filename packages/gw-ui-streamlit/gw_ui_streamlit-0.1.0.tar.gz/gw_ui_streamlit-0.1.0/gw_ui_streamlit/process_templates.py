from jinja2 import FileSystemLoader, Environment, select_autoescape, TemplateNotFound

from gw_ui_streamlit.utils import _fetch_tab


def _process_template_by_name(template_name, input_dict: dict, location):
    env = Environment(
            loader=FileSystemLoader(location),
            autoescape=select_autoescape(),
            trim_blocks=True,
    )
    template_result = None
    try:
        template = env.get_template(template_name)
        template_result = template.render(input_dict)
    except TemplateNotFound:
        _fetch_tab("Output").warning(f"Template - {template_name} was not found")

    return template_result
