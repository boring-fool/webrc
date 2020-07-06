from jinja2 import Environment,FileSystemLoader
env = Environment(loader=FileSystemLoader('./Templates'))
def render(name,d:dict):
    template = env.get_template(name)
    return template.render(**d)