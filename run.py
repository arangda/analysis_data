from app import app

def do():
    app.run(processes=4,debug=True)

#if __name__ == '__main__':
 #   do()