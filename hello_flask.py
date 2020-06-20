    from flask import Flask, render_template,request,redirect
from vsearch import search4letters
app = Flask(__name__)
def log_request(req: 'flask_request', res:str) -> None:
    dbconfig = {'host':'@localhost',
                'user':'vsearch',
                'password':'1234',
                'database':'vsearchlogDB',}
    import mysql.connector
    conn = mysql.connector.connect(**dbconfig)
    cursor=conn.cursor()
    _SQL = """insert into log
              (phrase, letters, ip, browser_string, results)
              values
              (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req.form['phrase'],
                          req.form['letters'],
                          req.remote_addr,
                          req.user_agent.browser,
                          res, ))
    con.commit()
    cursor.close()
    conn.close()
@app.route('/')
def hello():
    return redirect('/entry')
@app.route('/search4',methods=['POST'])
def do_search() -> str:
    phrase=request.form['phrase']
    letters=request.form['letters']
    title='Here are your results:'
    results=str(search4letters(phrase.lower(),letters.lower()))
    log_request=(request,results)
    return render_template('results.html',the_phrase=phrase,the_letters=letters,the_title=title,
    the_results=results,)
@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',the_title='Welcome to search4letters on the web!')

@app.route('/viewlog')
def view_the_log() -> str:
    with open('vsearch.log') as log:
        contents=log.read()
    return contents
if __name__ == '__main__':
    app.run(debug=True)
