"""
So now, the workflow is much simpler and there is no need to remember long and complicated commands. 

To add a new language, you use:
(venv) $ flask translate init <language-code>

To update all the languages after making changes to the _() and _l() language markers:
(venv) $ flask translate update

And to compile all languages after updating the translation files:
(venv) $ flask translate compile

### Application factory refactoring:
The current_app variable does not work in this case because these commands are registered at start up, 
not during the handling of a request, which is the only time when current_app can be used. To remove the 
reference to app in this module, I resorted to another trick, which is to move these custom commands 
inside a register() function that takes the app instance as an argument.
"""

import os
import click

def register(app):
    @app.cli.group()
    def translate():
        """Translation and localization commands."""
        pass

    @translate.command()
    def update():
        """Update all languages."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system('pybabel update -i messages.pot -d app/translations'):
            raise RuntimeError('update command failed')
        os.remove('messages.pot')

    @translate.command()
    def compile():
        """Compile all languages."""
        if os.system('pybabel compile -d app/translations'):
            raise RuntimeError('compile command failed')

    @translate.command()
    @click.argument('lang')
    def init(lang):
        """Initialize a new language."""
        if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
            raise RuntimeError('extract command failed')
        if os.system(
                'pybabel init -i messages.pot -d app/translations -l ' + lang):
            raise RuntimeError('init command failed')
        os.remove('messages.pot')
