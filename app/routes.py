from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    '''
    The form.validate_on_submit() method does all the form processing work. 
    When the browser sends the GET request to receive the web page with the form, 
    this method is going to return False, so in that case the function skips the if 
    statement and goes directly to render the template in the last line of the function.
    
    When form.validate_on_submit() returns True, the login view function calls 
    two new functions, imported from Flask. The flash() function is a useful way to 
    show a message to the user. A lot of applications use this technique to let 
    the user know if some action has been successful or not. In this case, 
    I'm going to use this mechanism as a temporary solution, because I don't have all 
    the infrastructure necessary to log users in for real yet. The best I can do for now 
    is show a message that confirms that the application received the credentials.
    
    When you call the flash() function, Flask stores the message, but flashed messages 
    will not magically appear in web pages. The templates of the application need to render 
    these flashed messages in a way that works for the site layout. I'm going to add these 
    messages to the base template, so that all the templates inherit this functionality. 
    
    An interesting property of these flashed messages is that once they are requested once 
    through the get_flashed_messages function they are removed from the message list, so they 
    appear only once after the flash() function is called.
    '''
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data)) 
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)